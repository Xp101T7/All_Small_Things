# Create the bash script file with the workflow to review PR diffs grouped by folder
script = r'''#!/usr/bin/env bash
# pr-diff-review.sh — Pull a PR locally and show diffs grouped by folder buckets.
# Usage examples:
#   ./pr-diff-review.sh --pr 123
#   ./pr-diff-review.sh --branch feature/awesome --base develop
#   ./pr-diff-review.sh --pr 123 --groups "backend:src/backend|api" "frontend:src/frontend|web|ui" "infra:infra|k8s|terraform" "tests:test|tests"
# Options:
#   --remote <name>     Git remote name (default: origin)
#   --pr <number>       GitHub PR number to fetch as a local branch
#   --branch <name>     Use an existing local/remote branch instead of PR number
#   --base <name>       Base branch to compare against (default: main)
#   --groups "<label:dir1|dir2>" ...   Bucket directories (regex OR '|' matches). Unmatched files go to 'other'.
#   --no-color          Disable ANSI colors
#   --full              Show full diffs per group (not just --stat)
#   --stat              Show only stats (overrides --full)
#   --since <rev>       Compare since revision (uses 'rev..HEAD' when --branch is used; ignored with --pr)
#   --help              Show help
#
# Notes:
# - Requires bash 4+, git, awk, sed, column, tput (optional).

set -euo pipefail

REMOTE=origin
PR_NUM=
BRANCH=
BASE=main
GROUPS=()
COLOR=1
SHOW_FULL=0
ONLY_STAT=0
SINCE=

bold() { (( COLOR )) && tput bold || true; }
norm() { (( COLOR )) && tput sgr0 || true; }
green() { (( COLOR )) && tput setaf 2 || true; }
yellow() { (( COLOR )) && tput setaf 3 || true; }
blue() { (( COLOR )) && tput setaf 4 || true; }
magenta() { (( COLOR )) && tput setaf 5 || true; }
red() { (( COLOR )) && tput setaf 1 || true; }

usage() { sed -n '1,40p' "$0"; exit 0; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --remote) REMOTE="$2"; shift 2;;
    --pr) PR_NUM="$2"; shift 2;;
    --branch) BRANCH="$2"; shift 2;;
    --base) BASE="$2"; shift 2;;
    --groups) GROUPS+=("$2"); shift 2;;
    --no-color) COLOR=0; shift;;
    --full) SHOW_FULL=1; shift;;
    --stat) ONLY_STAT=1; shift;;
    --since) SINCE="$2"; shift 2;;
    --help|-h) usage;;
    *) echo "Unknown arg: $1"; usage;;
  esac
done

if [[ -z "$PR_NUM" && -z "$BRANCH" ]]; then
  echo "Error: specify either --pr <number> or --branch <name>"; exit 1;
fi

if ! command -v git >/dev/null 2>&1; then
  echo "git not found"; exit 1;
fi

# Determine head branch
TMP_LOCAL=
if [[ -n "$PR_NUM" ]]; then
  TMP_LOCAL="__pr_${PR_NUM//[^0-9a-zA-Z_-]/_}"
  echo "$(blue)Fetching PR #$PR_NUM from $REMOTE ...$(norm)"
  git fetch "$REMOTE" "pull/$PR_NUM/head:$TMP_LOCAL" --update-head-ok >/dev/null
  HEAD_REF="$TMP_LOCAL"
else
  HEAD_REF="$BRANCH"
  # Ensure branch exists locally (fetch if missing)
  if ! git show-ref --verify --quiet "refs/heads/$HEAD_REF"; then
    echo "$(blue)Fetching branch $HEAD_REF from $REMOTE ...$(norm)"
    git fetch "$REMOTE" "$HEAD_REF:$HEAD_REF" >/dev/null || true
  fi
fi

if ! git show-ref --verify --quiet "refs/heads/$BASE" && ! git show-ref --verify --quiet "refs/remotes/$REMOTE/$BASE"; then
  echo "$(yellow)Base '$BASE' not found locally; fetching from $REMOTE ...$(norm)"
  git fetch "$REMOTE" "$BASE:$BASE" >/dev/null || true
fi

# Compute diff range
if [[ -n "$PR_NUM" ]]; then
  DIFF_RANGE="$BASE...$HEAD_REF"
else
  if [[ -n "$SINCE" ]]; then
    DIFF_RANGE="$SINCE..$HEAD_REF"
  else
    DIFF_RANGE="$BASE...$HEAD_REF"
  fi
fi

# Collect changed files
mapfile -t FILES < <(git diff --name-only "$DIFF_RANGE")
if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "$(green)No changes between $DIFF_RANGE$(norm)"; exit 0;
fi

# Default groups if none provided: infer top-level dirs
if [[ ${#GROUPS[@]} -eq 0 ]]; then
  # Build top-level dir list from changed files
  TL=$(printf "%s\n" "${FILES[@]}" | awk -F/ 'NF>1 {print $1} NF==1 {print "__root__"}' | sort -u | tr '\n' '|')
  TL="${TL%|}"
  GROUPS=("root:^([^/]+)$" "top:$TL")
fi

# Parse groups into label -> regex
declare -A LABEL_TO_REGEX
declare -a ORDERED_LABELS
for g in "${GROUPS[@]}"; do
  # format "label:dir1|dir2|regex"
  label="${g%%:*}"
  pattern="${g#*:}"
  # Convert dirs to ^(dir1/|dir2/|...) regex unless it already looks like regex anchors
  if [[ "$pattern" =~ [\^\(\)\|\.\+\?\[\]] ]]; then
    regex="$pattern"
  else
    # treat tokens separated by '|' as directory prefixes
    tokens="${pattern}"
    # Build prefix regex: ^(dir1/|dir2/|...)
    re="^("
    IFS='|' read -r -a arr <<< "$tokens"
    for t in "${arr[@]}"; do
      t_escaped=$(printf '%s' "$t" | sed 's/[.[\*^$()+?{}|]/\\&/g')
      re+="$t_escaped/|"
    done
    re="${re%|})"
    regex="$re"
  fi
  LABEL_TO_REGEX["$label"]="$regex"
  ORDERED_LABELS+=("$label")
done

# Assign files to groups
declare -A GROUP_FILES
for f in "${FILES[@]}"; do
  matched=0
  for label in "${ORDERED_LABELS[@]}"; do
    re="${LABEL_TO_REGEX[$label]}"
    if [[ "$f" =~ $re ]]; then
      GROUP_FILES["$label"]+="$f"$'\n'
      matched=1
      break
    fi
  done
  if (( ! matched )); then
    GROUP_FILES["other"]+="$f"$'\n'
    if [[ -z "${LABEL_TO_REGEX[other]+x}" ]]; then
      LABEL_TO_REGEX["other"]=".*"
      ORDERED_LABELS+=("other")
    fi
  fi
done

sep() {
  printf '\n'
  (( COLOR )) && printf '%s' "$(magenta)============================================================$(norm)" || printf '============================================================'
  printf '\n\n'
}

# Output summary table
echo
echo "$(bold)Scope summary for $DIFF_RANGE$(norm)"
echo "Files changed: ${#FILES[@]}"
echo

for label in "${ORDERED_LABELS[@]}"; do
  files="${GROUP_FILES[$label]:-}"
  [[ -z "$files" ]] && continue
  count=$(printf '%s' "$files" | grep -c . || true)
  echo "$(bold)[$label]$(norm) — $count files"
  if (( ONLY_STAT )); then
    git diff --stat "$DIFF_RANGE" -- $(printf '%s' "$files" | tr '\n' ' ' | sed 's/ $//') | sed 's/^/  /'
  elif (( SHOW_FULL )); then
    sep
    git diff "$DIFF_RANGE" -- $(printf '%s' "$files" | tr '\n' ' ' | sed 's/ $//')
    sep
  else
    git diff --stat "$DIFF_RANGE" -- $(printf '%s' "$files" | tr '\n' ' ' | sed 's/ $//') | sed 's/^/  /'
    # Also show top 10 largest files by churn
    echo
    printf '%s' "$files" | grep . | xargs -I{} git diff --numstat "$DIFF_RANGE" -- "{}" 2>/dev/null \
      | awk '{print $1+$2, $0}' | sort -nr | head -n 10 | awk '{add=$2; del=$3; $1=""; $2=""; $3=""; sub(/^  */,""); printf "    %5s(+)/%5s(-)  %s\n", add, del, $0}'
    echo
  fi
done

# Clean up temp branch if created
if [[ -n "$TMP_LOCAL" ]]; then
  # Don't delete if currently checked out
  CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
  if [[ "$CURRENT_BRANCH" != "$TMP_LOCAL" ]]; then
    git branch -D "$TMP_LOCAL" >/dev/null 2>&1 || true
  else
    echo "$(yellow)Note: temp branch '$TMP_LOCAL' is currently checked out; not deleted.$(norm)"
  fi
fi
'''
path = "/mnt/data/pr-diff-review.sh"
with open(path, "w") as f:
    f.write(script)

import os, stat
os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

path