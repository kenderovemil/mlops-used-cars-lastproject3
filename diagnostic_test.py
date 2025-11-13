import os
import sys

print("=" * 60)
print("DIAGNOSTIC JOB - Testing Azure ML Environment")
print("=" * 60)

print(f"\n✅ Python version: {sys.version}")
print(f"✅ Current working directory: {os.getcwd()}")
print(f"✅ Environment variables:")
for key in sorted(os.environ.keys()):
    if 'AZURE' in key or 'ML' in key:
        print(f"   {key}={os.environ[key][:50]}...")

print("\n✅ Testing file system write:")
test_file = "test_output.txt"
with open(test_file, "w") as f:
    f.write("Hello from Azure ML!")
print(f"   Created: {test_file}")

print("\n✅ Testing basic imports:")
try:
    import pandas as pd
    print(f"   pandas: {pd.__version__}")
except Exception as e:
    print(f"   pandas: ERROR - {e}")

try:
    import sklearn
    print(f"   sklearn: {sklearn.__version__}")
except Exception as e:
    print(f"   sklearn: ERROR - {e}")

print("\n" + "=" * 60)
print("DIAGNOSTIC COMPLETE")
print("=" * 60)
