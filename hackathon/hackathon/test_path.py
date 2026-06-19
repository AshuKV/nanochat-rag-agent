"""
Quick test to verify the vector store path is correct
"""
import os
from ingest_code import DB_CHROMA_PATH

print("="*70)
print("PATH VERIFICATION TEST")
print("="*70)

print(f"\n📍 DB_CHROMA_PATH from ingest_code.py:")
print(f"   Relative: {DB_CHROMA_PATH}")
print(f"   Absolute: {os.path.abspath(DB_CHROMA_PATH)}")

print(f"\n📂 Current working directory:")
print(f"   {os.getcwd()}")

print(f"\n✅ Path exists? {os.path.exists(DB_CHROMA_PATH)}")

if os.path.exists(DB_CHROMA_PATH):
    print(f"\n📊 Contents:")
    contents = os.listdir(DB_CHROMA_PATH)
    for item in contents:
        print(f"   • {item}")
else:
    print(f"\n❌ Path does not exist!")
    print(f"\n🔍 Looking for vector_stores in parent directories...")
    
    # Check different possible locations
    possible_paths = [
        "vector_stores/db_chroma_code",
        "../vector_stores/db_chroma_code",
        "../../vector_stores/db_chroma_code",
        "../../../vector_stores/db_chroma_code"
    ]
    
    for path in possible_paths:
        abs_path = os.path.abspath(path)
        exists = os.path.exists(path)
        print(f"   {path}")
        print(f"      → {abs_path}")
        print(f"      → Exists: {exists}")

print("="*70)

