# 研答通（MVP）

基于 React + TypeScript + Vite 与 FastAPI 的文档智能助手第一阶段实现。当前目标只做最小可用闭环：

- 上传 TXT / Markdown / PDF 文档
- 选择任务：摘要、问答、提纲生成
- 后端读取文档并调用云端模型封装层
- 前端展示结果、加载态、错误态、空结果态
- 同请求本地缓存，减少重复模型调用
- 最近文档复用与最近结果历史
- 后端把调用日志写入本地 JSONL
- 未提供真实 API Key 时，默认使用可替换的 mock 模型返回，方便本地演示

## 目录结构

```text
project/
├─ backend/
│  ├─ app/
│  │  ├─ api/
│  │  ├─ core/
│  │  ├─ schemas/
│  │  ├─ services/
│  │  └─ main.py
│  ├─ tests/
│  └─ requirements.txt
├─ data/
│  ├─ logs/
│  ├─ parsed/
│  └─ uploads/
├─ frontend/
│  ├─ public/
│  ├─ src/
│  ├─ package.json
│  └─ vite.config.ts
├─ scripts/
│  ├─ bootstrap.ps1
│  └─ dev.ps1
├─ .env.example
└─ README.md
```

## 数据流

1. 前端选择文件、任务类型和问题或指令。
2. 前端先调用 `POST /api/upload` 上传文件。
3. 后端保存原始文件到 `data/uploads/`，提取纯文本并保存到 `data/parsed/`。
4. 前端拿到 `file_id` 后，再调用 `POST /api/ask`、`/api/summary` 或 `/api/outline`。
5. 后端根据 `file_id` 读取解析文本，构造 Prompt，调用 [backend/app/services/model_client.py](/C:/Users/Administrator/Desktop/project/backend/app/services/model_client.py)。
6. 后端把调用时间、任务类型、模型名、输入输出字符数、token、耗时、成功状态、错误信息写入 `data/logs/call_logs.jsonl`。
7. 前端展示结果和请求信息。

## API 设计

### `POST /api/upload`

- 请求：`multipart/form-data`，字段 `file`
- 返回：`file_id`、原始文件名、类型、字符数、解析状态

### `POST /api/ask`

```json
{
  "file_id": "xxx",
  "question": "请概括这篇文章的核心方法"
}
```

### `POST /api/summary`

```json
{
  "file_id": "xxx",
  "instruction": "突出研究背景和创新点"
}
```

### `POST /api/outline`

```json
{
  "file_id": "xxx",
  "instruction": "生成 6 页答辩提纲"
}
```

### `GET /api/logs?limit=20`

- 返回最近调用日志

### `GET /api/logs/summary?limit=100`

- 返回调用汇总统计，包括成功率、平均延迟、P95、缓存命中、token 总量、任务分布、模型分布和错误类型

### `GET /api/health`

- 返回服务健康状态、模型提供方和是否启用 mock

### 统一响应结构

```json
{
  "success": true,
  "data": {},
  "error": null,
  "request_id": "optional"
}
```

## 已完成项

- 后端 FastAPI 骨架、配置管理、统一响应与异常处理
- TXT / Markdown / PDF 上传与文本抽取
- 云端模型调用封装，支持 `mock` 与 OpenAI 兼容接口两种模式
- ask / summary / outline / logs / health 接口
- JSONL 调用日志
- 本地结果缓存与缓存命中标记
- React 前端单页 MVP
- 分阶段加载态、禁用重复提交、429 友好提示
- 最近文档复用与最近 5 次结果历史
- 日志汇总接口与日志导出脚本
- 证据目录与实验记录模板
- 文档稳定指纹与更明确的截断反馈字段
- API 集成测试覆盖上传、任务调用与日志汇总
- 前端统计面板直接读取 `/api/logs/summary`
- Demo 模式支持一键填充示例文档与示例提示
- PDF/TXT/MD 统一结构化解析结果落盘，支持页级结构保留
- 文本分块结果落盘，`ask` 任务已接入轻量检索
- `ask` 结果可返回结构化引用依据（页码 + 证据片段）
- 三类任务已统一接入最小上下文编排层，`summary / outline` 改为覆盖式 chunk 上下文
- `ask` 检索未命中时会显式拒绝无依据回答，不再伪造引用
- `summary / outline` 现在也可返回结构化来源片段
- 日志汇总已包含检索状态、引用数量等检索质量指标
- 日志与统计面板已区分 `answered / refused / error`
- 前端已区分展示：`ask` 的“引用依据”与 `summary / outline` 的“来源片段”
- 已支持最小模型分层路由：可按任务将 `ask`、`summary`、`outline` 分配到不同 tier/model
- 已支持固定样例集复跑脚本与样例报告导出
- 结果区已可展示模型路由层级与路由原因
- 日志汇总已兼容旧日志字段并可按 route tier 聚合
- PowerShell 启动脚本
- 基础服务层测试

