const javaInput = document.getElementById('java-input');
const tsOutput = document.getElementById('ts-output');
const convertBtn = document.getElementById('convert-btn');
const btnText = convertBtn.querySelector('.btn-text');
const loader = convertBtn.querySelector('.loader');
const copyBtn = document.getElementById('copy-btn');
const downloadBtn = document.getElementById('download-btn');
const clearBtn = document.getElementById('clear-btn');
const modelSelect = document.getElementById('model');
const statusMsg = document.getElementById('status-msg');

// API Configuration (Proxied through app.py)
const API_URL = '/convert';
const MODELS_URL = '/models';

async function fetchModels() {
    try {
        const response = await fetch(MODELS_URL);
        const data = await response.json();
        if (data.models && data.models.length > 0) {
            modelSelect.innerHTML = '';
            data.models.forEach(model => {
                const option = document.createElement('option');
                option.value = model;
                option.textContent = model;
                modelSelect.appendChild(option);
            });
            // Select llama3.2 if available as it's common
            const commonModel = data.models.find(m => m.includes('llama3.2') || m.includes('llama3'));
            if (commonModel) modelSelect.value = commonModel;
        }
    } catch (err) {
        console.error('Error fetching models:', err);
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
    updateStatus('Connecting to Ollama...', 'idle');

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                java_source_code: javaCode,
                model: modelSelect.value,
                target_flavor: 'typescript'
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

// Shortcut (Cmd/Ctrl + Enter)
document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
        performConversion();
    }
});
