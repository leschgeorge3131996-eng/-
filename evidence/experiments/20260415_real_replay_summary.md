# Real Replay Summary

## Date

- 2026-04-15

## Scope

- Fixed sample set replay with the real cloud model
- 4 samples
- 12 total tasks

## Result Overview

- `summary`: 4 / 4 answered
- `ask`: 4 / 4 answered
- `outline`: 1 / 4 answered, 3 failed

## Main Findings

1. The current system is already stable enough for:
- summary
- ask with retrieval and citations

2. The current weak point is:
- outline latency and timeout stability under real-model replay

3. Citation/source evidence behaved as expected:
- `ask` returned citations on matched cases
- `summary` returned source chunks

4. The replay confirms that the system is not a chat shell:
- it can answer grounded questions
- it can refuse unsupported questions
- it exposes evidence and route information

## Risks Observed

- `outline` is currently the slowest task type
- real-model replay can still hit timeout / network instability
- route tier is still `task_specific` in the current run because tiered model config was not enabled during this replay

## Recommended Next Action

1. Refresh screenshots for:
- summary success
- ask success with citations
- ask refusal
- outline success

2. Decide whether to enable real `lite/pro` model routing and rerun the same sample set

3. Consider tightening outline generation strategy or timeout handling before larger-scale external demos

