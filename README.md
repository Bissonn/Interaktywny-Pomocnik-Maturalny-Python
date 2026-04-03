# Matematyka + Python — Apka edukacyjna

## Pliki

```
matma_app/
├── app.py                  ← główna apka Streamlit
├── codes.json              ← baza kodów dostępu
├── generate_codes.py       ← generuje nowe kody
├── requirements.txt
└── modules/
    ├── m01_rownania.py
    ├── m02_ciagi.py
    ├── m03_funkcje.py
    ├── m04_statystyka.py
    └── m05_optymalizacja.py
```

## Jak wdrożyć (Streamlit Cloud — bezpłatnie)

1. GitHub → nowe **prywatne** repozytorium
2. Wgraj wszystkie pliki
3. share.streamlit.io → "New app" → wskaż `app.py` → Deploy

## Jak generować kody dla kupujących

Po zakupie w Naffy uruchamiasz lokalnie:

```bash
python generate_codes.py        # generuje 1 kod (limit 3 użycia)
python generate_codes.py 5      # generuje 5 kodów
python generate_codes.py 1 5    # 1 kod z limitem 5 użyć
```

Wygenerowany kod wklejasz ręcznie do szablonu maila
potwierdzającego w Naffy (Produkty → Szczegóły → Email z potwierdzeniem).

Potem aktualizujesz codes.json w repozytorium GitHub
(push) — Streamlit Cloud automatycznie przeładuje apkę.

## Jak zmienić limit użyć

W `app.py` linia:
```python
MAX_USES = 3   # ← zmień na 5 jeśli chcesz limit 5 użyć
```

## Uruchomienie lokalne

```bash
pip install -r requirements.txt
streamlit run app.py
```

Kod testowy: `MATURA-DEMO-2025`
