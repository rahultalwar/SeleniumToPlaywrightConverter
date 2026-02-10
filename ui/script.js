const javaInput = document.getElementById('java-input');
const tsOutput = document.getElementById('ts-output');
const convertBtn = document.getElementById('convert-btn');
const btnText = convertBtn.querySelector('.btn-text');
const loader = convertBtn.querySelector('.loader');
const copyBtn = document.getElementById('copy-btn');
const downloadBtn = document.getElementById('download-btn');
const clearBtn = document.getElementById('clear-btn');
const modelDropdown = document.getElementById('model-dropdown');
const statusMsg = document.getElementById('status-msg');

// API Configuration - works for both local and Vercel
const BASE_URL = '';
const API_URL = `${BASE_URL}/convert`;
const MODELS_URL = `${BASE_URL}/models`;
const HEALTH_URL = `${BASE_URL}/health`;

// Model display names with descriptions
const MODEL_INFO = {
    'llama-3.1-8b-instant': { name: 'Llama 3.1 8B', context: 'Fast & efficient' },
    'llama-3.3-70b-versatile': { name: 'Llama 3.3 70B', context: 'Most capable' },
    'mixtral-8x7b-32768': { name: 'Mixtral 8x7B', context: '32K context' }
};

// Fetch with timeout and retry
async function fetchWithRetry(url, options, retries = 3, timeout = 30000) {
    for (let i = 0; i < retries; i++) {
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), timeout);
            
            const response = await fetch(url, {
                ...options,
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            return response;
        } catch (err) {
            console.warn(`Attempt ${i + 1} failed:`, err.message);
            if (i === retries - 1) throw err;
            // Wait before retry (exponential backoff)
            await new Promise(r => setTimeout(r, 1000 * (i + 1)));
        }
    }
}

// Fetch available models from server and update dropdown
async function fetchModels() {
    try {
        console.log('Fetching models from:', MODELS_URL);
        updateStatus('Loading available models...', 'idle');
        
        const response = await fetchWithRetry(MODELS_URL, {
            method: 'GET',
            headers: { 'Accept': 'application/json' }
        }, 2, 10000);
        
        console.log('Models response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('Models data:', data);
        
        if (data.models && data.models.length > 0) {
            // Clear existing options
            modelDropdown.innerHTML = '';
            
            // Add options for each available model
            data.models.forEach(model => {
                const option = document.createElement('option');
                option.value = model;
                const info = MODEL_INFO[model] || { name: model, context: '' };
                option.textContent = `${info.name}`;
                option.title = info.context;
                modelDropdown.appendChild(option);
            });
            
            // Select default if provided
            if (data.default && data.models.includes(data.default)) {
                modelDropdown.value = data.default;
            }
            
            updateStatus('Ready to convert. Select a model to begin.', 'idle');
        }
    } catch (err) {
        console.error('Error fetching models:', err);
        updateStatus('Using default models (API may be waking up...)', 'idle');
        // Reset to default options after a delay
        setTimeout(() => {
            updateStatus('Ready to convert.', 'idle');
        }, 3000);
    }
}

// Initialize
fetchModels();

async function performConversion() {
    const javaCode = javaInput.value.trim();
    if (!javaCode) {
        updateStatus('Please enter some Java code.', 'error');
        return;
    }

    setLoading(true);
    const selectedModel = modelDropdown.value;
    const modelInfo = MODEL_INFO[selectedModel] || { name: selectedModel };
    updateStatus(`Converting with ${modelInfo.name}...`, 'idle');

    try {
        console.log('Sending conversion request to:', API_URL);
        
        const response = await fetchWithRetry(API_URL, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                java_source_code: javaCode,
                target_flavor: 'typescript',
                model: selectedModel
            })
        }, 2, 30000);

        console.log('Convert response status:', response.status);
        
        const responseText = await response.text();
        console.log('Raw response:', responseText.substring(0, 200));
        
        let data;
        try {
            data = JSON.parse(responseText);
        } catch (e) {
            console.error('Failed to parse JSON:', e);
            throw new Error('Invalid response from server');
        }

        if (data.status === 'success') {
            tsOutput.textContent = data.playwright_code;
            Prism.highlightElement(tsOutput);
            updateStatus('Conversion successful!', 'success');
        } else {
            updateStatus(data.error_message || 'Conversion failed.', 'error');
            tsOutput.textContent = `// Error:\n${data.error_message || 'Unknown error'}`;
        }
    } catch (err) {
        console.error('API Error:', err);
        if (err.name === 'AbortError') {
            updateStatus('Request timed out. Server may be cold-starting, please try again.', 'error');
        } else {
            updateStatus(`Network error: ${err.message}. Server may be offline.`, 'error');
        }
        tsOutput.textContent = `// Error: ${err.message}\n// Please check console for details.`;
    } finally {
        setLoading(false);
    }
}

function setLoading(isLoading) {
    convertBtn.disabled = isLoading;
    if (isLoading) {
        btnText.style.opacity = '0';
        loader.classList.remove('hidden');
    } else {
        btnText.style.opacity = '1';
        loader.classList.add('hidden');
    }
}

function updateStatus(msg, type) {
    statusMsg.textContent = msg;
    statusMsg.className = type;
}

// Actions
copyBtn.addEventListener('click', () => {
    const code = tsOutput.textContent;
    navigator.clipboard.writeText(code).then(() => {
        const originalText = copyBtn.textContent;
        copyBtn.textContent = '✅';
        setTimeout(() => copyBtn.textContent = originalText, 2000);
    });
});

downloadBtn.addEventListener('click', () => {
    const code = tsOutput.textContent;
    const blob = new Blob([code], { type: 'text/typescript' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'ConvertedTest.spec.ts';
    a.click();
});

clearBtn.addEventListener('click', () => {
    javaInput.value = '';
    tsOutput.textContent = '// Converted code will appear here...';
    updateStatus('Ready to convert.', 'idle');
});

convertBtn.addEventListener('click', performConversion);

// Update status when model changes
modelDropdown.addEventListener('change', () => {
    const selectedModel = modelDropdown.value;
    const info = MODEL_INFO[selectedModel];
    if (info) {
        updateStatus(`Selected ${info.name}. Ready to convert.`, 'idle');
    }
});

// Shortcut (Cmd/Ctrl + Enter)
document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
        performConversion();
    }
});
