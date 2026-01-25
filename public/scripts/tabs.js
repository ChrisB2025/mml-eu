/**
 * Tab functionality
 * Handles tab switching for content panels
 */

(function() {
  'use strict';

  function init() {
    initTabs();
  }

  /**
   * Initialize all tab components
   */
  function initTabs() {
    const tabMenus = document.querySelectorAll('.tab-menu');

    tabMenus.forEach(tabMenu => {
      const tabContainer = tabMenu.closest('.tabs');
      if (!tabContainer) return;

      const tabLinks = tabMenu.querySelectorAll('.tab-link');
      const tabContent = tabContainer.querySelector('.tab-content');

      if (!tabContent) return;

      const tabPanes = tabContent.querySelectorAll('.tab-pane');

      tabLinks.forEach((link, index) => {
        link.addEventListener('click', function(e) {
          e.preventDefault();

          // Get tab identifier
          const tabId = link.getAttribute('data-w-tab') || link.getAttribute('data-tab') || `Tab ${index + 1}`;

          // Deactivate all tabs
          tabLinks.forEach(l => {
            l.classList.remove('current');
            l.setAttribute('aria-selected', 'false');
          });

          // Activate clicked tab
          link.classList.add('current');
          link.setAttribute('aria-selected', 'true');

          // Hide all panes
          tabPanes.forEach(pane => {
            pane.classList.remove('tab-active');
            pane.style.display = 'none';
          });

          // Show corresponding pane
          const targetPane = Array.from(tabPanes).find(pane => {
            const paneId = pane.getAttribute('data-w-tab') || pane.getAttribute('data-tab');
            return paneId === tabId;
          }) || tabPanes[index];

          if (targetPane) {
            targetPane.classList.add('tab-active');
            targetPane.style.display = '';
          }
        });
      });

      // Initialize first tab as active if none are active
      const hasActiveTab = Array.from(tabLinks).some(l =>
        l.classList.contains('current')
      );

      if (!hasActiveTab && tabLinks.length > 0) {
        tabLinks[0].click();
      }
    });
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
