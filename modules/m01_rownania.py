import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math


def render():
    st.header("📐 Funkcje liniowe i kwadratowe")

    tab1, tab2 = st.tabs(["🎛️ Interaktywny kalkulator", "📝 Zadania"])

    # ─────────────────────────────────────────────────────────────
    with tab1:
        st.subheader("Funkcja liniowa: f(x) = ax + b")
        col1, col2 = st.columns(2)
        with col1:
            a_lin = st.slider("a (nachylenie)", -5.0, 5.0, 2.0, 0.5, key="lin_a")
        with col2:
            b_lin = st.slider("b (wyraz wolny)", -10.0, 10.0, -3.0, 0.5, key="lin_b")

        x = np.linspace(-6, 6, 400)
        fig, ax = plt.subplots(figsize=(8, 3.5))
        ax.plot(x, a_lin*x + b_lin, "#1a4f8a", lw=2.5,
                label=f"f(x) = {a_lin}x + ({b_lin})")
        ax.axhline(0, color="k", lw=0.8); ax.axvline(0, color="k", lw=0.8)
        if a_lin != 0:
            xr = -b_lin / a_lin
            ax.plot(xr, 0, "ro", markersize=10, zorder=5,
                    label=f"Miejsce zerowe: x = {round(xr,4)}")
        ax.set_title(f"f(x) = {a_lin}x + ({b_lin})", fontsize=12)
        ax.legend(); ax.grid(True, alpha=0.3)
        st.pyplot(fig); plt.close()

        if a_lin != 0:
            xr = -b_lin / a_lin
            st.success(f"Miejsce zerowe: **x = {round(xr,4)}**  "
                       f"(f(x)=0 → {a_lin}x = {-b_lin} → x = {round(xr,4)})")
        else:
            st.warning("a = 0 → funkcja stała, brak miejsca zerowego")

        st.divider()
        st.subheader("Funkcja kwadratowa: f(x) = ax² + bx + c")
        col1, col2, col3 = st.columns(3)
        with col1: a = st.slider("a (x²)", -4.0, 4.0, 1.0, 0.5, key="kw_a")
        with col2: b = st.slider("b (x)",  -10.0, 10.0, -2.0, 0.5, key="kw_b")
        with col3: c = st.slider("c",      -10.0, 10.0, -3.0, 0.5, key="kw_c")

        delta = b**2 - 4*a*c
        xw = -b / (2*a) if a != 0 else 0
        yw = a*xw**2 + b*xw + c if a != 0 else c

        fig, ax = plt.subplots(figsize=(8, 4))
        y = a*x**2 + b*x + c
        ax.plot(x, y, "#1a4f8a", lw=2.5,
                label=f"f(x) = {a}x² + ({b})x + ({c})")
        ax.fill_between(x, y, alpha=0.07, color="#1a4f8a")
        ax.axhline(0, color="k", lw=0.8); ax.axvline(0, color="k", lw=0.8)

        if a != 0:
            if delta > 0:
                x1 = (-b - math.sqrt(delta)) / (2*a)
                x2 = (-b + math.sqrt(delta)) / (2*a)
                ax.plot([x1, x2], [0, 0], "ro", markersize=10, zorder=5,
                        label=f"x₁={round(x1,3)}, x₂={round(x2,3)}")
            elif delta == 0:
                ax.plot(xw, 0, "ro", markersize=10, zorder=5,
                        label=f"x₀={round(xw,3)} (podwójny)")
            ax.plot(xw, yw, "g^", markersize=11, zorder=5,
                    label=f"Wierzchołek ({round(xw,3)}, {round(yw,3)})")

        ax.set_ylim(max(y.min()-2, -40), min(y.max()+2, 40))
        ax.set_title(f"Δ = {round(delta,2)}", fontsize=11)
        ax.legend(fontsize=9); ax.grid(True, alpha=0.3)
        st.pyplot(fig); plt.close()

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Δ = b² - 4ac", round(delta, 4))
            st.metric("Wierzchołek xw", round(xw, 4) if a != 0 else "—")
        with col2:
            st.metric("Wierzchołek yw", round(yw, 4) if a != 0 else "—")
            if a != 0:
                if delta > 0:
                    x1 = (-b - math.sqrt(delta))/(2*a)
                    x2 = (-b + math.sqrt(delta))/(2*a)
                    st.metric("Pierwiastki", f"x₁={round(x1,3)}, x₂={round(x2,3)}")
                elif delta == 0:
                    st.metric("Pierwiastek", f"x₀={round(xw,3)}")
                else:
                    st.metric("Pierwiastki", "Brak (Δ<0)")

    # ─────────────────────────────────────────────────────────────
    with tab2:
        _zadania()


