import { fetchJson, summaryUrl } from "../utils/api.js";
import { abbreviateAmount } from "../utils/format.js";
import { showError, clearError } from "../utils/dom.js";
import { setupDateRangeFilter } from "../utils/filters.js";

let revenueByDayChart = null;

function renderRevenueByDay(rows) {
  const msgId = "revenue-by-day-msg";
  const canvas = document.getElementById("revenue-by-day-chart");
  if (revenueByDayChart) {
    revenueByDayChart.destroy();
    revenueByDayChart = null;
  }
  if (!rows.length || rows.every((r) => r.total_amount === 0)) {
    showError(msgId, canvas, null, "Aún no hay cobros registrados en este periodo.");
    return;
  }
  clearError(msgId, canvas);
  const labels = rows.map((r) => {
    const [, m, d] = r.day.split("-");
    return `${d}/${m}`;
  });
  revenueByDayChart = new Chart(canvas.getContext("2d"), {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Ingresos",
        data: rows.map((r) => r.total_amount),
        backgroundColor: "rgba(90, 157, 181, 0.55)",
        borderColor: "#5A9DB5",
        borderWidth: 1,
        borderRadius: 3,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: { label: (ctx) => abbreviateAmount(ctx.parsed.y) },
        },
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: "#94a3b8", maxRotation: 0, autoSkip: true, maxTicksLimit: 8 } },
        y: {
          grid: { color: "#e6e9ee", borderDash: [4, 4] },
          ticks: { color: "#94a3b8", callback: (value) => abbreviateAmount(value) },
        },
      },
    },
  });
}

export async function loadRevenueByDay(dateFrom, dateTo) {
  try {
    const summary = await fetchJson(summaryUrl(dateFrom, dateTo));
    renderRevenueByDay(summary.revenue_by_day);
  } catch (err) {
    showError("revenue-by-day-msg", document.getElementById("revenue-by-day-chart"), err.status);
  }
}

export function initRevenueByDay() {
  setupDateRangeFilter({
    formId: "revenue-by-day-filter-form",
    fromId: "revenue-by-day-date-from",
    toId: "revenue-by-day-date-to",
    clearId: "revenue-by-day-clear",
    onApply: loadRevenueByDay,
  });
  loadRevenueByDay(null, null);
}
