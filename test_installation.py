# test_installation.py
# Verify that the Educational Bitcoin Mining Simulator can run on this system

import sys
import os

def check_python_version():
    """Check if Python version is adequate"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} - TOO OLD")
        print("  Please install Python 3.7 or higher")
        return False

def check_tkinter():
    """Check if tkinter is available"""
    print("\nChecking tkinter (GUI library)...")
    try:
        import tkinter
        print("✓ tkinter is available - OK")
        return True
    except ImportError:
        print("✗ tkinter is NOT available")
        print("  Please reinstall Python with tcl/tk support")
        return False

def check_required_modules():
    """Check if required standard library modules are available"""
    print("\nChecking required modules...")
    modules = ["hashlib", "threading", "time", "datetime"]
    all_ok = True
    
    for module in modules:
        try:
            __import__(module)
            print(f"✓ {module} - OK")
        except ImportError:
            print(f"✗ {module} - MISSING")
            all_ok = False
    
    return all_ok

def check_files():
    """Check if all required files exist"""
    print("\nChecking project files...")
    required_files = ["main.py", "mining.py", "blockchain.py", "config.py"]
    all_ok = True
    
    for filename in required_files:
        if os.path.exists(filename):
            print(f"✓ {filename} - OK")
        else:
            print(f"✗ {filename} - MISSING")
            all_ok = False
    
    return all_ok

def test_imports():
    """Test if project modules can be imported"""
    print("\nTesting project imports...")
    try:
        import config
        print("✓ config.py - OK")
    except Exception as e:
        print(f"✗ config.py - ERROR: {e}")
        return False
    
    try:
        import blockchain
        print("✓ blockchain.py - OK")
    except Exception as e:
        print(f"✗ blockchain.py - ERROR: {e}")
        return False
    
    try:
        import mining
        print("✓ mining.py - OK")
    except Exception as e:
        print(f"✗ mining.py - ERROR: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic blockchain functionality"""
    print("\nTesting basic functionality...")
    try:
        from blockchain import Block, Blockchain
        
        # Test block creation
        block = Block(0, "0", 0, "Test", 0, 2)
        print("✓ Block creation - OK")
        
        # Test hash calculation
        hash_value = block.calculate_hash()
        if len(hash_value) == 64:
            print("✓ SHA-256 hash calculation - OK")
        else:
            print(f"✗ Hash length incorrect: {len(hash_value)}")
            return False
        
        # Test blockchain creation
        blockchain = Blockchain()
        if len(blockchain.chain) == 1:
            print("✓ Blockchain initialization - OK")
        else:
            print("✗ Blockchain initialization failed")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Functionality test failed: {e}")
        return False

def main():
    """Run all checks"""
    print("=" * 60)
    print("Educational Bitcoin Mining Simulator")
    print("Installation Verification Test")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Tkinter GUI", check_tkinter),
        ("Standard Modules", check_required_modules),
        ("Project Files", check_files),
        ("Module Imports", test_imports),
        ("Basic Functionality", test_basic_functionality)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} - EXCEPTION: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    all_passed = all(result for _, result in results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} - {name}")
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ ALL CHECKS PASSED!")
        print("\nYour system is ready to run the simulator.")
        print("\nTo start the simulator, run:")
        print("  python main.py")
        print("\nOr double-click:")
        print("  run_simulator.bat")
        return 0
    else:
        print("\n✗ SOME CHECKS FAILED")
        print("\nPlease fix the issues above before running the simulator.")
        print("See README.md for detailed installation instructions.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
