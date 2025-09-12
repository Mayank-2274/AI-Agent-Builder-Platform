// API Base URL
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const form = document.getElementById('dataForm');
const companyInput = document.getElementById('company');
const urlInput = document.getElementById('url');
const messageDiv = document.getElementById('message');
const viewDataBtn = document.getElementById('viewData');
const dataDisplay = document.getElementById('dataDisplay');
const dataList = document.getElementById('dataList');

// Form submission handler
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        Company: companyInput.value.trim(),
        URL: urlInput.value.trim(),
        Data: "Auto-generated entry" // Default value since Data field is not shown
    };
    
    // Validate form data
    if (!formData.Company || !formData.URL) {
        showMessage('Please fill in Company and URL fields', 'error');
        return;
    }
    
    try {
        // Show loading state
        form.classList.add('loading');
        
        const response = await fetch(`${API_BASE_URL}/add_data`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showMessage(`✅ ${result.message}`, 'success');
            form.reset();
            
            // Auto-refresh data display if it's visible
            if (!dataDisplay.classList.contains('hidden')) {
                setTimeout(loadAllData, 1000);
            }
        } else {
            throw new Error(result.detail || 'Failed to add data');
        }
        
    } catch (error) {
        console.error('Error adding data:', error);
        showMessage(`❌ Error: ${error.message}`, 'error');
    } finally {
        form.classList.remove('loading');
    }
});

// View data button handler
viewDataBtn.addEventListener('click', async () => {
    if (dataDisplay.classList.contains('hidden')) {
        await loadAllData();
        dataDisplay.classList.remove('hidden');
        dataDisplay.classList.add('fade-in');
        viewDataBtn.textContent = 'Hide Data';
    } else {
        dataDisplay.classList.add('hidden');
        viewDataBtn.textContent = 'View All Data';
    }
});

// Load all data from API
async function loadAllData() {
    try {
        viewDataBtn.classList.add('loading');
        
        const response = await fetch(`${API_BASE_URL}/get_data`);
        const result = await response.json();
        
        if (response.ok) {
            displayData(result.data);
            showMessage(`📊 Loaded ${result.count} entries`, 'success');
        } else {
            throw new Error(result.detail || 'Failed to load data');
        }
        
    } catch (error) {
        console.error('Error loading data:', error);
        showMessage(`❌ Error loading data: ${error.message}`, 'error');
        dataList.innerHTML = '<p style="text-align: center; color: #e53e3e;">Failed to load data. Make sure the API server is running.</p>';
    } finally {
        viewDataBtn.classList.remove('loading');
    }
}

// Display data in the UI
function displayData(data) {
    if (!data || data.length === 0) {
        dataList.innerHTML = '<p style="text-align: center; color: #718096;">No data found. Add some entries to get started!</p>';
        return;
    }
    
    dataList.innerHTML = data.map(item => `
        <div class="data-item fade-in">
            <h3>🏢 ${escapeHtml(item.Company)}</h3>
            <p><strong>🌐 URL:</strong> <a href="${escapeHtml(item.URL)}" target="_blank" class="url">${escapeHtml(item.URL)}</a></p>
            <p><strong>📋 Data:</strong> ${escapeHtml(item.Data)}</p>
            <p><strong>🆔 ID:</strong> <code style="background: #e2e8f0; padding: 2px 6px; border-radius: 4px; font-size: 0.85em;">${item._id}</code></p>
            <div style="margin-top: 10px;">
                <button onclick="deleteEntry('${item._id}')" class="btn btn-danger" style="background: linear-gradient(145deg, #e53e3e, #c53030); color: white; padding: 8px 15px; font-size: 0.85em;">🗑️ Delete</button>
            </div>
        </div>
    `).join('');
}

// Delete entry function
async function deleteEntry(entryId) {
    if (!confirm('Are you sure you want to delete this entry?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/delete_data/${entryId}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showMessage('✅ Entry deleted successfully', 'success');
            // Refresh the data display
            await loadAllData();
        } else {
            throw new Error(result.detail || 'Failed to delete entry');
        }
        
    } catch (error) {
        console.error('Error deleting entry:', error);
        showMessage(`❌ Error: ${error.message}`, 'error');
    }
}

// Show message to user
function showMessage(text, type) {
    messageDiv.textContent = text;
    messageDiv.className = `message ${type} fade-in`;
    messageDiv.classList.remove('hidden');
    
    // Auto-hide success messages after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            messageDiv.classList.add('hidden');
        }, 5000);
    }
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Auto-focus first input on load
document.addEventListener('DOMContentLoaded', () => {
    companyInput.focus();
    
    // Check if API server is running
    checkApiConnection();
});

// Check API connection
async function checkApiConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/`);
        if (response.ok) {
            showMessage('🟢 Connected to API server', 'success');
        } else {
            throw new Error('API server responded with error');
        }
    } catch (error) {
        showMessage('🔴 API server not connected. Make sure to run: python api_server.py', 'error');
    }
}

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl+Enter to submit form
    if (e.ctrlKey && e.key === 'Enter') {
        form.dispatchEvent(new Event('submit'));
    }
    
    // Escape to hide data display
    if (e.key === 'Escape' && !dataDisplay.classList.contains('hidden')) {
        dataDisplay.classList.add('hidden');
        viewDataBtn.textContent = 'View All Data';
    }
});

// Add some visual feedback for form interactions
[companyInput, urlInput].forEach(input => {
    input.addEventListener('focus', (e) => {
        e.target.style.transform = 'scale(1.02)';
    });
    
    input.addEventListener('blur', (e) => {
        e.target.style.transform = 'scale(1)';
    });
});