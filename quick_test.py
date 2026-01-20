#!/usr/bin/env python3
import sys
sys.path.insert(0, '/workspaces/programming-in-C/Arkserver/manager')

print("Test rapide des modules...")
from modules.backups import BackupManager
bm = BackupManager()
print(f"✅ format_size(1024) = {bm.format_size(1024)}")
print(f"✅ format_size(1048576) = {bm.format_size(1048576)}")
print(f"✅ format_size(1073741824) = {bm.format_size(1073741824)}")
print("\n✅ Tests de formatage OK!")
