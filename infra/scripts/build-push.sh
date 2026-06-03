#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
source "${ROOT}/.env.scp" 2>/dev/null || true

REGISTRY="${SCP_REGISTRY:-your-registry.scp.example.com/hr}"
TAG="${IMAGE_TAG:-latest}"

docker build -t "${REGISTRY}/hr-ai-agent:${TAG}" "${ROOT}/ai-agent"
docker build -t "${REGISTRY}/hr-interview-backend:${TAG}" "${ROOT}/backend"
docker build -t "${REGISTRY}/hr-interview-frontend:${TAG}" "${ROOT}/frontend"

docker push "${REGISTRY}/hr-ai-agent:${TAG}"
docker push "${REGISTRY}/hr-interview-backend:${TAG}"
docker push "${REGISTRY}/hr-interview-frontend:${TAG}"

echo "Pushed ${REGISTRY}/*:${TAG}"
