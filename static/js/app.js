// Personal Financial Analyst - Frontend JavaScript

// API Base URL
const API_BASE = window.location.origin;

// DOM Elements
const queryInput = document.getElementById('queryInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const resultsSection = document.getElementById('resultsSection');
const loadingState = document.getElementById('loadingState');
const resultsContent = document.getElementById('resultsContent');
const errorState = document.getElementById('errorState');
const examplesGrid = document.getElementById('examplesGrid');
const historyList = document.getElementById('historyList');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadExamples();
    loadHistory();
    checkSystemStatus();
    
    // Event listeners
    analyzeBtn.addEventListener('click', handleAnalyze);
    queryInput.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            handleAnalyze();
        }
    });
});

// Main analyze function
async function handleAnalyze() {
    const query = queryInput.value.trim();
    
    if (!query) {
        showError('請輸入查詢內容');
        return;
    }
    
    // Show loading state
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/api/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showResults(data);
            loadHistory(); // Refresh history
        } else {
            showError(data.error || '分析失敗');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('網絡錯誤，請稍後重試');
    }
}

// Show loading state
function showLoading() {
    resultsSection.style.display = 'block';
    loadingState.style.display = 'block';
    resultsContent.style.display = 'none';
    errorState.style.display = 'none';
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    
    // Disable analyze button
    analyzeBtn.disabled = true;
}

// Show results
function showResults(data) {
    // Hide loading
    loadingState.style.display = 'none';
    resultsContent.style.display = 'block';
    errorState.style.display = 'none';
    
    // Enable analyze button
    analyzeBtn.disabled = false;
    
    // Update execution time and steps count
    document.getElementById('executionTime').textContent = `${data.execution_time}秒`;
    document.getElementById('stepsCount').textContent = data.steps.length;
    
    // Render steps
    renderSteps(data.steps);
    
    // Render answer
    renderAnswer(data.answer);
}

// Render execution steps
function renderSteps(steps) {
    const stepsList = document.getElementById('stepsList');
    stepsList.innerHTML = '';
    
    steps.forEach((step, index) => {
        const stepElement = document.createElement('div');
        stepElement.className = `step-item ${step.status}`;
        
        stepElement.innerHTML = `
            <div class="step-number">${index + 1}</div>
            <div class="step-content">
                <div class="step-description">${escapeHtml(step.description)}</div>
                <div class="step-status">狀態: ${getStatusText(step.status)}</div>
            </div>
        `;
        
        stepsList.appendChild(stepElement);
    });
}

// Render answer
function renderAnswer(answer) {
    const answerContent = document.getElementById('answerContent');
    
    // Convert markdown-style headers to HTML
    const formatted = answer
        .replace(/^## (.+)$/gm, '<h2>$1</h2>')
        .replace(/^### (.+)$/gm, '<h3>$1</h3>')
        .replace(/^\*\*(.+?)\*\*$/gm, '<strong>$1</strong>');
    
    answerContent.innerHTML = formatted;
}

// Show error
function showError(message) {
    resultsSection.style.display = 'block';
    loadingState.style.display = 'none';
    resultsContent.style.display = 'none';
    errorState.style.display = 'block';
    
    document.getElementById('errorMessage').textContent = message;
    
    // Enable analyze button
    analyzeBtn.disabled = false;
    
    // Scroll to error
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Reset results
function resetResults() {
    resultsSection.style.display = 'none';
    queryInput.focus();
}

// Load examples
async function loadExamples() {
    try {
        const response = await fetch(`${API_BASE}/api/examples`);
        const data = await response.json();
        
        if (data.success) {
            renderExamples(data.examples);
        }
    } catch (error) {
        console.error('Failed to load examples:', error);
    }
}

// Render examples
function renderExamples(examples) {
    examplesGrid.innerHTML = '';
    
    examples.forEach(category => {
        const categoryElement = document.createElement('div');
        categoryElement.className = 'example-category';
        
        const queriesHtml = category.queries
            .map(query => `
                <span class="example-query" onclick="setQuery('${escapeHtml(query)}')">
                    ${escapeHtml(query)}
                </span>
            `)
            .join('');
        
        categoryElement.innerHTML = `
            <div class="category-title">${escapeHtml(category.category)}</div>
            <div class="example-queries">
                ${queriesHtml}
            </div>
        `;
        
        examplesGrid.appendChild(categoryElement);
    });
}

// Set query from example
function setQuery(query) {
    queryInput.value = query;
    queryInput.focus();
    
    // Optionally auto-execute
    // handleAnalyze();
}

// Load history
async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE}/api/history`);
        const data = await response.json();
        
        if (data.success) {
            renderHistory(data.history);
        }
    } catch (error) {
        console.error('Failed to load history:', error);
    }
}

// Render history
function renderHistory(history) {
    if (!history || history.length === 0) {
        historyList.innerHTML = '<p class="empty-state">暫無查詢歷史</p>';
        return;
    }
    
    historyList.innerHTML = '';
    
    history.forEach(item => {
        const historyElement = document.createElement('div');
        historyElement.className = 'history-item';
        historyElement.onclick = () => setQuery(item.query);
        
        const timestamp = new Date(item.timestamp).toLocaleString('zh-TW');
        
        historyElement.innerHTML = `
            <div class="history-query">${escapeHtml(item.query)}</div>
            <div class="history-meta">
                ${timestamp} · ${item.execution_time.toFixed(2)}秒
            </div>
        `;
        
        historyList.appendChild(historyElement);
    });
}

// Refresh history
function refreshHistory() {
    loadHistory();
}

// Check system status
async function checkSystemStatus() {
    try {
        const response = await fetch(`${API_BASE}/api/status`);
        const data = await response.json();
        
        if (data.success) {
            updateStatusIndicator(true, data.status);
        } else {
            updateStatusIndicator(false, '離線');
        }
    } catch (error) {
        updateStatusIndicator(false, '離線');
    }
}

// Update status indicator
function updateStatusIndicator(online, status) {
    const statusText = document.querySelector('.status-text');
    const statusDot = document.querySelector('.status-dot');
    
    if (online) {
        statusText.textContent = '系統就緒';
        statusDot.style.background = 'var(--success-color)';
    } else {
        statusText.textContent = '系統離線';
        statusDot.style.background = 'var(--error-color)';
    }
}

// Get status text in Chinese
function getStatusText(status) {
    const statusMap = {
        'pending': '等待中',
        'in_progress': '執行中',
        'completed': '已完成',
        'verified': '已驗證',
        'failed': '失敗'
    };
    
    return statusMap[status] || status;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Auto-check status every 30 seconds
setInterval(checkSystemStatus, 30000);
