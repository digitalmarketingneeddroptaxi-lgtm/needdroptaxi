/**
 * InstantAlt Autonomous Remediation Agent v2.0
 * Automatically discovers missing alt attributes and remediates them in real time.
 */
(function () {
  'use strict';

  // 1. Locate the agent script element & get the agent ID
  var currentScript = document.currentScript || (function () {
    var scripts = document.getElementsByTagName('script');
    for (var i = 0; i < scripts.length; i++) {
      if (scripts[i].getAttribute('data-agent-id')) return scripts[i];
    }
    return null;
  })();

  var agentId = (currentScript && currentScript.getAttribute('data-agent-id')) || window.__INSTANTALT_AGENT_ID__ || 'agent-ia-8f3c2e1a';
  window.__INSTANTALT_AGENT_ID__ = agentId;
  document.documentElement.setAttribute('data-instantalt-agent', agentId);

  // 2. Default remediation mappings for known images
  var KNOWN_REMEDIATIONS = {
    'taxi-p1-768-512-90': 'Need Drop Taxi - Reliable outstation cab and one-way taxi service vehicle in Chennai',
    'new-ndt-logo': 'Need Drop Taxi Official Logo',
    'trip_fare_estimator_mockup': 'Trip Fare Estimator Mobile App Interface',
    'outstationtrip2': 'Outstation Taxi Service Chennai',
    'localrental1': 'Local Taxi Rental Service Chennai',
    'airportpickup': 'Airport Transfer Taxi Service Chennai'
  };

  function deriveAltText(img) {
    var src = img.src || img.getAttribute('src') || '';
    if (!src) return 'Website image';

    // Check known mappings
    for (var key in KNOWN_REMEDIATIONS) {
      if (src.indexOf(key) !== -1) {
        return KNOWN_REMEDIATIONS[key];
      }
    }

    // Contextual fallback from filename & domain
    var filename = src.split('/').pop().split('?')[0].replace(/\.[^/.]+$/, '');
    var readable = filename.replace(/[-_.]/g, ' ').trim();
    if (readable && readable.length > 2) {
      return 'Need Drop Taxi - ' + readable.charAt(0).toUpperCase() + readable.slice(1);
    }
    return 'Need Drop Taxi - Taxi and transportation service in Chennai';
  }

  function remediateImages() {
    var images = document.querySelectorAll('img');
    var fixedCount = 0;

    images.forEach(function (img) {
      var alt = img.getAttribute('alt');
      var isMissing = alt === null || alt.trim() === '';

      if (isMissing) {
        var newAlt = deriveAltText(img);
        img.setAttribute('alt', newAlt);
        img.setAttribute('data-instantalt-remediated', 'true');
        fixedCount++;
      }
    });

    if (fixedCount > 0) {
      console.log('InstantAlt Agent [' + agentId + ']: Remediated ' + fixedCount + ' image(s) with accessible alt text.');
    }
  }

  // Run on DOM ready and observe dynamic DOM changes
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', remediateImages);
  } else {
    remediateImages();
  }

  // MutationObserver for dynamic SPAs / Astro islands
  if (window.MutationObserver) {
    var observer = new MutationObserver(function (mutations) {
      var shouldCheck = false;
      for (var i = 0; i < mutations.length; i++) {
        if (mutations[i].addedNodes && mutations[i].addedNodes.length > 0) {
          shouldCheck = true;
          break;
        }
      }
      if (shouldCheck) {
        remediateImages();
      }
    });

    observer.observe(document.body || document.documentElement, {
      childList: true,
      subtree: true
    });
  }

  console.log('InstantAlt: Autonomous Remediation Agent active and monitoring (ID: ' + agentId + ').');
})();
