package com.samsung.hr.temporal;

import io.temporal.workflow.WorkflowInterface;
import io.temporal.workflow.WorkflowMethod;

import java.util.Map;

@WorkflowInterface
public interface InterviewScoringWorkflow {

    @WorkflowMethod(name = "InterviewScoringWorkflow")
    Map<String, Object> run(
            String sessionId,
            String intervieweeText,
            String questionContext,
            boolean useWebSearch);
}
