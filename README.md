# AI搜索观察 · GEO 可见度监测 Skill

<img src="assets/aissgc-mark.svg" alt="AI搜索观察标志" width="64">

品牌出现在 AI 的回答中了吗？输入品牌官网和最多三个用户会问的问题，查看回答全文、品牌提及、首段出现情况、官网引用和可获得的来源信息。

由 [AI搜索观察](https://www.aissgc.com/) 站长贝果开发。选择已有 Agent 的模型工具，或使用自己的豆包与 DeepSeek API。

## 安装

以下示例将技能安装到 Codex。其他兼容 Agent Skills 的工具请使用各自的技能目录。

```bash
git clone https://github.com/caicai998/aissgc-geo-visibility.git
mkdir -p ~/.codex/skills
cp -R aissgc-geo-visibility/aissgc-geo-visibility ~/.codex/skills/
```

重启或刷新技能列表后，可以对 Agent 说：

> 使用 $aissgc-geo-visibility 检查我的品牌在 AI 回答中的可见度，先让我选择使用模式。

## 两种监测方式

| 模式 | 使用方式 | 前提 |
| --- | --- | --- |
| 当前 Agent 模式 | 在对话中逐题查看原始回答和可获得的引用 | 宿主须提供独立模型调用工具；联网、引用与费用取决于宿主 |
| 豆包 / DeepSeek API 模式 | 启动本地网页，分别查看豆包联网回答和 DeepSeek 回答 | 自备 API Key 和 Python 依赖；调用可能收费 |

当前 Agent 模式不能将普通网页搜索结果冒充模型原始回答。如果宿主无法提供独立模型回答，技能会说明限制。豆包和 DeepSeek 测量条件不同，结果分别呈现；失败调用不计入有效回答分母。

## 启动 API 模式

```bash
cd ~/.codex/skills/aissgc-geo-visibility/scripts
python3 -m venv .venv
.venv/bin/pip install requests reportlab
```

在此目录创建 `.env`，填写自己的火山方舟 API Key 和接入点 ID；DeepSeek Key 可选：

```text
ARK_API_KEY=填写自己的火山方舟API密钥
ARK_MODEL=填写自己的ep接入点ID
DEEPSEEK_API_KEY=填写自己的DeepSeek API密钥
```

```bash
.venv/bin/python server.py
```

访问 http://localhost:8000。豆包需开通联网搜索权限；DeepSeek chat API 不提供联网引用。结果中的标题只来自接口提供的信息，正文链接不一定是正式引用。网页可生成 PDF，当前 Agent 模式直接在对话中展示。不要提交 `.env`、数据库或客户报告。

## 分享与反馈

欢迎在自己的案例和教程中说明使用了 [AI搜索观察的 GEO 可见度监测 Skill](https://github.com/caicai998/aissgc-geo-visibility)，并通过 GitHub Issues 反馈问题。请勿上传密钥或客户隐私数据。
