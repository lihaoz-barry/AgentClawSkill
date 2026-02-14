"""
Sample Script: Basic Job Search Automation
Demonstrates how to use the browser agent to search for jobs
"""
from browser_agent import BrowserAgent
from config_manager import ConfigManager


def main():
    # Initialize configuration and browser agent
    config = ConfigManager()
    browser = BrowserAgent(config)
    
    print("🚀 Launching browser...")
    browser.launch(headless=False)
    
    print("🔍 Searching for jobs...")
    jobs = browser.search_jobs(
        query="Python Developer",
        location="Remote"
    )
    
    print(f"\n✅ Found {len(jobs)} jobs:")
    for i, job in enumerate(jobs, 1):
        print(f"\n{i}. {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Platform: {job['platform']}")
        print(f"   URL: {job['url']}")
    
    # Get cookies
    print("\n🍪 Getting browser cookies...")
    cookies = browser.get_cookies()
    print(f"Found {len(cookies)} cookies")
    
    # Close browser
    print("\n🛑 Closing browser...")
    browser.close()
    
    print("\n✨ Done!")


if __name__ == '__main__':
    main()
