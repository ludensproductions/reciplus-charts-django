export function showError(msgElId, canvasEl, status, fallbackText) {
  canvasEl.style.display = "none";
  const msgEl = document.getElementById(msgElId);
  msgEl.style.display = "block";
  msgEl.textContent = status === 401
    ? "Tu sesión expiró. Entra de nuevo desde la app Reciplus."
    : (fallbackText || "No se pudo cargar la información.");
}

export function clearError(msgElId, canvasEl) {
  canvasEl.style.display = "block";
  const msgEl = document.getElementById(msgElId);
  msgEl.style.display = "none";
  msgEl.textContent = "";
}
