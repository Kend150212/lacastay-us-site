/* LacaStay cookie consent — built-in, free forever, no third-party service.
   - Shows a banner until the visitor accepts or declines.
   - Choice is persisted in localStorage under 'lacastay_cookie_consent'.
   - If gtag is present (Consent Mode v2), analytics/ad storage stay 'denied'
     until the visitor accepts, and are updated on every choice.
   - Any link with [data-cookie-reset] (footer "Cookie settings") clears the
     choice and re-opens the banner.
   - Banner copy is translated by i18n.js via data-i18n: this script injects the
     banner synchronously during parsing, so the nodes exist before i18n.js
     applies translations on DOMContentLoaded.
*/
(function () {
  var KEY = 'lacastay_cookie_consent';

  function applyConsent(v) {
    if (typeof window.gtag === 'function') {
      var g = (v === 'granted') ? 'granted' : 'denied';
      window.gtag('consent', 'update', {
        ad_storage: g,
        analytics_storage: g,
        ad_user_data: g,
        ad_personalization: g
      });
    }
  }

  // Consent Mode v2 default: everything denied until the visitor decides.
  // (No-op today — the site ships no tracking scripts — but keeps us correct
  // the day GA4 or a pixel is added.)
  if (typeof window.gtag === 'function') {
    window.gtag('consent', 'default', {
      ad_storage: 'denied',
      analytics_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied'
    });
  }

  var stored = null;
  try { stored = localStorage.getItem(KEY); } catch (e) {}
  if (stored) { applyConsent(stored); }

  var el = document.createElement('div');
  el.className = 'cookie-banner';
  el.id = 'cookieBanner';
  el.setAttribute('role', 'dialog');
  el.setAttribute('aria-live', 'polite');
  el.setAttribute('aria-label', 'Cookie consent');
  el.hidden = !!stored;
  el.innerHTML =
    '<p data-i18n="cookie.text">We use cookies to remember your preferences and analyze site traffic. Accept or decline — the site works the same either way.</p>' +
    '<div class="cookie-actions">' +
    '<button type="button" class="btn btn-primary cookie-accept" data-i18n="cookie.accept">Accept</button>' +
    '<button type="button" class="btn btn-outline cookie-decline" data-i18n="cookie.decline">Decline</button>' +
    '</div>';
  document.body.appendChild(el);

  function choose(v) {
    try { localStorage.setItem(KEY, v); } catch (e) {}
    applyConsent(v);
    el.hidden = true;
  }

  el.querySelector('.cookie-accept').addEventListener('click', function () { choose('granted'); });
  el.querySelector('.cookie-decline').addEventListener('click', function () { choose('declined'); });

  document.querySelectorAll('[data-cookie-reset]').forEach(function (link) {
    link.addEventListener('click', function (ev) {
      ev.preventDefault();
      try { localStorage.removeItem(KEY); } catch (e) {}
      el.hidden = false;
    });
  });

  // Public API for future integrations (e.g. embedded demo widgets).
  window.lacastayConsent = {
    get: function () { try { return localStorage.getItem(KEY); } catch (e) { return null; } },
    reset: function () { try { localStorage.removeItem(KEY); } catch (e) {} el.hidden = false; }
  };
})();
