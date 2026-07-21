// The Sweet Rolls - global front-end helpers
document.addEventListener('DOMContentLoaded', function () {
    // Auto-dismiss alerts after 4s
    document.querySelectorAll('.alert').forEach(function (alertEl) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alertEl);
            bsAlert.close();
        }, 4000);
    });
});

// ---------- Page loader: brief logo/spinner animation on every page change ----------
(function () {
    const loader = document.getElementById('pageLoader');
    if (!loader) return;

    const MIN_VISIBLE_MS = 450;  // minimum time the loader stays visible
    const NAV_DELAY_MS = 350;    // how long to show loader before navigating away
    const shownAt = Date.now();

    function hideLoader() {
        const elapsed = Date.now() - shownAt;
        const wait = Math.max(0, MIN_VISIBLE_MS - elapsed);
        setTimeout(function () {
            loader.classList.add('is-hidden');
        }, wait);
    }

    if (document.readyState === 'complete') {
        hideLoader();
    } else {
        window.addEventListener('load', hideLoader);
    }

    // If the page is restored from bfcache (browser back/forward), make sure
    // the loader isn't stuck visible.
    window.addEventListener('pageshow', function (event) {
        if (event.persisted) {
            loader.classList.add('is-hidden');
        }
    });

    // Intercept clicks on internal links (nav menu, logo, buttons, cards, etc.)
    // so the loader animation plays briefly before the new page appears.
    document.addEventListener('click', function (e) {
        const link = e.target.closest('a[href]');
        if (!link) return;

        const href = link.getAttribute('href');
        if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:')) return;
        if (link.target === '_blank' || link.hasAttribute('download')) return;
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;

        let url;
        try {
            url = new URL(href, window.location.href);
        } catch (err) {
            return;
        }
        if (url.origin !== window.location.origin) return;

        e.preventDefault();
        loader.classList.remove('is-hidden');
        setTimeout(function () {
            window.location.href = url.href;
        }, NAV_DELAY_MS);
    });
})();
