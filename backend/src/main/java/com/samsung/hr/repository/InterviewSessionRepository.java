package com.samsung.hr.repository;

import com.samsung.hr.domain.InterviewSession;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface InterviewSessionRepository extends JpaRepository<InterviewSession, UUID> {
}
