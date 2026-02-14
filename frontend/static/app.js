/**
 * ExoExplore - Interactive Exoplanet Website
 * Features: 3D hero animation, smooth scrolling, API integration, charts
 */

// ===== CONFIGURATION =====
const API_BASE_URL = window.location.origin.includes('localhost') 
    ? 'http://localhost:5000' 
    : window.location.origin;

// ===== THREE.JS HERO ANIMATION =====
let scene, camera, renderer, particles, starField;

function initThreeJS() {
    const canvas = document.getElementById('hero-canvas');
    if (!canvas) return;

    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Create starfield
    createStarField();
    
    // Create floating particles
    createParticles();
    
    // Create a glowing planet
    createHeroPlanet();

    camera.position.z = 30;

    animate();
}

function createStarField() {
    const geometry = new THREE.BufferGeometry();
    const count = 3000;
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);

    for (let i = 0; i < count * 3; i += 3) {
        positions[i] = (Math.random() - 0.5) * 200;
        positions[i + 1] = (Math.random() - 0.5) * 200;
        positions[i + 2] = (Math.random() - 0.5) * 200;

        // Star colors (mostly white/blue with some yellow/red)
        const colorChoice = Math.random();
        if (colorChoice > 0.9) {
            colors[i] = 1; colors[i + 1] = 0.8; colors[i + 2] = 0.4; // Yellow
        } else if (colorChoice > 0.95) {
            colors[i] = 1; colors[i + 1] = 0.4; colors[i + 2] = 0.4; // Red
        } else {
            colors[i] = 0.9; colors[i + 1] = 0.95; colors[i + 2] = 1; // Blue-white
        }
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
        size: 0.2,
        vertexColors: true,
        transparent: true,
        opacity: 0.8,
        sizeAttenuation: true
    });

    starField = new THREE.Points(geometry, material);
    scene.add(starField);
}

