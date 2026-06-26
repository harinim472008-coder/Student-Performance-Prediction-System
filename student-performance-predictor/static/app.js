const form = document.getElementById("predictionForm");
const resultBox = document.getElementById("result");
const summaryContainer = document.getElementById("summary");
const predictionCanvas = document.getElementById("predictionChart");
const summaryCanvas = document.getElementById("summaryChart");

function asNumber(value) {
  return Number.parseFloat(value);
}

function formatNumber(value) {
  return Number(value).toFixed(2);
}

function renderResult(data) {
  resultBox.classList.remove("empty", "error");
  resultBox.innerHTML = `
    <p><strong>Predicted Final Score:</strong> ${data.predicted_score}</p>
    <p><strong>Performance Band:</strong> ${data.performance_band}</p>
  `;
}

function renderError(message) {
  resultBox.classList.remove("empty");
  resultBox.classList.add("error");
  resultBox.textContent = message;
}

function statRow(label, value) {
  return `<p><strong>${label}:</strong> ${value}</p>`;
}

function drawBarChart(canvas, labels, values, maxValue, colorPalette) {
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  const width = canvas.width;
  const height = canvas.height;

  ctx.clearRect(0, 0, width, height);

  const padding = { top: 28, right: 24, bottom: 42, left: 42 };
  const chartWidth = width - padding.left - padding.right;
  const chartHeight = height - padding.top - padding.bottom;
  const barGap = 16;
  const barWidth = (chartWidth - barGap * (labels.length - 1)) / labels.length;

  ctx.strokeStyle = "#94a3b8";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(padding.left, padding.top);
  ctx.lineTo(padding.left, padding.top + chartHeight);
  ctx.lineTo(padding.left + chartWidth, padding.top + chartHeight);
  ctx.stroke();

  ctx.fillStyle = "#64748b";
  ctx.font = "12px Segoe UI";
  ctx.fillText("0", padding.left - 18, padding.top + chartHeight + 4);
  ctx.fillText(String(maxValue), padding.left - 26, padding.top + 6);

  values.forEach((value, index) => {
    const safeValue = Math.max(0, Number(value));
    const barHeight = (safeValue / maxValue) * chartHeight;
    const x = padding.left + index * (barWidth + barGap);
    const y = padding.top + chartHeight - barHeight;

    ctx.fillStyle = colorPalette[index % colorPalette.length];
    ctx.fillRect(x, y, barWidth, barHeight);

    ctx.fillStyle = "#1e293b";
    ctx.font = "12px Segoe UI";
    ctx.fillText(formatNumber(safeValue), x, y - 6);

    ctx.fillStyle = "#334155";
    ctx.font = "11px Segoe UI";
    ctx.fillText(labels[index], x, padding.top + chartHeight + 18);
  });
}

function drawPredictionGraph(payload, predictedScore) {
  const labels = ["attendance", "study_hours", "previous_grades", "predicted_score"];
  const values = [
    payload.attendance,
    (payload.study_hours / 24) * 100,
    payload.previous_grades,
    predictedScore,
  ];

  drawBarChart(predictionCanvas, labels, values, 100, [
    "#0ea5e9",
    "#22c55e",
    "#f97316",
    "#6366f1",
  ]);
}

async function handlePredict(event) {
  event.preventDefault();

  const payload = {
    attendance: asNumber(document.getElementById("attendance").value),
    study_hours: asNumber(document.getElementById("study_hours").value),
    previous_grades: asNumber(document.getElementById("previous_grades").value),
  };

  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Prediction request failed.");
    }

    renderResult(data);
    drawPredictionGraph(payload, Number(data.predicted_score));
  } catch (error) {
    renderError(error.message);
  }
}

function renderSummary(data) {
  const metrics = data.metrics || {};
  const stats = data.statistics || {};

  const cards = Object.keys(stats).map((name) => {
    const s = stats[name];
    return `
      <div class="stat-box">
        <h3>${name}</h3>
        ${statRow("Mean", formatNumber(s.mean))}
        ${statRow("Median", formatNumber(s.median))}
        ${statRow("Std", formatNumber(s.std))}
        ${statRow("Min", formatNumber(s.min))}
        ${statRow("Max", formatNumber(s.max))}
      </div>
    `;
  });

  summaryContainer.innerHTML = `
    <div class="stat-box">
      <h3>Model Metrics</h3>
      ${statRow("Rows", data.row_count)}
      ${statRow("R2 Score", formatNumber(metrics.r2_score))}
      ${statRow("RMSE", formatNumber(metrics.rmse))}
    </div>
    ${cards.join("")}
  `;

  const meanLabels = Object.keys(stats);
  const meanValues = meanLabels.map((key) => Number(stats[key].mean));
  drawBarChart(summaryCanvas, meanLabels, meanValues, 100, [
    "#2563eb",
    "#16a34a",
    "#f59e0b",
    "#9333ea",
  ]);
}

async function loadSummary() {
  try {
    const response = await fetch("/api/summary");
    const data = await response.json();
    renderSummary(data);
  } catch (error) {
    summaryContainer.innerHTML = `<p>Unable to load summary: ${error.message}</p>`;
  }
}

form.addEventListener("submit", handlePredict);
loadSummary();
