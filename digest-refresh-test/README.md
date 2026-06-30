# Dependabot Digest Refresh Test

This scaffold tests whether GitHub-hosted Dependabot can update a Docker image digest when the visible tag does not change.

The controlled fixture uses this image name by default:

```text
ghcr.io/jaysundu/testactions-dependabot-digest-fixture:1.0.0
```

Override it by setting `IMAGE` if needed.

## Test Steps

1. Build and push the first fixture image:

```bash
bash scripts/build-digest-fixture.sh fixture-a
```

2. Copy the top-level `Digest` value from the `docker buildx imagetools inspect` output.

3. Generate the consumer Dockerfile and Dependabot config:

```bash
bash scripts/write-digest-consumer.sh sha256:<digest-a>
```

4. Commit and push the generated files:

```bash
git add .github/dependabot.yml digest-refresh-test scripts
git commit -m "Test Dependabot Docker digest refreshes"
git push
```

5. Build and push different fixture content to the same tag:

```bash
bash scripts/build-digest-fixture.sh fixture-b
```

6. Trigger Dependabot manually in GitHub:

```text
Insights -> Dependency graph -> Dependabot -> Recent update jobs -> Check for updates
```

The test uses `.github/dependabot.yml` with explicit GHCR registry credentials. Configure `GHCR_TOKEN` as a Dependabot secret, not an Actions secret. A GitHub classic PAT with `read:packages` is sufficient.

## Pass Condition

Dependabot opens a PR that changes only the digest:

```diff
-FROM ghcr.io/jaysundu/testactions-dependabot-digest-fixture:1.0.0@sha256:<digest-a>
+FROM ghcr.io/jaysundu/testactions-dependabot-digest-fixture:1.0.0@sha256:<digest-b>
```

## Fail Condition

Dependabot reports the dependency is up to date, opens no PR, or only handles visible tag updates.

## Observed Result

The same-tag digest-only update test passed. Dependabot opened PRs for the unchanged fixture tag after the registry digest was changed by repushing new fixture content.

## Repeat The Test

To repeat the test after merging the current Dependabot PR, push new content to the same tag:

```bash
IMAGE=ghcr.io/jaysundu/testactions-dependabot-digest-fixture:1.0.1 \
  bash scripts/build-digest-fixture.sh fixture-f
```

Then run Dependabot `Check for updates` again.

Do not run `scripts/write-digest-consumer.sh` during the repeat step. Dependabot should be the process that changes `digest-refresh-test/consumer/Dockerfile`.

## GHCR Access

Dependabot needs access to GHCR package metadata. The generated `.github/dependabot.yml` uses a `GHCR_TOKEN` Dependabot secret and a `docker-registry` entry for `https://ghcr.io`.
