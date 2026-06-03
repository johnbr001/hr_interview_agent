package com.samsung.hr.domain;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "rag_documents")
@Getter
@Setter
public class RagDocument {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false)
    private String fileName;

    @Column(nullable = false)
    private String storagePath;

    @Column(nullable = false)
    private String ingestStatus = "PENDING";

    private Integer chunkCount;

    @Column(nullable = false, updatable = false)
    private Instant uploadedAt = Instant.now();
}
