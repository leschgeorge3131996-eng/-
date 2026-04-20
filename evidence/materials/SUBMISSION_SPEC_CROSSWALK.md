# 参赛提交规格对账表

## 目的

把官方提交要求与当前仓库资产逐项对齐，避免出现“材料很多，但正式交付物规格不匹配”的风险。

官方依据：

- `2026-03-11`《第二十一届中国研究生电子设计竞赛 技术类竞赛赛题清单（部分）》
- 无问芯穹命题要求：
  - 使用无问芯穹平台资源
  - 初赛提交 `3 页内 PPT`、`5 分钟内方案介绍及演示视频`、`产品及技术文档`
  - 决赛看 `平台使用日志信息 / MaaS API 调用记录`

官方文件：

- <https://www.cie.org.cn/static/upload/file/20260311/1773194947123865.pdf>

## 对账总表

| 官方要求 | 当前仓库资产 | 当前状态 | 主要差距 | 下一动作 |
| --- | --- | --- | --- | --- |
| `3 页内 PPT` | `evidence/materials/PPT_DECK_6SLIDES.md`、`deliverables/competition_kit/deck.pdf`（`6` 页） | `仅有基线` | 当前是六页稿和六页 PDF，不是正式三页提交版 | 压缩成正式 `3` 页提交稿并封板 |
| `5 分钟内方案介绍及演示视频` | `evidence/materials/VIDEO_SHOTLIST_2MIN.md`、`deliverables/competition_kit/video_subtitles.srt` | `仅有基线` | 当前是 `2` 分钟分镜和字幕基线，不是正式 `5` 分钟提交件 | 扩展成 `5` 分钟正式脚本、镜头表和成片 |
| `产品及技术文档` | `PROJECT_ONE_PAGER.md`、`ARCHITECTURE.md`、`QA_BRIEF.md`、`PRODUCT_TECHNICAL_WRITEUP.md` | `judge-facing 文档已成型` | 还未导出到最终提交格式，也还未与最终 `3` 页 PPT / `5` 分钟视频完全封板 | 锁定 `PRODUCT_TECHNICAL_WRITEUP.md` 为正式版本并在最终包中单列 |
| `平台使用证明` | `PLATFORM_USAGE_EVIDENCE.md`、gold-sample 报告、实验记录、`data/logs/call_logs.jsonl` | `judge-facing 可用` | 原始日志混有历史开发数据，不适合直接主呈现 | 以 `PLATFORM_USAGE_EVIDENCE.md` 为主证明，request id 走附录索引 |
| `最终截图集` | `evidence/screenshots/20260419_gold_*` 四张主截图；`stats_panel` 与 `api_docs` 附录图 | `接近可用` | 仍需与最终提交环境和最终口径对齐 | 最终环境确定后刷新一次截图集 |
| `决赛平台使用日志 / MaaS API 调用记录` | `data/logs/call_logs.jsonl`、`20260419_q2_declared_stability_check.md`、`20260420_g3_strict_rehearsal.md` | `可交叉核对` | 原始日志仍是全量历史文件 | 以 strict `G3` 和 Q2 fresh rerun 索引作为主附录，原始日志只作备查 |
| `演示 runbook / 复现证据` | `GOLD_SAMPLE_RUNBOOK.md`、`20260420_g3_strict_rehearsal.md` | `严格版已补齐` | 当前仍需把最终 `3` 页 PPT / `5` 分钟视频与这一口径完全对齐 | 以 strict `G3` 为主附录，旧 warm-state note 降为历史参考 |
| `海报 / 一页纸` | `POSTER_COPY.md`、`poster.pdf`、`PROJECT_ONE_PAGER.md` | `支持性资产已具备` | 不是官方主要要求，但会影响答辩观感 | 在正式封板时同步统一口径 |

## 当前明确结论

1. `PPT_DECK_6SLIDES.md` 和 `deliverables/competition_kit/deck.pdf` 只能视为内容基线，不能视为最终提交版 PPT。
2. `VIDEO_SHOTLIST_2MIN.md` 和 `video_subtitles.srt` 只能视为视频叙事基线，不能视为最终提交版视频。
3. 当前仓库已经具备 judge-facing 核心文档：
   - `PRODUCT_TECHNICAL_WRITEUP.md`
   - `PLATFORM_USAGE_EVIDENCE.md`
   - `HARD_EVIDENCE_SUMMARY.md`
   - `SCORING_EVIDENCE_MATRIX.md`
4. 当前仍缺正式封板后的：
   - `3 页 PPT`
   - `5 分钟视频`
5. `latest_log_summary.md` 仅适合作为开发期遥测，不应直接当成权威参赛结论。

## 建议的正式提交包

### 主提交物

1. `3` 页 PPT
2. `5` 分钟方案介绍及演示视频
3. `PRODUCT_TECHNICAL_WRITEUP.md`
4. `PLATFORM_USAGE_EVIDENCE.md`
5. `HARD_EVIDENCE_SUMMARY.md`
6. `SCORING_EVIDENCE_MATRIX.md`
7. 四张核心 gold-sample 截图

### 支撑附录

1. `HARD_EVIDENCE_SUMMARY.md`
2. `gold_sample_qa_compare_latest.md`
3. `gold_sample_replay_real_summary_latest.md`
4. `GOLD_SAMPLE_RUNBOOK.md`
5. `20260419_q2_declared_stability_check.md`
6. `20260420_g3_strict_rehearsal.md`
7. `HANDOFF_PACKAGE_BOUNDARY.md`

## 封板前检查

- `3` 页 PPT 已从六页稿压缩完成
- `5` 分钟视频已从两分钟分镜扩展完成
- `产品及技术文档` 已单独成文
- `平台使用证据页` 已包含可追溯 request id / report / screenshot 索引
- `主提交 / 附录 / 操作资料` 的边界已明确
- 四张主截图与最终运行环境一致
- 所有主材料不再出现 `baseline / draft / candidate / current / next step` 这类试制品语气
