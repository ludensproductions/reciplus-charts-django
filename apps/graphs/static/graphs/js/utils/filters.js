/** Cablea un form de filtro desde/hasta + botón limpiar genérico para cualquier gráfica. */
export function setupDateRangeFilter({ formId, fromId, toId, clearId, onApply }) {
  const form = document.getElementById(formId);
  const fromInput = document.getElementById(fromId);
  const toInput = document.getElementById(toId);
  const clearBtn = document.getElementById(clearId);

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    onApply(fromInput.value || null, toInput.value || null);
  });

  clearBtn.addEventListener("click", () => {
    fromInput.value = "";
    toInput.value = "";
    onApply(null, null);
  });
}
