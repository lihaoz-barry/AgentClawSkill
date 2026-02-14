"""
Browser Agent for Job Search Automation
Uses Playwright to automate job searches and applications
"""
import os
import asyncio
from typing import List, Dict, Any, Optional
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
import time


class BrowserAgent:
    """Agent for controlling browser automation"""
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.headless = False
        self.running = False
    
    def launch(self, headless: bool = False):
        """Launch the browser"""
        if self.running:
            return
        
        self.headless = headless
        self.playwright = sync_playwright().start()
        
        # Launch browser with options
        self.browser = self.playwright.chromium.launch(
            headless=headless,
            args=['--start-maximized'] if not headless else []
        )
        
        # Create context with viewport
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080} if not headless else None,
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        # Create a page
        self.page = self.context.new_page()
        self.running = True
    
    def is_running(self) -> bool:
        """Check if browser is running"""
        return self.running and self.browser is not None
    
    def close(self):
        """Close the browser"""
        if self.page:
            self.page.close()
            self.page = None
        
        if self.context:
            self.context.close()
            self.context = None
        
        if self.browser:
            self.browser.close()
            self.browser = None
        
        if self.playwright:
            self.playwright.stop()
            self.playwright = None
        
        self.running = False
    
    def toggle_visibility(self) -> bool:
        """
        Toggle between headed and headless mode
        Note: This requires relaunching the browser
        """
        current_headless = self.headless
        
        # Save current state
        cookies = self.get_cookies() if self.context else []
        
        # Relaunch with opposite mode
        self.close()
        self.launch(headless=not current_headless)
        
        # Restore cookies
        if cookies and self.context:
            self.context.add_cookies(cookies)
        
        return self.headless
    
    def get_status(self) -> Dict[str, Any]:
        """Get current browser status"""
        status = {
            'running': self.running,
            'headless': self.headless,
            'sessions': [],
            'current_url': ''
        }
        
        if self.page:
            try:
                status['current_url'] = self.page.url
            except:
                pass
        
        if self.context:
            status['sessions'] = len(self.context.cookies())
        
        return status
    
    def get_cookies(self) -> List[Dict[str, Any]]:
        """Get all cookies from current context"""
        if not self.context:
            return []
        
        return self.context.cookies()
    
    def search_jobs(self, query: str, location: str) -> List[Dict[str, Any]]:
        """
        Search for jobs on whitelisted platforms
        Returns a list of job postings
        """
        if not self.is_running():
            raise Exception("Browser not running")
        
        jobs = []
        whitelist = self.config_manager.get_whitelist()
        
        # Search on LinkedIn (example)
        if any('linkedin.com' in domain for domain in whitelist):
            linkedin_jobs = self._search_linkedin(query, location)
            jobs.extend(linkedin_jobs)
        
        # Search on Indeed (example)
        if any('indeed.com' in domain for domain in whitelist):
            indeed_jobs = self._search_indeed(query, location)
            jobs.extend(indeed_jobs)
        
        return jobs
    
    def _search_linkedin(self, query: str, location: str) -> List[Dict[str, Any]]:
        """Search for jobs on LinkedIn"""
        if not self.page:
            return []
        
        jobs = []
        
        try:
            # Navigate to LinkedIn jobs
            search_url = f'https://www.linkedin.com/jobs/search/?keywords={query}&location={location}'
            self.page.goto(search_url, timeout=30000)
            self.page.wait_for_timeout(2000)
            
            # Extract job listings
            job_cards = self.page.query_selector_all('.job-card-container, .jobs-search-results__list-item')
            
            for card in job_cards[:10]:  # Limit to first 10
                try:
                    title_elem = card.query_selector('.job-card-list__title, .job-card-container__link')
                    company_elem = card.query_selector('.job-card-container__company-name, .job-card-container__primary-description')
                    
                    if title_elem:
                        job = {
                            'title': title_elem.inner_text().strip(),
                            'company': company_elem.inner_text().strip() if company_elem else 'Unknown',
                            'platform': 'LinkedIn',
                            'url': title_elem.get_attribute('href') or '',
                            'location': location
                        }
                        jobs.append(job)
                except Exception as e:
                    continue
        
        except Exception as e:
            print(f"Error searching LinkedIn: {e}")
        
        return jobs
    
    def _search_indeed(self, query: str, location: str) -> List[Dict[str, Any]]:
        """Search for jobs on Indeed"""
        if not self.page:
            return []
        
        jobs = []
        
        try:
            # Navigate to Indeed
            search_url = f'https://www.indeed.com/jobs?q={query}&l={location}'
            self.page.goto(search_url, timeout=30000)
            self.page.wait_for_timeout(2000)
            
            # Extract job listings
            job_cards = self.page.query_selector_all('.job_seen_beacon, .jobsearch-SerpJobCard')
            
            for card in job_cards[:10]:  # Limit to first 10
                try:
                    title_elem = card.query_selector('.jobTitle, h2.jobTitle')
                    company_elem = card.query_selector('.companyName')
                    link_elem = card.query_selector('a')
                    
                    if title_elem:
                        job = {
                            'title': title_elem.inner_text().strip(),
                            'company': company_elem.inner_text().strip() if company_elem else 'Unknown',
                            'platform': 'Indeed',
                            'url': f"https://www.indeed.com{link_elem.get_attribute('href')}" if link_elem else '',
                            'location': location
                        }
                        jobs.append(job)
                except Exception as e:
                    continue
        
        except Exception as e:
            print(f"Error searching Indeed: {e}")
        
        return jobs
    
    def apply_to_job(self, job_url: str) -> Dict[str, Any]:
        """
        Apply to a job posting
        This is a basic implementation - real application would be more complex
        """
        if not self.is_running():
            raise Exception("Browser not running")
        
        if not self.config_manager.is_domain_whitelisted(job_url):
            return {
                'success': False,
                'message': 'Domain not whitelisted'
            }
        
        try:
            self.page.goto(job_url, timeout=30000)
            self.page.wait_for_timeout(2000)
            
            # Look for apply button
            apply_button = self.page.query_selector('button:has-text("Apply"), a:has-text("Apply")')
            
            if apply_button:
                # In a real implementation, this would fill out the application
                return {
                    'success': True,
                    'message': 'Navigated to application page',
                    'url': self.page.url
                }
            else:
                return {
                    'success': False,
                    'message': 'Apply button not found'
                }
        
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
