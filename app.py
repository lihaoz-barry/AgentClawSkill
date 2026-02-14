"""
Job Search Automation System - Main Application
A web application for automating job searches and applications using agent browser
"""
import os
import json
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from browser_agent import BrowserAgent
from config_manager import ConfigManager

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Warn if using default secret key
if app.secret_key == 'dev-secret-key-change-in-production':
    import warnings
    warnings.warn(
        "Using default secret key! Please set FLASK_SECRET_KEY in .env for production.",
        UserWarning
    )

# Initialize managers
config_manager = ConfigManager()
browser_agent = None


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')


@app.route('/api/config', methods=['GET', 'POST'])
def manage_config():
    """Manage whitelist domains and prompts"""
    if request.method == 'GET':
        config = config_manager.get_config()
        return jsonify(config)
    
    elif request.method == 'POST':
        data = request.json
        config_manager.update_config(data)
        return jsonify({'status': 'success', 'message': 'Configuration updated'})


@app.route('/api/whitelist', methods=['GET', 'POST', 'DELETE'])
def manage_whitelist():
    """Manage whitelist domains"""
    if request.method == 'GET':
        domains = config_manager.get_whitelist()
        return jsonify({'domains': domains})
    
    elif request.method == 'POST':
        domain = request.json.get('domain')
        if domain:
            config_manager.add_to_whitelist(domain)
            return jsonify({'status': 'success', 'message': f'Added {domain} to whitelist'})
        return jsonify({'status': 'error', 'message': 'Domain is required'}), 400
    
    elif request.method == 'DELETE':
        domain = request.json.get('domain')
        if domain:
            config_manager.remove_from_whitelist(domain)
            return jsonify({'status': 'success', 'message': f'Removed {domain} from whitelist'})
        return jsonify({'status': 'error', 'message': 'Domain is required'}), 400


@app.route('/api/browser/status', methods=['GET'])
def browser_status():
    """Get browser agent status"""
    global browser_agent
    if browser_agent and browser_agent.is_running():
        status = browser_agent.get_status()
        return jsonify(status)
    return jsonify({
        'running': False,
        'headless': False,
        'sessions': []
    })


@app.route('/api/browser/launch', methods=['POST'])
def launch_browser():
    """Launch browser agent"""
    global browser_agent
    data = request.json or {}
    headless = data.get('headless', False)
    
    try:
        if browser_agent is None:
            browser_agent = BrowserAgent(config_manager)
        
        browser_agent.launch(headless=headless)
        return jsonify({
            'status': 'success',
            'message': f'Browser launched in {"headless" if headless else "headed"} mode'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/browser/toggle-visibility', methods=['POST'])
def toggle_browser_visibility():
    """Toggle browser between headed and headless mode"""
    global browser_agent
    if not browser_agent or not browser_agent.is_running():
        return jsonify({'status': 'error', 'message': 'Browser not running'}), 400
    
    try:
        new_mode = browser_agent.toggle_visibility()
        return jsonify({
            'status': 'success',
            'headless': new_mode,
            'message': f'Browser switched to {"headless" if new_mode else "headed"} mode'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/browser/close', methods=['POST'])
def close_browser():
    """Close browser agent"""
    global browser_agent
    if browser_agent:
        browser_agent.close()
        browser_agent = None
        return jsonify({'status': 'success', 'message': 'Browser closed'})
    return jsonify({'status': 'error', 'message': 'Browser not running'}), 400


@app.route('/api/browser/cookies', methods=['GET'])
def get_cookies():
    """Get browser cookies/sessions"""
    global browser_agent
    if not browser_agent or not browser_agent.is_running():
        return jsonify({'status': 'error', 'message': 'Browser not running'}), 400
    
    try:
        cookies = browser_agent.get_cookies()
        return jsonify({'cookies': cookies})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/job/search', methods=['POST'])
def search_jobs():
    """Search for jobs based on criteria"""
    global browser_agent
    if not browser_agent or not browser_agent.is_running():
        return jsonify({'status': 'error', 'message': 'Browser not running'}), 400
    
    data = request.json or {}
    query = data.get('query', 'software engineer')
    location = data.get('location', 'Remote')
    
    try:
        jobs = browser_agent.search_jobs(query, location)
        return jsonify({'status': 'success', 'jobs': jobs})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/job/apply', methods=['POST'])
def apply_job():
    """Apply to a specific job"""
    global browser_agent
    if not browser_agent or not browser_agent.is_running():
        return jsonify({'status': 'error', 'message': 'Browser not running'}), 400
    
    data = request.json or {}
    job_url = data.get('job_url')
    
    if not job_url:
        return jsonify({'status': 'error', 'message': 'Job URL is required'}), 400
    
    try:
        result = browser_agent.apply_to_job(job_url)
        return jsonify({'status': 'success', 'result': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/newsletter/subscribe', methods=['POST'])
def subscribe_newsletter():
    """Subscribe to daily job newsletter"""
    data = request.json or {}
    email = data.get('email')
    preferences = data.get('preferences', {})
    
    if not email:
        return jsonify({'status': 'error', 'message': 'Email is required'}), 400
    
    # Store newsletter subscription
    config_manager.add_newsletter_subscription(email, preferences)
    return jsonify({'status': 'success', 'message': 'Subscribed to daily newsletter'})


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    app.run(host='0.0.0.0', port=port, debug=debug)
