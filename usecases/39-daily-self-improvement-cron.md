# Daily Self-Improvement Cron (Usecase #39)

## Purpose
Automated daily check-in to track personal growth, review progress, and identify areas for improvement.

## Trigger
- **Frequency:** Daily at 18:00 (6 PM) Hong Kong time
- **Type:** Cron job (isolated execution, can use elevated thinking)

## Tasks

### 1. Review Yesterday's Progress
- Check `memory/YYYY-MM-DD.md` from previous day
- Extract wins, challenges, and lessons learned
- Note patterns or recurring themes

### 2. Current State Assessment
- What did I accomplish today?
- What got in the way?
- How am I feeling (energy, motivation, mood)?

### 3. Growth Metrics
- Track against personal goals (from MEMORY.md)
- Identify gaps between intention and action
- One thing that went well + one thing to improve

### 4. Actionable Insights
- Extract 1-3 concrete improvements for tomorrow
- Update HEARTBEAT.md if a new check is needed
- Log findings to `memory/YYYY-MM-DD.md`

### 5. Memory Update (if significant)
- Quarterly: distill weekly notes into MEMORY.md
- Document patterns, lessons, shifts in thinking

## Output
- Brief report to Feishu (summary card)
- Updated memory files
- Optional: reminder message if something urgent surfaced

## Notes
- Non-intrusive (text-based, no notifications unless flagged)
- Runs independent of main session
- Can use Claude's extended thinking for deeper reflection
