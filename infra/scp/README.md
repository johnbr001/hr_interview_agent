# Samsung Cloud Platform (SCP) Deployment

## Prerequisites

- SCP Kubernetes cluster (or managed K8s on SCP)
- Container registry (SCP Container Registry or Harbor)
- Temporal cluster reachable from the namespace
- Managed PostgreSQL or in-cluster Postgres

## Deploy steps

1. Set `REGISTRY` in manifests under `k8s/` to your SCP registry path.
2. Create secrets from `secrets.example.yaml` (never commit real keys).
3. `kubectl apply -f k8s/namespace.yaml`
4. `kubectl apply -f k8s/pvc.yaml`
5. `kubectl apply -f k8s/configmap.yaml`
6. `kubectl apply -f k8s/secrets.yaml`
7. Build and push images:

```bash
./infra/scripts/build-push.sh
```

8. Apply workloads: `ai-agent-deployment.yaml`, `backend-deployment.yaml`, `frontend-deployment.yaml`

## Networking

- Expose frontend via SCP Load Balancer or Ingress.
- Backend is internal; frontend nginx proxies `/api` to the backend service.
- AI agent workers have no public port — only Temporal task queue polling.

## Observability

Add SCP-compatible logging agents (Fluent Bit) and metrics (Prometheus) per your org standards.
