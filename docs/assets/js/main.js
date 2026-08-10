// Zero-Cost AI Business v4 — shared JS utilities

// Copy text to clipboard with fallback
function copyToClipboard(text, buttonEl) {
  const fallback = () => {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(ta);
  };
  if (navigator.clipboard) {
    navigator.clipboard.writeText(text).catch(fallback);
  } else {
    fallback();
  }
  if (buttonEl) {
    const orig = buttonEl.textContent;
    buttonEl.textContent = 'Copied!';
    setTimeout(() => { buttonEl.textContent = orig; }, 1500);
  }
}

// Add copy button to all .output elements
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.output').forEach(el => {
    if (el.dataset.copyable === 'false') return;
    const btn = document.createElement('button');
    btn.className = 'btn btn-sm';
    btn.textContent = 'Copy';
    btn.style.marginTop = '8px';
    btn.addEventListener('click', () => copyToClipboard(el.textContent, btn));
    el.parentNode.insertBefore(btn, el.nextSibling);
  });
});

// GoatCounter event tracking (for A/B test measurement)
function trackEvent(name, payload) {
  if (window.goatcounter) {
    window.goatcounter.count({
      path: name,
      title: JSON.stringify(payload || {}),
      event: true,
    });
  }
}

// Track outbound clicks (affiliate + tip CTAs)
document.addEventListener('click', (e) => {
  const link = e.target.closest('a[href]');
  if (!link) return;
  const href = link.getAttribute('href') || '';
  if (href.startsWith('http') && !href.includes(window.location.hostname)) {
    const isAffiliate = link.getAttribute('rel')?.includes('sponsored') ||
                        link.closest('.affiliate-section');
    trackEvent('outbound_click', {
      url: href,
      type: isAffiliate ? 'affiliate' : 'external',
      page: window.location.pathname,
    });
  }
  if (href.includes('crypto-tips')) {
    trackEvent('tip_cta_click', { page: window.location.pathname });
  }
});
