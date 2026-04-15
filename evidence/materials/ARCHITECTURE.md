# 架构说明

```mermaid
flowchart LR
    A[Frontend Web] --> B[FastAPI Backend]
    B --> C[File Upload Storage]
    B --> D[Parser Layer]
    D --> E[Parsed Pages]
    D --> F[Chunks]
    B --> G[Context Planner]
    G --> H[Retrieval]
    G --> I[Coverage Selection]
    H --> J[Model Client]
    I --> J
    J --> K[Volcengine Ark]
    B --> L[JSONL Logs]
    B --> M[Summary Export]
    A --> N[Stats Panel]
    A --> O[Demo Mode]
```

## 说明

- Frontend 负责上传、任务输入、结果展示、统计面板与 demo 模式
- Backend 负责解析、分块、上下文编排、检索、模型调用和日志留存
- Parser 保留页级结构
- Chunk 层为检索和后续引用打基础
- Context Planner 决定不同任务如何选择上下文
- Volcengine Ark 负责生成能力
- JSONL Logs 和导出脚本负责证据沉淀