function createParticles() {
    const geometry = new THREE.BufferGeometry();
    const count = 500;
    const positions = new Float32Array(count * 3);

    for (let i = 0; i < count * 3; i += 3) {
        positions[i] = (Math.random() - 0.5) * 100;
        positions[i + 1] = (Math.random() - 0.5) * 100;
        positions[i + 2] = (Math.random() - 0.5) * 100;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

    const material = new THREE.PointsMaterial({
        color: 0x00d4ff,
        size: 0.5,
        transparent: true,
        opacity: 0.6,
        blending: THREE.AdditiveBlending
    });

    particles = new THREE.Points(geometry, material);
    scene.add(particles);
}

function createHeroPlanet() {
    const geometry = new THREE.SphereGeometry(5, 64, 64);
    
    // Create a custom shader material for the planet
    const material = new THREE.MeshPhongMaterial({
        color: 0x2d3436,
        emissive: 0x1a1a2e,
        specular: 0x00d4ff,
        shininess: 50,
        transparent: true,
        opacity: 0.9
    });

    const planet = new THREE.Mesh(geometry, material);
    planet.position.set(15, -5, -10);
    scene.add(planet);

    // Add atmosphere glow
    const atmosphereGeometry = new THREE.SphereGeometry(5.5, 64, 64);
    const atmosphereMaterial = new THREE.MeshBasicMaterial({
        color: 0x00d4ff,
        transparent: true,
        opacity: 0.1,
        side: THREE.BackSide
    });
    const atmosphere = new THREE.Mesh(atmosphereGeometry, atmosphereMaterial);
    atmosphere.position.copy(planet.position);
    scene.add(atmosphere);

    // Animate planet
    gsap.to(planet.rotation, {
        y: Math.PI * 2,
        duration: 60,
        repeat: -1,
        ease: "none"
    });

    // Store reference for animation
    window.heroPlanet = planet;
}

function animate() {
    requestAnimationFrame(animate);

    // Rotate starfield slowly
    if (starField) {
        starField.rotation.y += 0.0002;
        starField.rotation.x += 0.0001;
    }

    // Animate particles
    if (particles) {
        particles.rotation.y -= 0.001;
        const positions = particles.geometry.attributes.position.array;
        for (let i = 1; i < positions.length; i += 3) {
            positions[i] += Math.sin(Date.now() * 0.001 + positions[i - 1]) * 0.02;
        }
        particles.geometry.attributes.position.needsUpdate = true;
    }

    renderer.render(scene, camera);
}

function onWindowResize() {
    if (!camera || !renderer) return;
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

// ===== GSAP ANIMATIONS =====
function initGSAPAnimations() {
    gsap.registerPlugin(ScrollTrigger);

    // Hero text animation
    gsap.from('.hero-title .title-line', {
        y: 100,
        opacity: 0,
        duration: 1.2,
        stagger: 0.2,
        ease: "power4.out"
    });

    gsap.from('.hero-subtitle', {
        y: 50,
        opacity: 0,
        duration: 1,
        delay: 0.6,
        ease: "power3.out"
    });

    gsap.from('.hero-stats .stat', {
        y: 50,
        opacity: 0,
        duration: 0.8,
        stagger: 0.15,
        delay: 0.8,
        ease: "power3.out"
    });

    gsap.from('.cta-button', {
        y: 30,
        opacity: 0,
        duration: 0.8,
        delay: 1.2,
        ease: "power3.out"
    });

    // Section animations
    gsap.utils.toArray('.section-header').forEach(header => {
        gsap.from(header, {
            scrollTrigger: {
                trigger: header,
                start: "top 80%",
                toggleActions: "play none none reverse"
            },
            y: 50,
            opacity: 0,
            duration: 0.8,
            ease: "power3.out"
        });
    });

    // About cards animation
    gsap.from('.about-card', {
        scrollTrigger: {
            trigger: '.about-grid',
            start: "top 80%"
        },
        y: 60,
        opacity: 0,
        duration: 0.8,
        stagger: 0.15,
        ease: "power3.out"
    });

    // Timeline items
    gsap.from('.timeline-item', {
        scrollTrigger: {
            trigger: '.timeline',
            start: "top 80%"
        },
        x: -50,
        opacity: 0,
        duration: 0.8,
        stagger: 0.2,
        ease: "power3.out"
    });

    // Planet cards
    gsap.from('.planet-card', {
        scrollTrigger: {
            trigger: '.planet-showcase',
            start: "top 80%"
        },
        y: 80,
        opacity: 0,
        duration: 0.8,
        stagger: 0.2,
        ease: "power3.out"
    });

    // Bio cards
    gsap.from('.bio-card', {
        scrollTrigger: {
            trigger: '.biosignature-grid',
            start: "top 80%"
        },
        scale: 0.8,
        opacity: 0,
        duration: 0.6,
        stagger: 0.1,
        ease: "back.out(1.7)"
    });

    // Movie cards
    gsap.from('.movie-card', {
        scrollTrigger: {
            trigger: '.movies-grid',
            start: "top 80%"
        },
        y: 60,
        opacity: 0,
        duration: 0.8,
        stagger: 0.1,
        ease: "power3.out"
    });

    // Parallax effect for hero
    gsap.to('.hero-content', {
        scrollTrigger: {
            trigger: '.hero',
            start: "top top",
            end: "bottom top",
            scrub: 1
        },
        y: 200,
        opacity: 0
    });
}

// ===== COUNTERS ANIMATION =====
function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');
    
    counters.forEach(counter => {
        const target = parseFloat(counter.getAttribute('data-count'));
        const duration = 2000;
        const increment = target / (duration / 16);
        let current = 0;

        const updateCounter = () => {
            current += increment;
            if (current < target) {
                counter.textContent = target % 1 === 0 
                    ? Math.floor(current).toLocaleString()
                    : current.toFixed(1);
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target % 1 === 0 
                    ? target.toLocaleString()
                    : target.toFixed(1);
            }
        };

        // Start animation when element is in view
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    updateCounter();
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        observer.observe(counter);
    });
}

// ===== NAVIGATION =====
function initNavigation() {
    const navbar = document.querySelector('.navbar');
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    // Navbar scroll effect
    window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(10, 10, 10, 0.95)';
            navbar.style.padding = '0.8rem 3rem';
        } else {
            navbar.style.background = 'rgba(10, 10, 10, 0.8)';
            navbar.style.padding = '1rem 3rem';
        }
    });

    // Mobile menu toggle
    hamburger?.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        hamburger.classList.toggle('active');
    });

    // Close mobile menu on link click
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            hamburger.classList.remove('active');
        });
    });
}

