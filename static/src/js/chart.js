const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Moisture Level',
            data: [],
            borderWidth: 1,
            backgroundColor: 'rgba(82, 99, 255, 0.5)'
        },
        {
            label: 'Temperature',
            data: [],
            borderWidth: 1,
            backgroundColor: 'rgba(255, 111, 0, 0.7)'
        },
        {
            label: 'Light Level',
            data: [],
            borderWidth: 1,
            backgroundColor: 'rgba(255, 208, 0, 0.7)'
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        },
        maintainAspectRatio: true
    }
});