def _zadania():
    st.subheader("Zadania")

    # ── ZADANIE 1 ───────────────────────────────────────────────
    with st.expander("📌 Zadanie 1 — Proste  *(2 pkt)*"):
        st.markdown("""
Dla jakiej wartości parametru **m** prosta `y = (m−2)x + 5`
jest rosnąca?
        """)
        if st.button("Pokaż rozwiązanie", key="lin_z1"):
            st.success("""
**Rozwiązanie:**

Prosta f(x) = ax + b jest rosnąca, gdy **a > 0**.

Tu a = m − 2, więc warunek to:

m − 2 > 0  →  **m > 2**

✅ Odpowiedź: m ∈ (2, +∞)
            """)

    # ── ZADANIE 2 ───────────────────────────────────────────────
    with st.expander("📌 Zadanie 2 — Równanie kwadratowe z parametrem  *(4 pkt)*"):
        st.markdown("""
Znajdź wartości parametru **m**, dla których równanie

&nbsp;&nbsp;&nbsp;`x² − 2mx + (m² − m − 6) = 0`

ma **dwa różne pierwiastki rzeczywiste**.
        """)
        if st.button("Pokaż rozwiązanie", key="kw_z2"):
            st.success("""
**Rozwiązanie:**

Warunek dwóch różnych pierwiastków: **Δ > 0**

Δ = (−2m)² − 4·1·(m²−m−6)
  = 4m² − 4m² + 4m + 24
  = **4m + 24**

Δ > 0  →  4m + 24 > 0  →  **m > −6**

✅ Odpowiedź: m ∈ (−6, +∞)
            """)

    # ── ZADANIE 3 ───────────────────────────────────────────────
    with st.expander("📌 Zadanie 3 — Zadanie z kontekstem  *(5 pkt)*"):
        st.markdown("""
Firma produkuje gadżety. Dzienny zysk (w złotych) opisuje wzór:

&nbsp;&nbsp;&nbsp;`P(x) = −2x² + 80x − 600`

gdzie x to liczba wyprodukowanych gadżetów (x ∈ ℕ).

**a)** Ile gadżetów dziennie firma powinna produkować, żeby zysk był największy?

**b)** Jaki jest maksymalny dzienny zysk?

**c)** Przy jakiej produkcji firma wychodzi na zero (zysk = 0)?
        """)
        if st.button("Pokaż rozwiązanie", key="kw_z3"):
            st.success("""
**Rozwiązanie:**

P(x) = −2x² + 80x − 600,  a = −2 < 0 → parabola skierowana w dół → maksimum w wierzchołku

**a)** Wierzchołek:
xw = −b/(2a) = −80/(2·(−2)) = −80/(−4) = **20 gadżetów**

**b)** Maksymalny zysk:
P(20) = −2·400 + 80·20 − 600 = −800 + 1600 − 600 = **200 zł**

**c)** Miejsca zerowe (P(x) = 0):
−2x² + 80x − 600 = 0  | ÷(−2)
x² − 40x + 300 = 0
Δ = 1600 − 1200 = 400
x₁ = (40−20)/2 = **10**,  x₂ = (40+20)/2 = **30**

✅ Firma wychodzi na zero przy produkcji 10 lub 30 gadżetów.
            """)
