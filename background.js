const API_URL = "https://jayphishingdetection.onrender.com/api/check_url";

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url: msg.url })
  })
    .then(r => r.json())
    .then(data => sendResponse(data))
    .catch(() => sendResponse({ is_phishing: false }));
  return true; // keep channel open
});

chrome.webNavigation.onBeforeNavigate.addListener(async function(details) {
    // Skip non-main frame, extension pages, and safe redirects
    if (details.frameId !== 0 || 
        details.url.startsWith('chrome://') ||
        details.url.startsWith('chrome-extension://') || 
        details.url.includes('warning.html')) {
        return;
    }

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: details.url })
        });
        const data = await response.json();

        // Update statistics
        chrome.storage.local.get(['urlsChecked', 'phishingBlocked'], function(result) {
            let urlsChecked = (result.urlsChecked || 0) + 1;
            let phishingBlocked = (result.phishingBlocked || 0);
            
            if (data.is_phishing) {
                phishingBlocked += 1;
            }

            chrome.storage.local.set({
                urlsChecked: urlsChecked,
                phishingBlocked: phishingBlocked
            }, function() {
                console.log('Stats updated:', {urlsChecked, phishingBlocked});
            });
        });

        // Show warning if phishing detected
        if (data.is_phishing) {
            chrome.tabs.update(details.tabId, {
                url: chrome.runtime.getURL(
                    `warning.html?url=${encodeURIComponent(details.url)}&confidence=${data.confidence}`
                )
            });
        }
    } catch (error) {
        console.error('Error checking URL:', error);
    }
}, {
    url: [{
        urlMatches: '.*'
    }]
});
