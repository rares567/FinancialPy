import subprocess, sys

python_path = sys.executable

print("Deleting old database...")
subprocess.run([python_path, "drop_db.py"])

print("Creating database...")
subprocess.run([python_path, "create_db.py"])

print("Populating stocks...")
subprocess.run([python_path, "populate_stocks.py"])

print("Populating prices...")
subprocess.run([python_path, "populate_prices.py"])

print("All tasks completed successfully!")