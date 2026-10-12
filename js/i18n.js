/* LacaStay i18n — EN default, VI secondary. Persists choice in localStorage.
   Usage in HTML: <tag data-i18n="namespace.section.key">fallback</tag>
   For HTML content: data-i18n-html="key". For attributes: data-i18n-attr="attr:key;attr:key". */
(function () {
  var LANG_KEY = "lacastay-lang";
  var FRAGMENTS = ["a", "b", "c"]; // en.a.json / vi.a.json etc. under assets/i18n/
  var dict = {};
  var currentLang = "en";

  function deepMerge(target, source) {
    for (var k in source) {
      if (source[k] && typeof source[k] === "object" && !Array.isArray(source[k])) {
        target[k] = target[k] && typeof target[k] === "object" ? target[k] : {};
        deepMerge(target[k], source[k]);
      } else {
        target[k] = source[k];
      }
    }
    return target;
  }

  function t(key) {
    var parts = key.split(".");
    var node = dict;
    for (var i = 0; i < parts.length; i++) {
      if (node == null) return null;
      node = node[parts[i]];
    }
    return typeof node === "string" ? node : null;
  }

  function applyI18n() {
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var v = t(el.getAttribute("data-i18n"));
      if (v != null) el.textContent = v;
    });
    document.querySelectorAll("[data-i18n-html]").forEach(function (el) {
      var v = t(el.getAttribute("data-i18n-html"));
      if (v != null) el.innerHTML = v;
    });
    document.querySelectorAll("[data-i18n-attr]").forEach(function (el) {
      el.getAttribute("data-i18n-attr").split(";").forEach(function (pair) {
        var idx = pair.indexOf(":");
        if (idx < 0) return;
        var attr = pair.slice(0, idx).trim();
        var key = pair.slice(idx + 1).trim();
        var v = t(key);
        if (v != null) el.setAttribute(attr, v);
      });
    });
    document.documentElement.setAttribute("lang", currentLang);
    document.querySelectorAll(".lang-switch button").forEach(function (btn) {
      btn.classList.toggle("active", btn.getAttribute("data-lang") === currentLang);
    });
  }

  function loadLang(lang) {
    currentLang = lang;
    var fetches = FRAGMENTS.map(function (f) {
      return fetch("assets/i18n/" + lang + "." + f + ".json")
        .then(function (r) { return r.ok ? r.json() : {}; })
        .catch(function () { return {}; });
    });
    // Also resolve relative path when page is in a subfolder — all pages are at root, so this is fine.
    Promise.all(fetches).then(function (parts) {
      dict = {};
      parts.forEach(function (p) { deepMerge(dict, p); });
      try { localStorage.setItem(LANG_KEY, lang); } catch (e) {}
      applyI18n();
      if (typeof window.lacastayAfterI18n === "function") window.lacastayAfterI18n(lang);
    });
  }

  function initLang() {
    var saved = null;
    try { saved = localStorage.getItem(LANG_KEY); } catch (e) {}
    loadLang(saved === "vi" ? "vi" : "en");
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".lang-switch button").forEach(function (btn) {
      btn.addEventListener("click", function () { loadLang(btn.getAttribute("data-lang")); });
    });
    var toggle = document.querySelector(".nav-toggle");
    if (toggle) {
      toggle.addEventListener("click", function () {
        document.querySelector(".main-nav").classList.toggle("open");
      });
    }
    document.querySelectorAll(".faq-q").forEach(function (q) {
      q.addEventListener("click", function () {
        q.closest(".faq-item").classList.toggle("open");
      });
    });
    initLang();
  });

  window.lacastaySetLang = loadLang;
})();
