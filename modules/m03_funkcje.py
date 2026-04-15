import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def render():
    st.header("📈 Funkcje i wykresy")

    tab1, tab2 = st.tabs(["🎛️ Interaktywny kalkulator", "📝 Zadania"])

    with tab1:
        fn_type = st.selectbox("Typ funkcji:", [
            "Trygonometryczna: A·sin(Bx + C) + D",
            "Wykładnicza: a · qˣ",
            "Logarytmiczna: log_a(x)",
            "Sześcienna: ax³ + bx² + cx + d",
        ], key="fn_type")

        x = np.linspace(-4*np.pi, 4*np.pi, 1000)

        if fn_type.startswith("Trygonometryczna"):
            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)
            with col1: A = st.slider("A (amplituda)",   -3.0, 3.0, 1.0, 0.25, key="tA")
            with col2: B = st.slider("B (okres: 2π/B)", -4.0, 4.0, 1.0, 0.25, key="tB")
            with col3: C = st.slider("C (przesunięcie)", -np.pi, np.pi, 0.0,
                                     float(np.pi/6), key="tC",
                                     format="%.2f")
            with col4: D = st.slider("D (przesunięcie pionowe)", -3.0, 3.0, 0.0, 0.25, key="tD")

            x_plot = np.linspace(-2*np.pi, 2*np.pi, 800)
            y_sin  = A * np.sin(B*x_plot + C) + D
            y_cos  = A * np.cos(B*x_plot + C) + D

            fig, ax = plt.subplots(figsize=(9, 4))
            ax.plot(x_plot, y_sin, "#1a4f8a", lw=2.5,
                    label=f"{A}·sin({B}x + {round(C,2)}) + {D}")
            ax.plot(x_plot, y_cos, "#991f1f", lw=2, ls="--",
                    label=f"{A}·cos({B}x + {round(C,2)}) + {D}")
            ax.axhline(0, color="k", lw=0.8); ax.axvline(0, color="k", lw=0.8)
            ax.axhline(D, color="gray", lw=0.6, ls=":")
            ax.set_xticks([-2*np.pi, -np.pi, 0, np.pi, 2*np.pi])
            ax.set_xticklabels(["-2π", "-π", "0", "π", "2π"])
            ax.legend(fontsize=9); ax.grid(True, alpha=0.3)
            st.pyplot(fig); plt.close()

            if B != 0:
                okres = round(2*np.pi / abs(B), 4)
                col1, col2, col3 = st.columns(3)
                col1.metric("Amplituda |A|", abs(A))
                col2.metric("Okres T = 2π/|B|", okres)
                col3.metric("Przesunięcie pionowe D", D)

        elif fn_type.startswith("Wykładnicza"):
            col1, col2 = st.columns(2)
            with col1: a_exp = st.slider("a (współczynnik)", -5.0, 5.0, 1.0, 0.5, key="ea")
            with col2: q_exp = st.slider("q (podstawa, q>0, q≠1)", 0.1, 5.0, 2.0, 0.1, key="eq")

            x_plot = np.linspace(-3, 3, 400)
            if q_exp > 0 and q_exp != 1:
                y = a_exp * q_exp**x_plot
                fig, ax = plt.subplots(figsize=(9, 4))
                ax.plot(x_plot, y, "#1a4f8a", lw=2.5,
                        label=f"f(x) = {a_exp}·{q_exp}ˣ")
                ax.axhline(0, color="k", lw=0.8); ax.axvline(0, color="k", lw=0.8)
                ax.set_ylim(-10, 20)
                ax.legend(); ax.grid(True, alpha=0.3)
                st.pyplot(fig); plt.close()
                trend = "rosnąca" if q_exp > 1 else "malejąca"
                st.info(f"q = {q_exp} {'> 1' if q_exp>1 else '< 1'} → funkcja **{trend}**  |  "
                        f"Dziedzina: ℝ  |  Zbiór wartości: (0, +∞) gdy a>0")
            else:
                st.warning("Podstawa q musi być > 0 i ≠ 1")

        elif fn_type.startswith("Logarytmiczna"):
            base = st.slider("Podstawa a (a>0, a≠1)", 0.1, 10.0, 2.0, 0.1, key="lb")
            x_plot = np.linspace(0.01, 6, 400)
            if base > 0 and base != 1:
                y = np.log(x_plot) / np.log(base)
                fig, ax = plt.subplots(figsize=(9, 4))
                ax.plot(x_plot, y, "#1a4f8a", lw=2.5, label=f"f(x) = log_{base}(x)")
                ax.axhline(0, color="k", lw=0.8); ax.axvline(0, color="k", lw=0.8)
                ax.axvline(1, color="green", lw=1, ls=":", alpha=0.7,
                           label="f(1) = 0 zawsze")
                ax.set_ylim(-3, 4)
                ax.legend(); ax.grid(True, alpha=0.3)
                st.pyplot(fig); plt.close()
                trend = "rosnąca" if base > 1 else "malejąca"
                st.info(f"a = {base} → funkcja **{trend}**  |  "
                        f"Dziedzina: (0, +∞)  |  Zbiór wartości: ℝ  |  "
                        f"log_{base}(1) = 0  |  log_{base}({base}) = 1")

        else:  # Sześcienna
            col1, col2, col3 = st.columns(4)
            with col1: a3 = st.slider("a (x³)", -3.0, 3.0, 1.0, 0.5, key="s3a")
            with col2: b3 = st.slider("b (x²)", -3.0, 3.0, 1.0, 0.5, key="s3b")
            with col3: c3 = st.slider("c (x)",  -5.0, 5.0,-3.0, 0.5, key="s3c")
            with col4: d3 = st.slider("d",      -5.0, 5.0, 0.0, 0.5, key="s3d")

            x_plot = np.linspace(-4, 4, 500)
            y = a3*x_plot**3 + b3*x_plot**2 + c3*x_plot + d3
            fig, ax = plt.subplots(figsize=(9, 4))
            ax.plot(x_plot, y, "#1a4f8a", lw=2.5,
                    label=f"f(x) = {a3}x³ + {b3}x² + {c3}x + {d3}")
            ax.axhline(0, color="k", lw=0.8); ax.axvline(0, color="k", lw=0.8)
            ax.set_ylim(-20, 20)
            ax.legend(); ax.grid(True, alpha=0.3)
            st.pyplot(fig); plt.close()

    with tab2:
        _zadania()


