package com.samsung.hr.dto;

import jakarta.validation.constraints.NotBlank;

public record ScoreRequest(
        @NotBlank String intervieweeText,
        String questionContext,
        boolean useWebSearch) {}
