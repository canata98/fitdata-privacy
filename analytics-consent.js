(function () {
  const measurementId = "G-HRDGLSTKS1";
  const consentKey = "fitdata_analytics_consent";
  const existingConsent = localStorage.getItem(consentKey);
  const isGerman = document.documentElement.lang === "de";

  const copy = isGerman
    ? {
        text: "Wir verwenden Google Analytics, um die Website zu verbessern. Analytics wird nur nach deiner Zustimmung geladen.",
        accept: "Akzeptieren",
        decline: "Ablehnen",
        privacy: "Datenschutz",
        privacyHref: "privacy-de.html",
      }
    : {
        text: "We use Google Analytics to improve the website. Analytics loads only after your consent.",
        accept: "Accept",
        decline: "Decline",
        privacy: "Privacy",
        privacyHref: "privacy-en.html",
      };

  function loadAnalytics() {
    if (window.__fitdataAnalyticsLoaded) return;
    window.__fitdataAnalyticsLoaded = true;

    window.dataLayer = window.dataLayer || [];
    window.gtag = function gtag() {
      window.dataLayer.push(arguments);
    };

    const tag = document.createElement("script");
    tag.async = true;
    tag.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`;
    document.head.appendChild(tag);

    window.gtag("consent", "default", {
      analytics_storage: "granted",
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
    });
    window.gtag("js", new Date());
    window.gtag("config", measurementId, {
      anonymize_ip: true,
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
    });
  }

  function trackOutboundLinks() {
    document.addEventListener("click", function (event) {
      const link = event.target.closest("a");
      if (!link || !window.gtag) return;

      const href = link.getAttribute("href") || "";
      if (href.includes("apps.apple.com")) {
        window.gtag("event", "app_store_click", {
          link_url: link.href,
          page_location: window.location.href,
        });
      }
    });
  }

  function showBanner() {
    const style = document.createElement("style");
    style.textContent = `
      .analytics-consent {
        position: fixed;
        left: 20px;
        right: 20px;
        bottom: 20px;
        z-index: 1000;
        display: flex;
        gap: 16px;
        align-items: center;
        justify-content: space-between;
        max-width: 920px;
        margin: 0 auto;
        padding: 16px 18px;
        border: 1px solid rgba(17, 17, 17, 0.1);
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.96);
        color: #111111;
        box-shadow: rgba(0, 0, 0, 0.16) 0 18px 50px -24px;
        backdrop-filter: blur(18px);
        font-family: 'Atkinson Hyperlegible', system-ui, -apple-system, sans-serif;
      }
      .analytics-consent p {
        margin: 0;
        font-size: 14px;
        line-height: 1.45;
      }
      .analytics-consent a {
        color: #111111;
        font-weight: 700;
      }
      .analytics-consent-actions {
        display: flex;
        gap: 10px;
        flex-shrink: 0;
      }
      .analytics-consent button {
        border: 0;
        border-radius: 999px;
        padding: 9px 16px;
        font: 700 14px 'Gabarito', system-ui, sans-serif;
        cursor: pointer;
      }
      .analytics-consent-accept {
        background: #E8722A;
        color: #ffffff;
      }
      .analytics-consent-decline {
        background: #F7EFE5;
        color: #111111;
      }
      @media (max-width: 640px) {
        .analytics-consent {
          flex-direction: column;
          align-items: stretch;
          left: 12px;
          right: 12px;
          bottom: 12px;
        }
        .analytics-consent-actions {
          width: 100%;
        }
        .analytics-consent button {
          flex: 1;
        }
      }
    `;
    document.head.appendChild(style);

    const banner = document.createElement("div");
    banner.className = "analytics-consent";
    banner.setAttribute("role", "dialog");
    banner.setAttribute("aria-live", "polite");
    banner.innerHTML = `
      <p>${copy.text} <a href="${copy.privacyHref}">${copy.privacy}</a></p>
      <div class="analytics-consent-actions">
        <button class="analytics-consent-decline" type="button">${copy.decline}</button>
        <button class="analytics-consent-accept" type="button">${copy.accept}</button>
      </div>
    `;

    banner.querySelector(".analytics-consent-accept").addEventListener("click", function () {
      localStorage.setItem(consentKey, "granted");
      banner.remove();
      loadAnalytics();
    });

    banner.querySelector(".analytics-consent-decline").addEventListener("click", function () {
      localStorage.setItem(consentKey, "denied");
      banner.remove();
    });

    document.body.appendChild(banner);
  }

  if (existingConsent === "granted") {
    loadAnalytics();
  } else if (existingConsent !== "denied") {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", showBanner);
    } else {
      showBanner();
    }
  }

  trackOutboundLinks();
})();
