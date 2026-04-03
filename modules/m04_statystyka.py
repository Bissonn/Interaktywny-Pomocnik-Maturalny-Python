import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import statistics
import math


def render():
    st.header("📊 Statystyka opisowa")

    tab1, tab2 = st.tabs(["🎛️ Interaktywny kalkulator", "📝 Zadania"])

    with tab1:
        st.subheader("Wpisz dane i oblicz miary statystyczne")

        dane_str = st.text_area(
            "Dane (oddzielone przecinkami):",
            value="45, 62, 71, 58, 83, 77, 69, 54, 80, 66, 72, 91, 55, 78, 64",
            height=80,
            key="stat_dane"
        )

        try:
            dane = [float(x.strip()) for x in dane_str.split(",") if x.strip()]
            if len(dane) < 2:
                st.warning("Wpisz co najmniej 2 liczby"); return
        except ValueError:
            st.error("Błąd: wpisz liczby oddzielone przecinkami"); return

        dane_sort = sorted(dane)
        n = len(dane)
        sr    = sum(dane) / n
        med   = statistics.median(dane)
        war   = sum((x-sr)**2 for x in dane) / n
        odch  = math.sqrt(war)
        q1    = np.percentile(dane, 25)
        q3    = np.percentile(dane, 75)
        rozst = max(dane) - min(dane)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Średnia x̄", round(sr, 4))
        col2.metric("Mediana Me", round(med, 4))
        col3.metric("Odch. std. s", round(odch, 4))
        col4.metric("Wariancja s²", round(war, 4))

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Min", round(min(dane), 2))
        col2.metric("Max", round(max(dane), 2))
        col3.metric("Rozstęp", round(rozst, 2))
        col4.metric("n", n)

        bins_n = st.slider("Liczba przedziałów histogramu", 3, 15, 6, 1, key="stat_bins")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))

        ax1.hist(dane, bins=bins_n, color="steelblue", edgecolor="white", alpha=0.85)
        ax1.axvline(sr,  color="red",   lw=2.5, ls="--", label=f"Średnia={round(sr,2)}")
        ax1.axvline(med, color="green", lw=2.5, ls=":",  label=f"Mediana={round(med,2)}")
        ax1.set_title(f"Histogram (bins={bins_n})"); ax1.legend(fontsize=9)
        ax1.set_xlabel("Wartość"); ax1.set_ylabel("Liczba")

        bp = ax2.boxplot(dane, vert=True, patch_artist=True,
                         boxprops=dict(facecolor="lightblue", color="navy"),
                         medianprops=dict(color="red", lw=2.5),
                         whiskerprops=dict(color="navy"),
                         capprops=dict(color="navy"))
        ax2.set_title("Wykres pudełkowy"); ax2.set_ylabel("Wartość")
        for val, lbl in [(q1,"Q1"), (med,"Me"), (q3,"Q3")]:
            ax2.annotate(f"{lbl}={round(val,1)}", xy=(1.06, val),
                         fontsize=9, color="navy")

        plt.tight_layout()
        st.pyplot(fig); plt.close()

        with st.expander("📐 Szczegółowe obliczenia krok po kroku"):
            st.markdown(f"""
**n = {n}**  
Dane posortowane: {dane_sort}

**Średnia:**  
x̄ = ({" + ".join(str(round(x,1)) for x in dane[:5])}{"..." if n>5 else ""}) / {n} = **{round(sr,4)}**

**Mediana:**  
{"Środkowy element (pozycja " + str(n//2+1) + "): " + str(med) if n%2==1
  else "Średnia dwóch środkowych: (" + str(dane_sort[n//2-1]) + "+" + str(dane_sort[n//2]) + ")/2 = " + str(round(med,4))}

**Wariancja:**  
s² = Σ(xᵢ − x̄)² / n = **{round(war,4)}**

**Odchylenie standardowe:**  
s = √s² = √{round(war,4)} = **{round(odch,4)}**

**Kwartyle:**  Q1 = {round(q1,2)},  Q3 = {round(q3,2)},  IQR = {round(q3-q1,2)}
            """)

    with tab2:
        _zadania()


