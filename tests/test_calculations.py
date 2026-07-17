from datetime import date, datetime
from decimal import Decimal

import pytest

from roda_moedas.calculations import EntryInput, SHEET_COLUMNS, build_sheet_row, calculate_totals, USERS


def test_reis_is_second_user():
    assert USERS[:3] == ["Vanda", "Reis", "Renato"]


def test_partial_1eur_and_50cent_troca_remainder_goes_to_banco():
    entry = EntryInput(
        user="Reis",
        entry_date=date(2026, 7, 17),
        moeda_1eur=10,      # 10.00 EUR total
        moeda_05eur=6,      # 3.00 EUR total
        moeda_2eur=2,       # 4.00 EUR total
        moeda_02eur=5,      # 1.00 EUR total
        moeda_01eur=7,      # 0.70 EUR total, always banco
        moeda_005eur=3,     # 0.15 EUR total, always banco
        nota_20eur=1,       # 20.00 EUR total
        nota_10eur=1,       # 10.00 EUR total
        nota_5eur=1,        # 5.00 EUR total
        troca_1eur_amount=Decimal("4.00"),
        troca_05eur_amount=Decimal("1.50"),
    )

    totals = calculate_totals(entry)

    assert totals["Troca_Total"] == Decimal("5.50")
    assert totals["Grand_Total"] == Decimal("53.85")
    assert totals["Banco_Total"] == Decimal("48.35")


def test_10_and_5_cent_coins_can_never_be_allocated_to_troca():
    entry = EntryInput(
        user="Vanda",
        entry_date=date(2026, 7, 17),
        moeda_01eur=10,
        moeda_005eur=10,
        troca_1eur_amount=Decimal("0.00"),
        troca_05eur_amount=Decimal("0.00"),
    )

    totals = calculate_totals(entry)

    assert totals["Grand_Total"] == Decimal("1.50")
    assert totals["Troca_Total"] == Decimal("0.00")
    assert totals["Banco_Total"] == Decimal("1.50")


def test_rejects_troca_allocation_larger_than_available_coin_total():
    entry = EntryInput(
        user="Reis",
        entry_date=date(2026, 7, 17),
        moeda_1eur=2,
        troca_1eur_amount=Decimal("3.00"),
    )

    with pytest.raises(ValueError, match="cannot exceed"):
        calculate_totals(entry)


def test_sheet_row_preserves_v1_column_names_and_order():
    entry = EntryInput(
        user="Reis",
        entry_date=date(2026, 7, 17),
        moeda_1eur=2,
        moeda_05eur=2,
        troca_1eur_amount=Decimal("1.00"),
        troca_05eur_amount=Decimal("0.50"),
        notes="test row",
    )

    row = build_sheet_row(entry, timestamp=datetime(2026, 7, 17, 12, 30, 0))

    assert list(row.keys()) == SHEET_COLUMNS
    assert row["Timestamp"] == "2026-07-17 12:30:00"
    assert row["Moeda_1EUR_Total"] == 2.0
    assert row["Moeda_05EUR_Total"] == 1.0
    assert row["Troca_Total"] == 1.5
    assert row["Banco_Total"] == 1.5
    assert row["Grand_Total"] == 3.0
    assert row["Notes"] == "test row"
