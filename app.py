import sys
from datetime import datetime
from decimal import Decimal
from pathlib import Path

import pandas as pd
import streamlit as st

# Allow `streamlit run app.py` without installing the package first.
sys.path.insert(0, str(Path(__file__).parent / "src"))

from roda_moedas.calculations import (  # noqa: E402
    EntryInput,
    USERS,
    build_sheet_row,
    calculate_totals,
    money,
)
from roda_moedas.sheets import get_store  # noqa: E402


st.set_page_config(
    page_title="Roda Moedas",
    page_icon="💰",
    layout="wide",
)

st.title("💰 Roda Moedas")
st.caption("Registo mensal de moedas e notas")
st.markdown("---")

store, store_mode = get_store()
if store_mode == "dry-run":
    st.info("🧪 Modo de teste ativo: os dados ficam apenas nesta sessão e não são gravados no Google Sheets.")


def eur(value: Decimal) -> str:
    return f"{money(value):,.2f} €".replace(",", " ")


def denomination_input(label: str, denomination: Decimal, key: str) -> int:
    """Render a quantity input with its live EUR total immediately beside it."""
    input_col, total_col = st.columns([2, 1])
    with input_col:
        quantity = st.number_input(label, min_value=0, step=1, value=0, format="%d", key=key)
    with total_col:
        st.metric("Total", eur(Decimal(quantity) * denomination))
    return int(quantity)


st.subheader("📋 Dados do registo")

selected_user = st.selectbox("Utilizador", USERS, index=0)
entry_date = st.date_input("Data", value=datetime.now().date())

st.markdown("### 🪙 Moedas")
coin_col1, coin_col2, coin_col3 = st.columns(3)
with coin_col1:
    moeda_2eur = denomination_input("2 €", Decimal("2.00"), "moeda_2eur")
    moeda_1eur = denomination_input("1 €", Decimal("1.00"), "moeda_1eur")
with coin_col2:
    moeda_05eur = denomination_input("0,50 €", Decimal("0.50"), "moeda_05eur")
    moeda_02eur = denomination_input("0,20 €", Decimal("0.20"), "moeda_02eur")
with coin_col3:
    moeda_01eur = denomination_input("0,10 €", Decimal("0.10"), "moeda_01eur")
    moeda_005eur = denomination_input("0,05 €", Decimal("0.05"), "moeda_005eur")

total_1eur_available = Decimal(moeda_1eur) * Decimal("1.00")
total_05eur_available = Decimal(moeda_05eur) * Decimal("0.50")

# If a user lowers the coin quantity after choosing a troca-notas amount, clamp the
# current selection so Streamlit never keeps an impossible value in session state.
st.session_state["troca_1eur_amount"] = min(
    float(st.session_state.get("troca_1eur_amount", 0.0)), float(total_1eur_available)
)
st.session_state["troca_05eur_amount"] = min(
    float(st.session_state.get("troca_05eur_amount", 0.0)), float(total_05eur_available)
)

st.markdown("### 🔄 Troca-notas")
st.caption(
    "Escolhe quanto do valor total em moedas de 1 € e 0,50 € vai para troca-notas. "
    "O restante passa automaticamente para banco. Moedas de 0,05 €, 0,10 €, 0,20 € e 2 € vão sempre para banco."
)
troca_col1, troca_col2 = st.columns(2)
with troca_col1:
    st.caption(f"Disponível em moedas de 1 €: **{eur(total_1eur_available)}**")
    troca_1eur_amount = st.number_input(
        "Valor em moedas de 1 € para troca-notas (€)",
        min_value=0.0,
        max_value=float(total_1eur_available),
        step=1.0,
        format="%.2f",
        key="troca_1eur_amount",
    )
