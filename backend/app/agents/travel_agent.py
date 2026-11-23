"""
Travel Agent — LangChain Agent Core
=====================================
Main AI agent that uses LLMs + tools to answer travel queries.
Supports Gemini (free), OpenAI, and Ollama providers.

If LangChain is not installed, falls back to a simple database-only mode.
"""

import uuid
from typing import Optional

from app.config import settings
from app.agents.prompts import TRAVEL_AGENT_SYSTEM_PROMPT
from app.agents.tools import ALL_TOOLS

# Try importing LangChain — graceful fallback if not installed
try:
    from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

# In-memory chat history (per session)
_chat_histories: dict[str, list] = {}


def _get_llm():
    """Initialize the LLM based on provider setting."""
    if not LANGCHAIN_AVAILABLE:
        raise ImportError(
            "LangChain is not installed. Run: pip install langchain langchain-core"
        )

    provider = settings.llm_provider.lower()

    if provider == "gemini":
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
        except ImportError:
            raise ImportError(
                "langchain-google-genai is not installed. "
                "Run: pip install langchain-google-genai"
            )
        if not settings.google_api_key:
            raise ValueError(
                "GOOGLE_API_KEY is not set. Add it to your .env file. "
                "Get a free key at https://aistudio.google.com/"
            )
        return ChatGoogleGenerativeAI(
            model=settings.llm_model or "gemini-2.0-flash",
            google_api_key=settings.google_api_key,
            temperature=0.7,
            convert_system_message_to_human=True,
        )

    elif provider == "openai":
        try:
            from langchain_openai import ChatOpenAI
        except ImportError:
            raise ImportError(
                "langchain-openai is not installed. "
                "Run: pip install langchain-openai"
            )
        if not settings.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY is not set. Add it to your .env file."
            )
        kwargs = {
            "model": settings.llm_model or "gpt-4o-mini",
            "api_key": settings.openai_api_key,
            "temperature": 0.7,
        }
        if settings.openai_api_key.startswith("sk-or-"):
            kwargs["base_url"] = "https://openrouter.ai/api/v1"
            
        return ChatOpenAI(**kwargs)

    elif provider == "ollama":
        try:
            from langchain_community.chat_models import ChatOllama
        except ImportError:
            raise ImportError(
                "langchain-community is not installed. "
                "Run: pip install langchain-community"
            )
        return ChatOllama(
            model=settings.llm_model or "llama3",
            temperature=0.7,
        )

    else:
        raise ValueError(
            f"Unknown LLM provider: '{provider}'. "
            f"Valid options: gemini, openai, ollama. "
            f"Set LLM_PROVIDER in your .env file."
        )


def _get_chat_history(session_id: str) -> list:
    """Get or create chat history for a session."""
    if session_id not in _chat_histories:
        _chat_histories[session_id] = []
    return _chat_histories[session_id]


def _execute_tool(tool_name: str, tool_args: dict) -> str:
    """Find and execute a tool by name."""
    for t in ALL_TOOLS:
        if t.name == tool_name:
            try:
                return str(t.invoke(tool_args))
            except Exception as e:
                return f"Tool error ({tool_name}): {str(e)}"
    return f"Unknown tool: {tool_name}"


