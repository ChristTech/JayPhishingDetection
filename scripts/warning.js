document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const url = decodeURIComponent(urlParams.get('url'));
    
    // Decode and display URL
    const encodedUrl = urlParams.get('url');
    const decodedUrl = decodeURIComponent(encodedUrl);
    document.getElementById('detectedUrl').textContent = decodedUrl;
    
    // Format and display confidence
    const confidence = parseFloat(urlParams.get('confidence')).toFixed(2);
    document.getElementById('confidence').textContent = confidence;
    
    // Update confidence bar
    const confidenceBar = document.getElementById('confidenceBar');
    confidenceBar.style.width = `${confidence}%`;
    
    // Add button handlers
    document.getElementById('backButton').addEventListener('click', function() {
        // Redirect to Google's homepage
        chrome.tabs.update({ url: 'https://www.google.com' });
    });
    
    document.getElementById('proceedButton').addEventListener('click', async function() {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/whitelist', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    url: url,
                    temporary: true
                })
            });
            
            const data = await response.json();
            if (data.success) {
                chrome.tabs.update({ url: url });
            }
        } catch (error) {
            console.error('Error temporary whitelisting URL:', error);
        }
    });
    
    document.getElementById('whitelistButton').addEventListener('click', async function() {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/whitelist', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    url: url,
                    temporary: false
                })
            });
            
            const data = await response.json();
            if (data.success) {
                chrome.tabs.update({ url: url });
            }
        } catch (error) {
            console.error('Error whitelisting URL:', error);
        }
    });
});