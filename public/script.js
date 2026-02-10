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

// API Configuration - Vercel serverless functions
const API_URL = '/convert';
const MODELS_URL = '/models';
const HEALTH_URL = '/health';

// Model display names with descriptions
const MODEL_INFO = {
    'moonshot-v1-8k': { name: 'Moonshot v1 (8K)', context: '8K context' },
    'moonshot-v1-32k': { name: 'Moonshot v1 (32K)', context: '32K context' },
    'moonshot-v1-128k': { name: 'Moonshot v1 (128K)', context: '128K context' }
};

// Fetch available models from server and update dropdown
async function fetchModels() {
    try {
        const response = await fetch(MODELS_URL);
        const data = await response.json();
        
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
        }
    } catch (err) {
        console.error('Error fetching models:', err);
        // Keep default options if fetch fails
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
    updateStatus(`Connecting to Moonshot AI (${modelInfo.name})...`, 'idle');

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                java_source_code: javaCode,
                target_flavor: 'typescript',
                model: selectedModel
            })
        });

        const data = await response.json();

        if (data.status === 'success') {
            tsOutput.textContent = data.playwright_code;
            Prism.highlightElement(tsOutput);
            updateStatus('Conversion successful!', 'success');
        } else {
            updateStatus(data.error_message || 'Conversion failed.', 'error');
            tsOutput.textContent = `// Error:\n${data.error_message}`;
        }
    } catch (err) {
        console.error('API Error:', err);
        updateStatus('Network error or server offline.', 'error');
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

// Update status when model changes to show context info
modelDropdown.addEventListener('change', () => {
    const selectedModel = modelDropdown.value;
    const info = MODEL_INFO[selectedModel];
    if (info) {
        updateStatus(`Selected ${info.name} - ${info.context}. Ready to convert.`, 'idle');
    }
});

// Shortcut (Cmd/Ctrl + Enter)
document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
        performConversion();
    }
});
