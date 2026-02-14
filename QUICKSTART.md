# Quick Start Guide - Job Search Automation System

## 🚀 Getting Started in 5 Minutes

### Step 1: Clone and Setup
```bash
git clone https://github.com/lihaoz-barry/AgentClawSkill.git
cd AgentClawSkill

# Run automated setup
./setup.sh        # Linux/Mac
# or
setup.bat         # Windows
```

### Step 2: Configure (Optional)
```bash
# Edit .env file to customize settings
nano .env

# Key settings:
# FLASK_SECRET_KEY - Change for production
# BROWSER_HEADLESS - True/False for default browser mode
```

### Step 3: Launch the Application
```bash
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

python app.py
```

### Step 4: Access the Web UI
Open your browser to: **http://localhost:5000**

## 📋 Quick Tutorial

### 1. Launch Browser Agent
- Click "Launch Browser (Headed)" to see the browser in action
- Or click "Launch Headless" for background operation

### 2. Manage Whitelist Domains
- Add trusted job sites like "linkedin.com", "indeed.com"
- Remove domains you don't want to search

### 3. Search for Jobs
- Enter job title/keywords (e.g., "Python Developer")
- Enter location (e.g., "Remote", "San Francisco")
- Click "Search Jobs"
- View results and click "Apply" to navigate to job pages

### 4. View Cookie Sessions
- Click "View Cookies" to see browser session data
- Useful for authenticated job searches

### 5. Subscribe to Newsletter
- Enter your email
- Get daily job alerts automatically

### 6. Customize Prompts
- Modify AI prompts for job search behavior
- Save changes to personalize automation

## 🎯 Common Use Cases

### Background Job Search (Headless)
```bash
python sample_headless_search.py
```
Searches multiple platforms in background, saves results to JSON.

### Interactive Job Search
```bash
python sample_job_search.py
```
Launch browser and search interactively.

### Manage Domains Programmatically
```bash
python sample_whitelist_management.py
```
Add/remove domains via Python API.

### Daily Newsletter (Background)
```bash
python newsletter_scheduler.py
```
Runs daily job search and sends results at 9 AM.

## 🔧 Troubleshooting

### Browser won't launch
```bash
playwright install chromium
```

### Port 5000 in use
Edit `.env` and set `PORT=8000`

### Import errors
```bash
pip install -r requirements.txt
```

## 📚 Next Steps

- Read full [README.md](README.md) for detailed documentation
- Check API endpoints for integration
- Customize prompts for your job preferences
- Set up daily newsletter for automation

## 💡 Tips

- Start with headed mode to see what's happening
- Switch to headless for production/background operation
- Whitelist only domains you trust
- Use the install config script to verify setup:
  ```bash
  python install_config.py
  ```

## 🆘 Need Help?

- Run test suite: `python test_suite.py`
- Check logs in `logs/` directory
- Review sample scripts for examples
- Open an issue on GitHub

---

**Ready to automate your job search!** 🎉
