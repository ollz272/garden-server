var chartData = JSON.parse(document.getElementById('chartData').textContent);

function addChart(elementID, individualChartData){
    const myChart = new Chart(individualChartData.element_id, {
      type: 'line',
      data: {
          labels: individualChartData.time ,
          datasets: [{
              label: individualChartData.chart_title,
              data: individualChartData.data,
              borderWidth: 1,
              backgroundColor: 'rgba(82, 99, 255, 0.5)',
              tension: 0.1,
          },]
      },
      options: {
          normalized: true,
          responsive: true,
          scales: {
              y: {
                  beginAtZero: true
              },
              x: {
                type: 'time',
                time: {
                    unit: 'seconds'
                },
              },
          },
          maintainAspectRatio: false
      }
    });
};

for (const [elementID, individualChartData] of Object.entries(chartData)) {
  addChart(elementID, individualChartData);
}