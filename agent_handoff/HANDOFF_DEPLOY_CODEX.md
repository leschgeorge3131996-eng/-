# 🛠️ 部署交接 + 改动清单（给 Codex）

> 用途：Claude（本会话）做的一系列改动已全部进 git。你（Codex）读完本文件即可：① 核对/拉取这些改动；② 把项目部署成可访问的公网链接。
> 本文件自洽，不需要翻聊天记录。**最后更新：2026-06-03，HEAD `d7195ad`。**

---

## 0. TL;DR（先读这三条，能省你很多事）

1. **我的改动不需要你手动"重做"。** 全部已 `commit` 并推到 `origin/master`，工作树干净。你只需要：
   ```
   git -C <repo> fetch origin && git -C <repo> reset --hard origin/master   # 或 git pull --ff-only
   ```
   当前最新 = `d7195ad`。下面 §4 是按主题分组的 changelog，给你上下文，不是要你逐条复现。

2. **公网走 Render，别回腾讯云那台。** `yandatong.top`（→ 腾讯云 `106.54.228.138`）的拦截在**腾讯云边缘**（webblock，疑备案），在应用上游——把 app 重新部署到那台机器**不会**让域名复活。我今天（06-03）又实测过，状态见 §3。要可访问的公网链接，用我已备好的 `render.yaml`（§2、§5）。腾讯云那条路只能在腾讯云控制台解备案，非代码可修。

3. **部署只需要一个密钥：`WUQIONG_API_KEY`。** 代金券号那把，在本地 `.env` 里（`sk-` 开头，长度 19，已验证可用、计费到代金券账户）。**绝不要 commit 它。** 其余所有配置我都写进了 `render.yaml`。

---

## 1. 仓库当前状态

| 项 | 值 |
|---|---|
| remote `origin` | `https://github.com/leschgeorge3131996-eng/-.git`（仓库名就是一个 `-`，正常） |
| 分支 | `master` |
| HEAD | `d7195ad`（= `origin/master`，已同步） |
| 工作树 | 干净，无未提交改动 |
| 另有 remote `hf` | 指向旧的 HuggingFace Space（已弃用，别管） |

---

## 2. 部署相关文件（你最关心的）

### `render.yaml`（仓库根，已就绪）
- 单服务、**同源** Docker（后端 FastAPI 直接 serve `frontend/dist`，无跨域、无第二次 build）。
- `plan: free`、`region: singapore`（对大陆访问较友好）、`healthCheckPath: /api/health`。
- `CORS_ORIGINS: https://*.onrender.com` —— 通配，匹配 Render 分配的任意子域，避免浏览器 POST/DELETE 被 CSRF Origin 校验 403。
- 环境变量里 **只有 `WUQIONG_API_KEY` 是 `sync: false`**（要在 Render 面板手填）；其余（含 `MODEL_QA=deepseek-v4-flash`、`MODEL_SUMMARY/OUTLINE=qwen3-235b-a22b-instruct-2507`、`MODEL_PROVIDER=infinigence_ai`、`WUQIONG_BASE_URL`、`DEMO_MODE=true`、各上限）都已写死。
  - **今天的改动 `d7195ad`**：把这三个模型名从 `sync:false` 改成明文 `value:`，目的是把面板手填项从 4 个压到 1 个（只剩 API key），减少手滑。要换模型就改这个文件再 redeploy。

### `Dockerfile`（已就绪，无需改）
- 两段构建：`node:20` build 前端 → `python:3.12-slim` 运行时，`COPY --from=web /web/dist /app/frontend/dist`。
- `CMD ... uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT}` —— **读 `${PORT}`**，Render 注入 `10000` 能直接用；`ENV PORT=7860` 只是本地默认值，会被覆盖。
- **端侧 ONNX 默认不加载**：`edge_embedding_enabled` 默认 `False`（`backend/app/core/config.py:94`），`render.yaml` 未设 `EDGE_EMBEDDING_ENABLED` → Render 上不会加载本地 BGE 模型 → **省内存**（free 档只有 512MB，这点很关键）。

### healthcheck
- `/api/health` 真实存在（`backend/app/api/routes.py:85`，测试 `backend/tests/test_api.py:204` 覆盖），返回含 `demo_mode`。Render 健康检查不会卡。

---

## 3. 腾讯云公网拦截实测（2026-06-03，我今天复测的结论）

| 检查 | 结果 |
|---|---|
| `Resolve-DnsName yandatong.top` | 仍 → 腾讯云 `106.54.228.138`（未变） |
| HTTP 80 直连 | **超时**（5 天前还返回 302 webblock 拦截页，现在直接超时） |
| HTTPS 443 直连 | **TLS reset** |
| 后端 `106.54.228.138:8000` | **超时**（端口不通） |

**结论**：拦截在腾讯云边缘（最可能 ICP 备案问题），不是 app 层。**redeploy 到这台机器无效**。若一定要救 `yandatong.top`：去腾讯云控制台查备案状态——按天/周算，两周窗口内不靠谱，所以现实选择是 Render。

---

## 4. 本会话改动 changelog（按主题分组，给你上下文）

> 范围 `27815b1`(06-02 20:11) → `d7195ad`(06-03 17:03)，全部已推 `origin/master`。这些大多是**证据/材料/脚本**层，核心检索/回链/拒答逻辑**没动**（封板冻结）。

