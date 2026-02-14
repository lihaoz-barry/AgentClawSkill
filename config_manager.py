"""
Configuration Manager for Job Search Automation
Handles whitelist domains, prompts, and user preferences
"""
import json
import os
from typing import Dict, List, Any


class ConfigManager:
    """Manages configuration for the job search automation system"""
    
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return self._default_config()
        return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            'whitelist_domains': [
                'linkedin.com',
                'indeed.com',
                'glassdoor.com',
                'monster.com',
                'ziprecruiter.com'
            ],
            'prompts': {
                'job_search': 'Search for {query} jobs in {location}',
                'application': 'Apply to job with resume and cover letter',
                'data_extraction': 'Extract job title, company, location, and description'
            },
            'preferences': {
                'auto_apply': False,
                'save_searches': True,
                'notification_email': '',
                'search_interval_hours': 24
            },
            'newsletter_subscriptions': []
        }
    
    def _save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_config(self) -> Dict[str, Any]:
        """Get current configuration"""
        return self.config
    
    def update_config(self, updates: Dict[str, Any]):
        """Update configuration with new values"""
        self.config.update(updates)
        self._save_config()
    
    def get_whitelist(self) -> List[str]:
        """Get whitelist domains"""
        return self.config.get('whitelist_domains', [])
    
    def add_to_whitelist(self, domain: str):
        """Add domain to whitelist"""
        if 'whitelist_domains' not in self.config:
            self.config['whitelist_domains'] = []
        
        if domain not in self.config['whitelist_domains']:
            self.config['whitelist_domains'].append(domain)
            self._save_config()
    
    def remove_from_whitelist(self, domain: str):
        """Remove domain from whitelist"""
        if domain in self.config.get('whitelist_domains', []):
            self.config['whitelist_domains'].remove(domain)
            self._save_config()
    
    def is_domain_whitelisted(self, url: str) -> bool:
        """Check if a URL's domain is whitelisted"""
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        
        for whitelisted in self.get_whitelist():
            if whitelisted in domain:
                return True
        return False
    
    def get_prompt(self, prompt_type: str) -> str:
        """Get a specific prompt template"""
        return self.config.get('prompts', {}).get(prompt_type, '')
    
    def update_prompt(self, prompt_type: str, prompt: str):
        """Update a specific prompt template"""
        if 'prompts' not in self.config:
            self.config['prompts'] = {}
        
        self.config['prompts'][prompt_type] = prompt
        self._save_config()
    
    def add_newsletter_subscription(self, email: str, preferences: Dict[str, Any]):
        """Add newsletter subscription"""
        if 'newsletter_subscriptions' not in self.config:
            self.config['newsletter_subscriptions'] = []
        
        subscription = {
            'email': email,
            'preferences': preferences,
            'active': True
        }
        
        # Remove existing subscription for this email
        self.config['newsletter_subscriptions'] = [
            s for s in self.config['newsletter_subscriptions'] 
            if s.get('email') != email
        ]
        
        self.config['newsletter_subscriptions'].append(subscription)
        self._save_config()
