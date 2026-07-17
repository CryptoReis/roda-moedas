"""Calculation helpers for Roda Moedas.

The app stores the same Google Sheets columns as v1, but v2 separates the
amount sent to troca-notas from the total amount of 1 EUR and 0.50 EUR coins.
Any 1 EUR / 0.50 EUR value not allocated to troca-notas automatically remains
in the banco total.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP


D = Decimal
CENT = D("0.01")

USERS = ["Vanda", "Reis", "Renato", "André", "Daniela", "Silvia", "Parada", "Mafalda"]

SHEET_COLUMNS = [
    "Timestamp",
    "User",
    "Date",
    "Moeda_2EUR_Qty",
    "Moeda_2EUR_Total",
    "Moeda_1EUR_Qty",
    "Moeda_1EUR_Total",
    "Moeda_05EUR_Qty",
    "Moeda_05EUR_Total",
    "Moeda_02EUR_Qty",
    "Moeda_02EUR_Total",
    "Moeda_01EUR_Qty",
    "Moeda_01EUR_Total",
    "Moeda_005EUR_Qty",
    "Moeda_005EUR_Total",
    "Nota_20EUR_Qty",
    "Nota_20EUR_Total",
    "Nota_10EUR_Qty",
    "Nota_10EUR_Total",
    "Nota_5EUR_Qty",
    "Nota_5EUR_Total",
    "Troca_Total",
    "Banco_Total",
    "Grand_Total",
    "Notes",
]


@dataclass(frozen=True)
class EntryInput:
    user: str
    entry_date: date
    moeda_2eur: int = 0
    moeda_1eur: int = 0
    moeda_05eur: int = 0
    moeda_02eur: int = 0
    moeda_01eur: int = 0
    moeda_005eur: int = 0
    nota_20eur: int = 0
    nota_10eur: int = 0
    nota_5eur: int = 0
    troca_1eur_amount: Decimal = D("0.00")
    troca_05eur_amount: Decimal = D("0.00")
    notes: str = ""


def money(value: Decimal | int | float | str) -> Decimal:
    """Return a two-decimal Decimal suitable for EUR values."""
    return D(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)


def euro_float(value: Decimal) -> float:
    return float(money(value))


def denomination_total(quantity: int, denomination: Decimal) -> Decimal:
    if quantity < 0:
        raise ValueError("Quantities cannot be negative")
    return money(D(quantity) * denomination)


def validate_allocation(inputs: EntryInput) -> None:
    if inputs.troca_1eur_amount < 0 or inputs.troca_05eur_amount < 0:
        raise ValueError("Troca-notas amounts cannot be negative")

    total_1eur = denomination_total(inputs.moeda_1eur, D("1.00"))
    total_05eur = denomination_total(inputs.moeda_05eur, D("0.50"))

    if money(inputs.troca_1eur_amount) > total_1eur:
        raise ValueError("The 1 EUR troca-notas amount cannot exceed the total 1 EUR coins amount")
    if money(inputs.troca_05eur_amount) > total_05eur:
        raise ValueError("The 0.50 EUR troca-notas amount cannot exceed the total 0.50 EUR coins amount")

    # 1 EUR coins can only be allocated in whole-euro steps; 0.50 EUR coins in 50-cent steps.
    if money(inputs.troca_1eur_amount) % D("1.00") != 0:
        raise ValueError("The 1 EUR troca-notas amount must be a whole-euro amount")
    if money(inputs.troca_05eur_amount) % D("0.50") != 0:
        raise ValueError("The 0.50 EUR troca-notas amount must be a multiple of 0.50 EUR")


def calculate_totals(inputs: EntryInput) -> dict[str, Decimal]:
    validate_allocation(inputs)

    totals = {
        "Moeda_2EUR_Total": denomination_total(inputs.moeda_2eur, D("2.00")),
        "Moeda_1EUR_Total": denomination_total(inputs.moeda_1eur, D("1.00")),
        "Moeda_05EUR_Total": denomination_total(inputs.moeda_05eur, D("0.50")),
        "Moeda_02EUR_Total": denomination_total(inputs.moeda_02eur, D("0.20")),
        "Moeda_01EUR_Total": denomination_total(inputs.moeda_01eur, D("0.10")),
        "Moeda_005EUR_Total": denomination_total(inputs.moeda_005eur, D("0.05")),
        "Nota_20EUR_Total": denomination_total(inputs.nota_20eur, D("20.00")),
        "Nota_10EUR_Total": denomination_total(inputs.nota_10eur, D("10.00")),
        "Nota_5EUR_Total": denomination_total(inputs.nota_5eur, D("5.00")),
    }

    troca_total = money(inputs.troca_1eur_amount) + money(inputs.troca_05eur_amount)
    grand_total = money(sum(totals.values(), D("0.00")))
    banco_total = money(grand_total - troca_total)

    totals["Troca_Total"] = money(troca_total)
    totals["Banco_Total"] = banco_total
    totals["Grand_Total"] = grand_total
    return totals


def build_sheet_row(inputs: EntryInput, timestamp: datetime | None = None) -> dict[str, object]:
    totals = calculate_totals(inputs)
    timestamp = timestamp or datetime.now()

    row = {
        "Timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "User": inputs.user,
        "Date": str(inputs.entry_date),
        "Moeda_2EUR_Qty": inputs.moeda_2eur,
        "Moeda_2EUR_Total": euro_float(totals["Moeda_2EUR_Total"]),
        "Moeda_1EUR_Qty": inputs.moeda_1eur,
        "Moeda_1EUR_Total": euro_float(totals["Moeda_1EUR_Total"]),
        "Moeda_05EUR_Qty": inputs.moeda_05eur,
        "Moeda_05EUR_Total": euro_float(totals["Moeda_05EUR_Total"]),
        "Moeda_02EUR_Qty": inputs.moeda_02eur,
        "Moeda_02EUR_Total": euro_float(totals["Moeda_02EUR_Total"]),
        "Moeda_01EUR_Qty": inputs.moeda_01eur,
        "Moeda_01EUR_Total": euro_float(totals["Moeda_01EUR_Total"]),
        "Moeda_005EUR_Qty": inputs.moeda_005eur,
        "Moeda_005EUR_Total": euro_float(totals["Moeda_005EUR_Total"]),
        "Nota_20EUR_Qty": inputs.nota_20eur,
        "Nota_20EUR_Total": euro_float(totals["Nota_20EUR_Total"]),
        "Nota_10EUR_Qty": inputs.nota_10eur,
        "Nota_10EUR_Total": euro_float(totals["Nota_10EUR_Total"]),
        "Nota_5EUR_Qty": inputs.nota_5eur,
        "Nota_5EUR_Total": euro_float(totals["Nota_5EUR_Total"]),
        "Troca_Total": euro_float(totals["Troca_Total"]),
        "Banco_Total": euro_float(totals["Banco_Total"]),
        "Grand_Total": euro_float(totals["Grand_Total"]),
        "Notes": inputs.notes,
    }
    return {column: row[column] for column in SHEET_COLUMNS}
