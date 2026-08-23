const useCDNFallback = true;

function loadFallback(libraryName) {
    if (!useCDNFallback) {
        return;
    }
    const fallbackScript = document.createElement('script');
    fallbackScript.src = `/static/assets/js/${libraryName}`;
    document.head.appendChild(fallbackScript);
}