## 未完成项

- 真实无问芯穹 API 协议适配与联调
- PDF 结构化解析和页码引用
- 文本分块、检索、上下文压缩
- 多轮会话、评测与 benchmark

## 环境准备

### 1. 配置环境变量

```powershell
Copy-Item .env.example .env
```

如果你还没有真实 API Key，保持：

```env
MODEL_PROVIDER=mock
USE_MOCK_MODEL=true
```

如果你要接真实云端接口，修改：

```env
MODEL_PROVIDER=volcengine_ark
USE_MOCK_MODEL=false
WUQIONG_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
WUQIONG_API_KEY=你的密钥
MODEL_QA=你的 Endpoint ID
MODEL_SUMMARY=你的 Endpoint ID
MODEL_OUTLINE=你的 Endpoint ID
```

当前 [backend/app/services/model_client.py](/C:/Users/Administrator/Desktop/project/backend/app/services/model_client.py) 默认按 OpenAI 兼容的 `/chat/completions` 协议调用。接火山方舟时，`MODEL_*` 建议填写控制台创建好的 `Endpoint ID`。

### 2. 安装依赖

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap.ps1
```

脚本会优先创建 `.venv` 并安装后端依赖；如果当前环境不允许正常创建虚拟环境，会自动回退到工作区本地依赖目录 `.python_packages/`。

### 3. 一键启动

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1
```

- 前端默认地址：`http://localhost:5173`
- 后端默认地址：`http://localhost:8000`
- API 文档：`http://localhost:8000/docs`

## 手动启动

### 后端

```powershell
.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

如果当前环境走的是 `.python_packages/` 回退模式：

```powershell
$env:PYTHONPATH="$PWD;$PWD\.python_packages"
python -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端

```powershell
cd frontend
npm run dev
```

## 如何验证

1. 打开前端页面，上传一个 `.txt`、`.md` 或 `.pdf` 文件。
2. 选择“摘要 / 问答 / 提纲生成”之一。
3. 输入问题或指令，点击提交。
4. 页面应展示结果、模型名、请求 ID、耗时。
5. 查看 `data/logs/call_logs.jsonl`，确认存在调用记录。
6. 调用 `GET /api/logs`，确认日志接口可读。

## 测试

```powershell
.venv\Scripts\python.exe -m pytest backend/tests
```

## 日志汇总导出

```powershell
python scripts\export_log_summary.py --format md --output evidence\reports\latest_log_summary.md
```

也可以导出 JSON：

```powershell
python scripts\export_log_summary.py --format json
```

## 固定样例集复跑

```powershell
.venv\Scripts\python.exe scripts\replay_sample_set.py --mock --clear-cache --format md --output evidence\reports\sample_replay_latest.md
```

## 下一步建议

1. 先用真实火山方舟 Endpoint 跑通摘要、问答、提纲三条链路，再决定是否分任务换模型。
2. 在 `data/parsed/` 基础上加入 PDF 分页解析，为后续页码引用预留结构。
3. 增加轻量分块和检索层，把“整篇直发”升级为“检索后发送”。
4. 给日志加一个简单的统计面板，沉淀比赛证据。
