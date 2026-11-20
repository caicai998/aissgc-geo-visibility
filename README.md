# GEO 品牌可见度监测技能

本项目由 [AI搜索观察](https://www.aissgc.com/) 站长贝果开发。

检查品牌是否出现在 AI 对用户问题的回答中，并展示可获得的引用来源。支持两种由用户选择的使用方式：

| 模式 | 使用方式 | 需要的配置 |
| --- | --- | --- |
| 当前 Agent 模式 | 在对话中使用宿主提供的独立模型调用工具，结果在对话中呈现 | 无需火山方舟或 DeepSeek Key；需要宿主提供适用的模型工具，费用取决于宿主 |
| 豆包 / DeepSeek API 模式 | 启动本地网页，分别监测豆包联网回答和 DeepSeek chat API 回答 | 用户自己的 API Key、豆包接入点 ID 和 Python 依赖；API 调用可能收费 |

当前 Agent 模式依赖具体宿主的能力：如果没有能返回独立模型原始回答的工具，不能完成独立监测。可用模型、联网和引用数据因工具而异；普通搜索结果不是模型回答。不同模式和通道的结果需要分开解读。

## 安装

将 `geo-visibility` 文件夹复制到兼容 Agent Skills 的代理工具的技能目录，例如 Codex 的 `~/.codex/skills/geo-visibility`。重启或刷新技能列表后，向 Agent 提出“使用 geo-visibility 监测这个品牌”，并选择模式。不同 Agent 的安装位置以其文档为准。

## API 模式配置

需要 Python 3、火山方舟 API Key 和接入点 ID；DeepSeek API Key 可选。按照技能提示在本地环境变量或技能目录 `scripts/.env` 中配置，安装 `requests` 和 `reportlab`。密钥和数据保存在本地，请勿提交。

豆包接口需有联网搜索权限；DeepSeek chat API 不提供联网引用。两通道分别统计，调用失败不计入有效回答分母。本地网页可生成 PDF；当前 Agent 模式在对话中输出结果。
