package com.samsung.hr.dto;

import jakarta.validation.constraints.NotBlank;

public record CreateSessionRequest(
        @NotBlank String interviewerName,
        @NotBlank String candidateName,
        String roleTitle) {}
