
    document.addEventListener('DOMContentLoaded', function() {
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

        // --- Revenue Chart (Line) ---
        const ctx = document.getElementById('revenueChart');
        
        // Get the data from the json_script tag
        const revenueData = JSON.parse(document.getElementById('revenue-chart-data').textContent);

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: revenueData.labels, // Use the real labels
                datasets: [{
                    label: 'Revenue',
                    data: revenueData.revenues, // Use the real revenue data
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
                    legend: {
                        display: false
                    },
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

        // --- Bar Chart ---
        const barCtx = document.getElementById('barChart').getContext('2d');
        
        // Get data from the json_script tag
        const monthlyBookingsData = JSON.parse(document.getElementById('monthly-bookings-data').textContent);

        const monthlyLabels = monthlyBookingsData.monthly_bookings_labels;
        const monthlyCounts = monthlyBookingsData.monthly_bookings_counts;

        const backgroundColors = [
            'rgba(67, 97, 238, 0.8)',
            'rgba(42, 157, 143, 0.8)',
            'rgba(233, 196, 106, 0.8)',
            'rgba(231, 111, 81, 0.8)',
            'rgba(156, 82, 230, 0.8)',
            'rgba(255, 159, 64, 0.8)'
        ];

        new Chart(barCtx, {
            type: 'bar',
            data: {
                labels: monthlyLabels,
                datasets: [{
                    label: 'Number of Bookings',
                    data: monthlyCounts,
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
                indexAxis: 'y',
                scales: {
                    x: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Number of Bookings'
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
