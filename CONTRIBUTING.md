# Contributing to AI Travel Planning Agent

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 🚀 How to Contribute

### 1. Fork & Clone
```bash
git fork https://github.com/YOUR_USERNAME/AI-Travel-Planning-Agent
git clone https://github.com/YOUR_USERNAME/AI-Travel-Planning-Agent.git
cd AI-Travel-Planning-Agent
```

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Set Up Development Environment
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### 4. Make Your Changes
- Write clean, documented code
- Add tests for new features
- Update documentation if needed

### 5. Submit a Pull Request
```bash
git add .
git commit -m "feat: description of your changes"
git push origin feature/your-feature-name
```
Then open a Pull Request on GitHub.

## 📊 Contributing Data

We especially welcome contributions to our datasets:
- **New Indian tourist destinations** (with descriptions, coordinates, categories)
- **World attractions** data
- **Hotel/cost data** for underrepresented regions
- **Translations** for non-English destinations

### Data Format
Please follow the schema in `data/cleaned/` and include:
- Source attribution
- Data quality verification
- No personally identifiable information (PII)

## 🐛 Reporting Bugs

Open an issue with:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)

## 💡 Feature Requests

Open an issue with the `enhancement` label describing:
- The feature you'd like
- Why it would be useful
- Any implementation ideas

## 📜 Code Style

- **Python**: Follow PEP 8, use type hints
- **JavaScript/React**: Follow ESLint rules, use functional components
- **Commits**: Follow [Conventional Commits](https://www.conventionalcommits.org/)

## 📋 Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). Please be respectful and inclusive.

## 🙏 Thank You!

Every contribution matters, whether it's code, data, documentation, or bug reports!