async def chat_with_agent(
    message: str,
    session_id: Optional[str] = None,
) -> tuple[str, str]:
    """
    Send a message to the travel agent and get a response.

    Args:
        message: User's travel query
        session_id: Optional session ID for chat memory

    Returns:
        Tuple of (agent_reply, session_id)
    """
    # Generate session ID if not provided
    if not session_id:
        session_id = str(uuid.uuid4())

    # Get chat history
    history = _get_chat_history(session_id)

    try:
        # Check if LangChain is available
        if not LANGCHAIN_AVAILABLE:
            # Fallback: use tools directly without LLM
            reply = _fallback_response(message)
            history.append({"role": "user", "content": message})
            history.append({"role": "agent", "content": reply})
            return reply, session_id

        # Initialize LLM
        llm = _get_llm()

        # Bind tools to the LLM
        llm_with_tools = llm.bind_tools(ALL_TOOLS)

        # Build messages
        messages = [SystemMessage(content=TRAVEL_AGENT_SYSTEM_PROMPT)]

        # Add chat history (last 10 messages)
        for h in history[-10:]:
            if isinstance(h, dict):
                # Convert dict history to LangChain messages
                if h.get("role") == "user":
                    messages.append(HumanMessage(content=h["content"]))
                else:
                    messages.append(AIMessage(content=h["content"]))
            else:
                messages.append(h)

        messages.append(HumanMessage(content=message))

        # Invoke the agent
        response = llm_with_tools.invoke(messages)

        # Process tool calls if any (up to 3 rounds of tool calls)
        max_rounds = 3
        current_round = 0

        while (
            hasattr(response, "tool_calls")
            and response.tool_calls
            and current_round < max_rounds
        ):
            messages.append(response)

            for tool_call in response.tool_calls:
                tool_name = tool_call.get("name", "")
                tool_args = tool_call.get("args", {})
                tool_call_id = tool_call.get("id", f"call_{current_round}")

                tool_result = _execute_tool(tool_name, tool_args)
                messages.append(
                    ToolMessage(
                        content=tool_result,
                        tool_call_id=tool_call_id,
                    )
                )

            # Get next response
            response = llm_with_tools.invoke(messages)
            current_round += 1

        if isinstance(response.content, list):
            reply = "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in response.content)
        else:
            reply = response.content or "I processed your request but couldn't generate a text response. Please try rephrasing."

        # Save to chat history
        history.append(HumanMessage(content=message))
        history.append(AIMessage(content=reply))

        return reply, session_id

    except ImportError as e:
        error_msg = (
            f"⚠️ Missing package: {str(e)}\n\n"
            f"Please install the required packages:\n"
            f"```\n"
            f"pip install langchain langchain-core langchain-google-genai\n"
            f"```"
        )
        return error_msg, session_id

    except ValueError as e:
        error_msg = f"⚠️ Configuration error: {str(e)}"
        return error_msg, session_id

    except Exception as e:
        error_str = str(e)
        if "api_key" in error_str.lower() or "authenticate" in error_str.lower() or "api key" in error_str.lower():
            error_msg = (
                "🔑 API Key Error: Your API key is missing or invalid.\n\n"
                "**Fix:**\n"
                "1. Open `.env` file\n"
                "2. Add your key: `GOOGLE_API_KEY=your_key_here`\n"
                "3. Get a free key at https://aistudio.google.com/\n"
                "4. Restart the server"
            )
        elif "quota" in error_str.lower() or "rate" in error_str.lower():
            error_msg = (
                "⏳ Rate limit reached. Please wait a moment and try again."
            )
        elif "503" in error_str or "high demand" in error_str.lower():
            error_msg = (
                "⏳ Google Gemini is currently experiencing temporary high demand. "
                "Please wait a moment and try your message again."
            )
        elif "model" in error_str.lower() and "not found" in error_str.lower():
            error_msg = (
                f"❌ Model not found: {settings.llm_model}\n\n"
                f"Check `LLM_MODEL` in your `.env` file. "
                f"For Gemini, try: `gemini-2.0-flash`"
            )
        else:
            error_msg = (
                f"❌ Error: {error_str}\n\n"
                f"Please try again or rephrase your question."
            )

        return error_msg, session_id


def _fallback_response(message: str) -> str:
    """Simple fallback when LangChain is not available — uses tools directly."""
    import json

    msg_lower = message.lower()

    # Try to figure out intent and use tools directly
    if any(word in msg_lower for word in ["india", "rajasthan", "kerala", "goa", "himachal", "delhi", "mumbai"]):
        from app.agents.tools import search_destinations
        results = search_destinations.invoke({"query": message, "source": "india", "limit": 5})
        data = json.loads(results)
        if isinstance(data, list) and data:
            lines = ["Here are some destinations I found:\n"]
            for d in data:
                lines.append(f"**{d.get('place_name', 'Unknown')}** ({d.get('state', d.get('country', ''))})")
                lines.append(f"  - Category: {d.get('category', 'N/A')}")
                lines.append(f"  - Rating: ⭐ {d.get('rating', 'N/A')}")
                lines.append(f"  - {d.get('description', '')[:150]}")
                lines.append("")
            lines.append("\n*Note: Install LangChain for full AI-powered responses.*")
            return "\n".join(lines)

    elif any(word in msg_lower for word in ["airport", "flight", "fly"]):
        from app.agents.tools import find_nearest_airports
        city = message.split()[-1]  # Simple extraction
        results = find_nearest_airports.invoke({"city": city})
        return f"Airport search results:\n{results}\n\n*Install LangChain for AI responses.*"

    else:
        from app.agents.tools import search_destinations
        results = search_destinations.invoke({"query": message, "source": "all", "limit": 5})
        data = json.loads(results)
        if isinstance(data, list) and data:
            lines = ["Here are some destinations matching your query:\n"]
            for d in data:
                name = d.get("place_name", "Unknown")
                loc = d.get("state", d.get("country", ""))
                lines.append(f"- **{name}** ({loc}) — ⭐ {d.get('rating', 'N/A')} — {d.get('category', '')}")
            lines.append("\n*Install LangChain and set your API key for full AI-powered planning.*")
            return "\n".join(lines)

    return (
        "👋 Welcome to TravelBuddy AI!\n\n"
        "I can search destinations for you, but for full AI-powered responses, "
        "please install LangChain:\n\n"
        "```\npip install langchain langchain-core langchain-google-genai\n```\n\n"
        "Then add your API key to `.env`:\n"
        "`GOOGLE_API_KEY=your_key`"
    )


def clear_session(session_id: str):
    """Clear chat history for a session."""
    if session_id in _chat_histories:
        del _chat_histories[session_id]


def list_sessions() -> list[str]:
    """List all active session IDs."""
    return list(_chat_histories.keys())
