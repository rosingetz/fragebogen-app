import streamlit as st
import plotly.graph_objects as go
import json
from datetime import datetime

from questions import QUESTIONS, CATEGORIES, LIKERT_LABELS
from database import init_db, save_vorarbeiter, save_bewerber, get_all_vorarbeiter, get_all_bewerber, delete_vorarbeiter, delete_bewerber, reset_all
from scoring import calculate_personal_scores, compute_benchmark, compute_match
from pdf_report import generate_pdf

st.set_page_config(
    page_title="Mitarbeiter-Assessment Vorarbeiter",
    page_icon="📋",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main > div { padding-top: 2rem; }
    .stRadio > label { font-weight: 600; }
    .block-container { max-width: 800px; }
    div[data-testid="stExpander"] div[role="button"] p { font-size: 1.1rem; }
</style>
""", unsafe_allow_html=True)

init_db()

if "page" not in st.session_state:
    st.session_state.page = "role_select"
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "show_admin" not in st.session_state:
    st.session_state.show_admin = False

st.title("👷 Mitarbeiter-Assessment Vorarbeiter")
st.markdown("Erfassung von Soft Skills und Verhaltensmustern im gewerblich-technischen Bereich")

st.sidebar.markdown("## Navigation")

if st.sidebar.button("🔄 Neustart"):
    for key in ["page", "answers", "role"]:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.page = "role_select"
    st.rerun()

st.sidebar.divider()
with st.sidebar.expander("⚙️ Admin-Bereich", expanded=False):
    vor_data = get_all_vorarbeiter()
    bew_data = get_all_bewerber()
    st.markdown(f"**Vorarbeiter-Datensätze:** {len(vor_data)}")
    st.markdown(f"**Bewerber-Datensätze:** {len(bew_data)}")

    if vor_data:
        st.markdown("### Vorarbeiter-Daten")
        for r in vor_data:
            col1, col2 = st.columns([3, 1])
            col1.markdown(f"`#{r['id']}` {r['profile_name'] or 'unbenannt'} – {r['timestamp']}")
            if col2.button("🗑️", key=f"del_v_{r['id']}"):
                delete_vorarbeiter(r["id"])
                st.rerun()

    if bew_data:
        st.markdown("### Bewerber-Daten")
        for r in bew_data[:10]:
            col1, col2 = st.columns([3, 1])
            col1.markdown(f"`#{r['id']}` – {r['timestamp']}")
            if col2.button("🗑️", key=f"del_b_{r['id']}"):
                delete_bewerber(r["id"])
                st.rerun()

    if vor_data or bew_data:
        if st.button("⚠️ Alle Daten löschen", type="secondary"):
            reset_all()
            st.rerun()

    export_all = {}
    if vor_data:
        export_all["vorarbeiter"] = [dict(r) for r in vor_data]
    if bew_data:
        export_all["bewerber"] = [dict(r) for r in bew_data]
    if export_all:
        st.download_button(
            label="📥 Daten exportieren (JSON)",
            data=json.dumps(export_all, indent=2, ensure_ascii=False),
            file_name="assessment_export.json",
            mime="application/json",
        )


role = st.radio(
    "Rolle auswählen:",
    ["Bestands-Vorarbeiter", "Bewerber"],
    horizontal=True,
    key="role",
    on_change=lambda: setattr(st.session_state, "page", "role_select"),
)

st.divider()

if st.session_state.get("page") == "role_select":
    st.session_state.answers = {}

profile_name = ""
if role == "Bestands-Vorarbeiter":
    profile_name = st.text_input(
        "Name / Kürzel (optional, z. B. für spätere Zuordnung):",
        placeholder="z. B. 'Hans Meier' oder 'HM'",
    )

answers = {}
with st.form(key="questionnaire"):
    for cat in CATEGORIES:
        st.subheader(cat)
        cat_questions = [q for q in QUESTIONS if q["category"] == cat]
        for q in cat_questions:
            val = st.radio(
                q["text"],
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: f"{x} – {LIKERT_LABELS[x]}",
                key=f"q_{q['id']}",
                horizontal=True,
                index=2,
            )
            answers[str(q["id"])] = val
        st.markdown("---")

    submitted = st.form_submit_button(
        "Als Vorarbeiter speichern" if role == "Bestands-Vorarbeiter" else "Auswertung anzeigen",
        use_container_width=True,
        type="primary",
    )

if submitted:
    st.session_state.answers = answers
    bench = compute_benchmark(get_all_vorarbeiter())

    if role == "Bestands-Vorarbeiter":
        save_vorarbeiter(answers, profile_name)
        new_count = len(get_all_vorarbeiter())
        st.success(f"✅ Daten gespeichert! Vielen Dank. (Datensatz #{new_count})")
        st.balloons()
        scores = calculate_personal_scores(answers)
        bench = compute_benchmark(get_all_vorarbeiter()) or scores
        overall, per_domain = compute_match(scores, bench)
        pdf_bytes = generate_pdf(scores, bench, overall or 100, per_domain or {c: 100 for c in CATEGORIES}, answers)
        filename = f"Vorarbeiter_{profile_name or new_count}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        st.download_button("📄 PDF speichern", data=pdf_bytes, file_name=filename, mime="application/pdf", use_container_width=True)

    else:
        if not bench or len(get_all_vorarbeiter()) < 2:
            st.warning(
                "⚠️ Es liegen noch zu wenige Vorarbeiter-Daten vor, um einen aussagekräftigen "
                "Vergleich zu erstellen. (Mindestens 2 Datensätze erforderlich)"
            )
        else:
            save_bewerber(answers)
            scores = calculate_personal_scores(answers)
            overall, per_domain = compute_match(scores, bench)

            st.divider()
            st.header("📊 Auswertung")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Gesamt-Übereinstimmung", f"{overall}%")
            with col2:
                max_cat = max(per_domain, key=per_domain.get)
                st.metric("Stärkste Kategorie", max_cat.split("&")[0].strip(), f"{per_domain[max_cat]}%")
            with col3:
                min_cat = min(per_domain, key=per_domain.get)
                st.metric("Entwicklungspotenzial", min_cat.split("&")[0].strip(), f"{per_domain[min_cat]}%")

            st.divider()

            cats_list = list(CATEGORIES.keys())
            bewerber_vals = [scores[cat] for cat in cats_list]
            benchmark_vals = [bench[cat] for cat in cats_list]

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=bewerber_vals + [bewerber_vals[0]],
                theta=cats_list + [cats_list[0]],
                fill="toself",
                name="Bewerber",
                line_color="#1f77b4",
                opacity=0.7,
            ))
            fig.add_trace(go.Scatterpolar(
                r=benchmark_vals + [benchmark_vals[0]],
                theta=cats_list + [cats_list[0]],
                fill="toself",
                name="Vorarbeiter-Benchmark",
                line_color="#ff7f0e",
                opacity=0.5,
                line_dash="dash",
            ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[1, 5],
                                    tickvals=[1, 2, 3, 4, 5],
                                    ticktext=["1", "2", "3", "4", "5"]),
                ),
                title="Vergleich: Bewerber vs. Vorarbeiter-Profil",
                height=500,
                margin=dict(t=60, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2),
            )
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Detail-Ergebnis pro Kategorie")
            col_left, col_right = st.columns([1, 1])
            with col_left:
                for cat in CATEGORIES:
                    pct = per_domain[cat]
                    color = "🟢" if pct >= 80 else "🟡" if pct >= 60 else "🔴"
                    st.markdown(f"{color} **{cat}:** {pct}%")
            with col_right:
                st.markdown("**Legende:**")
                st.markdown("🟢 ≥ 80% — Starke Übereinstimmung")
                st.markdown("🟡 60–79% — Leichte Abweichung")
                st.markdown("🔴 < 60% — Entwicklungsbereich")

            st.divider()
            st.subheader("Profil im Detail")
            with st.expander("Alle Frage-Antworten anzeigen"):
                for q in QUESTIONS:
                    val = int(answers.get(str(q["id"]), 3))
                    label = LIKERT_LABELS[val]
                    st.markdown(f"**{q['id']}.** {q['text']}")
                    st.markdown(f"→ *{label}*")
                    st.progress((val - 1) / 4)

            st.divider()
            pdf_bytes = generate_pdf(scores, bench, overall, per_domain, answers)
            filename = f"Bewerber_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
            st.download_button("📄 PDF speichern", data=pdf_bytes, file_name=filename, mime="application/pdf", use_container_width=True)

            st.session_state.page = "results"
