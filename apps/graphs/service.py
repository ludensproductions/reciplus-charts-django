"""Agregación de datos para las gráficas de reciplus-charts-django."""
from __future__ import annotations

from datetime import date, timedelta

from django.db.models import Count, Sum
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone

from apps.graphs import consts as graphs_consts
from hsl_7.models import Appointment, InvoicingSettings, Payment, Refund
from shared.choices import AppointmentStatus


class GraphsService:
    """Agregaciones de datos para las gráficas — una gráfica por método."""

    def get_profits_and_losses(
        self,
        doctor_user_id: int | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> dict:
        """Depósitos (Payment aprobados) y retiros (Refund completados) por mes, más
        saldo acumulado y flujo neto — listo para alimentar la gráfica de barras+líneas.

        [doctor_user_id] acota todo a un solo doctor (vista de doctor); None trae la
        plataforma completa (vista de administrador). [date_from]/[date_to] acotan por
        mes (default: últimos MONTHS_BACK meses)."""
        if date_from is None or date_to is None:
            default_from, default_to = self._default_profits_losses_range()
            date_from = (date_from or default_from).replace(day=1)
            date_to = date_to or default_to

        months = self._months_between(date_from, date_to)
        start = months[0]

        deposits_qs = Payment.objects.filter(
            status=Payment.Status.APPROVED, created_at__date__gte=start, created_at__date__lte=date_to,
        )
        withdrawals_qs = Refund.objects.filter(
            status=Refund.Status.COMPLETED, cancelled_at__date__gte=start, cancelled_at__date__lte=date_to,
        )
        if doctor_user_id is not None:
            deposits_qs = deposits_qs.filter(doctor_user_id=doctor_user_id)
            withdrawals_qs = withdrawals_qs.filter(doctor_user_id=doctor_user_id)

        deposits_qs = deposits_qs.annotate(month=TruncMonth("created_at")).values("month").annotate(total=Sum("amount"))
        deposits_by_month = {self._normalize_month_key(row["month"]): float(row["total"]) for row in deposits_qs}

        withdrawals_qs = (
            withdrawals_qs.annotate(month=TruncMonth("cancelled_at")).values("month").annotate(total=Sum("refund_amount"))
        )
        withdrawals_by_month = {self._normalize_month_key(row["month"]): float(row["total"] or 0) for row in withdrawals_qs}

        labels: list[str] = []
        deposits: list[float] = []
        withdrawals: list[float] = []
        net_flow: list[float] = []
        balance: list[float] = []
        running_balance = 0.0

        for month in months:
            deposit = deposits_by_month.get(month, 0.0)
            withdrawal = withdrawals_by_month.get(month, 0.0)
            net = deposit - withdrawal
            running_balance += net

            labels.append(month.strftime("%b %Y"))
            deposits.append(deposit)
            withdrawals.append(-withdrawal)  # negativo: barra roja ancla hacia abajo desde 0
            net_flow.append(net)
            balance.append(running_balance)

        return {
            "labels": labels,
            "deposits": deposits,
            "withdrawals": withdrawals,
            "net_flow": net_flow,
            "balance": balance,
        }

    def get_doctor_summary(
        self, doctor_user_id: int | None, date_from: date | None = None, date_to: date | None = None,
    ) -> dict:
        """Resumen de citas y cobros — mismo cálculo que apps.stats en reciplus-djangoninja.

        [doctor_user_id] acota a un solo doctor (vista de doctor); None trae la
        plataforma completa (vista de administrador)."""
        date_from, date_to = self._default_date_range(date_from, date_to)

        appointments_qs = Appointment.objects.all()
        payments_qs = Payment.objects.filter(status=Payment.Status.APPROVED)
        if doctor_user_id is not None:
            appointments_qs = appointments_qs.filter(doctor_user_id=doctor_user_id)
            payments_qs = payments_qs.filter(doctor_user_id=doctor_user_id)
        if date_from:
            appointments_qs = appointments_qs.filter(starting_time__date__gte=date_from)
            payments_qs = payments_qs.filter(created_at__date__gte=date_from)
        if date_to:
            appointments_qs = appointments_qs.filter(starting_time__date__lte=date_to)
            payments_qs = payments_qs.filter(created_at__date__lte=date_to)

        status_display = dict(AppointmentStatus.choices)
        appointments_by_status = [
            {
                "status": row["status"],
                "status_display": status_display.get(row["status"], row["status"]),
                "count": row["count"],
            }
            for row in appointments_qs.values("status").annotate(count=Count("id"))
        ]
        total_appointments = sum(row["count"] for row in appointments_by_status)

        payments_by_method = [
            {
                "payment_method": row["provider__key"],
                "payment_method_display": row["provider__name"],
                "count": row["count"],
                "total_amount": float(row["total_amount"] or 0),
            }
            for row in payments_qs.values("provider__key", "provider__name").annotate(
                count=Count("id"), total_amount=Sum("amount"),
            )
        ]
        total_collected = sum(row["total_amount"] for row in payments_by_method)

        day_totals = {
            row["day"]: row
            for row in payments_qs.annotate(day=TruncDate("created_at")).values("day").annotate(
                count=Count("id"), total_amount=Sum("amount"),
            )
        }
        revenue_by_day = []
        if date_from and date_to:
            current = date_from
            while current <= date_to:
                row = day_totals.get(current)
                revenue_by_day.append({
                    "day": current.isoformat(),
                    "count": row["count"] if row else 0,
                    "total_amount": float(row["total_amount"] or 0) if row else 0.0,
                })
                current += timedelta(days=1)

        mp_gross = float(
            payments_qs.filter(provider__key=graphs_consts.PROVIDER_MERCADOPAGO)
            .aggregate(total=Sum("amount"))["total"] or 0
        )
        fee_pct = self._mercadopago_fee_pct()
        mercado_pago_expected_balance = round(mp_gross - (mp_gross * fee_pct / 100), 2)

        return {
            "date_from": date_from.isoformat() if date_from else None,
            "date_to": date_to.isoformat() if date_to else None,
            "total_appointments": total_appointments,
            "appointments_by_status": appointments_by_status,
            "payments_by_method": payments_by_method,
            "revenue_by_day": revenue_by_day,
            "total_collected": total_collected,
            "mercado_pago_expected_balance": mercado_pago_expected_balance,
        }

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _mercadopago_fee_pct(self) -> float:
        """% de comisión de plataforma sobre MercadoPago — configurable por el admin
        (InvoicingSettings, misma fila que el precio del timbre)."""
        settings_row = InvoicingSettings.objects.first()
        return float(settings_row.mercadopago_platform_fee_pct) if settings_row else 5.0

    def _default_profits_losses_range(self) -> tuple[date, date]:
        """Últimos MONTHS_BACK meses (día 1 del más viejo, hoy)."""
        today = timezone.now().date()
        year, month = today.year, today.month
        for _ in range(graphs_consts.MONTHS_BACK - 1):
            month -= 1
            if month == 0:
                month, year = 12, year - 1
        return date(year, month, 1), today

    def _months_between(self, start: date, end: date) -> list[date]:
        """Meses (día 1) desde el mes de [start] hasta el mes de [end], inclusive."""
        months = []
        year, month = start.year, start.month
        while (year, month) <= (end.year, end.month):
            months.append(date(year, month, 1))
            month += 1
            if month == 13:
                month, year = 1, year + 1
        return months

    def _normalize_month_key(self, value) -> date:
        """TruncMonth regresa datetime (aware si USE_TZ) o date según el backend —
        normaliza a date(año, mes, 1) para poder comparar contra la lista de meses."""
        normalized = value.date() if hasattr(value, "date") else value
        return normalized.replace(day=1)

    def _default_date_range(self, date_from: date | None, date_to: date | None) -> tuple[date | None, date | None]:
        if date_from is None and date_to is None:
            date_to = timezone.now().date()
            date_from = date_to - timedelta(days=graphs_consts.STATS_DEFAULT_RANGE_DAYS - 1)
        return date_from, date_to
