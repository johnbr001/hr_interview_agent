package com.samsung.hr.repository;

import com.samsung.hr.domain.ScoreTurn;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.UUID;

public interface ScoreTurnRepository extends JpaRepository<ScoreTurn, UUID> {
    List<ScoreTurn> findBySession_IdOrderByScoredAtAsc(UUID sessionId);
}
