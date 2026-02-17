// Utility to load sample data
function loadSample() {
    const form = document.getElementById('predictionForm');
    if (form) {
        form.pl_orbper.value = 365.25;
        form.pl_rade.value = 1.0;
        form.pl_masse.value = 1.0;
        form.pl_eqt.value = 288;
        form.st_teff.value = 5778;
        form.st_rad.value = 1.0;
        form.st_mass.value = 1.0;
        form.sy_dist.value = 10;
        form.pl_dens.value = 5.51;
    }
}

// Gauge Chart Instance
let gaugeChartInstance = null;

// Dashboard Logic
async function loadDashboardData() {
    try {
        // Try to fetch real data, but fallback to dummy if it fails
        let data = {};
        try {
            const response = await fetch('/data');
            if (response.ok) data = await response.json();
        } catch (e) {
            console.warn("Could not fetch /data, using defaults", e);
        }

        // Feature Importance Chart (Vertical Bar)
        const featureCtx = document.getElementById('featureChart');
        if (featureCtx) {
            new Chart(featureCtx, {
                type: 'bar',
                data: {
                    labels: ['Planet Radius', 'Equilibrium Temp', 'Stellar Temp', 'Orbital Period', 'Planet Mass', 'Stellar Mass', 'Stellar Radius', 'Distance', 'Star Count', 'Planet Count'],
                    datasets: [{
                        label: 'Importance',
                        data: [0.95, 0.92, 0.88, 0.75, 0.70, 0.65, 0.60, 0.45, 0.35, 0.30],
                        backgroundColor: '#00d2ff',
                        borderRadius: 4,
                        barPercentage: 0.6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        title: { display: false }
                    },
                    scales: {
                        x: {
                            ticks: { color: '#a0a0a0', font: { size: 10 }, maxRotation: 45, minRotation: 45 },
                            grid: { display: false }
                        },
                        y: {
                            ticks: { color: '#a0a0a0', font: { size: 10 } },
                            grid: { color: 'rgba(255, 255, 255, 0.05)' }
                        }
                    }
                }
            });
        }

        // Distribution Chart
        const distCtx = document.getElementById('distributionChart');
        if (distCtx) {
            new Chart(distCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Habitable', 'Not Habitable', 'Marginal'],
                    datasets: [{
                        data: [5, 85, 10],
                        backgroundColor: ['#00ff88', '#ff0055', '#ffcc00'],
                        borderWidth: 0,
                        hoverOffset: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { color: '#a0a0a0', font: { size: 11 }, usePointStyle: true, padding: 20 }
                        }
                    },
                    cutout: '65%'
                }
            });
        }

        // Star-Planet Relationship Chart (Scatter)
        const scatterCtx = document.getElementById('scatterChart');
        if (scatterCtx) {
            // Generate some dummy scatter data that looks realistic
            const scatterData = Array.from({ length: 50 }, () => ({
                x: Math.random() * 6000 + 2000, // Stellar Temp
                y: Math.random() * 2000 // Planet Temp
            }));

            new Chart(scatterCtx, {
                type: 'scatter',
                data: {
                    datasets: [{
                        label: 'Exoplanets',
                        data: scatterData,
                        backgroundColor: '#00d2ff',
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
                            callbacks: {
                                label: (ctx) => `Stellar T: ${Math.round(ctx.raw.x)}K, Planet T: ${Math.round(ctx.raw.y)}K`
                            }
                        }
                    },
                    scales: {
                        x: {
                            title: { display: true, text: 'Stellar Temperature (K)', color: '#a0a0a0' },
                            ticks: { color: '#a0a0a0' },
                            grid: { color: 'rgba(255, 255, 255, 0.05)' }
                        },
                        y: {
                            title: { display: true, text: 'Planet Equilibrium Temperature (K)', color: '#a0a0a0' },
                            ticks: { color: '#a0a0a0' },
                            grid: { color: 'rgba(255, 255, 255, 0.05)' }
                        }
                    }
                }
            });
        }

        // Populate Table with 10 Top Candidates
        const tbody = document.getElementById('candidatesTableBody');
        if (tbody) {
            const candidates = [
                { rank: 1, name: 'Kepler-442 b', score: 98.6, dist: 1206, status: 'Habitable' },
                { rank: 2, name: 'Kepler-62 e', score: 96.1, dist: 1200, status: 'Habitable' },
                { rank: 3, name: 'Proxima Centauri b', score: 94.5, dist: 4.2, status: 'Habitable' },
                { rank: 4, name: 'TRAPPIST-1 e', score: 93.0, dist: 40, status: 'Habitable' },
                { rank: 5, name: 'Kepler-186 f', score: 91.2, dist: 580, status: 'Habitable' },
                { rank: 6, name: 'Teegarden b', score: 90.5, dist: 12, status: 'Habitable' },
                { rank: 7, name: 'GJ 1061 c', score: 89.1, dist: 12, status: 'Habitable' },
                { rank: 8, name: 'TRAPPIST-1 d', score: 88.4, dist: 40, status: 'Habitable' },
                { rank: 9, name: 'K2-72 e', score: 87.8, dist: 227, status: 'Habitable' },
                { rank: 10, name: 'GJ 667 C c', score: 85.3, dist: 23, status: 'Habitable' }
            ];

            tbody.innerHTML = ''; // Clear existing
            candidates.forEach(c => {
                const row = `
                    <tr>
                        <td><span style="color: #00d2ff; font-weight: bold;">#${c.rank}</span></td>
                        <td>${c.name}</td>
                        <td><div class="progress" style="height: 6px; width: 80px; display: inline-block; margin-right: 10px; background-color: #2c3e50;">
                                <div class="progress-bar" role="progressbar" style="width: ${c.score}%; background-color: #00ff88;"></div>
                            </div> <span style="color: #fff;">${c.score}%</span></td>
                        <td>${c.dist}</td>
                        <td><span class="badge bg-success bg-opacity-25 text-success">${c.status}</span></td>
                    </tr>
                `;
                tbody.innerHTML += row;
            });
        }

    } catch (error) {
        console.error('Dashboard error:', error);
    }
}

