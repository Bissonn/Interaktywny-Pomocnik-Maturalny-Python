import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def render():
    st.header("🔢 Ciągi arytmetyczne i geometryczne")

    tab1, tab2 = st.tabs(["🎛️ Interaktywny kalkulator", "📝 Zadania"])

    with tab1:
        kind = st.radio("Typ ciągu:", ["Arytmetyczny", "Geometryczny"],
                        horizontal=True, key="ciag_kind")

        if kind == "Arytmetyczny":
            col1, col2, col3 = st.columns(3)
            with col1: a1 = st.slider("a₁ (pierwszy wyraz)", -20, 20, 2, 1, key="ca1")
            with col2: r  = st.slider("r (różnica)",         -10, 10, 3, 1, key="cr")
            with col3: n  = st.slider("n (ile wyrazów)",       3, 25, 10, 1, key="cn")

            wyrazy = [a1 + (i-1)*r for i in range(1, n+1)]
            an = wyrazy[-1]
            sn = n/2 * (a1 + an)

            col1, col2, col3 = st.columns(3)
            col1.metric("aₙ (n-ty wyraz)", round(an, 4))
            col2.metric(f"Sₙ (suma {n} wyrazów)", round(sn, 4))
            col3.metric("Różnica r", r)

            st.caption(f"Wzór: aₙ = {a1} + (n−1)·{r}  |  "
                       f"a_{n} = {a1} + {n-1}·{r} = {an}  |  "
                       f"S_{n} = {n}/2·({a1}+{an}) = {round(sn,2)}")

            fig, ax = plt.subplots(figsize=(9, 3.5))
            ax.plot(range(1, n+1), wyrazy, "bo-", markersize=7, lw=1.8)
            ax.fill_between(range(1, n+1), wyrazy, alpha=0.08, color="blue")
            if n <= 15:
                for i, v in enumerate(wyrazy):
                    ax.annotate(str(v), (i+1, v), textcoords="offset points",
                                xytext=(0, 7), ha="center", fontsize=7)
            ax.set_title(f"Ciąg arytmetyczny: a₁={a1}, r={r}", fontsize=11)
            ax.set_xlabel("n"); ax.set_ylabel("aₙ"); ax.grid(True, alpha=0.3)
            st.pyplot(fig); plt.close()

        else:  # Geometryczny
            col1, col2, col3 = st.columns(3)
            with col1: a1 = st.slider("a₁ (pierwszy wyraz)", -10, 20, 1, 1,   key="ga1")
            with col2: q  = st.slider("q (iloraz)",           -4.0, 4.0, 2.0, 0.25, key="gq")
            with col3: n  = st.slider("n (ile wyrazów)",       3, 15, 8, 1,    key="gn")

            if q == 0:
                st.warning("Iloraz q nie może być 0!"); return

            wyrazy = [round(a1 * q**(i-1), 5) for i in range(1, n+1)]
            an = wyrazy[-1]
            sn = a1*n if q == 1 else round(a1*(q**n - 1)/(q - 1), 5)

            col1, col2, col3 = st.columns(3)
            col1.metric("aₙ (n-ty wyraz)", round(an, 5))
            col2.metric(f"Sₙ (suma {n} wyrazów)", round(sn, 5))
            col3.metric("Iloraz q", q)

            st.caption(f"Wzór: aₙ = {a1}·{q}^(n−1)  |  "
                       f"a_{n} = {round(an,5)}  |  S_{n} = {round(sn,5)}")

            fig, ax = plt.subplots(figsize=(9, 3.5))
            ax.plot(range(1, n+1), wyrazy, "rs-", markersize=7, lw=1.8, color="#991f1f")
            ax.fill_between(range(1, n+1), wyrazy, alpha=0.08, color="#991f1f")
            if n <= 12:
                for i, v in enumerate(wyrazy):
                    ax.annotate(str(round(v, 3)), (i+1, v),
                                textcoords="offset points", xytext=(0, 7),
                                ha="center", fontsize=7)
            ax.set_title(f"Ciąg geometryczny: a₁={a1}, q={q}", fontsize=11)
            ax.set_xlabel("n"); ax.set_ylabel("aₙ"); ax.grid(True, alpha=0.3)
            st.pyplot(fig); plt.close()

    with tab2:
        _zadania()


def _zadania():
    st.subheader("Zadania")

    with st.expander("📌 Zadanie 1 — Proste  *(2 pkt)*"):
        st.markdown("""
Ciąg arytmetyczny ma pierwszy wyraz **a₁ = 5** i różnicę **r = −3**.

Oblicz sumę pierwszych **10 wyrazów**.
        """)
        if st.button("Pokaż rozwiązanie", key="ciag_z1"):
            st.success("""
**Rozwiązanie:**

a₁ = 5,  r = −3,  n = 10

a₁₀ = 5 + (10−1)·(−3) = 5 − 27 = **−22**

S₁₀ = 10/2 · (a₁ + a₁₀) = 5 · (5 + (−22)) = 5 · (−17) = **−85**

✅ S₁₀ = −85
            """)

    with st.expander("📌 Zadanie 2 — Ciąg geometryczny  *(4 pkt)*"):
        st.markdown("""
Pierwszy wyraz ciągu geometrycznego wynosi **a₁ = 3**,
a suma pierwszych czterech wyrazów wynosi **S₄ = 45**.

Wyznacz iloraz **q** i oblicz **S₈**.
        """)
        if st.button("Pokaż rozwiązanie", key="ciag_z2"):
            st.success("""
**Rozwiązanie:**

S₄ = a₁·(q⁴−1)/(q−1) = 45
3·(q⁴−1)/(q−1) = 45
1 + q + q² + q³ = 15
q³ + q² + q − 14 = 0

Sprawdzamy q = 2:  8 + 4 + 2 − 14 = 0 ✓

**q = 2**

S₈ = 3·(2⁸−1)/(2−1) = 3·255 = **765**

Wyrazy: 3, 6, 12, 24, 48, 96, 192, 384
Suma:   3+6+12+24+48+96+192+384 = 765 ✓
            """)

    with st.expander("📌 Zadanie 3 — Zadanie z kontekstem  *(5 pkt)*"):
        st.markdown("""
Pewna firma inwestuje pieniądze. Na początku roku 2020 zainwestowała **10 000 zł**.
Każdy kolejny rok inwestycja rosła o **8%** w stosunku do poprzedniego roku.

**a)** Ile wynosi inwestycja na początku roku 2025 (po 5 latach)?

**b)** Po ilu pełnych latach inwestycja przekroczy **20 000 zł**?
        """)
        if st.button("Pokaż rozwiązanie", key="ciag_z3"):
            import math
            a1 = 10000; q = 1.08
            a6 = a1 * q**5
            n = math.ceil(math.log(2) / math.log(q))
            st.success(f"""
**Rozwiązanie:**

To ciąg geometryczny: a₁ = 10 000,  q = 1,08

**a)** Po 5 latach (a₆ = a₁·q⁵):
a₆ = 10 000 · 1,08⁵ = 10 000 · {round(1.08**5, 5)} = **{round(a6, 2)} zł**

**b)** Szukamy n: a₁·qⁿ > 20 000
10 000 · 1,08ⁿ > 20 000
1,08ⁿ > 2
n > log(2)/log(1,08) = {round(math.log(2)/math.log(1.08), 3)}

✅ Po **{n} pełnych latach** inwestycja przekroczy 20 000 zł.
(Sprawdzenie: 10 000 · 1,08^{n} = {round(a1*q**n, 2)} zł)
            """)
