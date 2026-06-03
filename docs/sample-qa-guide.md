# Sample Q&A Guides (RAG testing)

## Ready-to-upload PDF (undergraduate business major)

**File:** [`sample-qa-guide-undergraduate-business.pdf`](./sample-qa-guide-undergraduate-business.pdf)

1. Start the app (backend, AI worker, frontend).
2. Open the WebUI and begin an interview session.
3. Under **Upload Q&A PDF (RAG)**, choose `docs/sample-qa-guide-undergraduate-business.pdf`.
4. Wait for ingest to finish, then score answers against business-major questions.

The PDF contains 10 questions with strong/weak answer rubrics (grades A–F) for topics such as choosing a business major, team projects, ethics, career goals, and role fit.

### Regenerate the PDF

```powershell
pip install -r scripts/requirements-generate-pdf.txt
python scripts/generate_sample_business_pdf.py
```

---

## Generic examples (markdown only)

### Question: Describe a time you handled conflict on a team.

**Strong answer (A):** Specific situation, your role, actions taken, measurable outcome, reflection.

**Weak answer (F):** Vague, blames others, no outcome.

### Question: Why do you want this role?

**Strong answer (B+):** Links motivation to role requirements and company values.

**Weak answer (D):** Generic praise only, no role fit.

### Question: Explain a technical decision you regret and what you learned.

**Strong answer (A):** Honest tradeoff, learning applied later.

**Weak answer (F):** Claims no mistakes.
