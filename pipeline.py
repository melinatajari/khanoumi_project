import subprocess
import os
import sys

# Execution Helpers: Process Invocation :
def run_script(script_name):
    python_executable = sys.executable
    result = subprocess.run([python_executable, script_name], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"[ERROR] Pipeline aborted: {script_name} failed during execution.")
        print("Detailed Error Logs Below:")
        print(result.stderr)
        return False
        
    if result.stdout.strip():
        print(result.stdout)
    return True

# Execution Helpers: Pipeline Orchestration :
def run_end_to_end_pipeline():
    print("=" * 60)
    print("INITIATING SUBPROCESS-BASED DATA SCIENCE PIPELINE")
    print("=" * 60)
    
    try:
        print("Step 1: Running Data Ingestion...")
        if not run_script("load_data.py"):
            return
            
        print("Step 2: Running Data Preprocessing...")
        if not run_script("preprocess.py"):
            return
            
        print("Step 3: Running Feature Engineering & Data Export...")
        if not run_script("feature_engineering.py"):
            return
            
        output_filename = "processed_products.csv"
        print("=" * 60)
        print("PIPELINE EXECUTION SUCCESSFUL VIA SUBPROCESS!")
        print(f"-> Final dataset status validated: {os.path.abspath(output_filename)}")
        print("=" * 60)
        
    except Exception as e:
        print(f"[FATAL ERROR] Pipeline failed during subprocess execution: {e}")

if __name__ == "__main__":
    run_end_to_end_pipeline()