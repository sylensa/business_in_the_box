/* global bootstrap: false */
(() => {
  'use strict';


  // Toggle sidebar
  const toggleBtn = document.getElementById('toggleBtn');
  const sidebar = document.getElementById('sidebar');

  toggleBtn.addEventListener('click', function() {
    sidebar.classList.toggle('show');
  });
})();
