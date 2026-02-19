function setLoading(state) {
  document.getElementById("loading").style.display = state ? "block" : "none";
}

function showError(msg) {
  document.getElementById("error").innerText = msg;
}

async function runPrediction() {
  const data = {
    pl_rade: 0.3,
    pl_bmasse: 0.4,
    pl_dens: 0.6,
    pl_eqt: 0.5,
    pl_orbper: 0.2,
    sy_dist: 0.1,
    st_lum: 0.4,
    st_teff: 0.5,
    st_met: 0.3,
    st_spectral_score: 0.85
  };

  setLoading(true);

  try {
    const res = await fetch("/api/v1/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });

    if (!res.ok) throw new Error("Prediction failed");

    const out = await res.json();
    renderChart(out.probabilities);

  } catch (e) {
    showError(e.message);
  } finally {
    setLoading(false);
  }
}

function renderChart(probs) {
  new Chart(document.getElementById("probChart"), {
    type: "bar",
    data: {
      labels: ["Non", "Potential", "High"],
      datasets: [{ data: probs }]
    }
  });
}

fetch("/api/v1/top-planets")
  .then(r => r.json())
  .then(rows => {
    document.getElementById("table").innerHTML =
      rows.map(r =>
        `<tr><td>${r.pl_name}</td><td>${r.score.toFixed(3)}</td></tr>`
      ).join("");
  });
