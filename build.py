#!/usr/bin/env python3
"""
Build script for calisma_saati_hesaplama application.
This script automatically creates a PyInstaller spec with proper language file inclusion.
"""
import os
import subprocess
import sys

def build_app():
    print("Building calisma_saati_hesaplama application...")
    
    # First, generate a basic spec file
    subprocess.run(['pyi-makespec', '--windowed', "-F", 'app.py']) 
    
    # Read the generated spec file
    with open('app.spec', 'r') as file:
        spec_content = file.read()
    
    # Modify the spec file to include language files
    # We're looking for the datas=[] line and replacing it with our configuration
    modified_spec = spec_content.replace(
        'datas=[]',
        "datas=[('utils/languages/*.json', 'utils/languages')]"
    )
    
    # Write the modified spec back
    with open('app.spec', 'w') as file:
        file.write(modified_spec)
    
    print("Modified spec file to include language files")
    
    # Build the application with PyInstaller
    subprocess.run(['pyinstaller', 'app.spec'])
    
    print("Build complete! Executable is in the 'dist' directory.")

if __name__ == "__main__":
    build_app()