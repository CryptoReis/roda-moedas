from datetime import date, datetime
from decimal import Decimal

from roda_moedas.calculations import EntryInput, SHEET_COLUMNS, build_sheet_row


V1_EXPORT_COLUMNS = [
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


def test_v2_sheet_columns_exactly_match_original_v1_export_order():
    assert SHEET_COLUMNS == V1_EXPORT_COLUMNS


def test_new_troca_split_logic_does_not_add_columns_to_google_sheets_export():
    entry = EntryInput(
        user="Reis",
        entry_date=date(2026, 7, 17),
        moeda_2eur=3,
        moeda_1eur=10,
        moeda_05eur=8,
        moeda_02eur=4,
        moeda_01eur=5,
        moeda_005eur=6,
        nota_20eur=7,
        nota_10eur=2,
        nota_5eur=1,
        troca_1eur_amount=Decimal("6.00"),
        troca_05eur_amount=Decimal("2.50"),
        notes="compatibility check",
    )

    row = build_sheet_row(entry, timestamp=datetime(2026, 7, 17, 22, 45, 0))

    assert list(row) == V1_EXPORT_COLUMNS
    assert set(row) == set(V1_EXPORT_COLUMNS)
    assert "Troca_1EUR_Total" not in row
    assert "Troca_05EUR_Total" not in row
    assert "Banco_1EUR_Total" not in row
    assert "Banco_05EUR_Total" not in row

    # The v1-compatible aggregate columns carry the new split result.
    assert row["Troca_Total"] == 8.5
    assert row["Banco_Total"] == 178.1
    assert row["Grand_Total"] == 186.6


def test_export_keeps_new_005_010_values_in_existing_v1_columns():
    entry = EntryInput(
        user="Vanda",
        entry_date=date(2026, 7, 17),
        moeda_01eur=11,
        moeda_005eur=9,
    )

    row = build_sheet_row(entry, timestamp=datetime(2026, 7, 17, 22, 45, 0))

    assert row["Moeda_01EUR_Qty"] == 11
    assert row["Moeda_01EUR_Total"] == 1.1
    assert row["Moeda_005EUR_Qty"] == 9
    assert row["Moeda_005EUR_Total"] == 0.45
    assert row["Troca_Total"] == 0.0
    assert row["Banco_Total"] == 1.55
    assert row["Grand_Total"] == 1.55
