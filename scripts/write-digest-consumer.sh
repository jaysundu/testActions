#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 sha256:<digest>" >&2
  exit 2
fi

DIGEST="$1"
if [[ ! "${DIGEST}" =~ ^sha256:[a-f0-9]{64}$ ]]; then
  echo "Expected a full digest like sha256:<64 lowercase hex characters>." >&2
  exit 2
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGE="${IMAGE:-ghcr.io/jaysundu/testactions-dependabot-digest-fixture:1.0.0}"
CONSUMER_DIR="${ROOT}/digest-refresh-test/consumer"
DEPENDABOT_FILE="${ROOT}/.github/dependabot.yml"

mkdir -p "${CONSUMER_DIR}" "${ROOT}/.github"

if [[ -e "${DEPENDABOT_FILE}" && "${FORCE:-}" != "1" ]]; then
  cat >&2 <<EOF
${DEPENDABOT_FILE} already exists.

Edit it manually or rerun with FORCE=1 if you want this script to replace it.
EOF
  exit 1
fi

cat > "${CONSUMER_DIR}/Dockerfile" <<EOF
# This Dockerfile is only for testing Dependabot same-tag digest refreshes.
FROM ${IMAGE}@${DIGEST}
EOF

cat > "${DEPENDABOT_FILE}" <<'EOF'
# Generated for the Dependabot digest-refresh test.
version: 2

updates:
  - package-ecosystem: docker
    directory: /digest-refresh-test/consumer
    schedule:
      interval: daily
EOF

cat <<EOF
Wrote:
  ${CONSUMER_DIR}/Dockerfile
  ${DEPENDABOT_FILE}

Commit and push those files before mutating the fixture tag.
EOF
