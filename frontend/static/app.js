/**
 * PlanetAI - Hybrid Application Logic
 * Integrates Website interactions, 3D Visualization, and AI Dashboard features.
 */

// Global State
let featureChart = null;
let distributionChart = null;

document.addEventListener('DOMContentLoaded', () => {
    initThreeJS();
    initNavigation();
    initForms();
    initCharts(); // Initialize empty charts

    // GSAP Animations
    gsap.registerPlugin(ScrollTrigger);
    initAnimations();
});

// ===== 3D VISUALIZATION (Particles + Glowing Core) =====
function initThreeJS() {
    const canvas = document.getElementById('hero-canvas');
    if (!canvas) return;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });

    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Particle System
    const particlesGeometry = new THREE.BufferGeometry();
    const particlesCount = 3000;
    const posArray = new Float32Array(particlesCount * 3);

    for (let i = 0; i < particlesCount * 3; i++) {
        posArray[i] = (Math.random() - 0.5) * 50; // Spread out
    }

    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

    // Glowing Material
    const particlesMaterial = new THREE.PointsMaterial({
        size: 0.05,
        color: 0x007bff,
        transparent: true,
        opacity: 0.8,
        blending: THREE.AdditiveBlending
    });

    const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
    scene.add(particlesMesh);

    camera.position.z = 20;

    // Mouse Interaction
    let mouseX = 0;
    let mouseY = 0;

    document.addEventListener('mousemove', (event) => {
        mouseX = event.clientX / window.innerWidth - 0.5;
        mouseY = event.clientY / window.innerHeight - 0.5;
    });

    // Animation Loop
    const clock = new THREE.Clock();

    function tick() {
        const elapsedTime = clock.getElapsedTime();

        // Rotate entire system
        particlesMesh.rotation.y = elapsedTime * 0.05;
        particlesMesh.rotation.x = mouseY * 0.1;
        particlesMesh.rotation.y += mouseX * 0.1;

        renderer.render(scene, camera);
        window.requestAnimationFrame(tick);
    }
    tick();

    // Resize
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
}

// ===== NAVIGATION & ANIMATIONS =====
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');

            // Only intercept hash links (anchors on same page)
            if (targetId.startsWith('#')) {
                e.preventDefault();
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            }
            // Normal links let browser handle navigation
        });
    });
}

function initAnimations() {
    // Hero Elements
    gsap.from('.hero-title', { opacity: 0, y: 50, duration: 1, delay: 0.5 });
    gsap.from('.hero-subtitle', { opacity: 0, y: 30, duration: 1, delay: 0.8 });
    gsap.from('.hero-stats', { opacity: 0, y: 30, duration: 1, delay: 1 });
    gsap.from('.btn-lg', { opacity: 0, scale: 0.9, duration: 0.5, delay: 1.2 });

    // Scroll Triggers for Sections
    gsap.utils.toArray('.content-section').forEach(section => {
        gsap.from(section, {
            opacity: 0,
            y: 50,
            duration: 1,
            scrollTrigger: {
                trigger: section,
                start: "top 80%",
                toggleActions: "play none none reverse"
            }
        });
    });

    // Stagger Cards
    gsap.from('.info-card', {
        opacity: 0,
        y: 30,
        stagger: 0.2,
        duration: 0.8,
        scrollTrigger: {
            trigger: '.cards-grid',
            start: "top 85%"
        }
    });
}

// ===== FORM & PREDICTION (DASHBOARD) =====
function initForms() {
    // Random Planet
    const randomBtn = document.getElementById('random-planet-btn');
    if (randomBtn) {
        randomBtn.addEventListener('click', async (e) => {
            e.preventDefault(); // Prevent form submission if inside form
            try {
                const response = await fetch('/random-planet');
                const data = await response.json();
                if (data.success) {
                    populateForm(data.planet);
                }
            } catch (error) {
                console.error('Error fetching random planet:', error);
            }
        });
    }

    // Preset Buttons
    const presetBtns = document.querySelectorAll('.preset-btn');
    const presets = {
        earth: {
            pl_orbper: 365.25,
            pl_rade: 1.0,
            pl_bmasse: 1.0,
            pl_eqt: 288,
            st_teff: 5778,
            st_rad: 1.0,
            st_mass: 1.0,
            sy_dist: 10.0,
            sy_snum: 1,
            sy_pnum: 1
        },
        mars: {
            pl_orbper: 687.0,
            pl_rade: 0.53,
            pl_bmasse: 0.11,
            pl_eqt: 210,
            st_teff: 5778,
            st_rad: 1.0,
            st_mass: 1.0,
            sy_dist: 10.0,
            sy_snum: 1,
            sy_pnum: 8
        },
        jupiter: {
            pl_orbper: 4333.0,
            pl_rade: 11.2,
            pl_bmasse: 318.0,
            pl_eqt: 165,
            st_teff: 5778,
            st_rad: 1.0,
            st_mass: 1.0,
            sy_dist: 10.0,
            sy_snum: 1,
            sy_pnum: 8
        },
        proxima: {
            pl_orbper: 11.2,
            pl_rade: 1.17,
            pl_bmasse: 1.27,
            pl_eqt: 234,
            st_teff: 3042,
            st_rad: 0.14,
            st_mass: 0.12,
            sy_dist: 1.3,
            sy_snum: 1,
            sy_pnum: 1
        }
    };

    presetBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const key = btn.dataset.preset;
            if (presets[key]) {
                populateForm(presets[key]);
            }
        });
    });


    // Prediction Form
    const form = document.getElementById('prediction-form');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = form.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Analyzing...';

            const formData = new FormData(form);
            const payload = Object.fromEntries(formData.entries());

            // Convert types
            for (const key in payload) {
                if (key !== 'model_type') {
                    // Ensure backend receives numeric types
                    payload[key] = parseFloat(payload[key]);
                }
            }

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const result = await response.json();

                if (result.success) {
                    displayResults(result);
                    updateCharts(result);

                    // Scroll to results
                    document.getElementById('analyze').scrollIntoView({ behavior: 'smooth' });
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                console.error('Prediction failed', error);
                alert('Analysis failed. Check console.');
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Analyze Habitability';
            }
        });
    }

    function populateForm(planet) {
        for (const [key, value] of Object.entries(planet)) {
            const input = document.getElementById(key);
            if (input) input.value = value;
        }
    }
}

