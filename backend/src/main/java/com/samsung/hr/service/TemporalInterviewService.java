package com.samsung.hr.service;

import com.samsung.hr.temporal.IngestRagDocumentWorkflow;
import com.samsung.hr.temporal.InterviewScoringWorkflow;
import io.temporal.client.WorkflowClient;
import io.temporal.client.WorkflowOptions;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.Map;
import java.util.UUID;

@Service
public class TemporalInterviewService {

    private final WorkflowClient workflowClient;
    private final String taskQueue;

    public TemporalInterviewService(
            WorkflowClient workflowClient, @Value("${temporal.task-queue}") String taskQueue) {
        this.workflowClient = workflowClient;
        this.taskQueue = taskQueue;
    }

    @SuppressWarnings("unchecked")
    public Map<String, String> scoreTurn(
            UUID sessionId,
            String intervieweeText,
            String questionContext,
            boolean useWebSearch) {
        InterviewScoringWorkflow stub =
                workflowClient.newWorkflowStub(
                        InterviewScoringWorkflow.class,
                        WorkflowOptions.newBuilder()
                                .setTaskQueue(taskQueue)
                                .setWorkflowId("score-" + sessionId + "-" + UUID.randomUUID())
                                .build());
        Map<String, Object> result =
                stub.run(
                        sessionId.toString(),
                        intervieweeText,
                        questionContext != null ? questionContext : "",
                        useWebSearch);
        return Map.of(
                "grade", String.valueOf(result.get("grade")),
                "rationale", String.valueOf(result.get("rationale")));
    }

    public int ingestRagDocument(String filePath, UUID documentId) {
        IngestRagDocumentWorkflow stub =
                workflowClient.newWorkflowStub(
                        IngestRagDocumentWorkflow.class,
                        WorkflowOptions.newBuilder()
                                .setTaskQueue(taskQueue)
                                .setWorkflowId("ingest-" + documentId)
                                .build());
        return stub.run(filePath, documentId.toString());
    }
}
