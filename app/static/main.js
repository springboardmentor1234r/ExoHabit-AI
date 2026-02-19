document.getElementById("predictForm").addEventListener("submit", async e => {
    e.preventDefault();
    let data = {};

    new FormData(e.target).forEach((v, k) => data[k] = parseFloat(v));

    const res = await fetch("/api/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-API-KEY": "EXOHABITAI_KEY"
        },
        body: JSON.stringify(data)
    });

    const out = await res.json();
    document.getElementById("result").innerHTML =
        `<h4>${out.prediction}</h4><pre>${JSON.stringify(out.probabilities, null, 2)}</pre>`;
});
