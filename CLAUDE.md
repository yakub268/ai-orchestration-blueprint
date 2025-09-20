# CLAUDE.md — Project Memory

Use this with `journals/Journal.md` to brief Claude:
- Today’s goals
- Constraints
- Recently changed files
- Known risks

Claude, when starting:
1) Read this file + today’s Journal entry.
2) Confirm goals/constraints back to me.
3) Run Semgrep on changed paths, summarize results before coding.
4) Keep commits small; write clear messages.
