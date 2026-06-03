package com.samsung.hr.temporal;

import io.temporal.workflow.WorkflowInterface;
import io.temporal.workflow.WorkflowMethod;

@WorkflowInterface
public interface IngestRagDocumentWorkflow {

    @WorkflowMethod(name = "IngestRagDocumentWorkflow")
    int run(String filePath, String documentId);
}
