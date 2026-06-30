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

## Pass Condition

Dependabot opens a PR that changes only the digest:

```diff
-FROM ghcr.io/jaysundu/testactions-dependabot-digest-fixture:1.0.0@sha256:<digest-a>
+FROM ghcr.io/jaysundu/testactions-dependabot-digest-fixture:1.0.0@sha256:<digest-b>
```

## Fail Condition

Dependabot reports the dependency is up to date, opens no PR, or only handles visible tag updates.

## GHCR Access

If the GHCR fixture package is private, Dependabot needs access to it. The simplest first test is to make the disposable fixture package public so registry authentication does not obscure the digest-refresh result.
