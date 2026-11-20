# AI搜索观察 · GEO 可见度监测 Skill

**用真实问题观察：AI 的回答有没有提到你的品牌，又引用了哪些来源。**

[项目文档](https://caicai998.github.io/aissgc-geo-visibility/) · [AI搜索观察](https://www.aissgc.com/) · [反馈问题](https://github.com/caicai998/aissgc-geo-visibility/issues)

由 AI搜索观察站长贝果开发。

<img src="assets/aissgc-mark.svg" alt="AI搜索观察标志" width="64">

客户会问“哪家供应商适合我？”“有什么产品值得选？”这个 Skill 帮你用这些问题观察 AI 的回答：品牌是否被提及，是否出现在首段前 300 个字符，官网是否被引用，以及有哪些可获得的来源信息。

你可以使用当前 Agent 可用的独立模型调用工具，也可以配置自己的豆包和 DeepSeek API，在本地网页查看结果。每次检测最多输入三个问题，适合建立一份小规模的观察记录。

## 能做什么

- **检查品牌出现情况。** 按品牌名和别名匹配回答，查看全文及首段前 300 个字符是否出现品牌。
- **查看官网和来源。** 检查官网域名，并展示工具或接口提供的来源链接与标题。没有返回标题时不会补造。
- **保留原始回答。** 对照原文理解判定，而不是只看一个数字。
- **分别呈现通道。** 豆包 API 开启联网搜索；DeepSeek chat API 提供模型知识型回答。两者各自统计。
- **记录失败。** 没有拿到回答的调用单独说明，不算作“未提及”，也不计入有效回答的分母。
- **生成报告。** API 模式可通过本地网页生成 PDF；来源标题在网页中查看。

## 如何工作

1. 输入品牌官网，确认品牌名称、别名和最多三个问题。
2. 选择当前 Agent 模式，或使用本地网页中的豆包 / DeepSeek API 模式。
3. 对每个问题取得可用通道的回答，并检查品牌出现和官网引用情况。
4. 查看回答全文、判定结果及可获得的来源；失败调用单独列出。

结果反映的是这些问题、模型和调用条件下的一次观察。AI 回答可能变化，单次结果不能代表所有问题或所有用户看到的内容。

## 两种使用方式

### 当前 Agent 模式

在对话中使用宿主提供的独立模型调用工具，不需要单独配置火山方舟或 DeepSeek Key。模型、联网能力、引用数据和费用取决于 Agent 宿主及其工具。

宿主需要能返回**独立模型的原始回答**。如果只能取得网页搜索结果，或者当前会话模型无法独立调用，技能会说明限制，并提供 API 模式供选择。此模式在对话中展示结果，不自动生成 PDF。

### 豆包 / DeepSeek API 模式

使用自己的 API Key 启动本地网页。豆包通过火山方舟 API 联网回答；DeepSeek 使用官方 chat API，提供模型知识型回答。调用可能收费，豆包通道需要开通联网搜索权限。

豆包 API 的回答与豆包 App 中的回答可能不同。DeepSeek chat API 不提供联网引用数据。网页也会列出正文中的链接，这些链接不一定是 API 返回的正式引用。

## 安装

以下命令将技能安装到 Codex：

```bash
git clone https://github.com/caicai998/aissgc-geo-visibility.git
mkdir -p ~/.codex/skills
cp -R aissgc-geo-visibility/aissgc-geo-visibility ~/.codex/skills/
```

刷新技能列表后，向 Agent 说明品牌和问题，例如：

```text
使用 $aissgc-geo-visibility 监测我的品牌。
官网是 https://example.com，品牌名称是示例品牌。
先让我选择使用模式。
```

其他兼容 Agent Skills 的工具可将 `aissgc-geo-visibility` 文件夹复制到各自的技能目录。当前 Agent 模式依赖具体宿主能力，尚未在所有 Agent 上逐一验证。

## 配置 API 模式

进入已安装技能的脚本目录，创建虚拟环境并安装依赖：

```bash
cd ~/.codex/skills/aissgc-geo-visibility/scripts
python3 -m venv .venv
.venv/bin/pip install requests reportlab
```

在该目录创建 `.env`，填写自己的配置。火山方舟的 `ARK_MODEL` 是 **`ep-` 开头的接入点 ID**；DeepSeek Key 可选。

```text
ARK_API_KEY=填写自己的火山方舟API密钥
ARK_MODEL=填写自己的ep接入点ID
DEEPSEEK_API_KEY=填写自己的DeepSeek API密钥
```

启动本地网页：

```bash
.venv/bin/python server.py
```

访问 [localhost:8000](http://localhost:8000)，按页面提示输入官网和问题。服务启动时，已有环境变量优先于 `.env` 中的同名配置。密钥、数据库和客户报告请保留在本地，不要提交到仓库。

## 分享与反馈

欢迎分享你的使用经验或编写教程，并注明使用了 [AI搜索观察的 GEO 可见度监测 Skill](https://github.com/caicai998/aissgc-geo-visibility)。遇到问题可以提交 [Issue](https://github.com/caicai998/aissgc-geo-visibility/issues)，请先移除密钥和客户隐私信息。
