// static/js/script.js
// small UX helpers: warn on large files and show filename preview

document.addEventListener('DOMContentLoaded', function() {
  const fileInputs = document.querySelectorAll('input[type="file"]');
  fileInputs.forEach(fi => {
    fi.addEventListener('change', (e) => {
      const f = e.target.files[0];
      if (!f) return;
      // simple size check (10 MB)
      const maxMB = 10;
      if (f.size > maxMB * 1024 * 1024) {
        alert('File too large! please use files under ' + maxMB + ' MB.');
        e.target.value = '';
      }
    });
  });
});
