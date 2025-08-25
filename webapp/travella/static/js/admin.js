
    // Toggle sidebar on mobile
    document.querySelector('.toggle-sidebar').addEventListener('click', function() {
        document.getElementById('sidebar').classList.toggle('mobile-expanded');
        document.querySelector('.overlay').classList.toggle('active');
    });
    
    // Close sidebar when clicking on overlay
    document.querySelector('.overlay').addEventListener('click', function() {
        document.getElementById('sidebar').classList.remove('mobile-expanded');
        this.classList.remove('active');
    });
    
    // Auto-collapse sidebar on small screens
    function toggleSidebar() {
        const sidebar = document.getElementById('sidebar');
        const mainContent = document.querySelector('.main-content');
        
        if (window.innerWidth < 992) {
            sidebar.classList.add('collapsed');
            mainContent.classList.add('expanded');
        } else {
            sidebar.classList.remove('collapsed');
            mainContent.classList.remove('expanded');
        }
    }

    window.addEventListener('load', toggleSidebar);
    window.addEventListener('resize', toggleSidebar);
    
    // Sign out function
    const signout = () => document.getElementById('signOutForm').submit();

  // Revenue Chart (Line)
  const ctx = document.getElementById('revenueChart');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      datasets: [{
        label: 'Revenue',
        data: [12000, 14000, 18000, 16000, 19000, 22000, 24000, 21000, 23000, 25000, 28000, 30000],
        borderColor: '#4361ee',
        backgroundColor: 'rgba(67, 97, 238, 0.1)',
        fill: true,
        tension: 0.3,
        pointBackgroundColor: '#4361ee',
        pointRadius: 4,
        pointHoverRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { 
        legend: { display: false },
        tooltip: {
          mode: 'index',
          intersect: false
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            drawBorder: false
          }
        },
        x: {
          grid: {
            display: false
          }
        }
      }
    }
  });

  document.addEventListener('DOMContentLoaded', function() {
  const barCtx = document.getElementById('barChart').getContext('2d');

  // Example: Months vs Revenue
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
  const revenue = [12000, 14000, 18000, 16000, 19000, 22000]; // Replace with your real data

  const backgroundColors = [
    'rgba(67, 97, 238, 0.8)',
    'rgba(42, 157, 143, 0.8)',
    'rgba(233, 196, 106, 0.8)',
    'rgba(231, 111, 81, 0.8)',
    'rgba(156, 82, 230, 0.8)',
    'rgba(255, 159, 64, 0.8)' // Add as many colors as months
  ];

  const barChart = new Chart(barCtx, {
    type: 'bar',
    data: {
      labels: months,
      datasets: [{
        label: 'Revenue',
        data: revenue,
        backgroundColor: backgroundColors,
        borderColor: backgroundColors.map(color => color.replace('0.8', '1')),
        borderWidth: 1,
        borderRadius: 6,
        hoverBackgroundColor: backgroundColors.map(color => color.replace('0.8', '0.9'))
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y', // Horizontal bars; remove this if you want vertical bars
      scales: {
        x: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Revenue ($)'
          },
          grid: {
            drawBorder: false
          }
        },
        y: {
          grid: {
            display: false
          }
        }
      },
      plugins: {
        legend: {
          display: false
        }
      }
    }
  });
});
