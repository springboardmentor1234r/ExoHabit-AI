console.log("ExoHabitAI frontend loaded");

async function predictPlanet() {
  setLoading(true);

  try {
    const res = await fetch("/api/v1/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-KEY": "EXOHABITAI_KEY"
      },
      body: JSON.stringify({
        pl_rade: 0.3,
        pl_bmasse: 0.4,
        pl_dens: 0.6,
        pl_eqt: 0.5,
        pl_orbper: 0.2,
        sy_dist: 0.1,
        st_lum: 0.4,
        st_teff: 0.5,
        st_met: 0.3
      })
    });

if (!res.ok) {
  const text = await res.text();
  console.error("Backend error:", text);
  throw new Error(text);
}

const out = await res.json();

    renderChart(out.probabilities);
    renderLabel(out.prediction);

  } catch (err) {
    alert(err.message);
  } finally {
    setLoading(false);
  }
}

function renderChart(probs) {
  const ctx = document.getElementById("probChart");
  if (!ctx) return;

  new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Non-Habitable", "Potential", "High"],
      datasets: [{
        data: probs
      }]
    }
  });
}

function renderLabel(label) {
  document.getElementById("result").innerText = label;
}

function setLoading(state) {
  document.getElementById("loading").style.display = state ? "block" : "none";
}

document.addEventListener("DOMContentLoaded", predictPlanet);
