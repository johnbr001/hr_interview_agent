"""Generate docs/sample-qa-guide-undergraduate-business.pdf for RAG / WebUI upload tests."""

from pathlib import Path

from fpdf import FPDF

OUT = Path(__file__).resolve().parent.parent / "docs" / "sample-qa-guide-undergraduate-business.pdf"

SECTIONS = [
    (
        "Why did you choose an undergraduate business major?",
        "Strong answer (A):",
        "Names specific interests (e.g., strategy, finance, entrepreneurship), cites one "
        "concrete experience (course, internship, club), and connects the major to a clear career direction.",
        "Weak answer (F):",
        "Says only 'business pays well' or 'my parents wanted me to' with no personal motivation or examples.",
    ),
    (
        "Describe a team project from a business course and your contribution.",
        "Strong answer (A):",
        "Uses STAR format: situation, task, your role, actions (analysis, coordination, presentation), "
        "and measurable outcome (grade, client feedback, deadline met).",
        "Weak answer (D):",
        "Describes the group vaguely ('we did a marketing project') without stating personal actions or results.",
    ),
    (
        "How do you apply concepts from accounting or finance to real decisions?",
        "Strong answer (B):",
        "References a specific concept (e.g., break-even, cash flow, ROI) and a real example: "
        "student budget, small business case, or internship task.",
        "Weak answer (F):",
        "Cannot name a concept or gives only textbook definitions with no application.",
    ),
    (
        "Tell me about a time you showed leadership as a business student.",
        "Strong answer (A):",
        "Led a defined initiative (case competition, club event, group assignment) with clear goals, "
        "how you motivated others, and what changed because of your leadership.",
        "Weak answer (D):",
        "Equates leadership with 'being the loudest' or 'doing everything alone' without collaboration or outcome.",
    ),
    (
        "What is your understanding of business ethics? Give an example.",
        "Strong answer (B):",
        "Defines ethics in practical terms (transparency, fairness, compliance) and gives a relevant example: "
        "academic integrity, handling confidential data, or a case study dilemma with reasoned choice.",
        "Weak answer (F):",
        "Dismisses ethics ('everyone cuts corners') or cannot provide any example.",
    ),
    (
        "Where do you see yourself three years after graduation?",
        "Strong answer (B):",
        "Names 1-2 realistic paths (analyst, marketing associate, grad school) aligned with skills gained, "
        "and mentions steps already taken (internship, certifications, networking).",
        "Weak answer (D):",
        "Only says 'CEO' or 'rich' with no industry, role, or preparation plan.",
    ),
    (
        "How do you handle conflicting priorities during busy semesters?",
        "Strong answer (A):",
        "Explains prioritization method (deadlines, impact, stakeholder expectations), gives a specific week "
        "with multiple deadlines, and what you sacrificed or delegated.",
        "Weak answer (C):",
        "Says 'I just work harder' with no structure, prioritization, or example.",
    ),
    (
        "Why are you interested in this entry-level business role at our company?",
        "Strong answer (A):",
        "Links role requirements to coursework and experience, mentions company values or industry, "
        "and states what you will contribute in the first year.",
        "Weak answer (D):",
        "Generic praise ('great company') with no role fit, no research, and no link to business major skills.",
    ),
    (
        "Describe a mistake you made in a business class or internship and what you learned.",
        "Strong answer (A):",
        "Admits a real error (data error, missed deadline, weak analysis), explains corrective action, "
        "and a habit or process changed afterward.",
        "Weak answer (F):",
        "Claims never making mistakes or blames others entirely.",
    ),
    (
        "Which business specialization interests you most (e.g., marketing, finance, management) and why?",
        "Strong answer (B):",
        "Chooses one area with evidence: favorite courses, projects, mentors, or internship exposure; "
        "explains fit with strengths (analytical, creative, operational).",
        "Weak answer (D):",
        "Lists every specialization with no depth or says 'anything is fine.'",
    ),
]


class GuidePDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "HR Interview Q&A Guide", new_x="LMARGIN", new_y="NEXT", align="C")
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 8, "Undergraduate Business Major", new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def build() -> None:
    pdf = GuidePDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(
        0,
        5,
        "Use this document as reference material for scoring interview answers from "
        "candidates with an undergraduate business background. Upload via the HR Interview "
        "WebUI (RAG documents) before scoring sessions.",
    )
    pdf.ln(6)

    for i, (question, strong_label, strong_text, weak_label, weak_text) in enumerate(SECTIONS, 1):
        if pdf.get_y() > 240:
            pdf.add_page()
        pdf.set_font("Helvetica", "B", 11)
        pdf.multi_cell(0, 6, f"Question {i}: {question}")
        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 5, strong_label, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 5, strong_text)
        pdf.ln(1)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 5, weak_label, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 5, weak_text)
        pdf.ln(4)
        if i < len(SECTIONS):
            pdf.set_draw_color(200, 200, 200)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(4)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUT))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