with troca_col2:
    st.caption(f"Disponível em moedas de 0,50 €: **{eur(total_05eur_available)}**")
    troca_05eur_amount = st.number_input(
        "Valor em moedas de 0,50 € para troca-notas (€)",
        min_value=0.0,
        max_value=float(total_05eur_available),
        step=0.5,
        format="%.2f",
        key="troca_05eur_amount",
    )

st.markdown("### 💵 Notas")
bill_col1, bill_col2, bill_col3 = st.columns(3)
with bill_col1:
    nota_20eur = denomination_input("20 €", Decimal("20.00"), "nota_20eur")
with bill_col2:
    nota_10eur = denomination_input("10 €", Decimal("10.00"), "nota_10eur")
with bill_col3:
    nota_5eur = denomination_input("5 €", Decimal("5.00"), "nota_5eur")

notes = st.text_area("Notas", placeholder="Notas opcionais sobre este registo...")

entry = EntryInput(
    user=selected_user,
    entry_date=entry_date,
    moeda_2eur=moeda_2eur,
    moeda_1eur=moeda_1eur,
    moeda_05eur=moeda_05eur,
    moeda_02eur=moeda_02eur,
    moeda_01eur=moeda_01eur,
    moeda_005eur=moeda_005eur,
    nota_20eur=nota_20eur,
    nota_10eur=nota_10eur,
    nota_5eur=nota_5eur,
    troca_1eur_amount=Decimal(str(troca_1eur_amount)),
    troca_05eur_amount=Decimal(str(troca_05eur_amount)),
    notes=notes,
)

totals = calculate_totals(entry)

st.markdown("---")
st.markdown("### 📊 Resumo automático")
metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric("Total geral", eur(totals["Grand_Total"]))
metric_col2.metric("Para troca-notas", eur(totals["Troca_Total"]))
metric_col3.metric("Para banco", eur(totals["Banco_Total"]))

with st.expander("Detalhe dos cálculos", expanded=True):
    detail_df = pd.DataFrame(
        [
            {"Destino": "Troca-notas", "Categoria": "1 €", "Valor": eur(money(troca_1eur_amount))},
            {"Destino": "Troca-notas", "Categoria": "0,50 €", "Valor": eur(money(troca_05eur_amount))},
            {
                "Destino": "Banco",
                "Categoria": "Restante 1 €",
                "Valor": eur(totals["Moeda_1EUR_Total"] - money(troca_1eur_amount)),
            },
            {
                "Destino": "Banco",
                "Categoria": "Restante 0,50 €",
                "Valor": eur(totals["Moeda_05EUR_Total"] - money(troca_05eur_amount)),
            },
            {"Destino": "Banco", "Categoria": "20 €", "Valor": eur(totals["Nota_20EUR_Total"])},
            {"Destino": "Banco", "Categoria": "10 €", "Valor": eur(totals["Nota_10EUR_Total"])},
            {"Destino": "Banco", "Categoria": "5 €", "Valor": eur(totals["Nota_5EUR_Total"])},
            {"Destino": "Banco", "Categoria": "2 €", "Valor": eur(totals["Moeda_2EUR_Total"])},
            {"Destino": "Banco", "Categoria": "0,20 €", "Valor": eur(totals["Moeda_02EUR_Total"])},
            {"Destino": "Banco", "Categoria": "0,10 €", "Valor": eur(totals["Moeda_01EUR_Total"])},
            {"Destino": "Banco", "Categoria": "0,05 €", "Valor": eur(totals["Moeda_005EUR_Total"])},
        ]
    )
    st.dataframe(detail_df, width="stretch", hide_index=True)

st.markdown("---")
st.markdown("### ✅ Rever antes de submeter")
st.caption("Confirma estes valores antes de gravar o registo.")

review_col1, review_col2 = st.columns(2)
with review_col1:
    st.markdown("**Informação geral**")
    st.write(f"- Utilizador: **{selected_user}**")
    st.write(f"- Data: **{entry_date}**")
    if notes.strip():
        st.write(f"- Notas: {notes}")
    else:
        st.write("- Notas: —")

