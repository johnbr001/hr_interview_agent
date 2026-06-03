package com.samsung.hr.service;

import com.samsung.hr.domain.InterviewSession;
import com.samsung.hr.domain.ScoreTurn;
import com.samsung.hr.dto.*;
import com.samsung.hr.repository.InterviewSessionRepository;
import com.samsung.hr.repository.ScoreTurnRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Map;
import java.util.UUID;

@Service
public class InterviewService {

    private final InterviewSessionRepository sessionRepository;
    private final ScoreTurnRepository turnRepository;
    private final TemporalInterviewService temporalService;

    public InterviewService(
            InterviewSessionRepository sessionRepository,
            ScoreTurnRepository turnRepository,
            TemporalInterviewService temporalService) {
        this.sessionRepository = sessionRepository;
        this.turnRepository = turnRepository;
        this.temporalService = temporalService;
    }

    @Transactional
    public SessionResponse createSession(CreateSessionRequest request) {
        InterviewSession session = new InterviewSession();
        session.setInterviewerName(request.interviewerName());
        session.setCandidateName(request.candidateName());
        session.setRoleTitle(request.roleTitle());
        session = sessionRepository.save(session);
        return toSessionResponse(session);
    }

    public SessionResponse getSession(UUID id) {
        return sessionRepository
                .findById(id)
                .map(this::toSessionResponse)
                .orElseThrow(() -> new IllegalArgumentException("Session not found: " + id));
    }

    @Transactional
    public ScoreTurnResponse score(UUID sessionId, ScoreRequest request) {
        InterviewSession session =
                sessionRepository
                        .findById(sessionId)
                        .orElseThrow(() -> new IllegalArgumentException("Session not found"));

        Map<String, String> ai =
                temporalService.scoreTurn(
                        sessionId,
                        request.intervieweeText(),
                        request.questionContext(),
                        request.useWebSearch());

        ScoreTurn turn = new ScoreTurn();
        turn.setSession(session);
        turn.setQuestionContext(request.questionContext());
        turn.setIntervieweeText(request.intervieweeText());
        turn.setGrade(ai.get("grade"));
        turn.setRationale(ai.get("rationale"));
        turn = turnRepository.save(turn);

        return toTurnResponse(turn);
    }

    public List<ScoreTurnResponse> listTurns(UUID sessionId) {
        return turnRepository.findBySessionIdOrderByScoredAtAsc(sessionId).stream()
                .map(this::toTurnResponse)
                .toList();
    }

    private SessionResponse toSessionResponse(InterviewSession s) {
        return new SessionResponse(
                s.getId(),
                s.getInterviewerName(),
                s.getCandidateName(),
                s.getRoleTitle(),
                s.getCreatedAt());
    }

    private ScoreTurnResponse toTurnResponse(ScoreTurn t) {
        return new ScoreTurnResponse(
                t.getId(),
                t.getQuestionContext(),
                t.getIntervieweeText(),
                t.getGrade(),
                t.getRationale(),
                t.getScoredAt());
    }
}
