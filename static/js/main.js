/* Dreams Tours and Travels — main.js (Vanilla JS, no jQuery) */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    safeRun("initPreloader", initPreloader);
    safeRun("initNavbarScroll", initNavbarScroll);
    safeRun("initHeroEntrance", initHeroEntrance);
    safeRun("initAOS", initAOS);
    safeRun("initFleetTierSwitch", initFleetTierSwitch);
    safeRun("initCounters", initCounters);
    safeRun("initSmoothAnchors", initSmoothAnchors);
  });

  // Runs each init function in isolation — if one throws, it's logged to the
  // console but every other init still runs (nothing else gets blocked).
  function safeRun(name, fn) {
    try {
      fn();
    } catch (err) {
      console.error("[main.js] " + name + " failed:", err);
    }
  }

  function initPreloader() {
    var preloader = document.getElementById("dtPreloader");
    if (!preloader) return; // only exists on the Home page

    document.body.style.overflow = "hidden";

    var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var minDuration = reducedMotion ? 300 : 2000;

    setTimeout(function () {
      preloader.classList.add("dt-hide");
      document.body.style.overflow = "";
      setTimeout(function () {
        if (preloader.parentNode) preloader.parentNode.removeChild(preloader);
      }, 700);
    }, minDuration);
  }

  function initNavbarScroll() {
    var navbar = document.getElementById("dtNavbar");
    if (!navbar) return;
    var hasHero = !!document.querySelector(".dt-hero");
    function onScroll() {
      if (!hasHero || window.scrollY > 60) {
        navbar.classList.add("scrolled");
      } else {
        navbar.classList.remove("scrolled");
      }
    }
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  function initHeroEntrance() {
    if (!document.body.classList.contains("home-hero-entrance")) return;
    var navbar = document.getElementById("dtNavbar");
    var heroContent = document.querySelector(".dt-hero-content");
    var scrollIndicator = document.querySelector(".dt-scroll-indicator");
    var revealed = false;
    function reveal() {
      if (revealed) return;
      revealed = true;
      if (navbar) navbar.classList.add("dt-revealed");
      if (heroContent) heroContent.classList.add("dt-revealed");
      if (scrollIndicator) scrollIndicator.classList.add("dt-revealed");
      window.removeEventListener("scroll", onFirstScroll);
      window.removeEventListener("wheel", onFirstScroll);
      window.removeEventListener("touchmove", onFirstScroll);
    }
    function onFirstScroll() {
      if (window.scrollY > 4) reveal();
    }
    window.addEventListener("scroll", onFirstScroll, { passive: true });
    window.addEventListener("wheel", onFirstScroll, { passive: true });
    window.addEventListener("touchmove", onFirstScroll, { passive: true });
    setTimeout(reveal, 15000);
  }

  function initAOS() {
    if (typeof AOS !== "undefined") {
      AOS.init({ duration: 700, once: true, offset: 80, easing: "ease-out-cubic" });
    }
  }

  function initFleetTierSwitch() {
    var pillButtons = document.querySelectorAll("[data-fleet-tier]");
    if (!pillButtons.length) return;
    pillButtons.forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        var tier = btn.getAttribute("data-fleet-tier");
        var url = new URL(window.location.href);
        url.searchParams.set("tier", tier);
        window.location.href = url.toString();
      });
    });
  }

  function initCounters() {
    var counters = document.querySelectorAll("[data-counter-target]");
    if (!counters.length) return;
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.4 });
    counters.forEach(function (el) { observer.observe(el); });
  }

  function animateCounter(el) {
    var target = parseInt(el.getAttribute("data-counter-target"), 10) || 0;
    var duration = 1400;
    var startTime = null;
    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      el.textContent = Math.floor(progress * target) + (el.getAttribute("data-counter-suffix") || "");
      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        el.textContent = target + (el.getAttribute("data-counter-suffix") || "");
      }
    }
    requestAnimationFrame(step);
  }

  function initSmoothAnchors() {
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
      anchor.addEventListener("click", function (e) {
        var targetId = this.getAttribute("href");
        if (targetId.length < 2) return;
        var targetEl = document.querySelector(targetId);
        if (targetEl) {
          e.preventDefault();
          targetEl.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      });
    });
  }
})();