with review_col2:
    st.markdown("**Totais a gravar**")
    st.write(f"- Total geral: **{eur(totals['Grand_Total'])}**")
    st.write(f"- Para troca-notas: **{eur(totals['Troca_Total'])}**")
    st.write(f"- Para banco: **{eur(totals['Banco_Total'])}**")

review_df = pd.DataFrame(
    [
        {"Tipo": "Moeda", "Denominação": "2 €", "Quantidade": moeda_2eur, "Total": eur(totals["Moeda_2EUR_Total"]), "Destino": "Banco"},
        {
            "Tipo": "Moeda",
            "Denominação": "1 €",
            "Quantidade": moeda_1eur,
            "Total": eur(totals["Moeda_1EUR_Total"]),
            "Destino": f"{eur(money(troca_1eur_amount))} troca-notas / {eur(totals['Moeda_1EUR_Total'] - money(troca_1eur_amount))} banco",
        },
        {
            "Tipo": "Moeda",
            "Denominação": "0,50 €",
            "Quantidade": moeda_05eur,
            "Total": eur(totals["Moeda_05EUR_Total"]),
            "Destino": f"{eur(money(troca_05eur_amount))} troca-notas / {eur(totals['Moeda_05EUR_Total'] - money(troca_05eur_amount))} banco",
        },
        {"Tipo": "Moeda", "Denominação": "0,20 €", "Quantidade": moeda_02eur, "Total": eur(totals["Moeda_02EUR_Total"]), "Destino": "Banco"},
        {"Tipo": "Moeda", "Denominação": "0,10 €", "Quantidade": moeda_01eur, "Total": eur(totals["Moeda_01EUR_Total"]), "Destino": "Banco"},
        {"Tipo": "Moeda", "Denominação": "0,05 €", "Quantidade": moeda_005eur, "Total": eur(totals["Moeda_005EUR_Total"]), "Destino": "Banco"},
        {"Tipo": "Nota", "Denominação": "20 €", "Quantidade": nota_20eur, "Total": eur(totals["Nota_20EUR_Total"]), "Destino": "Banco"},
        {"Tipo": "Nota", "Denominação": "10 €", "Quantidade": nota_10eur, "Total": eur(totals["Nota_10EUR_Total"]), "Destino": "Banco"},
        {"Tipo": "Nota", "Denominação": "5 €", "Quantidade": nota_5eur, "Total": eur(totals["Nota_5EUR_Total"]), "Destino": "Banco"},
    ]
)
st.dataframe(review_df, width="stretch", hide_index=True)

submitted = st.button("✅ Confirmar e submeter registo", width="stretch", type="primary")

if submitted:
    if totals["Grand_Total"] == Decimal("0.00"):
        st.error("❌ Não é possível submeter um registo com total zero.")
    else:
        try:
            row = build_sheet_row(entry)
            store.append(row)
            if store_mode == "dry-run":
                st.success("🧪 Registo guardado apenas em modo de teste. Nenhum dado live foi alterado.")
            else:
                st.success("💾 Registo guardado no Google Sheets!")
        except Exception as exc:
            st.error(f"❌ Erro ao guardar o registo: {exc}")

st.markdown("---")
st.markdown("### 📜 Últimos 5 registos")
try:
    all_data = store.read()
    if not all_data.empty:
        last_5 = all_data.tail(5).sort_values(by="Timestamp", ascending=False)
        display_columns = ["Timestamp", "User", "Date", "Grand_Total", "Troca_Total", "Banco_Total", "Notes"]
        available_columns = [col for col in display_columns if col in last_5.columns]
        st.dataframe(last_5[available_columns], width="stretch", hide_index=True)
    else:
        st.info("Ainda não existem registos nesta sessão/folha.")
except Exception as exc:
    st.warning(f"Não foi possível carregar registos recentes: {exc}")
