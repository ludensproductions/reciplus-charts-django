export async function fetchJson(url) {
  const response = await fetch(url, { credentials: "same-origin" });
  if (!response.ok) {
    const error = new Error("request failed");
    error.status = response.status;
    throw error;
  }
  return response.json();
}

export function dateRangeQuery(dateFrom, dateTo) {
  const params = new URLSearchParams();
  if (dateFrom) params.set("date_from", dateFrom);
  if (dateTo) params.set("date_to", dateTo);
  const query = params.toString();
  return query ? `?${query}` : "";
}

export function summaryUrl(dateFrom, dateTo) {
  return `/api/graphs/summary${dateRangeQuery(dateFrom, dateTo)}`;
}
