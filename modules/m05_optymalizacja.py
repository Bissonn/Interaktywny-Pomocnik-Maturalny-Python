import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
import math


def pochodna(f, x, h=1e-7):
    return (f(x + h) - f(x - h)) / (2 * h)

def druga_pochodna(f, x, h=1e-5):
    return (f(x + h) - 2*f(x) + f(x - h)) / h**2


def render():
    st.header("🎯 Optymalizacja funkcji")
    st.caption("Pochodna obliczana dynamicznie — działa dla dowolnego wzoru")

    tab1, tab2 = st.tabs(["🎛️ Interaktywny kalkulator", "📝 Zadania"])

    with tab1:
        mode = st.radio("Tryb:", [
            "Pudełko bez wieka (klasyczne zadanie maturalne)",
            "Dowolna funkcja wielomianowa",
            "Optymalizacja zysku"
        ], key="opt_mode")

        if mode.startswith("Pudełko"):
            _pudelko()
        elif mode.startswith("Dowolna"):
            _wielomian()
        else:
            _zysk()

    with tab2:
        _zadania()


def _pudelko():
    st.subheader("Pudełko bez wieka")
    st.markdown("Z kartki A×B wycinasz kwadraty o boku **x** z narożników. "
                "Jakie x daje maksymalną objętość?")

    col1, col2 = st.columns(2)
    with col1: A = st.slider("A — szerokość kartki (cm)", 5, 80, 20, 5, key="pb_A")
    with col2: B = st.slider("B — długość kartki (cm)",   5, 100, 30, 5, key="pb_B")

    x_max = min(A, B) / 2

    def V(x): return x * (A - 2*x) * (B - 2*x)
    def dV(x): return pochodna(V, x)

    cA = 12; cB = -4*(A+B); cC = A*B
    delta = cB**2 - 4*cA*cC

    if delta < 0:
        st.error("Brak ekstremum w dziedzinie rzeczywistej")
        return

    x1 = (-cB - delta**0.5)/(2*cA)
    x2 = (-cB + delta**0.5)/(2*cA)
    kand = [xi for xi in [x1, x2] if 0 < xi < x_max]

    if not kand:
        st.error("Brak optimum w dziedzinie"); return

    x_opt = kand[0]; V_opt = V(x_opt)

    col1, col2, col3 = st.columns(3)
    col1.metric("Optymalna wysokość x*", f"{round(x_opt,4)} cm")
    col2.metric("Maksymalna objętość V*", f"{round(V_opt,3)} cm³")
    col3.metric("Wymiary dna", f"{round(A-2*x_opt,2)} × {round(B-2*x_opt,2)} cm")

    x_arr  = np.linspace(0.01, x_max-0.01, 600)
    V_arr  = V(x_arr)
    dV_arr = np.array([dV(xi) for xi in x_arr])

    fig, ax1 = plt.subplots(figsize=(9, 5))
    ax1.plot(x_arr, V_arr, "#1a4f8a", lw=2.5,
             label=f"V(x) = x·({A}−2x)·({B}−2x)")
    ax1.fill_between(x_arr, V_arr, alpha=0.08, color="#1a4f8a")
    ax1.plot(x_opt, V_opt, "r^", markersize=14, zorder=5,
             label=f"Max: x={round(x_opt,3)}, V={round(V_opt,2)}")
    ax1.axvline(x_opt, color="red", ls=":", lw=1.5, alpha=0.5)
    ax1.set_ylabel("V(x) [cm³]", color="#1a4f8a"); ax1.tick_params(axis='y', labelcolor="#1a4f8a")
    ax1.set_xlabel("x — wysokość pudełka (cm)")

    ax2 = ax1.twinx()
    ax2.plot(x_arr, dV_arr, "#c47a00", lw=2, ls="--", alpha=0.85, label="V′(x) — dynamiczna")
    ax2.axhline(0, color="#c47a00", lw=0.7, alpha=0.4)
    ax2.plot(x_opt, 0, "o", color="#c47a00", markersize=10, zorder=5,
             label=f"V′(x*)≈0")
    ax2.set_ylabel("V′(x)", color="#c47a00"); ax2.tick_params(axis='y', labelcolor="#c47a00")

    l1,lb1 = ax1.get_legend_handles_labels(); l2,lb2 = ax2.get_legend_handles_labels()
    ax1.legend(l1+l2, lb1+lb2, fontsize=9)
    ax1.set_title(f"Pudełko {A}×{B} cm  |  x*={round(x_opt,3)} cm,  V_max={round(V_opt,2)} cm³")
    ax1.grid(True, alpha=0.25)
    st.pyplot(fig); plt.close()

    with st.expander("📐 Rozwiązanie analityczne"):
        st.markdown(f"""
V(x) = x·({A}−2x)·({B}−2x)

**V′(x) = {cA}x² + ({cB})x + {cC}** = 0

Δ = ({cB})² − 4·{cA}·{cC} = **{round(delta,4)}**

x₁ = {round(x1,4)},  x₂ = {round(x2,4)}

{"x₁" if kand[0]==x1 else "x₂"} = {round(x_opt,4)} ∈ (0, {x_max}) ✓  →  **x* = {round(x_opt,4)} cm**

V′(x*) dynamicznie = {dV(x_opt):.2e} ≈ 0 ✓
        """)


