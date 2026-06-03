package com.samsung.hr.domain;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "score_turns")
@Getter
@Setter
public class ScoreTurn {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "session_id")
    private InterviewSession session;

    @Column(columnDefinition = "TEXT")
    private String questionContext;

    @Column(nullable = false, columnDefinition = "TEXT")
    private String intervieweeText;

    @Column(nullable = false, length = 1)
    private String grade;

    @Column(columnDefinition = "TEXT")
    private String rationale;

    @Column(nullable = false, updatable = false)
    private Instant scoredAt = Instant.now();
}
