import { fetchJson, summaryUrl } from "../utils/api.js";
import { formatCurrencyFull } from "../utils/format.js";
import { setupDateRangeFilter } from "../utils/filters.js";

function renderSummaryCards(summary) {
  const container = document.getElementById("summary-cards");
  const cards = [
    { label: "Citas totales", value: String(summary.total_appointments) },
    { label: "Total cobrado", value: formatCurrencyFull(summary.total_collected) },
    { label: "Balance esperado en MercadoPago", value: formatCurrencyFull(summary.mercado_pago_expected_balance) },
  ];
  container.innerHTML = cards.map((c) => `
    <div class="summary-card">
      <p class="label">${c.label}</p>
      <p class="value">${c.value}</p>
    </div>
  `).join("");
}

export async function loadSummaryCards(dateFrom, dateTo) {
  try {
    const summary = await fetchJson(summaryUrl(dateFrom, dateTo));
    renderSummaryCards(summary);
  } catch (err) {
    document.getElementById("summary-cards").innerHTML = "";
  }
}

export function initSummaryCards() {
  setupDateRangeFilter({
    formId: "summary-cards-filter-form",
    fromId: "summary-cards-date-from",
    toId: "summary-cards-date-to",
    clearId: "summary-cards-clear",
    onApply: loadSummaryCards,
  });
  loadSummaryCards(null, null);
}
