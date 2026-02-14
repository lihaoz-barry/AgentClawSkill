"""
Sample Script: Headless Mode Job Search
Demonstrates headless browser automation for background job searches
"""
from browser_agent import BrowserAgent
from config_manager import ConfigManager
import time


def main():
    print("🤖 Job Search Automation - Headless Mode\n")
    
    # Initialize
    config = ConfigManager()
    browser = BrowserAgent(config)
    
    # Launch in headless mode
    print("🚀 Launching browser in headless mode...")
    browser.launch(headless=True)
    
    # Search multiple job types
    searches = [
        ("Software Engineer", "San Francisco"),
        ("Data Scientist", "New York"),
        ("Product Manager", "Remote")
    ]
    
    all_jobs = []
    
    for query, location in searches:
        print(f"\n🔍 Searching: {query} in {location}")
        jobs = browser.search_jobs(query, location)
        print(f"   Found {len(jobs)} jobs")
        all_jobs.extend(jobs)
        time.sleep(2)  # Be nice to the servers
    
    print(f"\n📊 Total jobs found: {len(all_jobs)}")
    
    # Save results
    import json
    with open('job_results.json', 'w') as f:
        json.dump(all_jobs, f, indent=2)
    print("💾 Results saved to job_results.json")
    
    # Cleanup
    browser.close()
    print("\n✅ Done!")


if __name__ == '__main__':
    main()
