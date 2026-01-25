/**
 * Navigation functionality
 * Handles dropdown menus and mobile menu toggle
 */

(function() {
  'use strict';

  function init() {
    initDropdowns();
    initMobileMenu();
  }

  /**
   * Initialize dropdown menus
   */
  function initDropdowns() {
    const dropdowns = document.querySelectorAll('.dropdown');

    dropdowns.forEach(dropdown => {
      const toggle = dropdown.querySelector('.dropdown-toggle');
      const list = dropdown.querySelector('.dropdown-list');

      if (!toggle || !list) return;

      // Click to toggle dropdown
      toggle.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();

        const isOpen = dropdown.classList.contains('open');

        // Close all other dropdowns first
        closeAllDropdowns();

        if (!isOpen) {
          dropdown.classList.add('open');
          toggle.classList.add('open');
          list.classList.add('open');
          toggle.setAttribute('aria-expanded', 'true');
        }
      });

      // Hover behavior for desktop
      dropdown.addEventListener('mouseenter', function() {
        if (window.innerWidth > 991) {
          dropdown.classList.add('open');
          toggle.classList.add('open');
          list.classList.add('open');
          toggle.setAttribute('aria-expanded', 'true');
        }
      });

      dropdown.addEventListener('mouseleave', function() {
        if (window.innerWidth > 991) {
          dropdown.classList.remove('open');
          toggle.classList.remove('open');
          list.classList.remove('open');
          toggle.setAttribute('aria-expanded', 'false');
        }
      });
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
      if (!e.target.closest('.dropdown')) {
        closeAllDropdowns();
      }
    });

    // Close on escape key
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        closeAllDropdowns();
        closeMobileMenu();
      }
    });
  }

  /**
   * Close all dropdown menus
   */
  function closeAllDropdowns() {
    document.querySelectorAll('.dropdown').forEach(dropdown => {
      const toggle = dropdown.querySelector('.dropdown-toggle');
      const list = dropdown.querySelector('.dropdown-list');
      dropdown.classList.remove('open');
      if (toggle) {
        toggle.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
      if (list) list.classList.remove('open');
    });
  }

  /**
   * Initialize mobile menu toggle
   */
  function initMobileMenu() {
    const menuButton = document.querySelector('.nav-mobile-btn');
    const navMenu = document.querySelector('.nav-menu');
    const navContainer = document.querySelector('.nav-container');

    if (!menuButton || !navMenu) return;

    menuButton.addEventListener('click', function() {
      const isOpen = navContainer && navContainer.classList.contains('open');

      if (isOpen) {
        closeMobileMenu();
      } else {
        if (navContainer) navContainer.classList.add('open');
        menuButton.classList.add('open');
        navMenu.classList.add('open');
        menuButton.setAttribute('aria-expanded', 'true');
        document.body.style.overflow = 'hidden';
      }
    });

    // Close mobile menu on window resize to desktop
    window.addEventListener('resize', function() {
      if (window.innerWidth > 991) {
        closeMobileMenu();
      }
    });
  }

  /**
   * Close mobile menu
   */
  function closeMobileMenu() {
    const menuButton = document.querySelector('.nav-mobile-btn');
    const navMenu = document.querySelector('.nav-menu');
    const navContainer = document.querySelector('.nav-container');

    if (navContainer) navContainer.classList.remove('open');
    if (menuButton) {
      menuButton.classList.remove('open');
      menuButton.setAttribute('aria-expanded', 'false');
    }
    if (navMenu) navMenu.classList.remove('open');
    document.body.style.overflow = '';
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
