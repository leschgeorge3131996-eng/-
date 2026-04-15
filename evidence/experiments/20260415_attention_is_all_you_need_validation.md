# Attention Is All You Need Validation

## Date

- 2026-04-15

## Sample

- File: `evidence/samples/attention_is_all_you_need.pdf`
- Type: PDF

## Validation Results

### 1. English QA

- Question:
  - `Why does this paper avoid recurrent and convolutional structures?`
- Result:
  - `answered`
- Evidence:
  - citations returned
  - page numbers returned

### 2. Chinese QA on English paper

- Question:
  - `这篇论文为什么要放弃循环和卷积结构？`
- Result:
  - `answered`
- Evidence:
  - citations returned
  - page numbers returned

### 3. Off-topic QA

- Question:
  - `这篇论文有没有讨论黑洞蒸发？`
- Result:
  - `refused`
- Evidence:
  - refusal message shown
  - no fake citations

### 4. Summary

- Prompt:
  - `请概括这篇论文的研究背景、核心方法和主要贡献。`
- Result:
  - normal
- Evidence:
  - source chunks shown

### 5. Outline

- Prompt:
  - `请生成一个 6 页汇报提纲。`
- Result:
  - normal
- Evidence:
  - source chunks shown

## Conclusion

- Current system can handle a real academic paper across:
  - summary
  - QA
  - outline
  - citation evidence
  - refusal on unsupported questions

