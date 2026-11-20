---
name: aissgc-geo-visibility
description: Check whether a brand appears in AI answers and inspect available citations. Use when monitoring brand visibility using the current agent's available model tools or the bundled Doubao and DeepSeek API application.
---

# AI搜索观察 · GEO 品牌可见度监测

本技能由 [AI搜索观察](https://www.aissgc.com/) 站长贝果开发。

先让用户选择模式：

1. **当前 Agent 模式**：使用当前 Agent 可用的独立模型调用工具和联网能力，不要求配置火山方舟或 DeepSeek Key。实际可用性、模型、联网和费用取决于宿主与用户的授权。
2. **豆包 / DeepSeek API 模式**：运行本技能附带的本地网页；用户配置自己的 API Key。豆包联网回答与 DeepSeek chat API 知识回答分别统计。

如果用户已明确选择，直接使用其选择。两种模式都先确认品牌名称、别名、官网域名和最多三个用户问题；用户提供的问题原样使用。不要把品牌名称或官网额外加入问题，除非用户的问题本身包含它们。

## 当前 Agent 模式

检查宿主是否提供可独立提交问题并取得模型原始回答的工具。使用可用的工具逐题提交用户原题；若有联网选项，说明是否启用。记录实际模型或工具名称、时间、原始回答，以及工具返回的引用 URL 和标题。不要把普通网页搜索结果、Agent 推断或自行编写的回答当作目标模型的原始回答。若只拿到搜索结果或摘要而非模型原始回答，说明无法完成此项监测，提供 API 模式供选择。

对每条成功回答，按品牌名或别名做不区分大小写的文本匹配，分别判断全文是否提及、按空行切分的首段前 300 字符是否提及。官网域名出现在回答正文或引用 URL 中则记为官网被引用。提供回答全文和可核实的引用来源：网站域名、工具提供的标题及 URL；没有标题或引用元数据时明确标注未知，不能编造。说明联网状态、样本数和模型身份；身份不可确定时标注未知。失败单独列出，不算未提及，不计入分母。若只能由当前会话模型直接作答而没有独立调用工具，说明无法隔离已知品牌上下文，也不能将此作为独立监测结果。

当前 Agent 模式的结果直接在对话展示，不自动写入数据库或生成 PDF；不同宿主、模型和联网条件的结果不能视为相同测量。不要宣称无需任何付费，宿主可能收取用量费用。

## 豆包 / DeepSeek API 模式

首次使用时，在技能的 `scripts` 目录创建 Python 虚拟环境并安装 `requests`、`reportlab`。用户在自己的环境变量或该目录 `.env` 中配置 `ARK_API_KEY`、`ARK_MODEL`（火山方舟接入点 ID）及可选的 `DEEPSEEK_API_KEY`、`DEEPSEEK_MODEL`。不要要求用户把密钥发到聊天中。启动 `python server.py`，访问 http://localhost:8000，并按界面输入官网和问题；调用 API 可能收费。

本地网页展示成功回答、三项判定及可获得的来源网站、文章标题和链接。标题仅使用接口提供的数据；正文中的链接也会列出，但不一定是 API 引用注释。DeepSeek chat API 不提供联网引用数据。失败调用不计入分母。PDF 沿用原报告格式，来源标题仅在界面展示；可从界面或 `python server.py report [run_id]` 生成。数据和 `.env` 存在 `scripts` 目录，不要上传密钥、数据库或客户报告。服务重启后旧任务的轮询地址失效。
