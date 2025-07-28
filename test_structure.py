#!/usr/bin/env python3
"""
Test script to validate the code structure without running the full system
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported correctly"""
    print("Testing import structure...")
    
    try:
        # Test basic Python imports
        import time
        import logging
        import threading
        import random
        print("✓ Basic Python modules imported successfully")
        
        # Test if we can at least parse the files
        import ast
        
        files_to_check = [
            'src/view_generator.py',
            'src/safety_controller.py', 
            'src/simulation/view_simulator.py',
            'src/proxy/proxy_manager.py'
        ]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    content = f.read()
                    try:
                        ast.parse(content)
                        print(f"✓ {file_path} - syntax is valid")
                    except SyntaxError as e:
                        print(f"✗ {file_path} - syntax error: {e}")
                        return False
            else:
                print(f"✗ {file_path} - file not found")
                return False
        
        print("✓ All core files have valid Python syntax")
        return True
        
    except Exception as e:
        print(f"✗ Import test failed: {e}")
        return False

def test_config_files():
    """Test that configuration files exist and are valid"""
    print("\nTesting configuration files...")
    
    try:
        import yaml
        
        config_files = [
            'config/proxy_sources.yaml',
            'config/test_config.yaml'
        ]
        
        for config_file in config_files:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    try:
                        yaml.safe_load(f)
                        print(f"✓ {config_file} - valid YAML")
                    except yaml.YAMLError as e:
                        print(f"✗ {config_file} - YAML error: {e}")
                        return False
            else:
                print(f"✗ {config_file} - file not found")
                return False
        
        print("✓ All configuration files are valid")
        return True
        
    except ImportError:
        print("✗ PyYAML not available - cannot test config files")
        return False
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        return False

def test_entry_point():
    """Test that the main entry point is properly structured"""
    print("\nTesting entry point...")
    
    try:
        if os.path.exists('run_simulation.py'):
            with open('run_simulation.py', 'r') as f:
                content = f.read()
                
            # Check for key components
            required_elements = [
                'def main():',
                'sys.argv',
                'ViewGenerator',
                'if __name__ == "__main__":'
            ]
            
            for element in required_elements:
                if element in content:
                    print(f"✓ Found required element: {element}")
                else:
                    print(f"✗ Missing required element: {element}")
                    return False
            
            print("✓ Entry point structure is correct")
            return True
        else:
            print("✗ run_simulation.py not found")
            return False
            
    except Exception as e:
        print(f"✗ Entry point test failed: {e}")
        return False

def test_folder_structure():
    """Test that the folder structure is correct"""
    print("\nTesting folder structure...")
    
    required_structure = [
        'src/',
        'src/proxy/',
        'src/simulation/',
        'config/',
        'run_simulation.py',
        'requirements.txt',
        'README.md'
    ]
    
    all_good = True
    for path in required_structure:
        if os.path.exists(path):
            print(f"✓ {path}")
        else:
            print(f"✗ {path} - missing")
            all_good = False
    
    if all_good:
        print("✓ Folder structure is correct")
    
    return all_good

def main():
    """Run all tests"""
    print("=== YouTube View Generator - Structure Test ===\n")
    
    tests = [
        test_folder_structure,
        test_imports,
        test_config_files,
        test_entry_point
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print(f"\n=== Test Results ===")
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✓ All {total} tests passed! The system structure is correct.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Configure proxies in config/proxy_sources.yaml (optional)")
        print("3. Test with: python run_simulation.py 'https://youtube.com/watch?v=test' 10")
    else:
        print(f"✗ {total - passed} out of {total} tests failed.")
        print("Please fix the issues above before proceeding.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
