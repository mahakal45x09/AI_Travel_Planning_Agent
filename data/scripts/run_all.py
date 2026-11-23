"""
Master Data Pipeline — Run All Cleaning Scripts
================================================
Orchestrates all data cleaning and building scripts in the correct order.

Usage:
    python run_all.py
"""

import subprocess
import sys
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = BASE_DIR

SCRIPTS = [
    ("1. Clean Airports", "clean_airports.py"),
    ("2. Clean Countries", "clean_countries.py"),
    ("3. Clean Travel Details", "clean_travel_details.py"),
    ("4. Clean Reviews", "clean_reviews.py"),
    ("5. Build India Destinations", "build_india_dataset.py"),
    ("6. Build World Destinations", "build_world_dataset.py"),
]


def run_script(name: str, script: str):
    """Run a single cleaning script."""
    script_path = os.path.join(SCRIPTS_DIR, script)

    if not os.path.exists(script_path):
        print(f"  ⚠️  Script not found: {script}")
        return False

    print(f"\n{'='*60}")
    print(f"  Running: {name}")
    print(f"  Script:  {script}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=120,
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"  ❌ FAILED with exit code {result.returncode}")
            if result.stderr:
                print(f"  STDERR: {result.stderr}")
            return False
        return True
    except subprocess.TimeoutExpired:
        print(f"  ❌ TIMEOUT after 120 seconds")
        return False
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
        return False


def main():
    """Run all cleaning scripts."""
    print("=" * 60)
    print("  AI Travel Planning Agent — Data Pipeline")
    print("  Running all cleaning scripts...")
    print("=" * 60)

    start_time = time.time()
    results = []

    for name, script in SCRIPTS:
        success = run_script(name, script)
        results.append((name, success))

    # Summary
    elapsed = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"  PIPELINE COMPLETE ({elapsed:.1f}s)")
    print(f"{'='*60}")

    for name, success in results:
        status = "✅" if success else "❌"
        print(f"  {status} {name}")

    # List cleaned files
    cleaned_dir = os.path.join(os.path.dirname(SCRIPTS_DIR), "cleaned")
    if os.path.exists(cleaned_dir):
        print(f"\n  Cleaned files in {cleaned_dir}:")
        for f in sorted(os.listdir(cleaned_dir)):
            filepath = os.path.join(cleaned_dir, f)
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"    📄 {f} ({size_mb:.2f} MB)")

    failed = sum(1 for _, s in results if not s)
    if failed:
        print(f"\n  ⚠️  {failed} script(s) failed. Check output above.")
        sys.exit(1)
    else:
        print(f"\n  🎉 All scripts completed successfully!")


if __name__ == "__main__":
    main()