def _wielomian():
    st.subheader("Analiza ekstremów dowolnej funkcji")

    col1, col2, col3, col4 = st.columns(4)
    with col1: pa = st.slider("a (x³)", -3.0, 3.0, 1.0, 0.5, key="wp_a")
    with col2: pb = st.slider("b (x²)", -5.0, 5.0,-3.0, 0.5, key="wp_b")
    with col3: pc = st.slider("c (x)",  -9.0, 9.0,-9.0, 0.5, key="wp_c")
    with col4: pd = st.slider("d",      -5.0, 5.0, 2.0, 0.5, key="wp_d")

    col1, col2 = st.columns(2)
    with col1: x_od = st.slider("x od", -10, 0,  -4, 1, key="wp_od")
    with col2: x_do = st.slider("x do",   1, 15,  6, 1, key="wp_do")

    def f(x): return pa*x**3 + pb*x**2 + pc*x + pd

    x_arr  = np.linspace(x_od, x_do, 1000)
    y_arr  = f(x_arr)
    dy_arr = np.array([pochodna(f, xi) for xi in x_arr])

    # Ekstrema
    ekstrema = []
    for i in range(len(dy_arr)-1):
        if dy_arr[i]*dy_arr[i+1] <= 0:
            lo, hi = x_arr[i], x_arr[i+1]
            for _ in range(60):
                m = (lo+hi)/2
                if pochodna(f,lo)*pochodna(f,m) <= 0: hi = m
                else: lo = m
            xe = (lo+hi)/2; ye = f(xe); d2 = druga_pochodna(f, xe)
            typ = "MINIMUM" if d2>0.001 else "MAKSIMUM" if d2<-0.001 else "przegięcie"
            ekstrema.append((xe, ye, d2, typ))

    if ekstrema:
        rows = []
        for xe,ye,d2,typ in ekstrema:
            rows.append({"x": round(xe,4), "f(x)": round(ye,4),
                         "f′′(x)": round(d2,4), "Typ": typ})
        st.dataframe(rows, use_container_width=True)
    else:
        st.info("Brak ekstremów lokalnych w podanym przedziale")

    fig, ax1 = plt.subplots(figsize=(9, 5))
    nazwa = f"f(x) = {pa}x³ + ({pb})x² + ({pc})x + ({pd})"
    ax1.plot(x_arr, y_arr, "#1a4f8a", lw=2.5, label=nazwa)
    ax1.fill_between(x_arr, y_arr, alpha=0.07, color="#1a4f8a")
    ax1.axhline(0, color="k", lw=0.8); ax1.axvline(0, color="k", lw=0.8)
    for xe,ye,d2,typ in ekstrema:
        m = "^" if "MINIMUM" in typ else "v"
        c = "#2d6a2d" if "MINIMUM" in typ else "#991f1f"
        ax1.plot(xe, ye, marker=m, color=c, markersize=13, zorder=5,
                 label=f"{typ}: ({round(xe,3)},{round(ye,3)})")
    ax1.set_ylabel("f(x)", color="#1a4f8a"); ax1.tick_params(axis='y', labelcolor="#1a4f8a")

    ax2 = ax1.twinx()
    ax2.plot(x_arr, dy_arr, "#c47a00", lw=2, ls="--", alpha=0.85, label="f′(x)")
    ax2.axhline(0, color="#c47a00", lw=0.7, alpha=0.4)
    for xe,ye,d2,typ in ekstrema:
        ax2.plot(xe, 0, "o", color="#c47a00", markersize=8, zorder=5)
    ax2.set_ylabel("f′(x)", color="#c47a00"); ax2.tick_params(axis='y', labelcolor="#c47a00")

    l1,lb1=ax1.get_legend_handles_labels(); l2,lb2=ax2.get_legend_handles_labels()
    ax1.legend(l1+l2,lb1+lb2,fontsize=9)
    ax1.set_title(nazwa, fontsize=11); ax1.grid(True, alpha=0.3)
    st.pyplot(fig); plt.close()


