#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

IMAGE="${IMAGE:-ghcr.io/jaysundu/testactions-dependabot-digest-fixture:1.0.0}"
PLATFORM="${PLATFORM:-linux/amd64}"
FIXTURE_VALUE="${1:-fixture-a}"

docker buildx build \
  --platform "${PLATFORM}" \
  --build-arg "FIXTURE_VALUE=${FIXTURE_VALUE}" \
  -t "${IMAGE}" \
  --push \
  "${ROOT}/digest-refresh-test/fixture"

cat <<EOF

Pushed ${IMAGE} with FIXTURE_VALUE=${FIXTURE_VALUE}.

Copy the top-level Digest value from this output and pass it to:

  bash scripts/write-digest-consumer.sh sha256:<digest>

EOF

docker buildx imagetools inspect "${IMAGE}"