// ===== SMOOTH SCROLL =====
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// ===== TILT EFFECT =====
function initTiltEffect() {
    const cards = document.querySelectorAll('[data-tilt]');
    
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateZ(0)';
        });
    });
}

// ===== CHARTS =====
let featureImportanceChart, habitabilityChart, starPlanetChart;

function initCharts() {
    // Feature Importance Chart
    const featureCtx = document.getElementById('featureImportanceChart')?.getContext('2d');
    if (featureCtx) {
        featureImportanceChart = new Chart(featureCtx, {
            type: 'bar',
            data: {
                labels: ['Planet Radius', 'Equilibrium Temp', 'Stellar Temp', 'Orbital Period', 'Planet Mass', 'Stellar Mass', 'Stellar Radius', 'Distance', 'Star Count', 'Planet Count'],
                datasets: [{
                    label: 'Importance Score',
                    data: [0.95, 0.92, 0.88, 0.75, 0.70, 0.65, 0.60, 0.45, 0.35, 0.30],
                    backgroundColor: 'rgba(0, 212, 255, 0.6)',
                    borderColor: '#00d4ff',
                    borderWidth: 2,
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { color: '#b0b0b0' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { 
                            color: '#b0b0b0',
                            maxRotation: 45
                        }
                    }
                }
            }
        });
    }

    // Habitability Distribution Chart
    const habitabilityCtx = document.getElementById('habitabilityChart')?.getContext('2d');
    if (habitabilityCtx) {
        habitabilityChart = new Chart(habitabilityCtx, {
            type: 'doughnut',
            data: {
                labels: ['Habitable', 'Not Habitable', 'Marginal'],
                datasets: [{
                    data: [205, 36900, 107],
                    backgroundColor: [
                        'rgba(0, 255, 136, 0.8)',
                        'rgba(255, 68, 68, 0.8)',
                        'rgba(255, 193, 7, 0.8)'
                    ],
                    borderColor: [
                        '#00ff88',
                        '#ff4444',
                        '#ffc107'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#b0b0b0' }
                    }
                }
            }
        });
    }

    // Star-Planet Relationship Chart
    const starPlanetCtx = document.getElementById('starPlanetChart')?.getContext('2d');
    if (starPlanetCtx) {
        starPlanetChart = new Chart(starPlanetCtx, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Habitable Planets',
                    data: [
                        { x: 5778, y: 1.0 },
                        { x: 2550, y: 0.92 },
                        { x: 2500, y: 1.1 },
                        { x: 5800, y: 1.6 },
                        { x: 3200, y: 1.3 }
                    ],
                    backgroundColor: 'rgba(0, 255, 136, 0.6)',
                    borderColor: '#00ff88',
                    borderWidth: 2
                }, {
                    label: 'Non-Habitable Planets',
                    data: [
                        { x: 6000, y: 11.0 },
                        { x: 8000, y: 1.8 },
                        { x: 3000, y: 0.3 },
                        { x: 4500, y: 0.2 }
                    ],
                    backgroundColor: 'rgba(255, 68, 68, 0.6)',
                    borderColor: '#ff4444',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: '#b0b0b0' }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Stellar Temperature (K)',
                            color: '#b0b0b0'
                        },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { color: '#b0b0b0' }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Planet Radius (Earth radii)',
                            color: '#b0b0b0'
                        },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { color: '#b0b0b0' }
                    }
                }
            }
        });
    }
}

