"""
Comprehensive Test Suite for Job Search Automation System
Tests all major components and functionality
"""
import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    modules = {
        'flask': 'Flask',
        'playwright.sync_api': 'Playwright',
        'requests': 'Requests',
        'bs4': 'BeautifulSoup',
        'schedule': 'Schedule',
        'dotenv': 'python-dotenv',
        'psutil': 'psutil'
    }
    
    passed = 0
    for module, name in modules.items():
        try:
            __import__(module)
            print(f"  ✅ {name}")
            passed += 1
        except ImportError as e:
            print(f"  ❌ {name}: {e}")
    
    return passed == len(modules)


def test_config_manager():
    """Test configuration manager"""
    print("\nTesting ConfigManager...")
    try:
        from config_manager import ConfigManager
        
        config = ConfigManager()
        
        # Test whitelist
        assert len(config.get_whitelist()) > 0, "Whitelist should not be empty"
        print("  ✅ Default whitelist loaded")
        
        # Test adding domain
        config.add_to_whitelist('test.com')
        assert 'test.com' in config.get_whitelist(), "Domain should be added"
        print("  ✅ Add domain works")
        
        # Test removing domain
        config.remove_from_whitelist('test.com')
        assert 'test.com' not in config.get_whitelist(), "Domain should be removed"
        print("  ✅ Remove domain works")
        
        # Test domain whitelisting check
        assert config.is_domain_whitelisted('https://www.linkedin.com/jobs'), "LinkedIn should be whitelisted"
        assert not config.is_domain_whitelisted('https://malicious.com'), "Random domain should not be whitelisted"
        print("  ✅ Domain validation works")
        
        # Test prompts
        prompt = config.get_prompt('job_search')
        assert prompt != '', "Job search prompt should exist"
        print("  ✅ Prompts work")
        
        return True
    except Exception as e:
        print(f"  ❌ ConfigManager test failed: {e}")
        return False


def test_browser_agent():
    """Test browser agent (without launching browser)"""
    print("\nTesting BrowserAgent...")
    try:
        from browser_agent import BrowserAgent
        from config_manager import ConfigManager
        
        config = ConfigManager()
        agent = BrowserAgent(config)
        
        # Test initialization
        assert agent is not None, "Agent should initialize"
        print("  ✅ Agent initializes")
        
        # Test status check
        assert not agent.is_running(), "Agent should not be running initially"
        print("  ✅ Status check works")
        
        # Test domain whitelisting helper
        assert agent._is_domain_whitelisted('linkedin.com'), "LinkedIn should be whitelisted"
        assert not agent._is_domain_whitelisted('malicious.com'), "Random domain should not be whitelisted"
        print("  ✅ Domain whitelisting helper works")
        
        return True
    except Exception as e:
        print(f"  ❌ BrowserAgent test failed: {e}")
        return False


def test_flask_app():
    """Test Flask app setup"""
    print("\nTesting Flask App...")
    try:
        # Temporarily set test mode
        os.environ['FLASK_SECRET_KEY'] = 'test-key'
        
        from app import app
        
        assert app is not None, "App should initialize"
        print("  ✅ App initializes")
        
        # Test that routes are registered
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        required_routes = ['/', '/api/config', '/api/whitelist', '/api/browser/status']
        
        for route in required_routes:
            assert route in routes, f"Route {route} should be registered"
        print("  ✅ All required routes registered")
        
        return True
    except Exception as e:
        print(f"  ❌ Flask App test failed: {e}")
        return False


def test_sample_scripts():
    """Test that sample scripts are valid Python"""
    print("\nTesting Sample Scripts...")
    scripts = [
        'sample_job_search.py',
        'sample_headless_search.py',
        'sample_whitelist_management.py'
    ]
    
    passed = 0
    for script in scripts:
        try:
            with open(script, 'r') as f:
                compile(f.read(), script, 'exec')
            print(f"  ✅ {script} is valid")
            passed += 1
        except Exception as e:
            print(f"  ❌ {script}: {e}")
    
    return passed == len(scripts)


def main():
    """Run all tests"""
    print("=" * 60)
    print("Job Search Automation System - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration Manager", test_config_manager),
        ("Browser Agent", test_browser_agent),
        ("Flask Application", test_flask_app),
        ("Sample Scripts", test_sample_scripts)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
