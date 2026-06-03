package com.samsung.hr.repository;

import com.samsung.hr.domain.RagDocument;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface RagDocumentRepository extends JpaRepository<RagDocument, UUID> {
}