def _zadania():
    st.subheader("Zadania")

    with st.expander("📌 Zadanie 1 — Proste  *(3 pkt)*"):
        st.markdown("""
W klasie 10 uczniów napisało kartkówkę. Wyniki (punkty):

**4, 7, 5, 9, 6, 8, 7, 5, 10, 7**

Oblicz: **średnią arytmetyczną**, **medianę** i **odchylenie standardowe**.
        """)
        if st.button("Pokaż rozwiązanie", key="stat_z1"):
            dane = [4,7,5,9,6,8,7,5,10,7]
            sr = sum(dane)/len(dane)
            sor = sorted(dane)
            med = (sor[4]+sor[5])/2
            war = sum((x-sr)**2 for x in dane)/len(dane)
            odch = math.sqrt(war)
            st.success(f"""
**Rozwiązanie:**

Dane: {sorted(dane)}  (n = {len(dane)})

**Średnia:**
x̄ = ({'+'.join(map(str,dane))}) / 10 = {sum(dane)}/10 = **{sr}**

**Mediana** (n=10, parzyste → średnia 5. i 6. wyrazu):
Posortowane: {sor}
Me = ({sor[4]} + {sor[5]}) / 2 = **{med}**

**Wariancja:**
s² = Σ(xᵢ − {sr})² / 10 = {round(war,4)}

**Odchylenie standardowe:**
s = √{round(war,4)} = **{round(odch,4)}**

✅ Średnia = {sr},  Mediana = {med},  s = {round(odch,4)}
            """)

    with st.expander("📌 Zadanie 2 — Interpretacja  *(4 pkt)*"):
        st.markdown("""
Dwie drużyny piłkarskie strzeliły w sezonie tyle samo bramek (średnia = 2 gole/mecz).
Drużyna A ma odchylenie standardowe **s = 0,4**, drużyna B ma **s = 2,1**.

**a)** Która drużyna jest bardziej "przewidywalna"?

**b)** Co duże odchylenie standardowe oznacza w kontekście bramek?

**c)** Która drużyna jest bardziej ryzykowna jako kandydat do tytułu?
        """)
        if st.button("Pokaż rozwiązanie", key="stat_z2"):
            st.success("""
**Rozwiązanie:**

**a)** Drużyna **A** jest bardziej przewidywalna.
Małe odchylenie (s=0,4) oznacza że wyniki są skupione
blisko średniej — drużyna regularnie strzela ok. 2 bramki.

**b)** Duże odchylenie (s=2,1 dla drużyny B) oznacza
że wyniki są bardzo zróżnicowane — raz 0 bramek,
raz 5 bramek. Duże wahania formy.

**c)** Drużyna B jest **bardziej ryzykowna** — może wygrać
wysoko, ale może też dostać "klapę". Do tytułu potrzeba
stabilności, więc drużyna A jest lepszym kandydatem
przy tej samej średniej.

✅ s małe = stabilna · s duże = niestabilna, ryzykowna
            """)

    with st.expander("📌 Zadanie 3 — Z kontekstem  *(5 pkt)*"):
        st.markdown("""
Apteka zmierzyła temperaturę 20 losowych pacjentów (°C):

36.6, 37.2, 36.8, 38.1, 36.5, 37.0, 36.9, 38.4, 36.7, 37.3,
36.8, 37.8, 36.4, 37.1, 38.9, 36.6, 37.2, 36.8, 37.5, 36.9

**a)** Oblicz średnią i odchylenie standardowe.

**b)** Ilu pacjentów ma temperaturę w przedziale (x̄ − s, x̄ + s)?

**c)** Czy wynik b) jest zgodny z regułą 68% dla rozkładu normalnego?
        """)
        if st.button("Pokaż rozwiązanie", key="stat_z3"):
            dane = [36.6,37.2,36.8,38.1,36.5,37.0,36.9,38.4,36.7,37.3,
                    36.8,37.8,36.4,37.1,38.9,36.6,37.2,36.8,37.5,36.9]
            n = len(dane)
            sr = sum(dane)/n
            war = sum((x-sr)**2 for x in dane)/n
            odch = math.sqrt(war)
            w_przedziale = [x for x in dane if sr-odch < x < sr+odch]
            st.success(f"""
**Rozwiązanie:**

n = {n},  Suma = {round(sum(dane),1)}

**a)**
Średnia: x̄ = {round(sum(dane),1)}/{n} = **{round(sr,4)}°C**
Wariancja: s² = {round(war,4)}
Odchylenie: s = **{round(odch,4)}°C**

**b)** Przedział (x̄−s, x̄+s) = ({round(sr-odch,4)}, {round(sr+odch,4)})

Pacjenci w przedziale: {sorted(w_przedziale)}
Liczba: **{len(w_przedziale)} z {n}** = {round(len(w_przedziale)/n*100,1)}%

**c)** Reguła 68% mówi że dla rozkładu normalnego
ok. 68% obserwacji leży w przedziale (x̄−s, x̄+s).

Wynik: {round(len(w_przedziale)/n*100,1)}% — {"✅ zgodny z regułą 68%" if abs(len(w_przedziale)/n - 0.68) < 0.15 else "⚠️ odchylenie od reguły 68% (mała próba)"}

Przy n=20 normalne są odchylenia — reguła działa
dokładnie dla dużych prób.
            """)
