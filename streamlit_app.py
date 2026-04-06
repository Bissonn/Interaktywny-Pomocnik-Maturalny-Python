import streamlit as st
import json, os, sys

# Ustawienie ścieżki dla modułów
sys.path.insert(0, os.path.dirname(__file__))
from modules import m01_rownania, m02_ciagi, m03_funkcje, m04_statystyka, m05_optymalizacja

# Konfiguracja strony
st.set_page_config(
    page_title="Matematyka + Python | Matura",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Stylizacja UI
st.markdown("""
<style>
  #MainMenu, footer, header { visibility: hidden; }
  [data-testid="metric-container"] {
    background: #f7f4ee; border: 1px solid #d8d2c8;
    border-radius: 8px; padding: 0.5rem 1rem;
  }
  .app-header {
    background: linear-gradient(135deg, #0f0e0c 0%, #1a2a3a 100%);
    padding: 1.2rem 1.8rem; border-radius: 10px;
    margin-bottom: 1.2rem; border-left: 4px solid #c47a00;
  }
  .app-header h1 { color: white; font-size: 1.5rem; margin: 0 0 0.2rem; }
  .app-header p  { color: #8a9db5; margin: 0; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)

# ── LOGIKA KODÓW (ZUNIFIKOWANA) ───────────────────────────────

def load_codes_from_secrets():
    """Pobiera bazę kodów z Sejfu (Secrets)"""
    try:
        if "my_codes" in st.secrets:
            return json.loads(st.secrets["my_codes"])
        return {}
    except Exception:
        return {}

# Inicjalizacja bazy w pamięci sesji (żeby nie uderzać w Secrets co kliknięcie)
if "codes_db" not in st.session_state:
    st.session_state.codes_db = load_codes_from_secrets()

def verify_and_use(code: str) -> tuple[bool, str]:
    """
    Główna funkcja weryfikacji. 
    Zwraca (czy_ok, komunikat_lub_pozostale_proby).
    """
    code = code.strip().upper()
    db = st.session_state.codes_db

    if code not in db:
        return False, "❌ Nieprawidłowy kod dostępu."

    entry = db[code]
    uses = entry.get("uses", 0)
    max_uses = entry.get("max_uses", 13)

    if uses >= max_uses:
        return False, f"⚠️ Kod wygasł. Osiągnięto limit {max_uses} użyć."

    # Zwiększamy licznik w pamięci bieżącej sesji
    entry["uses"] = uses + 1
    remaining = max_uses - entry["uses"]
    
    return True, f"ok|{remaining}"

# ── Session state ─────────────────────────────────────────────
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_code" not in st.session_state: st.session_state.user_code = ""
if "remaining" not in st.session_state: st.session_state.remaining = 0

# ══════════════════════════════════════════════════════════════
# EKRAN LOGOWANIA
# ══════════════════════════════════════════════════════════════
def show_login():
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown("""
<div style="text-align:center; padding: 2rem 0 1.5rem;">
  <div style="font-size:3rem;">🧮</div>
  <h2 style="margin:.5rem 0 .2rem;">Matematyka + Python</h2>
  <p style="color:#6b6660;font-size:.9rem;">Matura rozszerzona 2025/2026</p>
</div>
""", unsafe_allow_html=True)

        st.markdown("#### Wpisz kod dostępu")
        st.caption("Kod otrzymałeś/aś w mailu po zakupie — format: **MATURA-XXXX-XXXX**")

        code_input = st.text_input(
            "Kod dostępu",
            placeholder="MATURA-XXXX-XXXX",
            max_chars=20,
            key="li_code",
            label_visibility="collapsed",
        ).strip().upper()

        if st.button("🔓 Wejdź", type="primary", use_container_width=True):
            if not code_input:
                st.warning("Wpisz kod dostępu.")
                return

            ok, msg = verify_and_use(code_input)

            if not ok:
                st.error(msg)
            else:
                # Rozdzielamy komunikat "ok|X"
                remaining_val = int(msg.split("|")[1])
                st.session_state.logged_in = True
                st.session_state.user_code = code_input
                st.session_state.remaining = remaining_val
                st.rerun()

        st.divider()
        st.markdown("""
<div style="text-align:center;font-size:.8rem;color:#8a9db5;">
  Nie masz kodu? <a href="http://bit.ly/4bUgTGn" target="_blank">Kup dostęp →</a>
  &nbsp;·&nbsp;
  Problemy? Napisz na DM
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# GŁÓWNA APKA
# ══════════════════════════════════════════════════════════════
def show_app():
    remaining = st.session_state.remaining
    code      = st.session_state.user_code

    st.markdown(f"""
<div class="app-header">
  <h1>🧮 Matematyka Rozszerzona + Python</h1>
  <p>Kod: {code} &nbsp;·&nbsp;
     Pozostałe logowania z tego kodu: <strong>{remaining}</strong>
     &nbsp;·&nbsp; Matura 2025/2026</p>
</div>
""", unsafe_allow_html=True)

    if remaining == 0:
        st.warning("ℹ️ To było ostatnie logowanie tym kodem.")
    elif remaining == 1:
        st.info(f"ℹ️ Zostało jeszcze **1 logowanie** tym kodem.")

    with st.sidebar:
        st.markdown("### 📚 Nawigacja")
        page = st.radio(
            "Wybierz temat:",
            [
                "📐 01 — Funkcje liniowe i kwadratowe",
                "🔢 02 — Ciągi",
                "📈 03 — Funkcje i wykresy",
                "📊 04 — Statystyka",
                "🎯 05 — Optymalizacja",
            ],
            label_visibility="collapsed",
            key="nav",
        )
        st.divider()
        if st.button("🚪 Wyloguj", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_code = ""
            st.session_state.remaining = 0
            st.rerun()

    if   page.startswith("📐"): m01_rownania.render()
    elif page.startswith("🔢"): m02_ciagi.render()
    elif page.startswith("📈"): m03_funkcje.render()
    elif page.startswith("📊"): m04_statystyka.render()
    elif page.startswith("🎯"): m05_optymalizacja.render()

# ── Entry point ───────────────────────────────────────────────
if st.session_state.logged_in:
    show_app()
else:
    show_login()