def _zysk():
    st.subheader("Optymalizacja zysku / kosztu")

    col1, col2, col3 = st.columns(3)
    with col1: pa = st.slider("a (x²)", -5.0, -0.1, -2.0, 0.1, key="zy_a")
    with col2: pb = st.slider("b (x)",   0.0, 200.0, 80.0, 5.0, key="zy_b")
    with col3: pc = st.slider("c (stały koszt)", -500.0, 0.0, -300.0, 50.0, key="zy_c")

    x_do = st.slider("Maks. produkcja (x do)", 10, 200, 60, 5, key="zy_xdo")

    def P(x): return pa*x**2 + pb*x + pc

    res = minimize_scalar(lambda t: -P(t), bounds=(0.01, x_do-0.01), method="bounded")
    x_opt = res.x; P_opt = P(x_opt)
    dy = pochodna(P, x_opt)

    col1, col2, col3 = st.columns(3)
    col1.metric("Optymalna produkcja x*", round(x_opt, 2))
    col2.metric("Maksymalny zysk P*", f"{round(P_opt, 2)} zł")
    col3.metric("P′(x*)", f"{dy:.2e} ≈ 0")

    x_arr  = np.linspace(0, x_do, 400)
    P_arr  = P(x_arr)
    dP_arr = np.array([pochodna(P, xi) for xi in x_arr])

    fig, ax1 = plt.subplots(figsize=(9, 5))
    ax1.plot(x_arr, P_arr, "#1a4f8a", lw=2.5,
             label=f"P(x) = {pa}x² + {pb}x + ({pc})")
    ax1.fill_between(x_arr, P_arr, alpha=0.08, color="#1a4f8a")
    ax1.plot(x_opt, P_opt, "r^", markersize=14, zorder=5,
             label=f"Max: x={round(x_opt,2)}, P={round(P_opt,2)} zł")
    ax1.axhline(0, color="k", lw=0.8)
    ax1.axvline(x_opt, color="red", ls=":", lw=1.5, alpha=0.6)
    ax1.set_ylabel("P(x) [zł]", color="#1a4f8a"); ax1.tick_params(axis='y', labelcolor="#1a4f8a")
    ax1.set_xlabel("x — produkcja")

    ax2 = ax1.twinx()
    ax2.plot(x_arr, dP_arr, "#c47a00", lw=2, ls="--", alpha=0.85, label="P′(x)")
    ax2.axhline(0, color="#c47a00", lw=0.7, alpha=0.4)
    ax2.plot(x_opt, 0, "o", color="#c47a00", markersize=10, zorder=5)
    ax2.set_ylabel("P′(x)", color="#c47a00"); ax2.tick_params(axis='y', labelcolor="#c47a00")

    l1,lb1=ax1.get_legend_handles_labels(); l2,lb2=ax2.get_legend_handles_labels()
    ax1.legend(l1+l2,lb1+lb2,fontsize=9)
    ax1.set_title(f"Optymalizacja zysku  |  x*={round(x_opt,2)}, P_max={round(P_opt,2)} zł")
    ax1.grid(True, alpha=0.3)
    st.pyplot(fig); plt.close()


