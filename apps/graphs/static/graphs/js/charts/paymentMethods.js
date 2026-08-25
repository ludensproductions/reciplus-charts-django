import { fetchJson, summaryUrl } from "../utils/api.js";
import { abbreviateAmount } from "../utils/format.js";
import { showError, clearError } from "../utils/dom.js";
import { setupDateRangeFilter } from "../utils/filters.js";

const PIE_COLORS = ["#5A9DB5", "#63c6a8", "#e0a83e", "#e07a7a", "#8b9dd6", "#c58bd6"];

let paymentMethodsChart = null;

function renderPaymentMethods(rows) {
  const msgId = "payment-methods-msg";
  const canvas = document.getElementById("payment-methods-chart");
  if (paymentMethodsChart) {
    paymentMethodsChart.destroy();
    paymentMethodsChart = null;
  }
  if (!rows.length) {
    showError(msgId, canvas, null, "Aún no hay cobros registrados.");
    return;
  }
  clearError(msgId, canvas);
  const labels = rows.map((r) => r.payment_method_display || r.payment_method || "—");
  const values = rows.map((r) => r.total_amount);
  paymentMethodsChart = new Chart(canvas.getContext("2d"), {
    type: "doughnut",
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: PIE_COLORS,
        borderColor: "#ffffff",
        borderWidth: 2,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "bottom", labels: { color: "#4a5568", usePointStyle: true, padding: 14 } },
        tooltip: {
          callbacks: { label: (ctx) => `${ctx.label}: ${abbreviateAmount(ctx.parsed)}` },
        },
      },
    },
  });
}

export async function loadPaymentMethods(dateFrom, dateTo) {
  try {
    const summary = await fetchJson(summaryUrl(dateFrom, dateTo));
    renderPaymentMethods(summary.payments_by_method);
  } catch (err) {
    showError("payment-methods-msg", document.getElementById("payment-methods-chart"), err.status);
  }
}

export function initPaymentMethods() {
  setupDateRangeFilter({
    formId: "payment-methods-filter-form",
    fromId: "payment-methods-date-from",
    toId: "payment-methods-date-to",
    clearId: "payment-methods-clear",
    onApply: loadPaymentMethods,
  });
  loadPaymentMethods(null, null);
}
