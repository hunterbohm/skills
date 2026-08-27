#!/usr/bin/env bash
# Publish the working tree to main.
#
# main is branch-protected (pull request + GitHub "validate" check), so this
# script validates locally, opens a pull request from a publish/* branch, lets
# it merge itself when the check passes, then fast-forwards local main.
#
# Usage: scripts/publish.sh "what changed"
set -euo pipefail
cd "$(dirname "$0")/.."
msg="${1:-Update skills}"
branch="$(git rev-parse --abbrev-ref HEAD)"

case "$branch" in
  main)
    git pull -q --ff-only origin main
    ;;
  publish/*)
    echo "continuing unfinished publish on $branch" ;;
  *)
    echo "publish.sh: switch to main first (git checkout main)" >&2
    exit 1 ;;
esac

python3 scripts/generate-catalog.py
npm run --silent validate

if [ -z "$(git status --porcelain)" ] && [ "$branch" = "main" ]; then
  echo "nothing to publish"
  exit 0
fi

if [ "$branch" = "main" ]; then
  branch="publish/$(date +%Y%m%d-%H%M%S)"
  git checkout -q -b "$branch"
fi
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -q -m "$msg"
fi
git push -q -u origin "$branch"

if ! gh pr view "$branch" --json number >/dev/null 2>&1; then
  gh pr create --base main --head "$branch" --title "$msg" \
    --body "Published with scripts/publish.sh." >/dev/null
fi
gh pr merge "$branch" --auto --squash >/dev/null
url="$(gh pr view "$branch" --json url --jq .url)"
echo "pull request open: $url"
echo "waiting for the validate check..."

if ! gh pr checks "$branch" --watch --fail-fast >/dev/null; then
  echo "validation FAILED on GitHub: $url" >&2
  echo "fix the problem, then run scripts/publish.sh again (you are on $branch)" >&2
  exit 1
fi
for _ in $(seq 1 30); do
  state="$(gh pr view "$branch" --json state --jq .state)"
  [ "$state" = "MERGED" ] && break
  sleep 5
done
if [ "$state" != "MERGED" ]; then
  echo "checks passed but the pull request is not merged yet: $url" >&2
  exit 1
fi
git checkout -q main
git pull -q --ff-only origin main
git branch -q -D "$branch"
echo "published $(git rev-parse --short HEAD) -> https://github.com/hunterbohm/skills"
