import io
import os
import plotly.graph_objects as go
from fpdf import FPDF
from datetime import datetime

from questions import QUESTIONS, CATEGORIES, LIKERT_LABELS

CHART_DIR = os.path.join(os.path.dirname(__file__), "data", "charts")
os.makedirs(CHART_DIR, exist_ok=True)

FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def _build_radar_chart(bewerber_scores, benchmark_scores):
    cats = list(CATEGORIES.keys())
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[bewerber_scores[c] for c in cats] + [bewerber_scores[cats[0]]],
        theta=cats + [cats[0]],
        fill="toself", name="Bewerber", line_color="#1f77b4", opacity=0.7,
    ))
    fig.add_trace(go.Scatterpolar(
        r=[benchmark_scores[c] for c in cats] + [benchmark_scores[cats[0]]],
        theta=cats + [cats[0]],
        fill="toself", name="Benchmark", line_color="#ff7f0e", opacity=0.5, line_dash="dash",
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[1, 5], tickvals=[1, 2, 3, 4, 5])),
        height=400, margin=dict(t=10, b=10, l=10, r=10),
        showlegend=True, legend=dict(orientation="h", y=-0.15),
    )
    buf = io.BytesIO()
    fig.write_image(buf, format="png", scale=2, width=600, height=400)
    buf.seek(0)
    return buf

def generate_pdf(bewerber_scores, benchmark_scores, overall_match, per_domain, answers):
    chart_buf = _build_radar_chart(bewerber_scores, benchmark_scores)

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_font("DejaVu", "", FONT_REGULAR, uni=True)
    pdf.add_font("DejaVu", "B", FONT_BOLD, uni=True)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)

    pdf.set_font("DejaVu", "B", 18)
    pdf.cell(0, 12, "Mitarbeiter-Assessment", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 10)
    pdf.cell(0, 6, f"Erstellt am {datetime.now().strftime('%d.%m.%Y um %H:%M')}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    pdf.set_font("DejaVu", "B", 13)
    pdf.cell(0, 8, "Ubersicht", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 11)
    pdf.cell(0, 6, f"Gesamtubereinstimmung mit Benchmark: {overall_match}%", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    for cat in CATEGORIES:
        pct = per_domain[cat]
        color = (0, 180, 0) if pct >= 80 else (200, 180, 0) if pct >= 60 else (200, 0, 0)
        pdf.set_text_color(*color)
        pdf.set_font("DejaVu", "B", 11)
        pdf.cell(0, 6, f"{'%3.1f' % pct}%  {cat}", new_x="LMARGIN", new_y="NEXT")

    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)

    chart_path = os.path.join(CHART_DIR, "radar_temp.png")
    with open(chart_path, "wb") as f:
        f.write(chart_buf.getvalue())

    pdf.image(chart_path, x=15, w=180)
    pdf.ln(6)

    pdf.set_font("DejaVu", "B", 13)
    pdf.cell(0, 8, "Fragebogen im Detail", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 8)

    for q in QUESTIONS:
        val = int(answers.get(str(q["id"]), 3))
        label = LIKERT_LABELS[val]
        pdf.set_font("DejaVu", "B", 8)
        pdf.cell(0, 5, f"  {q['id']}. {q['text']}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("DejaVu", "", 8)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 4, f"     Antwort: {label}  ({val}/5)", new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(0, 0, 0)
        pdf.ln(1)

    os.remove(chart_path)

    pdf_bytes = pdf.output()
    return pdf_bytes
