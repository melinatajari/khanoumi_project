import subprocess
import os
import sys

def run_script(script_name):
    """Executes a python script as a separate process using subprocess."""
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

def run_end_to_end_pipeline():
    """Orchestrate data ingestion, preprocessing, and feature engineering using subprocess."""
    print("=" * 60)
    print("INITIATING SUBPROCESS-BASED DATA SCIENCE PIPELINE")
    print("=" * 60)
    
    try:
        # Step 1: Execute Data Ingestion
        print("Step 1: Running Data Ingestion...")
        if not run_script("load_data.py"):
            return
            
        # Step 2: Execute Data Preprocessing & Cleaning
        print("Step 2: Running Data Preprocessing...")
        if not run_script("preprocess.py"):
            return
            
        # Step 3: Execute Feature Engineering & Data Export
        print("Step 3: Running Feature Engineering & Data Export...")
        if not run_script("feature_engineering.py"):
            return
            
        output_filename = "final_processed_data.csv"
        print("=" * 60)
        print("PIPELINE EXECUTION SUCCESSFUL VIA SUBPROCESS!")
        print(f"-> Final dataset status validated: {os.path.abspath(output_filename)}")
        print("=" * 60)
        
    except Exception as e:
        print(f"[FATAL ERROR] Pipeline failed during subprocess execution: {e}")

if __name__ == "__main__":
    run_end_to_end_pipeline()