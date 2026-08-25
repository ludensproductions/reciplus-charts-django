import { fetchJson, dateRangeQuery } from "../utils/api.js";
import { abbreviateAmount } from "../utils/format.js";
import { showError } from "../utils/dom.js";
import { setupDateRangeFilter } from "../utils/filters.js";

let profitsLossesChart = null;

function renderProfitsAndLosses(data) {
  const canvas = document.getElementById("profits-losses-chart");
  if (profitsLossesChart) {
    profitsLossesChart.destroy();
    profitsLossesChart = null;
  }
  profitsLossesChart = new Chart(canvas.getContext("2d"), {
    data: {
      labels: data.labels,
      datasets: [
        {
          type: "line",
          label: "Saldo",
          data: data.balance,
          borderColor: "#e0a83e",
          backgroundColor: "#e0a83e",
          pointBackgroundColor: "#e0a83e",
          pointBorderColor: "#ffffff",
          pointBorderWidth: 1,
          pointStyle: "circle",
          pointRadius: 5,
          borderWidth: 2,
          tension: 0.3,
          order: 0,
        },
        {
          type: "line",
          label: "Flujo neto",
          data: data.net_flow,
          borderColor: "#8b9dd6",
          backgroundColor: "#8b9dd6",
          pointBackgroundColor: "#8b9dd6",
          pointBorderColor: "#ffffff",
          pointBorderWidth: 1,
          pointStyle: "circle",
          pointRadius: 5,
          borderWidth: 2,
          tension: 0.3,
          order: 1,
        },
        {
          type: "bar",
          label: "Depósitos",
          data: data.deposits,
          backgroundColor: "rgba(120, 210, 150, 0.55)",
          borderColor: "#5cb87e",
          borderWidth: 1,
          borderRadius: 3,
          order: 2,
        },
        {
          type: "bar",
          label: "Retiros",
          data: data.withdrawals,
          backgroundColor: "rgba(240, 140, 140, 0.55)",
          borderColor: "#e07a7a",
          borderWidth: 1,
          borderRadius: 3,
          order: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: "index", intersect: false },
      scales: {
        x: { stacked: true, grid: { display: false }, ticks: { color: "#94a3b8" } },
        y: {
          stacked: true,
          grid: { color: "#e6e9ee", borderDash: [4, 4] },
          ticks: { color: "#94a3b8", callback: (value) => abbreviateAmount(value) },
        },
      },
      plugins: {
        legend: { position: "bottom", labels: { color: "#4a5568", usePointStyle: true, padding: 16 } },
        tooltip: {
          backgroundColor: "#ffffff",
          titleColor: "#4a5568",
          bodyColor: "#4a5568",
          borderColor: "#e6e9ee",
          borderWidth: 1,
          callbacks: { label: (ctx) => `${ctx.dataset.label}: ${abbreviateAmount(ctx.parsed.y)}` },
        },
      },
    },
  });
}

export async function loadProfitsAndLosses(dateFrom, dateTo) {
  try {
    const data = await fetchJson(`/graphs/api/profits-and-losses${dateRangeQuery(dateFrom, dateTo)}`);
    renderProfitsAndLosses(data);
  } catch (err) {
    showError("profits-losses-msg", document.getElementById("profits-losses-chart"), err.status);
  }
}

export function initProfitsAndLosses() {
  setupDateRangeFilter({
    formId: "profits-losses-filter-form",
    fromId: "profits-losses-date-from",
    toId: "profits-losses-date-to",
    clearId: "profits-losses-clear",
    onApply: loadProfitsAndLosses,
  });
  loadProfitsAndLosses(null, null);
}
