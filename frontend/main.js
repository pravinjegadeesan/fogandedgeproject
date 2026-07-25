const API_URL = "https://o3g9wp3ss2.execute-api.us-east-1.amazonaws.com/prod/energy";

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false
};

const tempChart = new Chart(document.getElementById('tempChart'), {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Temp (°C)', data: [], borderColor: 'red', fill: false }] },
    options: chartOptions
});

const powerChart = new Chart(document.getElementById('powerChart'), {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Power (W)', data: [], borderColor: 'orange', fill: false }] },
    options: chartOptions
});

const voltageChart = new Chart(document.getElementById('voltageChart'), {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Voltage (V)', data: [], borderColor: 'blue', fill: false }] },
    options: chartOptions
});

function updateDashboard() {
    axios.get(API_URL)
        .then(response => {
            const readings = response.data;
            if (readings.length === 0) return;

            const latest = readings[readings.length - 1];
            document.getElementById('temp').innerText = latest.temperature;
            document.getElementById('humidity').innerText = latest.humidity;
            document.getElementById('voltage').innerText = latest.voltage;
            document.getElementById('current').innerText = latest.current;
            document.getElementById('power').innerText = latest.power;
            document.getElementById('status').innerText = latest.status;

            const timeLabels = readings.map(r => new Date(r.timestamp).toLocaleTimeString());
            
            tempChart.data.labels = timeLabels;
            tempChart.data.datasets[0].data = readings.map(r => r.temperature);
            tempChart.update();

            powerChart.data.labels = timeLabels;
            powerChart.data.datasets[0].data = readings.map(r => r.power);
            powerChart.update();

            voltageChart.data.labels = timeLabels;
            voltageChart.data.datasets[0].data = readings.map(r => r.voltage);
            voltageChart.update();

            const tableBody = document.getElementById('table-body');
            tableBody.innerHTML = '';
            
            readings.slice().reverse().forEach(r => {
                tableBody.innerHTML += `<tr>
                    <td>${new Date(r.timestamp).toLocaleString()}</td>
                    <td>${r.temperature}</td>
                    <td>${r.humidity}</td>
                    <td>${r.voltage}</td>
                    <td>${r.current}</td>
                    <td>${r.power}</td>
                    <td>${r.status}</td>
                </tr>`;
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

updateDashboard();
setInterval(updateDashboard, 5000);
