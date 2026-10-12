/* LacaStay demo page — renders sample schedules from assets/data/demo-bookings.json.
   Booking data is rendered as-is; only UI labels and status badges are localized
   (via the demo.* keys in en.c.json / vi.c.json). */
(function () {
  var DATA_URL = "assets/data/demo-bookings.json";
  var I18N_URL = function (lang) { return "assets/i18n/" + lang + ".c.json"; };
  var data = null;
  var strings = {};
  var lang = "en";
  var tab = "salon";

  function t(key) {
    var parts = key.split(".");
    var node = strings;
    for (var i = 0; i < parts.length; i++) {
      if (node == null) return key;
      node = node[parts[i]];
    }
    return typeof node === "string" ? node : key;
  }

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function statusLabel(status) {
    var map = {
      "completed": t("demo.st.completed"),
      "in-progress": t("demo.st.in-progress"),
      "confirmed": t("demo.st.confirmed"),
      "reminder-sent": t("demo.st.reminder-sent"),
      "checked-in": t("demo.st.checked-in"),
      "arriving-today": t("demo.st.arriving-today"),
      "inquiry": t("demo.st.inquiry")
    };
    return map[status] || status;
  }

  function sourceBadge(source) {
    var isAI = source === "AI call";
    var label = isAI ? t("demo.src.ai") : source;
    var cls = isAI ? "demo-badge demo-badge-ai" : "demo-badge";
    return '<span class="' + cls + '">' + esc(label) + "</span>";
  }

  function apptRow(b) {
    return "<tr>" +
      "<td><strong>" + esc(b.time) + "</strong></td>" +
      "<td>" + esc(b.client) + "</td>" +
      "<td>" + esc(b.service) + "</td>" +
      "<td>" + esc(b.tech) + "</td>" +
      "<td>$" + esc(b.price) + "</td>" +
      '<td><span class="demo-badge demo-status-' + esc(b.status) + '">' + esc(statusLabel(b.status)) + "</span></td>" +
      "<td>" + sourceBadge(b.source) + "</td>" +
      "</tr>";
  }

  function stayRow(b) {
    return "<tr>" +
      "<td>" + esc(b.dates) + "</td>" +
      "<td>" + esc(b.guest) + "</td>" +
      "<td>" + esc(b.guests) + "</td>" +
      "<td>" + esc(b.nights) + "</td>" +
      "<td>$" + esc(b.total) + "</td>" +
      '<td><span class="demo-badge demo-status-' + esc(b.status) + '">' + esc(statusLabel(b.status)) + "</span></td>" +
      "<td>" + sourceBadge(b.source) + "</td>" +
      "</tr>";
  }

  function render() {
    if (!data) return;
    var biz = data[tab];
    var panel = document.getElementById("demo-panel");
    var summary = document.getElementById("demo-summary");
    if (!panel || !summary) return;

    var head, rows;
    if (tab === "rental") {
      head = "<tr><th>" + t("demo.bk.dates") + "</th><th>" + t("demo.bk.guest") + "</th><th>" +
        t("demo.bk.guests") + "</th><th>" + t("demo.bk.nights") + "</th><th>" + t("demo.bk.total") +
        "</th><th>" + t("demo.bk.status") + "</th><th>" + t("demo.bk.source") + "</th></tr>";
      rows = biz.bookings.map(stayRow).join("");
    } else {
      head = "<tr><th>" + t("demo.bk.time") + "</th><th>" + t("demo.bk.client") + "</th><th>" +
        t("demo.bk.service") + "</th><th>" + t("demo.bk.tech") + "</th><th>" + t("demo.bk.price") +
        "</th><th>" + t("demo.bk.status") + "</th><th>" + t("demo.bk.source") + "</th></tr>";
      rows = biz.bookings.map(apptRow).join("");
    }
    panel.innerHTML =
      '<div class="demo-biz"><h3>' + esc(biz.business) + '</h3><p class="hero-note">' +
      esc(biz.location) + "</p></div>" +
      '<div style="overflow-x:auto"><table class="compare-table"><thead>' + head +
      "</thead><tbody>" + rows + "</tbody></table></div>";

    var stats = [
      { n: biz.bookings.length, l: t("demo.sum.bookings") }
    ];
    if (biz.after_hours_bookings != null) stats.push({ n: biz.after_hours_bookings, l: t("demo.sum.afterhours") });
    if (biz.missed_calls_recovered != null) stats.push({ n: biz.missed_calls_recovered, l: t("demo.sum.recovered") });
    if (biz.after_hours_inquiries != null) stats.push({ n: biz.after_hours_inquiries, l: t("demo.sum.afterhours") });
    if (biz.inquiries_answered != null) stats.push({ n: biz.inquiries_answered, l: t("demo.sum.inquiries") });
    summary.innerHTML = stats.map(function (s) {
      return '<div class="demo-stat"><div class="stat-num">' + s.n + '</div><div class="stat-label">' + esc(s.l) + "</div></div>";
    }).join("");

    document.querySelectorAll(".demo-tab").forEach(function (btn) {
      btn.classList.toggle("active", btn.getAttribute("data-tab") === tab);
    });
  }

  function loadStrings(nextLang, done) {
    lang = nextLang;
    fetch(I18N_URL(lang))
      .then(function (r) { return r.ok ? r.json() : {}; })
      .catch(function () { return {}; })
      .then(function (json) { strings = json || {}; render(); if (done) done(); });
  }

  window.lacastayAfterI18n = function (nextLang) {
    loadStrings(nextLang || "en");
  };

  document.addEventListener("DOMContentLoaded", function () {
    var saved = "en";
    try { saved = localStorage.getItem("lacastay-lang") === "vi" ? "vi" : "en"; } catch (e) {}
    document.querySelectorAll(".demo-tab").forEach(function (btn) {
      btn.addEventListener("click", function () {
        tab = btn.getAttribute("data-tab");
        render();
      });
    });
    fetch(DATA_URL)
      .then(function (r) { if (!r.ok) throw new Error("fetch failed"); return r.json(); })
      .then(function (json) {
        data = json;
        loadStrings(saved);
      })
      .catch(function () {
        var panel = document.getElementById("demo-panel");
        if (panel) panel.innerHTML = "<p>Could not load sample schedule.</p>";
      });

    var form = document.getElementById("demo-form");
    if (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var ok = document.getElementById("demo-form-success");
        if (ok) ok.style.display = "block";
        form.reset();
      });
    }
  });
})();
