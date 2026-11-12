(function (window, document) {
  "use strict";

  var root = document.documentElement;
  var heroTextSelector = [
    ".blockWrap_ded721d803b44f1180a742509044a2e9 .itemPreview",
    ".blockWrap_d150b314595543938a60de851c5dcddf .itemPreview",
    ".blockWrap_a9a2de40559b45509502261114232594 .itemPreview",
    ".blockWrap_e14491e8e6384619ae0a873eb8eea901 .itemPreview",
    ".blockWrap_ae3c46523fa246afb26df1be038b1433 .itemPreview",
    ".blockWrap_b8166f0d6b2f49baaed81e89bc85e243 .itemPreview",
    ".blockWrap_fa3901180ed64e08bdfa17ef69e55e8d .itemPreview",
    ".blockWrap_e2d1827cfdc54ab882291d79bdeacc1f .itemPreview",
    ".blockWrap_b2eba23e70a8407a81f49aa13ed98a03 .itemPreview",
    ".blockWrap_df1d8b2f30d042e0bad4353f0e717d4c .itemPreview",
    ".blockWrap_dcf088aad5ce4746a3bf80f8232390f6 .itemPreview",
    ".blockWrap_fe6e7977b9aa4296adbb0b07bb917213 .itemPreview",
    ".outdoor-intro__panel"
  ].join(", ");

  function addClass(element, className) {
    if (element.classList) {
      element.classList.add(className);
    } else if ((" " + element.className + " ").indexOf(" " + className + " ") < 0) {
      element.className += " " + className;
    }
  }

  function removeClass(element, className) {
    if (element.classList) {
      element.classList.remove(className);
    } else {
      element.className = (" " + element.className + " ")
        .replace(" " + className + " ", " ")
        .replace(/^\s+|\s+$/g, "");
    }
  }

  addClass(root, "hero-reveal-enabled");

  function getScrollPosition() {
    return window.pageYOffset ||
      document.documentElement.scrollTop ||
      document.body.scrollTop ||
      0;
  }

  function revealHeroText() {
    addClass(root, "hero-reveal-visible");
    window.removeEventListener("scroll", checkScroll, false);
  }

  function checkScroll() {
    if (getScrollPosition() > 4) {
      revealHeroText();
    }
  }

  function setupHeroReveal() {
    var panels = document.querySelectorAll(heroTextSelector);
    var i;

    if (!panels.length) {
      removeClass(root, "hero-reveal-enabled");
      return;
    }

    window.addEventListener("scroll", checkScroll, false);
    for (i = 0; i < panels.length; i += 1) {
      panels[i].addEventListener("focus", revealHeroText, true);
    }
    checkScroll();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setupHeroReveal, false);
  } else {
    setupHeroReveal();
  }
})(window, document);
