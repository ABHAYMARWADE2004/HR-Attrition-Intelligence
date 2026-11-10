"""
Main pipeline runner — runs the pipeline in order:
1. Run EDA (saves charts to outputs/)
2. Train ML model (saves model to models/)

Data source: data/hr_attrition_final.csv
(a snapshot of the hr_attrition_final table originally built in Snowflake)

Usage:
    python main.py
"""

import os
import subprocess
import sys

# Always run from the project folder so relative paths work
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("outputs", exist_ok=True)
os.makedirs("models", exist_ok=True)

STEPS = [
    ("Running EDA", "src/eda.py"),
    ("Training ML model", "src/train_model.py"),
]

def run_step(title, script_path):
    print("\n" + "=" * 60)
    print(f"STEP: {title}")
    print("=" * 60)
    result = subprocess.run([sys.executable, script_path])
    if result.returncode != 0:
        print(f"\n❌ Failed at: {title} (exit code {result.returncode})")
        sys.exit(1)
    print(f"✅ Done: {title}")

if __name__ == "__main__":
    if not os.path.exists("data/hr_attrition_final.csv"):
        print("❌ data/hr_attrition_final.csv nahi mili. Pehle rebuild_data.py chalao.")
        sys.exit(1)

    for title, script in STEPS:
        run_step(title, script)
    print("\n🎉 Pipeline complete — model trained, charts saved, ready for app.py")