var chartData = JSON.parse(document.getElementById('chartData').textContent);

async function addChart(elementID, individualChartData){
    const myChart = new Chart(individualChartData.element_id, {
      type: 'line',
      data: {
          labels: individualChartData.time ,
          datasets: [{
              label: individualChartData.chart_title,
              data: individualChartData.data,
              borderWidth: 1,
              backgroundColor: individualChartData.colour,
              tension: 0.1,
          },]
      },
      options: {
          normalized: true,
          responsive: true,
          tooltips: {
              callbacks: {
                label: (item) => `${item.yLabel} individualChartData.unit`,
              },
          },
          scales: {
              y: {
                  beginAtZero: true
              },
              x: {
                type: 'time',
                time: {
                    parser: 'YYYY-MM-DDTHH:mm:ss'
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