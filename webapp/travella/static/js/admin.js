// Add 'collapsed' class to sidebar on small screens
function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  if (window.innerWidth < 768) {
    sidebar.classList.add('collapsed');
  } else {
    sidebar.classList.remove('collapsed');
  }
}

window.addEventListener('load', toggleSidebar);
window.addEventListener('resize', toggleSidebar);

// Revenue Chart (Line)
  const ctx = document.getElementById('revenueChart');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      datasets: [{
        label: 'Revenue',
        data: [12000, 14000, 18000, 16000, 19000, 22000],
        borderColor: '#00A9FF',
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } }
    }
  });

  // Pie Chart (Top Destinations)
  const pie = document.getElementById('pieChart');
  new Chart(pie, {
    type: 'pie',
    data: {
      labels: ['Paris', 'Rome', 'Bali', 'Kyoto', 'Maldives'],
      datasets: [{
        label: 'Top Destinations',
        data: [25, 20, 18, 15, 22],
        backgroundColor: ['#0d6efd', '#00A9FF', '#89CFF3', '#CDF5FD', '#0dcaf0']
      }],
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {legend: {position: 'right'}}
      }

    }
  });