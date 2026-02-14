"""
Sample Script: Whitelist Domain Management
Demonstrates how to manage whitelist domains programmatically
"""
from config_manager import ConfigManager


def main():
    print("✅ Whitelist Domain Management\n")
    
    config = ConfigManager()
    
    # Display current whitelist
    print("Current whitelist domains:")
    for i, domain in enumerate(config.get_whitelist(), 1):
        print(f"{i}. {domain}")
    
    # Add new domains
    print("\n➕ Adding new domains...")
    new_domains = [
        'dice.com',
        'careerbuilder.com',
        'simplyhired.com'
    ]
    
    for domain in new_domains:
        config.add_to_whitelist(domain)
        print(f"   Added: {domain}")
    
    # Display updated whitelist
    print("\n✅ Updated whitelist:")
    for i, domain in enumerate(config.get_whitelist(), 1):
        print(f"{i}. {domain}")
    
    # Test domain checking
    print("\n🔍 Testing domain whitelist:")
    test_urls = [
        'https://www.linkedin.com/jobs/search',
        'https://www.example.com/jobs',
        'https://www.indeed.com/viewjob',
    ]
    
    for url in test_urls:
        is_whitelisted = config.is_domain_whitelisted(url)
        status = "✅ Whitelisted" if is_whitelisted else "❌ Not whitelisted"
        print(f"{status}: {url}")


if __name__ == '__main__':
    main()
