// Dark Mode Toggle
function toggleTheme() {
    const theme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
}

// Load saved theme
if (localStorage.getItem('theme')) {
    document.documentElement.setAttribute('data-theme', localStorage.getItem('theme'));
}

// PWA Service Worker (for offline)
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js');  // Add sw.js file if needed for full offline
}

// Filter function already in index.html