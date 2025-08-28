(function(){
  function getCtx(id){ const el = document.getElementById(id); return el && el.getContext ? el.getContext('2d') : null; }

  function renderDoughnut(){
    const ctx = getCtx('doughnutChart');
    if(!ctx) return;
    const pct = Number(RESULTS.plagiarism_percent) || 0;
    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Plagiarism', 'Remaining'],
        datasets: [{
          data: [pct, Math.max(0, 100 - pct)],
          hoverOffset: 6,
          borderWidth: 0
        }]
      },
      options: {
        cutout: '72%',
        plugins: { legend: { position: 'bottom' } }
      }
    });
  }

  function renderMetricsBar(){
    const ctx = getCtx('metricsBarChart');
    if(!ctx) return;
    const labels = ['LCS %', 'Overlap %', 'Edit sim %', 'Substring cov %'];
    const data = [
      Number(RESULTS.lcs_percent) || 0,
      Number(RESULTS.overlap_percent) || 0,
      Number(RESULTS.edit_similarity_percent) || 0,
      Number(RESULTS.substring_coverage) || 0
    ];
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label: 'Metric value (%)',
          data,
          borderRadius: 6,
          barPercentage: 0.6
        }]
      },
      options: {
        scales: {
          y: { beginAtZero: true, max: 100 }
        },
        plugins: { legend: { display: false } }
      }
    });
  }

  function renderMatchesBar(){
    const ctx = getCtx('matchesBarChart');
    if(!ctx) return;
    const blocks = Array.isArray(RESULTS.matched_blocks) ? RESULTS.matched_blocks : [];
    const labels = blocks.map((b,i)=>`Block ${i+1}`);
    const data = blocks.map(b => Math.min(1000, b.length));
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label: 'Matched block length (chars)',
          data,
          borderRadius: 6
        }]
      },
      options: {
        indexAxis: 'y',
        scales: { x: { beginAtZero: true } },
        plugins: { legend: { display: false } }
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function(){
    try{
      renderDoughnut();
      renderMetricsBar();
      renderMatchesBar();
    }catch(err){
      console.error('chart render error', err);
    }
  });

})();
