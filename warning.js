window.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    document.getElementById('detectedUrl').textContent = urlParams.get('url');
    document.getElementById('confidence').textContent = urlParams.get('confidence');
    
    // Add event listeners to buttons
    document.getElementById('backButton').addEventListener('click', function() {
        window.history.back();
    });
    
    document.getElementById('proceedButton').addEventListener('click', function() {
        window.location.href = urlParams.get('url');
    });
});