1. **平台用量真实对账**（代金券账户跑出真实 chatcmpl id + 控制台对账）：`27815b1` `6c576b8` `b82647b` `8e5cb2e` `68aad4b`
2. **评测严谨化（三层）**：
   - judged eval（LLM 评审 + 强制人工复核 + 把源页喂给评审修假阴性）：`0b79b24` `b7d2b9f` `3bddbe6` `75de3f3`
   - 泛化评测（qwen3-235b 现生成 176 题，88.6%，发现两个真实弱点）：`515b45a` `3ed75d1` `a1aa4de`
   - 端侧 A/B（过度拒答 6→1、0 新捏造；curated 集 ON==OFF 证明 demo 路径安全；阈值探针诚实负结果）：`d4c41dd` `54b0e5a` `3fb546f` `e05e963` `65326dc` `02ad993` `864ebec`
   - embedding 对照（lexical 15/22 < bge-small 18/22 < bge-m3 20/22；决定保留 bge-small 做端侧）：`5403c6c` `9db0957` `1463e79` `7298884`
3. **ultracode 审计 + 修复**（56 agent 审计 → codex 复审 → 一批口径修复）：`2263310` `d73ef3e` `5668c66` `bfbf683` `689c383` `8a18a3a` `706a965`
4. **加分项③ agentic 做实**（把真实的有界二次重试 iter≤2 在 UI 暴露，而不是伪造休眠的 query 改写）：`c64fc01`
5. **量化证据**：端侧延迟/体积基准 `1d253d3`、bbox 证据回链量化 `ad0a039`、评委评分对照表 `bfc7d11`、汇总 `e3e5e92`
6. **材料口径统一 + 商业化真实单价**：`4182943` `bee8b90`
7. **组员交接文档**（PPT / 视频 / 索引）：`72cd949`
8. **部署配置**：`d7195ad`（render.yaml 模型名写死，见 §2）

---

## 5. Render 部署 runbook（你来执行）

> 因为 render.yaml 已在仓库里，用 **Blueprint** 流程最省事（自动读 yaml，不用手配 region/healthcheck/CORS）。

1. https://render.com → **GitHub 登录**（拥有 `leschgeorge3131996-eng/-` 的账号；大陆可能要梯子）。
2. 授权 Render 访问该 repo。
3. **New +** → **Blueprint** → 选 repo `leschgeorge3131996-eng/-`，分支 `master`。Render 解析 `render.yaml`。
4. 它只会问一个密钥 **`WUQIONG_API_KEY`** → 填本地 `.env` 里那把（代金券号、`sk-` 开头、长度 19）。
5. **Apply / Create** → build Dockerfile（首次约 8–12 分钟）。
6. 状态 **Live** 后，URL 形如 `https://yandatong.onrender.com`。

**部署后自检**：
- `GET <url>/api/health` → 200，body 含 `demo_mode`。
- 开站走一遍锁定流程：上传 `evidence/samples/chinese_llm_spatial_eval.pdf` → 问「这篇论文主要研究了什么问题？」→ 点 citation 回 PDF → 问「木星有几颗卫星？」拒答。（这一步同时验证 `WUQIONG_API_KEY` 在云侧通。）

**免费档已知短板**（写给用户知情，不是 bug）：
- 15 分钟无访问 sleep，冷唤醒 ~30s。演示前先开一次焐热。
- 512MB RAM。端侧 ONNX 已默认关掉省内存；万一 build/run OOM，把日志贴回。

---

## 6. 红线 / 别碰

- **不要改核心检索 / 回链 / 拒答逻辑**（`backend/app/services/*` 检索与 answer 决策）——交付前两周冻结，部署不属于代码改动。
- **不要 `git reset --hard` 到旧点**（会丢上面整批改动）；要同步就 `git pull --ff-only` 或 reset 到 `origin/master`。
- **不要 commit `WUQIONG_API_KEY`**（只进 Render 面板 / 本地 `.env`）。
- **端侧开关** `EDGE_EMBEDDING_ENABLED` 在 Render 上保持默认关（省内存）；本地 demo 想演端侧再开。
- 若你也会动材料：诚实口径红线见 `agent_handoff/TEAMMATE_HANDOFF.md`（默认模型 deepseek-v4-flash、strict G3 六轮、端侧"持平/补召回"不说"显著提升"、不说开放域 100%）。

---

## 7. 部署需要的环境信息（汇总）

| 变量 | 值 | 来源 |
|---|---|---|
| `WUQIONG_API_KEY` | 代金券号那把（`sk-…`，len 19，已验证） | 本地 `.env`，**手填进 Render**，不入 git |
| `MODEL_PROVIDER` | `infinigence_ai` | 已写死在 render.yaml |
| `WUQIONG_BASE_URL` | `https://cloud.infini-ai.com/maas/v1` | 已写死 |
| `MODEL_QA` | `deepseek-v4-flash` | 已写死（`d7195ad`） |
| `MODEL_SUMMARY` / `MODEL_OUTLINE` | `qwen3-235b-a22b-instruct-2507` | 已写死 |
| `DEMO_MODE` | `true` | 已写死 |
| `EDGE_EMBEDDING_ENABLED` | 未设 → 默认 `false` | 省内存，保持 |

本地起服务自检（确认改动没坏）：`pwsh scripts/dev.ps1` → 后端 `:8000` + 前端 `localhost:5173`，走一遍锁定流程即可。
