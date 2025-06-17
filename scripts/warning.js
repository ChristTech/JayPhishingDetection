document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const url = decodeURIComponent(urlParams.get('url'));
    const confidence = parseFloat(urlParams.get('confidence'));
    
    // Display URL and confidence
    document.getElementById('detectedUrl').textContent = url;
    document.getElementById('confidence').textContent = confidence.toFixed(2);
    
    // Update confidence meter if it exists
    const confidenceBar = document.getElementById('confidenceBar');
    if (confidenceBar) {
        confidenceBar.style.width = `${confidence}%`;
        // Adjust color based on confidence level
        if (confidence > 80) {
            confidenceBar.style.backgroundColor = '#e74c3c';  // High risk - red
        } else if (confidence > 50) {
            confidenceBar.style.backgroundColor = '#f39c12';  // Medium risk - orange
        } else {
            confidenceBar.style.backgroundColor = '#f1c40f';  // Low risk - yellow
        }
    }
    
    // Return to Safety button handler
    document.getElementById('backButton').addEventListener('click', function() {
        chrome.tabs.update({ 
            url: 'https://www.google.com'
        });
    });

    // Mark as Safe button handler (permanent whitelist)
    document.getElementById('whitelistButton').addEventListener('click', async function() {
        try {
            const response = await fetch('https://jayphishingdetection.onrender.com/api/whitelist', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    url: url,
                    temporary: false
                })
            });
            
            const data = await response.json();
            if (data.success) {
                console.log('URL permanently whitelisted');
                chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
                    chrome.tabs.update(tabs[0].id, {url: url});
                });
            }
        } catch (error) {
            console.error('Error whitelisting URL:', error);
        }
    });

    // Proceed Anyway button handler (temporary whitelist)
    document.getElementById('proceedButton').addEventListener('click', async function() {
        try {
            const response = await fetch('https://jayphishingdetection.onrender.com/api/whitelist', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    url: url,
                    temporary: true
                })
            });
            
            const data = await response.json();
            if (data.success) {
                console.log('URL temporarily whitelisted');
                chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
                    chrome.tabs.update(tabs[0].id, {url: url});
                });
            }
        } catch (error) {
            console.error('Error proceeding to URL:', error);
        }
    });
});