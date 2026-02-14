# 🔍 Job Search Automation System

An intelligent job search automation platform powered by browser agent technology. Automate your job search, manage applications, and receive daily newsletters with relevant job postings.

## ✨ Features

- 🌐 **Agent Browser Control**: Launch and control browser in headed or headless mode
- ✅ **Whitelist Domains**: Manage trusted job search platforms
- 💼 **Automated Job Search**: Search across multiple platforms simultaneously
- 🤖 **Auto-Apply**: Automate job application process
- 🍪 **Session Management**: View and manage browser cookies
- 📧 **Daily Newsletter**: Subscribe to automated job alerts
- ⚙️ **Customizable Prompts**: Configure AI prompts for data processing
- 🎯 **One-Click Control**: Toggle browser visibility with a single click
- 📊 **Real-time Status**: Monitor browser agent status in real-time

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Internet connection

### Installation

#### Linux/Mac

```bash
# Clone the repository
git clone https://github.com/lihaoz-barry/AgentClawSkill.git
cd AgentClawSkill

# Run setup script
chmod +x setup.sh
./setup.sh
```

#### Windows

```batch
# Clone the repository
git clone https://github.com/lihaoz-barry/AgentClawSkill.git
cd AgentClawSkill

# Run setup script
setup.bat
```

#### Manual Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Copy environment file
cp .env.example .env
```

## 🎯 Usage

### Starting the Application

```bash
# Activate virtual environment (if not already activated)
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Run the application
python app.py
```

The web interface will be available at: `http://localhost:5000`

### Web Interface Features

1. **Browser Control Panel**
   - Launch browser in headed or headless mode
   - Toggle visibility between modes
   - View real-time browser status
   - Close browser when done

2. **Whitelist Management**
   - Add trusted job search domains
   - Remove domains from whitelist
   - Default includes: LinkedIn, Indeed, Glassdoor, Monster, ZipRecruiter

3. **Job Search**
   - Enter job title/keywords
   - Specify location
   - Search across whitelisted platforms
   - View results with company details
   - One-click apply to jobs

4. **Cookie Management**
   - View all browser cookies
   - Monitor session data
   - Useful for authenticated searches

5. **Newsletter Subscription**
   - Subscribe with email
   - Receive daily job alerts
   - Customize preferences

6. **Prompt Configuration**
   - Customize AI prompts
   - Configure search strategies
   - Personalize automation behavior

## 📝 Sample Scripts

The repository includes sample scripts demonstrating various features:

### Basic Job Search

```bash
python sample_job_search.py
```

Demonstrates:
- Launching browser in headed mode
- Searching for jobs
- Retrieving cookies
- Proper cleanup

### Headless Mode Search

```bash
python sample_headless_search.py
```

Demonstrates:
- Background job searches
- Multiple search queries
- Saving results to JSON
- Headless browser operation

### Whitelist Management

```bash
python sample_whitelist_management.py
```

Demonstrates:
- Adding domains to whitelist
- Checking domain whitelist status
- Managing configuration programmatically

## 🔧 Configuration

### Environment Variables

Edit `.env` file to configure:

```bash
FLASK_SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True
BROWSER_HEADLESS=False
DEFAULT_JOB_SEARCH_QUERY=software engineer
DEFAULT_LOCATION=Remote
```

### Whitelist Domains

Default whitelisted domains:
- linkedin.com
- indeed.com
- glassdoor.com
- monster.com
- ziprecruiter.com

Add more domains via:
- Web UI (Whitelist panel)
- API: `POST /api/whitelist`
- Config file: `config.json`

## 🛠️ API Endpoints

### Browser Control

- `GET /api/browser/status` - Get browser status
- `POST /api/browser/launch` - Launch browser
- `POST /api/browser/toggle-visibility` - Toggle headed/headless
- `POST /api/browser/close` - Close browser
- `GET /api/browser/cookies` - Get cookies

### Configuration

- `GET /api/config` - Get configuration
- `POST /api/config` - Update configuration
- `GET /api/whitelist` - Get whitelist domains
- `POST /api/whitelist` - Add domain
- `DELETE /api/whitelist` - Remove domain

### Job Search

- `POST /api/job/search` - Search for jobs
- `POST /api/job/apply` - Apply to job

### Newsletter

- `POST /api/newsletter/subscribe` - Subscribe to newsletter

## 📦 Dependencies

- **Flask**: Web framework
- **Playwright**: Browser automation
- **BeautifulSoup4**: HTML parsing
- **Requests**: HTTP library
- **Schedule**: Task scheduling
- **python-dotenv**: Environment management
- **psutil**: Process utilities

## 🏗️ Project Structure

```
AgentClawSkill/
├── app.py                          # Main Flask application
├── browser_agent.py                # Browser automation logic
├── config_manager.py               # Configuration management
├── requirements.txt                # Python dependencies
├── setup.sh                        # Linux/Mac setup script
├── setup.bat                       # Windows setup script
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
├── templates/
│   └── index.html                  # Web UI template
├── static/
│   ├── css/
│   │   └── style.css              # Styles
│   └── js/
│       └── app.js                 # Frontend JavaScript
└── sample_*.py                     # Sample scripts
```

## 🔒 Security

- Whitelist domains to prevent malicious redirects
- Secure cookie handling
- Environment-based configuration
- No hardcoded credentials
- Input validation on all endpoints

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🐛 Troubleshooting

### Browser fails to launch
- Ensure Playwright browsers are installed: `playwright install chromium`
- Check for sufficient system resources
- Try headless mode if GUI issues occur

### Job search returns no results
- Verify whitelist domains are correct
- Check internet connection
- Some sites may require authentication

### Port 5000 already in use
- Change port in `.env`: `PORT=8000`
- Or kill process using port 5000

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub.

## 🎉 Acknowledgments

Built with modern web technologies and browser automation tools to make job searching easier and more efficient.
