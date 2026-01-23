/**
 * MML Europe - Form Handler
 * Handles async form submissions to Tally with success/error feedback
 *
 * Tally.so is EU-hosted and GDPR-compliant by default
 */

(function() {
  'use strict';

  /**
   * Initialize form handling on page load
   */
  function init() {
    document.querySelectorAll('form').forEach(function(form) {
      // Handle forms with Tally action URLs
      if (form.action && form.action.includes('tally.so')) {
        setupFormHandler(form);
      }
    });
  }

  /**
   * Setup async submission handler for a form
   * @param {HTMLFormElement} form
   */
  function setupFormHandler(form) {
    form.addEventListener('submit', async function(e) {
      e.preventDefault();

      const submitBtn = form.querySelector('input[type="submit"], button[type="submit"]');
      const formWrapper = form.closest('.w-form');
      const successMsg = formWrapper ? formWrapper.querySelector('.w-form-done') : null;
      const errorMsg = formWrapper ? formWrapper.querySelector('.w-form-fail') : null;

      // Disable button and show loading state
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.dataset.originalValue = submitBtn.value;
        submitBtn.value = 'Sending...';
      }

      // Hide previous messages
      if (successMsg) successMsg.style.display = 'none';
      if (errorMsg) errorMsg.style.display = 'none';

      try {
        const formData = new FormData(form);

        // Tally accepts standard form submissions
        // We submit via fetch and handle the response
        const response = await fetch(form.action, {
          method: 'POST',
          body: formData
        });

        // Tally returns a redirect on success, which fetch follows
        // A successful submission will have response.ok = true
        if (response.ok || response.redirected) {
          // Show success message
          if (successMsg) {
            successMsg.style.display = 'block';
          }
          form.reset();
        } else {
          throw new Error('Form submission failed');
        }
      } catch (error) {
        console.error('Form submission error:', error);
        // Show error message
        if (errorMsg) {
          errorMsg.style.display = 'block';
        }
      } finally {
        // Re-enable button
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.value = submitBtn.dataset.originalValue || 'Submit';
        }
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
