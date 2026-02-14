"""
Newsletter Scheduler for Job Search Automation
Sends daily job alerts to subscribed users
"""
import schedule
import time
from datetime import datetime
from config_manager import ConfigManager
from browser_agent import BrowserAgent


def send_newsletter():
    """Send daily newsletter to all subscribers"""
    print(f"\n📧 Starting newsletter generation at {datetime.now()}")
    
    config = ConfigManager()
    subscriptions = config.config.get('newsletter_subscriptions', [])
    
    if not subscriptions:
        print("No active subscriptions found")
        return
    
    # Initialize browser agent
    browser = BrowserAgent(config)
    
    try:
        # Launch in headless mode for background operation
        browser.launch(headless=True)
        
        for subscription in subscriptions:
            if not subscription.get('active', False):
                continue
            
            email = subscription.get('email')
            preferences = subscription.get('preferences', {})
            
            print(f"Processing subscription for: {email}")
            
            # Search for jobs based on preferences
            query = preferences.get('job_types', ['software engineer'])[0]
            location = preferences.get('location', 'Remote')
            
            jobs = browser.search_jobs(query, location)
            
            print(f"  Found {len(jobs)} jobs")
            
            # In a real implementation, this would send an email
            # For now, just log the results
            if jobs:
                print(f"  Top job: {jobs[0]['title']} at {jobs[0]['company']}")
        
        print("✅ Newsletter generation complete")
    
    except Exception as e:
        print(f"❌ Error generating newsletter: {e}")
    
    finally:
        browser.close()


def run_scheduler():
    """Run the newsletter scheduler"""
    print("🚀 Starting Newsletter Scheduler")
    print("Newsletter will be sent daily at 9:00 AM (server local time)")
    
    # Schedule newsletter for 9 AM daily (server local time)
    # Note: Consider using timezone-aware scheduling for production
    schedule.every().day.at("09:00").do(send_newsletter)
    
    # For testing: also run every hour
    # schedule.every().hour.do(send_newsletter)
    
    print("Scheduler is running. Press Ctrl+C to stop.")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


if __name__ == '__main__':
    # Run newsletter immediately for testing
    # send_newsletter()
    
    # Start scheduler
    run_scheduler()