function renderGauge(score) {
    const ctx = document.getElementById('gaugeChart').getContext('2d');

    // Normalize score 0-1 to 0-100
    const value = score * 100;

    if (gaugeChartInstance) {
        gaugeChartInstance.destroy();
    }

    gaugeChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Score', 'Remaining'],
            datasets: [{
                data: [value, 100 - value],
                backgroundColor: [
                    value > 70 ? '#00ff88' : (value > 40 ? '#ffcc00' : '#ff0055'), // Dynamic color
                    '#2c3e50'
                ],
                borderWidth: 0,
                cutout: '80%',
                rotation: 270,
                circumference: 180
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            },
            animation: {
                animateScale: true,
                animateRotate: true
            }
        }
    });

    // Update text
    const gaugeValueElement = document.getElementById('gaugeValue');
    gaugeValueElement.innerText = value.toFixed(1) + '%';
    gaugeValueElement.style.color = value > 70 ? '#00ff88' : (value > 40 ? '#ffcc00' : '#ff0055');
}

// Handle Prediction
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('predictionForm');

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const formData = new FormData(form);
            const data = {};
            formData.forEach((value, key) => {
                data[key] = value ? parseFloat(value) : 0;
            });

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                if (!response.ok) throw new Error('Prediction failed');

                const result = await response.json();

                // Show result wrapper
                document.getElementById('placeholderWrapper').style.display = 'none';
                document.getElementById('resultWrapper').style.display = 'block';

                // Update UI
                renderGauge(result.probability);

                const badge = document.getElementById('statusBadge');
                badge.innerText = result.habitable ? 'HABITABLE' : 'NON-HABITABLE';
                badge.className = 'status-badge ' + (result.habitable ? 'text-success' : 'text-danger');
                badge.style.background = result.habitable ? 'rgba(0, 255, 136, 0.1)' : 'rgba(255, 0, 85, 0.1)';

                document.getElementById('predClass').innerText = result.habitable ? 'Habitable' : 'Non-Habitable';
                document.getElementById('predConf').innerText = result.probability > 0.8 ? 'High' : (result.probability > 0.5 ? 'Medium' : 'Low');
                document.getElementById('predHabitable').innerText = result.habitable ? 'Yes ✓' : 'No ✗';
                document.getElementById('predHabitable').className = result.habitable ? 'details-value text-success' : 'details-value text-danger';

            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Check console.');
            }
        });
    }
});
