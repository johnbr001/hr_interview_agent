package com.samsung.hr.dto;

import java.time.Instant;
import java.util.UUID;

public record ScoreTurnResponse(
        UUID id,
        String questionContext,
        String intervieweeText,
        String grade,
        String rationale,
        Instant scoredAt) {}
