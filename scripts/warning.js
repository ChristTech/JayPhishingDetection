document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const url = decodeURIComponent(urlParams.get('url'));
    
    // Display the URL being checked
    document.getElementById('detectedUrl').textContent = url;

    // Mark as Safe button handler
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
                console.log('URL whitelisted successfully');
                // Use chrome.tabs API to navigate
                chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
                    chrome.tabs.update(tabs[0].id, {url: url});
                });
            } else {
                console.error('Whitelisting failed:', data.message);
            }
        } catch (error) {
            console.error('Error whitelisting URL:', error);
        }
    });
});