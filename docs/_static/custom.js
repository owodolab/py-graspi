document.addEventListener("DOMContentLoaded", function() {
  var summaries = document.querySelectorAll('.details-summary');

  summaries.forEach(function(summary) {
    summary.onclick = function() {
      var details = summary.parentNode;
      details.classList.toggle('details-open');
    };
  });
});
