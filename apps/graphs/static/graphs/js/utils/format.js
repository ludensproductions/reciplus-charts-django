export function abbreviateAmount(value) {
  const sign = value < 0 ? "-" : "";
  const abs = Math.abs(value);
  if (abs >= 1e9) return sign + "$" + (abs / 1e9).toFixed(2) + "B";
  if (abs >= 1e6) return sign + "$" + (abs / 1e6).toFixed(2) + "M";
  if (abs >= 1e3) return sign + "$" + (abs / 1e3).toFixed(2) + "K";
  return sign + "$" + abs.toFixed(2);
}

export function formatCurrencyFull(value) {
  return "$" + value.toLocaleString("es-MX", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}
