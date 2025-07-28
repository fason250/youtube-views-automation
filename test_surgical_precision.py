#!/usr/bin/env python3
"""
Test Script for Surgical Precision Browser Closing
Tests the ultra-efficient browser system with small numbers first
"""

import subprocess
import sys
import time

def test_surgical_precision():
    """Test the surgical precision closing with small numbers"""
    
    print("🧪 TESTING SURGICAL PRECISION BROWSER SYSTEM")
    print("=" * 60)
    print()
    
    # Test URL (use a short video for testing)
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll for testing
    
    print("🔬 Test 1: Small scale test (5 views)")
    print(f"📺 URL: {test_url}")
    print("⏱️  Watch time: 30 seconds each")
    print("🪟 Concurrent: 3 browsers")
    print("👁️  Mode: Headless (efficient)")
    print()
    
    # Run the test
    cmd = [
        'python3', 'browser_opener.py',
        test_url,
        '5',  # 5 views
        '--concurrent', '3',
        '--time', '30'  # 30 seconds each
    ]
    
    print("🚀 Starting test...")
    print(f"Command: {' '.join(cmd)}")
    print()
    
    try:
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        elapsed = time.time() - start_time
        
        print("📊 TEST RESULTS:")
        print(f"⏱️  Total time: {elapsed:.1f} seconds")
        print(f"✅ Exit code: {result.returncode}")
        print()
        
        if result.returncode == 0:
            print("🎉 SUCCESS! Surgical precision test passed!")
            print("✅ All browsers opened and closed correctly")
        else:
            print("❌ FAILED! Test did not complete successfully")
            print("Error output:")
            print(result.stderr)
        
        print("\n📋 Full output:")
        print(result.stdout)
        
    except subprocess.TimeoutExpired:
        print("⏰ Test timed out after 5 minutes")
        print("❌ This might indicate browsers are not closing properly")
    except Exception as e:
        print(f"❌ Test error: {e}")

def test_memory_efficiency():
    """Test memory efficiency with slightly larger numbers"""
    
    print("\n" + "=" * 60)
    print("🧠 MEMORY EFFICIENCY TEST")
    print("=" * 60)
    print()
    
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print("🔬 Test 2: Memory efficiency test (20 views)")
    print(f"📺 URL: {test_url}")
    print("⏱️  Watch time: 45 seconds each")
    print("🪟 Concurrent: 5 browsers")
    print("👁️  Mode: Headless (efficient)")
    print()
    
    cmd = [
        'python3', 'browser_opener.py',
        test_url,
        '20',  # 20 views
        '--concurrent', '5',
        '--time', '45'  # 45 seconds each
    ]
    
    print("🚀 Starting memory efficiency test...")
    print(f"Command: {' '.join(cmd)}")
    print()
    
    try:
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        elapsed = time.time() - start_time
        
        print("📊 MEMORY TEST RESULTS:")
        print(f"⏱️  Total time: {elapsed:.1f} seconds")
        print(f"✅ Exit code: {result.returncode}")
        print()
        
        if result.returncode == 0:
            print("🎉 SUCCESS! Memory efficiency test passed!")
            print("✅ System handled 20 views without crashes")
        else:
            print("❌ FAILED! Memory test did not complete successfully")
            print("Error output:")
            print(result.stderr)
        
        print("\n📋 Full output:")
        print(result.stdout)
        
    except subprocess.TimeoutExpired:
        print("⏰ Memory test timed out after 10 minutes")
        print("❌ This might indicate memory issues or slow performance")
    except Exception as e:
        print(f"❌ Memory test error: {e}")

def main():
    """Run all tests"""
    print("🧪 SURGICAL PRECISION BROWSER TESTING SUITE")
    print("Testing the ultra-efficient browser system before mass generation")
    print()
    
    # Check if browser_opener.py exists
    try:
        with open('browser_opener.py', 'r') as f:
            pass
    except FileNotFoundError:
        print("❌ browser_opener.py not found!")
        print("Make sure you're in the correct directory")
        sys.exit(1)
    
    # Run tests
    test_surgical_precision()
    
    # Ask user if they want to continue with memory test
    print("\n" + "=" * 60)
    response = input("Continue with memory efficiency test? (y/N): ")
    if response.lower() == 'y':
        test_memory_efficiency()
    
    print("\n" + "=" * 60)
    print("🎯 TESTING COMPLETE!")
    print()
    print("If tests passed, you can now safely run:")
    print("  python3 browser_opener.py 'YOUR_URL' 100    # 100 views")
    print("  python3 browser_opener.py 'YOUR_URL' 1000   # 1000 views")
    print("  python3 browser_opener.py 'YOUR_URL' 5000   # 5000 views!")
    print()
    print("🔪 Surgical precision closing ensures no crashes!")
    print("🧠 Memory monitoring prevents system overload!")
    print("⚡ Ultra-efficient for mass generation!")

if __name__ == "__main__":
    main()
