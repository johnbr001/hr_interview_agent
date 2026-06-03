package com.samsung.hr.dto;

import java.time.Instant;
import java.util.UUID;

public record SessionResponse(
        UUID id,
        String interviewerName,
        String candidateName,
        String roleTitle,
        Instant createdAt) {}