def _zadania():
    st.subheader("Zadania")

    with st.expander("📌 Zadanie 1 — Proste  *(2 pkt)*"):
        st.markdown("""
Funkcja f(x) = 3·sin(2x) ma okres T = ?

Wyznacz **amplitudę** i **okres** tej funkcji.
        """)
        if st.button("Pokaż rozwiązanie", key="fn_z1"):
            st.success("""
**Rozwiązanie:**

f(x) = A·sin(B·x),  gdzie A = 3, B = 2

**Amplituda:** |A| = **3**
(funkcja przyjmuje wartości od −3 do 3)

**Okres:** T = 2π/|B| = 2π/2 = **π**
(po przejściu odcinka długości π funkcja powtarza się)

✅ Amplituda = 3,  Okres = π ≈ 3,14
            """)

    with st.expander("📌 Zadanie 2 — Wykresy i transformacje  *(4 pkt)*"):
        st.markdown("""
Dany jest wykres funkcji **f(x) = 2ˣ**.

**a)** Narysuj (opisz) wykres funkcji g(x) = 2ˣ⁺¹ − 3.

**b)** Podaj dziedzinę i zbiór wartości funkcji g.

**c)** Czy funkcja g jest rosnąca czy malejąca? Uzasadnij.
        """)
        if st.button("Pokaż rozwiązanie", key="fn_z2"):
            st.success("""
**Rozwiązanie:**

g(x) = 2^(x+1) − 3 = 2·2ˣ − 3

**a)** Wykres g powstaje z wykresu f przez:
- Przesunięcie o 1 w lewo ("+1" przy x)
- Przesunięcie o 3 w dół ("−3")

Punkt (0,1) na f → (−1, −2) na g
Punkt (1,2) na f → (0, 1) na g
Asymptota pozioma: y = −3 (zamiast y = 0)

**b)** Dziedzina: **ℝ** (wszystkie liczby rzeczywiste)
Zbiór wartości: **(−3, +∞)**
(nigdy nie osiąga −3, bo 2^(x+1) > 0 zawsze)

**c)** **Rosnąca** — bo podstawa 2 > 1, a funkcja wykładnicza
z podstawą > 1 jest zawsze rosnąca. Przesunięcia nie
zmieniają monotoniczności.

✅ Dziedzina: ℝ,  ZW: (−3,+∞),  funkcja rosnąca
            """)

    with st.expander("📌 Zadanie 3 — Z kontekstem  *(5 pkt)*"):
        st.markdown("""
Temperatura powietrza w pewnym mieście w ciągu doby
opisuje funkcja:

&nbsp;&nbsp;&nbsp;**T(t) = −8·cos(πt/12) + 10**

gdzie t to czas w godzinach (t = 0 oznacza północ).

**a)** Jaka jest temperatura o północy (t = 0)?

**b)** O której godzinie temperatura jest najwyższa i ile wynosi?

**c)** Jaka jest amplituda i okres tej funkcji?
        """)
        if st.button("Pokaż rozwiązanie", key="fn_z3"):
            st.success("""
**Rozwiązanie:**

T(t) = −8·cos(πt/12) + 10

**a)** T(0) = −8·cos(0) + 10 = −8·1 + 10 = **2°C**

**b)** Maksimum cos = 1, ale jest minus, więc minimum cos daje maksimum T.
cos(πt/12) = −1  →  πt/12 = π  →  t = 12

T(12) = −8·(−1) + 10 = 8 + 10 = **18°C o godzinie 12:00 (południe)**

**c)** Amplituda: |A| = |−8| = **8°C**
(temperatura waha się o 8 stopni od wartości środkowej 10°C)

Okres: T = 2π / (π/12) = 2π · 12/π = **24 godziny** ✓
(pełny cykl doby — zgodnie z intuicją)

✅ O północy 2°C, maksimum 18°C o południu,
   amplituda 8°C, okres 24h
            """)
