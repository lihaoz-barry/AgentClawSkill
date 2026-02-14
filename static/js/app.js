// Job Search Automation System - Frontend JavaScript

// API Helper Functions
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(endpoint, options);
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        showNotification('API call failed: ' + error.message, 'error');
        return null;
    }
}

// Notification System
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type} show`;
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 4000);
}

// Browser Status Update
async function updateBrowserStatus() {
    const status = await apiCall('/api/browser/status');
    
    if (status) {
        const statusDot = document.getElementById('browserStatus');
        const statusText = document.getElementById('browserStatusText');
        const browserInfo = document.getElementById('browserInfo');
        const browserMode = document.getElementById('browserMode');
        const currentUrl = document.getElementById('currentUrl');
        const sessionCount = document.getElementById('sessionCount');
        
        if (status.running) {
            statusDot.classList.add('active');
            statusText.textContent = 'Running';
            browserInfo.style.display = 'block';
            browserMode.textContent = status.headless ? 'Headless' : 'Headed';
            currentUrl.textContent = status.current_url || '-';
            sessionCount.textContent = status.sessions || 0;
            
            // Enable buttons
            document.getElementById('toggleVisibility').disabled = false;
            document.getElementById('closeBrowser').disabled = false;
            document.getElementById('searchJobs').disabled = false;
            document.getElementById('viewCookies').disabled = false;
            document.getElementById('launchBrowser').disabled = true;
            document.getElementById('launchHeadless').disabled = true;
        } else {
            statusDot.classList.remove('active');
            statusText.textContent = 'Not Running';
            browserInfo.style.display = 'none';
            
            // Disable buttons
            document.getElementById('toggleVisibility').disabled = true;
            document.getElementById('closeBrowser').disabled = true;
            document.getElementById('searchJobs').disabled = true;
            document.getElementById('viewCookies').disabled = true;
            document.getElementById('launchBrowser').disabled = false;
            document.getElementById('launchHeadless').disabled = false;
        }
    }
}

// Browser Control Functions
document.getElementById('launchBrowser').addEventListener('click', async () => {
    showNotification('Launching browser in headed mode...', 'info');
    const result = await apiCall('/api/browser/launch', 'POST', { headless: false });
    
    if (result && result.status === 'success') {
        showNotification(result.message, 'success');
        await updateBrowserStatus();
    } else {
        showNotification('Failed to launch browser', 'error');
    }
});

document.getElementById('launchHeadless').addEventListener('click', async () => {
    showNotification('Launching browser in headless mode...', 'info');
    const result = await apiCall('/api/browser/launch', 'POST', { headless: true });
    
    if (result && result.status === 'success') {
        showNotification(result.message, 'success');
        await updateBrowserStatus();
    } else {
        showNotification('Failed to launch browser', 'error');
    }
});

document.getElementById('toggleVisibility').addEventListener('click', async () => {
    showNotification('Toggling browser visibility...', 'info');
    const result = await apiCall('/api/browser/toggle-visibility', 'POST');
    
    if (result && result.status === 'success') {
        showNotification(result.message, 'success');
        await updateBrowserStatus();
    } else {
        showNotification('Failed to toggle visibility', 'error');
    }
});

document.getElementById('closeBrowser').addEventListener('click', async () => {
    const result = await apiCall('/api/browser/close', 'POST');
    
    if (result && result.status === 'success') {
        showNotification(result.message, 'success');
        await updateBrowserStatus();
    } else {
        showNotification('Failed to close browser', 'error');
    }
});

// Whitelist Management
async function loadWhitelist() {
    const result = await apiCall('/api/whitelist');
    
    if (result && result.domains) {
        const domainList = document.getElementById('domainList');
        domainList.innerHTML = '';
        
        result.domains.forEach(domain => {
            const li = document.createElement('li');
            li.className = 'domain-item';
            li.innerHTML = `
                <span>${domain}</span>
                <button onclick="removeDomain('${domain}')">Remove</button>
            `;
            domainList.appendChild(li);
        });
    }
}

document.getElementById('addDomain').addEventListener('click', async () => {
    const domainInput = document.getElementById('newDomain');
    const domain = domainInput.value.trim();
    
    if (!domain) {
        showNotification('Please enter a domain', 'error');
        return;
    }
    
    const result = await apiCall('/api/whitelist', 'POST', { domain });
    
    if (result && result.status === 'success') {
        showNotification(result.message, 'success');
        domainInput.value = '';
        await loadWhitelist();
    } else {
        showNotification('Failed to add domain', 'error');
    }
});

async function removeDomain(domain) {
    const result = await apiCall('/api/whitelist', 'DELETE', { domain });
    
    if (result && result.status === 'success') {
        showNotification(result.message, 'success');
        await loadWhitelist();
    } else {
        showNotification('Failed to remove domain', 'error');
    }
}

// Job Search
document.getElementById('searchJobs').addEventListener('click', async () => {
    const query = document.getElementById('jobQuery').value.trim();
    const location = document.getElementById('jobLocation').value.trim();
    
    if (!query) {
        showNotification('Please enter a job search query', 'error');
        return;
    }
    
    showNotification('Searching for jobs...', 'info');
    const result = await apiCall('/api/job/search', 'POST', { query, location });
    
    if (result && result.status === 'success') {
        displayJobs(result.jobs);
        showNotification(`Found ${result.jobs.length} jobs`, 'success');
    } else {
        showNotification('Job search failed', 'error');
    }
});

function displayJobs(jobs) {
    const jobResults = document.getElementById('jobResults');
    jobResults.innerHTML = '';
    
    if (jobs.length === 0) {
        jobResults.innerHTML = '<p style="text-align: center; color: #666;">No jobs found</p>';
        return;
    }
    
    jobs.forEach(job => {
        const jobCard = document.createElement('div');
        jobCard.className = 'job-card';
        jobCard.innerHTML = `
            <h3>${job.title}</h3>
            <p><strong>Company:</strong> ${job.company}</p>
            <p><strong>Location:</strong> ${job.location}</p>
            <span class="job-platform">${job.platform}</span>
            <button onclick="applyToJob('${job.url}')">Apply</button>
        `;
        jobResults.appendChild(jobCard);
    });
}

async function applyToJob(jobUrl) {
    if (!jobUrl) {
        showNotification('Invalid job URL', 'error');
        return;
    }
    
    showNotification('Navigating to job application...', 'info');
    const result = await apiCall('/api/job/apply', 'POST', { job_url: jobUrl });
    
    if (result && result.status === 'success') {
        showNotification(result.result.message, 'success');
    } else {
        showNotification('Failed to apply to job', 'error');
    }
}

// Cookie Management
document.getElementById('viewCookies').addEventListener('click', async () => {
    const result = await apiCall('/api/browser/cookies');
    
    if (result && result.cookies) {
        const cookieDisplay = document.getElementById('cookieDisplay');
        
        if (result.cookies.length === 0) {
            cookieDisplay.innerHTML = '<p>No cookies found</p>';
        } else {
            cookieDisplay.innerHTML = '<pre>' + JSON.stringify(result.cookies, null, 2) + '</pre>';
        }
        
        showNotification(`Found ${result.cookies.length} cookies`, 'success');
    } else {
        showNotification('Failed to retrieve cookies', 'error');
    }
});

// Newsletter Subscription
document.getElementById('subscribeNewsletter').addEventListener('click', async () => {
    const email = document.getElementById('newsletterEmail').value.trim();
    
    if (!email) {
        showNotification('Please enter an email address', 'error');
        return;
    }
    
    const preferences = {
        job_types: ['full-time', 'remote'],
        frequency: 'daily'
    };
    
    const result = await apiCall('/api/newsletter/subscribe', 'POST', { email, preferences });
    
    const statusDiv = document.getElementById('newsletterStatus');
    
    if (result && result.status === 'success') {
        statusDiv.textContent = result.message;
        statusDiv.className = 'success';
        showNotification('Successfully subscribed to newsletter', 'success');
        document.getElementById('newsletterEmail').value = '';
    } else {
        statusDiv.textContent = 'Failed to subscribe';
        statusDiv.className = 'error';
        showNotification('Failed to subscribe to newsletter', 'error');
    }
});

// Prompt Configuration
document.getElementById('savePrompts').addEventListener('click', async () => {
    const jobSearchPrompt = document.getElementById('jobSearchPrompt').value;
    const applicationPrompt = document.getElementById('applicationPrompt').value;
    
    const config = {
        prompts: {
            job_search: jobSearchPrompt,
            application: applicationPrompt
        }
    };
    
    const result = await apiCall('/api/config', 'POST', config);
    
    if (result && result.status === 'success') {
        showNotification('Prompts saved successfully', 'success');
    } else {
        showNotification('Failed to save prompts', 'error');
    }
});

// Load Configuration on Page Load
async function loadConfiguration() {
    const config = await apiCall('/api/config');
    
    if (config && config.prompts) {
        document.getElementById('jobSearchPrompt').value = config.prompts.job_search || '';
        document.getElementById('applicationPrompt').value = config.prompts.application || '';
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    await updateBrowserStatus();
    await loadWhitelist();
    await loadConfiguration();
    
    // Update status every 5 seconds
    setInterval(updateBrowserStatus, 5000);
});