function displayResults(data) {
    console.log("Displaying results:", data);
    const container = document.getElementById('results-body');
    const pred = data.prediction;
    const isHabitable = pred.is_habitable === 1;

    const color = isHabitable ? '#28a745' : '#dc3545';
    const status = isHabitable ? 'HABITABLE CANDIDATE' : 'NON-HABITABLE';

    container.innerHTML = `
        <div style="text-align: center; width: 100%;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">${isHabitable ? '🌱' : '🌋'}</div>
            <h2 style="color: ${color}; margin-bottom: 0.5rem;">${status}</h2>
            <div style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1.5rem;">
                ${(pred.habitability_probability * 100).toFixed(1)}%
                <span style="font-size: 1rem; color: #a0a0c0; display: block;">Probability Score</span>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; text-align: left; background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 10px;">
                <div>
                    <span style="color: #a0a0c0; font-size: 0.8rem;">Model Confidence</span>
                    <div style="font-weight: 600;">${pred.confidence}</div>
                </div>
                <div>
                    <span style="color: #a0a0c0; font-size: 0.8rem;">Algorithm</span>
                    <div style="font-weight: 600;">${pred.model_used}</div>
                </div>
            </div>
        </div>
    `;

    // Remove empty state class
    container.classList.remove('empty');
}

// ===== CHARTS =====
function initCharts() {
    // Initialize Feature Chart (Empty)
    // Initialize Feature Chart (Empty)
    const ctxFeature = document.getElementById('featureChart');
    if (ctxFeature) {
        featureChart = new Chart(ctxFeature, {
            type: 'bar',
            data: {
                labels: ['Planet Radius', 'Equilibrium Temp', 'Stellar Temp', 'Orbital Period', 'Planet Mass', 'Stellar Mass', 'Stellar Radius', 'Distance', 'Star Count', 'Planet Count'],
                datasets: [{
                    label: 'Importance',
                    data: [0.95, 0.92, 0.88, 0.75, 0.70, 0.65, 0.60, 0.45, 0.35, 0.30],
                    backgroundColor: '#007bff',
                    borderRadius: 5
                }]
            },
            options: {
                indexAxis: 'x',
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#a0a0c0' } },
                    y: { grid: { display: false }, ticks: { color: '#a0a0c0' } }
                }
            }
        });
    }

    // Initialize Distribution Chart (Donut)
    const ctxDist = document.getElementById('distributionChart');
    if (ctxDist) {
        distributionChart = new Chart(ctxDist, {
            type: 'doughnut',
            data: {
                labels: ['Habitable', 'Non-Habitable', 'Marginal'],
                datasets: [{
                    data: [205, 36900, 107],
                    backgroundColor: ['#28a745', '#dc3545', '#ffc107'],
                    borderWidth: 0,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '60%',
                plugins: {
                    legend: { position: 'right', labels: { color: '#a0a0c0' } },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                let label = context.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed !== null) {
                                    label += context.parsed;
                                }
                                return label;
                            }
                        }
                    }
                }
            }
        });
    }

}

function updateCharts(result) {
    // Update Feature Chart
    if (featureChart && result.feature_importance) {
        const sorted = Object.entries(result.feature_importance).sort(([, a], [, b]) => b - a);
        featureChart.data.labels = sorted.map(([k]) => k);
        featureChart.data.datasets[0].data = sorted.map(([, v]) => v);
        featureChart.update();
    }

    // Donut Chart (Static Data, Highlighting Only)
    if (distributionChart && result.prediction) {
        // Highlight logic can be added here if needed, but data remains static as requested
    }
}

// ===== INTERACTIVE CARDS =====
function toggleCard(card) {
    card.classList.toggle('active');
}