def _zadania():
    st.subheader("Zadania")

    with st.expander("📌 Zadanie 1 — Proste  *(3 pkt)*"):
        st.markdown("""
Funkcja f(x) = −x² + 6x − 5.

**a)** Wyznacz współrzędne wierzchołka paraboli.

**b)** Wyznacz maksimum funkcji.

**c)** Dla jakich x funkcja przyjmuje wartości dodatnie?
        """)
        if st.button("Pokaż rozwiązanie", key="opt_z1"):
            st.success("""
**Rozwiązanie:**

f(x) = −x² + 6x − 5,  a=−1, b=6, c=−5

**a)** Wierzchołek:
xw = −b/(2a) = −6/(−2) = **3**
yw = f(3) = −9 + 18 − 5 = **4**
Wierzchołek: **(3, 4)**

**b)** a = −1 < 0 → parabola skierowana w dół
→ wierzchołek to **maksimum**
f_max = **4** dla x = 3

**c)** f(x) > 0 między miejscami zerowymi:
Δ = 36−20 = 16,  x₁=1, x₂=5
f(x) > 0 dla **x ∈ (1, 5)**

✅ Wierzchołek (3,4), f_max=4, f>0 dla x∈(1,5)
            """)

    with st.expander("📌 Zadanie 2 — Pudełko  *(5 pkt)*"):
        st.markdown("""
Z kwadratowego kawałka blachy o boku **24 cm** wycinamy
jednakowe kwadraciki z narożników i zginamy boki,
tworząc pudełko bez wieka.

Wyznacz wymiary pudełka o **największej objętości**.
        """)
        if st.button("Pokaż rozwiązanie", key="opt_z2"):
            st.success("""
**Rozwiązanie:**

Niech x = bok wyciętego kwadracika (cm)
Dziedzina: x ∈ (0, 12)

V(x) = x·(24−2x)·(24−2x) = x·(24−2x)²

V′(x) = (24−2x)² + x·2(24−2x)·(−2)
       = (24−2x)[(24−2x) − 4x]
       = (24−2x)(24−6x)

V′(x) = 0:
24−2x = 0 → x = 12 (poza dziedziną)
24−6x = 0 → **x = 4** ✓

Sprawdzenie: V′′(4) < 0 → maksimum ✓

**Wymiary pudełka:**
- Podstawa: 24−2·4 = **16 cm × 16 cm**
- Wysokość: **4 cm**

V = 4·16·16 = **1024 cm³**

✅ Pudełko 16×16×4 cm, V_max = 1024 cm³
            """)

    with st.expander("📌 Zadanie 3 — Z kontekstem  *(6 pkt)*"):
        st.markdown("""
Rolnik ma **120 m** siatki i chce ogrodzić prostokątną działkę,
przy czym jedna strona działki to ściana stodoły (nie wymaga ogrodzenia).

Jakie wymiary powinna mieć działka, żeby miała **największą powierzchnię**?
        """)
        if st.button("Pokaż rozwiązanie", key="opt_z3"):
            st.success("""
**Rozwiązanie:**

Niech x = długość boków prostopadłych do stodoły
Trzecia strona (równoległa do stodoły): y = 120 − 2x
Dziedzina: x ∈ (0, 60)

Pole: **P(x) = x·(120−2x) = 120x − 2x²**

P′(x) = 120 − 4x = 0
**x = 30 m**

P′′(x) = −4 < 0 → maksimum ✓

y = 120 − 2·30 = **60 m**

P_max = 30·60 = **1800 m²**

✅ Wymiary: 30 m × 60 m, pole = 1800 m²
(ściana stodoły = strona 60 m)
            """)
