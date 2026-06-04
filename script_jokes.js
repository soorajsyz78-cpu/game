// DOM Elements
const apiSelect = document.getElementById('api-select');
const categoryGroup = document.getElementById('category-group');
const categorySelect = document.getElementById('category-select');
const countInput = document.getElementById('count-input');
const getJokeBtn = document.getElementById('get-joke-btn');
const clearCacheBtn = document.getElementById('clear-cache-btn');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('error-message');
const jokesSection = document.getElementById('jokes-section');
const jokesContainer = document.getElementById('jokes-container');
const emptyState = document.getElementById('empty-state');
const timestamp = document.getElementById('timestamp');

// Event Listeners
apiSelect.addEventListener('change', onApiChange);
getJokeBtn.addEventListener('click', onGetJoke);
clearCacheBtn.addEventListener('click', onClearCache);

// Functions
function onApiChange() {
    const selectedApi = apiSelect.value;
    // Show category select only for JokeAPI
    categoryGroup.style.display = selectedApi === 'jokeapi' ? 'flex' : 'none';
}

async function onGetJoke() {
    const api = apiSelect.value;
    const category = categorySelect.value;
    const count = parseInt(countInput.value) || 1;

    // Show loading
    showLoading();
    hideError();

    try {
        const params = new URLSearchParams();
        params.append('api', api);
        params.append('count', count);
        if (api === 'jokeapi') {
            params.append('category', category);
        }

        const response = await fetch(`/api/joke?${params}`);
        const data = await response.json();

        if (data.success) {
            displayJokes(data.data, count);
            updateTimestamp(data.timestamp);
        } else {
            showError('Failed to fetch joke. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('An error occurred. Please try again.');
    } finally {
        hideLoading();
    }
}

async function onClearCache() {
    try {
        const response = await fetch('/api/clear-cache', { method: 'POST' });
        const data = await response.json();
        if (data.success) {
            showNotification('Cache cleared successfully!');
        }
    } catch (error) {
        console.error('Error clearing cache:', error);
        showError('Failed to clear cache');
    }
}

function displayJokes(jokes, count) {
    emptyState.classList.add('hidden');
    jokesSection.classList.remove('hidden');
    jokesContainer.innerHTML = '';

    // Handle single joke object or array
    const jokeArray = Array.isArray(jokes) ? jokes : [jokes];

    jokeArray.forEach((joke, index) => {
        if (joke) {
            const card = createJokeCard(joke, index + 1);
            jokesContainer.appendChild(card);
        }
    });
}

function createJokeCard(joke, number) {
    const card = document.createElement('div');
    card.className = 'joke-card';

    let contentHTML = `<div class="joke-number">Joke #${number}</div>`;
    contentHTML += '<div class="joke-content">';

    if (joke.joke) {
        // Single line joke
        contentHTML += `<div class="joke-single">${escapeHtml(joke.joke)}</div>`;
    } else if (joke.setup && joke.punchline) {
        // Two-part joke
        contentHTML += `<div class="joke-setup">${escapeHtml(joke.setup)}</div>`;
        contentHTML += `<div class="joke-punchline">${escapeHtml(joke.punchline)}</div>`;
    }

    contentHTML += '</div>';

    // Add metadata
    let metaHTML = '<div class="joke-meta">';
    if (joke.source) {
        metaHTML += `<span class="joke-source">📡 ${joke.source}</span>`;
    }
    if (joke.category) {
        metaHTML += `<span class="joke-category">📂 ${joke.category}</span>`;
    }
    metaHTML += '</div>';

    card.innerHTML = contentHTML + metaHTML;
    return card;
}

function showLoading() {
    loading.classList.remove('hidden');
    getJokeBtn.disabled = true;
}

function hideLoading() {
    loading.classList.add('hidden');
    getJokeBtn.disabled = false;
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
}

function hideError() {
    errorMessage.classList.add('hidden');
}

function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #4caf50;
        color: white;
        padding: 15px 20px;
        border-radius: 5px;
        z-index: 1000;
        animation: fadeIn 0.3s ease;
    `;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);
}

function updateTimestamp(iso8601) {
    const date = new Date(iso8601);
    const formatted = date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    timestamp.textContent = `Last updated: ${formatted}`;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    onApiChange(); // Set initial state
    hideError();
    hideLoading();
});