// ===== PREDICTION FORM =====
const PRESETS = {
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

function loadPreset(presetName) {
    const preset = PRESETS[presetName];
    if (preset) {
        Object.keys(preset).forEach(key => {
            const input = document.getElementById(key);
            if (input) input.value = preset[key];
        });
    }
}

function loadSampleData() {
    loadPreset('earth');
}

function resetForm() {
    document.getElementById('prediction-form').reset();
    document.getElementById('results-content').innerHTML = `
        <div class="results-placeholder">
            <span class="placeholder-icon">🔮</span>
            <p>Enter planet data and click "Predict" to see results</p>
        </div>
    `;
}

async function handlePrediction(e) {
    e.preventDefault();
    
    const form = e.target;
    const submitBtn = form.querySelector('.predict-btn');
    const resultsContent = document.getElementById('results-content');
    
    // Show loading state
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;
    
    // Collect form data
    const formData = {};
    const inputs = form.querySelectorAll('input');
    inputs.forEach(input => {
        formData[input.name] = parseFloat(input.value);
    });
    
    try {
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayPredictionResult(result);
        } else {
            displayError(result.error || 'Prediction failed');
        }
    } catch (error) {
        console.error('Prediction error:', error);
        // Fallback to mock prediction for demo
        displayMockPrediction(formData);
    } finally {
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;
    }
}

function displayPredictionResult(result) {
    const prediction = result.prediction;
    const resultsContent = document.getElementById('results-content');
    
    const isHabitable = prediction.is_habitable === 1;
    const probability = prediction.habitability_probability;
    
    resultsContent.innerHTML = `
        <div class="prediction-result animate-fadeInUp">
            <div class="habitability-score">
                <div class="score-circle" style="background: conic-gradient(
                    ${isHabitable ? '#00ff88' : '#ff4444'} 0% ${probability * 100}%, 
                    rgba(255,255,255,0.1) ${probability * 100}% 100%
                )">
                    <span class="score-value">${(probability * 100).toFixed(1)}%</span>
                </div>
                <h4>Habitability Score</h4>
                <span class="classification ${isHabitable ? 'habitable' : 'not-habitable'}">
                    ${prediction.classification}
                </span>
            </div>
            
            <div class="result-details">
                <h4>Prediction Details</h4>
                <div class="detail-grid">
                    <div class="detail-item">
                        <span class="detail-label">Classification</span>
                        <span class="detail-value">${prediction.classification}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Confidence</span>
                        <span class="detail-value">${prediction.confidence}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Habitable</span>
                        <span class="detail-value">${isHabitable ? 'Yes ✓' : 'No ✗'}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Probability</span>
                        <span class="detail-value">${(probability * 100).toFixed(2)}%</span>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function displayMockPrediction(data) {
    // Mock prediction logic for demo when API is unavailable
    const tempScore = Math.max(0, 1 - Math.abs(data.pl_eqt - 288) / 288);
    const radiusScore = Math.max(0, 1 - Math.abs(data.pl_rade - 1) / 1);
    const probability = (tempScore * 0.5 + radiusScore * 0.5);
    const isHabitable = probability > 0.5 ? 1 : 0;
    
    const mockResult = {
        success: true,
        prediction: {
            is_habitable: isHabitable,
            habitability_probability: probability,
            confidence: probability > 0.8 ? 'High' : probability > 0.5 ? 'Medium' : 'Low',
            classification: isHabitable ? 'Habitable' : 'Not Habitable'
        }
    };
    
    displayPredictionResult(mockResult);
}

function displayError(message) {
    const resultsContent = document.getElementById('results-content');
    resultsContent.innerHTML = `
        <div class="prediction-result" style="text-align: center; color: #ff4444;">
            <span style="font-size: 3rem;">⚠️</span>
            <h4 style="margin-top: 1rem;">Error</h4>
            <p>${message}</p>
        </div>
    `;
}

// ===== PLANET RANKING =====
const TOP_PLANETS = [
    { name: 'Kepler-442 b', score: 0.836, distance: 1206, status: 'Habitable' },
    { name: 'Kepler-62 e', score: 0.811, distance: 1200, status: 'Habitable' },
    { name: 'Kepler-62 f', score: 0.795, distance: 1200, status: 'Habitable' },
    { name: 'Kepler-296 e', score: 0.784, distance: 1510, status: 'Habitable' },
    { name: 'TRAPPIST-1 e', score: 0.770, distance: 40, status: 'Habitable' },
    { name: 'Kepler-438 b', score: 0.758, distance: 640, status: 'Habitable' },
    { name: 'Proxima Centauri b', score: 0.745, distance: 4.2, status: 'Marginal' },
    { name: 'Kepler-186 f', score: 0.732, distance: 580, status: 'Habitable' },
    { name: 'Kepler-452 b', score: 0.719, distance: 1400, status: 'Marginal' },
    { name: 'TRAPPIST-1 f', score: 0.701, distance: 40, status: 'Marginal' }
];

function initRankingTable() {
    const tbody = document.getElementById('ranking-tbody');
    if (!tbody) return;
    
    tbody.innerHTML = TOP_PLANETS.map((planet, index) => `
        <tr>
            <td class="rank">#${index + 1}</td>
            <td>${planet.name}</td>
            <td class="score">${(planet.score * 100).toFixed(1)}%</td>
            <td>${planet.distance}</td>
            <td>
                <span class="status-badge ${planet.status.toLowerCase().replace(' ', '-')}">
                    ${planet.status}
                </span>
            </td>
        </tr>
    `).join('');
}

// ===== API STATUS =====
async function checkApiStatus() {
    const statusElement = document.getElementById('api-status');
    if (!statusElement) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/health`, { 
            method: 'GET',
            headers: { 'Accept': 'application/json' }
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.model_loaded) {
                statusElement.textContent = 'Online ✓';
                statusElement.style.color = '#00ff88';
            } else {
                statusElement.textContent = 'Model Loading...';
                statusElement.style.color = '#ffc107';
            }
        } else {
            throw new Error('API unavailable');
        }
    } catch (error) {
        statusElement.textContent = 'Demo Mode';
        statusElement.style.color = '#ffc107';
    }
}

