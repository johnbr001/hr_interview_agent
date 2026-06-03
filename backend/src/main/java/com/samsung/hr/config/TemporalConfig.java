package com.samsung.hr.config;

import io.temporal.client.WorkflowClient;
import io.temporal.client.WorkflowClientOptions;
import io.temporal.serviceclient.WorkflowServiceStubs;
import io.temporal.serviceclient.WorkflowServiceStubsOptions;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class TemporalConfig {

    @Bean
    WorkflowServiceStubs workflowServiceStubs(@Value("${temporal.target}") String target) {
        return WorkflowServiceStubs.newServiceStubs(
                WorkflowServiceStubsOptions.newBuilder().setTarget(target).build());
    }

    @Bean
    WorkflowClient workflowClient(
            WorkflowServiceStubs stubs, @Value("${temporal.namespace}") String namespace) {
        return WorkflowClient.newInstance(
                stubs,
                WorkflowClientOptions.newBuilder().setNamespace(namespace).build());
    }
}
