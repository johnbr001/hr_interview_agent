const base = import.meta.env.VITE_API_BASE_URL ?? "";

export type Session = {
  id: string;
  interviewerName: string;
  candidateName: string;
  roleTitle: string | null;
  createdAt: string;
};

export type ScoreTurn = {
  id: string;
  questionContext: string | null;
  intervieweeText: string;
  grade: string;
  rationale: string;
  scoredAt: string;
};

async function json<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error((err as { detail?: string }).detail ?? res.statusText);
  }
  return res.json();
}

export async function createSession(body: {
  interviewerName: string;
  candidateName: string;
  roleTitle?: string;
}): Promise<Session> {
  const res = await fetch(`${base}/api/sessions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return json(res);
}

export async function scoreTurn(
  sessionId: string,
  body: {
    intervieweeText: string;
    questionContext?: string;
    useWebSearch: boolean;
  }
): Promise<ScoreTurn> {
  const res = await fetch(`${base}/api/sessions/${sessionId}/score`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return json(res);
}

export async function listTurns(sessionId: string): Promise<ScoreTurn[]> {
  const res = await fetch(`${base}/api/sessions/${sessionId}/turns`);
  return json(res);
}

export async function uploadRagPdf(file: File): Promise<unknown> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${base}/api/rag/documents`, {
    method: "POST",
    body: form,
  });
  return json(res);
}
