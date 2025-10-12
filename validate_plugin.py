#!/usr/bin/env python3
"""
Validation script for the Moret plugin

This script validates the plugin structure without requiring fz to be installed.
"""

import json
import os
import sys

def validate_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description} NOT FOUND: {filepath}")
        return False

def validate_json_file(filepath, description):
    """Validate a JSON file"""
    if not validate_file_exists(filepath, description):
        return False
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        print(f"  → Valid JSON with {len(data)} top-level keys")
        return True
    except json.JSONDecodeError as e:
        print(f"  → Invalid JSON: {e}")
        return False

def validate_shell_script(filepath, description):
    """Validate a shell script"""
    if not validate_file_exists(filepath, description):
        return False
    
    # Check if executable
    is_executable = os.access(filepath, os.X_OK)
    if is_executable:
        print(f"  → Executable: Yes")
    else:
        print(f"  → Executable: No (should be executable)")
    
    # Check shebang
    with open(filepath, 'r') as f:
        first_line = f.readline().strip()
        if first_line.startswith('#!/'):
            print(f"  → Shebang: {first_line}")
        else:
            print(f"  → No shebang found")
    
    return True

def validate_model_json(filepath):
    """Validate the model JSON structure"""
    print("\nValidating Model JSON Structure:")
    print("-" * 50)
    
    with open(filepath, 'r') as f:
        model = json.load(f)
    
    required_keys = ['id', 'varprefix', 'delim', 'commentline', 'output']
    for key in required_keys:
        if key in model:
            print(f"✓ Required key '{key}': {model[key] if key != 'output' else f'{len(model[key])} outputs'}")
        else:
            print(f"✗ Missing required key: {key}")
    
    if 'output' in model:
        print(f"\n  Output variables defined:")
        for output_key in model['output']:
            print(f"    - {output_key}")

def validate_calculator_json(filepath):
    """Validate the calculator JSON structure"""
    print("\nValidating Calculator JSON Structure:")
    print("-" * 50)
    
    with open(filepath, 'r') as f:
        calc = json.load(f)
    
    required_keys = ['uri', 'models']
    for key in required_keys:
        if key in calc:
            print(f"✓ Required key '{key}': {calc[key] if key != 'models' else list(calc[key].keys())}")
        else:
            print(f"✗ Missing required key: {key}")

def main():
    print("=" * 60)
    print("Moret Plugin Structure Validation")
    print("=" * 60)
    
    all_valid = True
    
    # Check directory structure
    print("\n1. Checking Directory Structure:")
    print("-" * 50)
    dirs = ['.fz', '.fz/models', '.fz/calculators']
    for d in dirs:
        if os.path.isdir(d):
            print(f"✓ Directory exists: {d}")
        else:
            print(f"✗ Directory NOT FOUND: {d}")
            all_valid = False
    
    # Check model files
    print("\n2. Checking Model Files:")
    print("-" * 50)
    all_valid &= validate_json_file('.fz/models/Moret.json', 'Model definition')
    
    # Check calculator files
    print("\n3. Checking Calculator Files:")
    print("-" * 50)
    all_valid &= validate_shell_script('.fz/calculators/Moret.sh', 'Calculator script')
    all_valid &= validate_json_file('.fz/calculators/Localhost_Moret.json', 'Calculator alias')
    
    # Check sample files
    print("\n4. Checking Sample Files:")
    print("-" * 50)
    all_valid &= validate_file_exists('godiva.m5', 'Sample input file')
    all_valid &= validate_file_exists('example_usage.py', 'Example usage script')
    all_valid &= validate_file_exists('README.md', 'README')
    all_valid &= validate_file_exists('.gitignore', 'Git ignore file')
    
    # Detailed validation
    print("\n5. Detailed Validation:")
    print("-" * 50)
    validate_model_json('.fz/models/Moret.json')
    validate_calculator_json('.fz/calculators/Localhost_Moret.json')
    
    # Summary
    print("\n" + "=" * 60)
    if all_valid:
        print("✓ ALL VALIDATIONS PASSED")
        print("=" * 60)
        print("\nThe Moret plugin structure is complete and valid!")
        print("\nNext steps:")
        print("  1. Install fz: pip install fz")
        print("  2. Install MORET at /opt/MORET/scripts/moret.py")
        print("  3. Run: python example_usage.py")
        return 0
    else:
        print("✗ SOME VALIDATIONS FAILED")
        print("=" * 60)
        print("\nPlease fix the issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
