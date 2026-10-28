import subprocess
import sys
import os
from pprint import pprint
# ============================================================
# Prevent NumPy / sklearn / BLAS from creating too many threads
# ============================================================
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
import multiprocessing
import warnings
from mpire import WorkerPool

def build_docs(folder_path):
    status = "ok"
    output_path = f"{folder_path}-docs"
    os.makedirs(output_path, exist_ok=True)

    result = subprocess.run(
        [
            sys.executable,
            "-m", "pdoc",
            "-o", output_path,
            folder_path
        ],
        capture_output=True,
        text=True
    )
    return {"status":status,"output_path":output_path}


def build_multiple_docs(folder_paths,progress_bar):
    results = []
    for folder_path in folder_paths:
        my_dict = {
            "folder_path":folder_path
        }
        results.append(my_dict)
    num_cores = max(multiprocessing.cpu_count()//2,1)
    with WorkerPool(n_jobs=num_cores,daemon=False) as pool:
        results = pool.map(build_docs,results,progress_bar=progress_bar)
    return results

if __name__=="__main__":
    folder_paths = [
        r"C:\Users\prakhar.a.gandhi\Downloads\knapsack\automateDocs",
        r"C:\Users\prakhar.a.gandhi\Downloads\knapsack\knapsack"
    ]
    progress_bar = True
    results = build_multiple_docs(folder_paths,progress_bar)
    pprint(results)
