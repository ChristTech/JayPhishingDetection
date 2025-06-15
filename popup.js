document.addEventListener('DOMContentLoaded', function() {
    // Get stats from storage and update display
    chrome.storage.local.get(['urlsChecked', 'phishingBlocked'], function(result) {
        document.getElementById('urlsChecked').textContent = result.urlsChecked || 0;
        document.getElementById('phishingBlocked').textContent = result.phishingBlocked || 0;
    });

    // Initial check when popup opens
    checkCurrentPage();

    // Add click handler for the check button
    document.getElementById('checkButton')?.addEventListener('click', function() {
        // Reset display state
        document.getElementById('loading').style.display = 'block';
        document.getElementById('result').style.display = 'none';
        
        // Recheck the page
        checkCurrentPage();
    });
});

function checkCurrentPage() {
    const loadingElement = document.getElementById('loading');
    const resultElement = document.getElementById('result');
    const statusElement = document.getElementById('status');

    loadingElement.style.display = 'block';
    resultElement.style.display = 'none';

    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        if (!tabs || !tabs[0]) {
            statusElement.textContent = 'Error: No active tab found';
            loadingElement.style.display = 'none';
            resultElement.style.display = 'block';
            return;
        }

        chrome.tabs.sendMessage(tabs[0].id, { action: "checkPage" }, function(response) {
            loadingElement.style.display = 'none';
            resultElement.style.display = 'block';
            
            if (chrome.runtime.lastError) {
                statusElement.textContent = 'Error: ' + chrome.runtime.lastError.message;
                return;
            }

            if (!response) {
                statusElement.textContent = 'Error: No response from content script';
                return;
            }

            if (response.success) {
                const statusDiv = document.getElementById('status');
                const confidenceDiv = document.getElementById('confidence');
                
                if (response.isPhishing) {
                    statusDiv.className = 'result dangerous';
                    statusDiv.textContent = 'Warning: Potential Phishing Site';
                } else {
                    statusDiv.className = 'result safe';
                    statusDiv.textContent = 'Safe: Legitimate Site';
                }
                
                confidenceDiv.textContent = `Confidence: ${response.confidence.toFixed(1)}%`;
                
                // Debug information
                console.log('Prediction details:', {
                    prediction: response.prediction,
                    confidence: response.confidence,
                    features: response.features
                });
            } else {
                statusElement.textContent = 'Error: ' + (response.error || 'Unknown error');
                console.error('Analysis failed:', response.error);
            }
        });
    });
}