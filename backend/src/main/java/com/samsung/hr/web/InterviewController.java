package com.samsung.hr.web;

import com.samsung.hr.dto.*;
import com.samsung.hr.service.InterviewService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/sessions")
public class InterviewController {

    private final InterviewService interviewService;

    public InterviewController(InterviewService interviewService) {
        this.interviewService = interviewService;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public SessionResponse create(@Valid @RequestBody CreateSessionRequest request) {
        return interviewService.createSession(request);
    }

    @GetMapping("/{id}")
    public SessionResponse get(@PathVariable UUID id) {
        return interviewService.getSession(id);
    }

    @PostMapping("/{id}/score")
    public ScoreTurnResponse score(
            @PathVariable UUID id, @Valid @RequestBody ScoreRequest request) {
        return interviewService.score(id, request);
    }

    @GetMapping("/{id}/turns")
    public List<ScoreTurnResponse> turns(@PathVariable UUID id) {
        return interviewService.listTurns(id);
    }
}