// ===== SAFETY: Ensure all content is visible =====
function ensureContentVisible() {
    // Force all sections and content to be visible
    const elements = document.querySelectorAll('section, .about-card, .planet-card, .bio-card, .movie-card, .timeline-item, .section-header');
    elements.forEach(el => {
        el.style.opacity = '1';
        el.style.visibility = 'visible';
        el.style.transform = 'none';
    });
}

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', () => {
    // Safety timeout: ensure content is visible after 3 seconds even if animations fail
    setTimeout(ensureContentVisible, 3000);
    
    // Initialize Three.js hero
    try {
        initThreeJS();
    } catch (e) {
        console.log('Three.js initialization skipped');
    }
    
    // Initialize GSAP animations
    try {
        initGSAPAnimations();
    } catch (e) {
        console.log('GSAP animations failed, ensuring content is visible');
        ensureContentVisible();
    }
    
    // Initialize navigation
    initNavigation();
    
    // Initialize smooth scroll
    initSmoothScroll();
    
    // Initialize tilt effects
    initTiltEffect();
    
    // Initialize counters
    animateCounters();
    
    // Initialize charts
    try {
        initCharts();
    } catch (e) {
        console.log('Chart initialization failed');
    }
    
    // Initialize ranking table
    initRankingTable();
    
    // Check API status
    checkApiStatus();
    
    // Setup prediction form
    const predictionForm = document.getElementById('prediction-form');
    if (predictionForm) {
        predictionForm.addEventListener('submit', handlePrediction);
    }
    
    // Window resize handler
    window.addEventListener('resize', onWindowResize);
    
    // Final safety check
    ensureContentVisible();
});

// Make functions globally available
window.loadPreset = loadPreset;
window.loadSampleData = loadSampleData;
window.resetForm = resetForm;
