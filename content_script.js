document.addEventListener("click", e => {
  const a = e.target.closest("a");
  if (!a) return;
  e.preventDefault();
  chrome.runtime.sendMessage({ url: a.href }, response => {
    if (response.is_phishing) {
      alert("Warning: This link may be phishing!");
    } else {
      window.location.href = a.href;
    }
  });
});
