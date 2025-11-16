# Anthropic 将 MCP 服务器转换为代码 API 以降低 Token 成本

原文标题：Anthropic Turns MCP Servers Into Code APIs to Cut Token Costs
原文链接：<https://kiadev.net/news/2025-11-08-anthropic-mcp-code-execution/>

## 为什么 MCP 代理在规模化时会遇到困难(Why MCP agents struggle at scale)

使用 Model Context Protocol 的代理面临实际的扩展问题：每个工具定义与每个中间结果都会被推入模型上下文。当天工作流包含很多工具或庞大负载时，Token 消耗、延迟与成本会飙升，并且很快触及上下文长度上限。

Agents that use the Model Context Protocol face a practical scaling problem: every tool definition and every intermediate result is pushed through the model context. When workflows involve many tools or large payloads, token consumption, latency, and cost can spike and context limits are reached quickly.

## 直接调用 MCP 工具的问题(The problem with direct MCP tool calls)

MCP 是一个开放标准，通过列出工具的服务器向模型暴露外部系统。在默认模式中，代理会把许多工具定义加载进模型上下文。每个工具都包含模式与元数据，且工具调用的中间输出被流式写回上下文，以便模型决定后续步骤。这意味着大型数据集可能被读取，然后再次通过模型传递给其他工具，从而在不改变任务逻辑的情况下成倍增加 Token 使用。

MCP is an open standard that exposes external systems to models via servers that list tools. In the default pattern an agent loads many tool definitions into the model context. Each tool includes schemas and metadata, and intermediate outputs from tool calls are streamed back into the context so the model can decide subsequent steps. That means large datasets can be read and then passed back again to other tools through the model, multiplying token usage without changing task logic.

## Anthropic如何用代码执行重新思考MCP(How Anthropic rethinks MCP with code execution)

Anthropic 提出的不同管线：将 MCP 服务器表示为代码级 API，并在沙箱中运行由模型编写的代码。MCP 客户端生成一个文件系统结构，镜像可用的服务器与工具。对于每个 MCP 工具，客户端创建一个轻量包装源文件，例如 servers/google-drive/getDocument.ts，它用类型化参数调用 MCP 工具。模型被指示编写导入这些包装器的 TypeScript，编排调用，并在运行时内部执行数据处理。模型不再直接摄入庞大的中间负载。

Anthropic proposes a different pipeline: represent MCP servers as code level APIs and run model-written code in a sandbox. The MCP client generates a filesystem structure that mirrors available servers and tools. For each MCP tool the client creates a thin wrapper source file, for example servers/google-drive/getDocument.ts, which calls the MCP tool with typed parameters. The model is instructed to write TypeScript that imports these wrappers, orchestrates calls, and performs data handling inside the runtime. The model no longer directly ingests large intermediate payloads.

## 具体示例(A concrete example)

在之前模式中，一个 Google Drive 的长转录文本会先返回给模型，然后在调用 Salesforce 工具时再次传递，可能消耗数以万计的 Token。在代码执行模式下，一个简短的 TypeScript 脚本调用 Google Drive 包装器，在执行环境内部处理转录内容，再调用 Salesforce 包装器，只提交所需的摘要或小样本。模型只看到紧凑输出，而不是完整负载。

In the previous pattern a Google Drive transcript might be returned through the model and then passed again when calling a Salesforce tool, costing tens of thousands of tokens. Under the code execution pattern a short TypeScript script calls the Google Drive wrapper, processes the transcript locally inside the execution environment, and calls the Salesforce wrapper with only the required summary or small sample. The model only sees compact outputs instead of entire payloads.

## 量化影响(Measured impact)

Anthropic 报告的某个端到端工作流，在转换为基于文件系统的 MCP API 与代码执行循环后，从约 150,000 个 Token 降至约 2,000 个 Token。对应于 98.7% 的 Token 使用下降，直接带来更低成本与减少延迟。

Anthropic reports a case where an end to end workflow went from about 150,000 tokens to roughly 2,000 tokens when converted to the filesystem based MCP APIs and code execution loop. That corresponds to a 98.7 percent reduction in token usage for that scenario, with direct benefits in lower cost and reduced latency.

## 设计与运营优势(Design and operational benefits)

渐进式工具发现：代理不再需要预加载所有工具定义。它可以检查已生成的文件系统，列出服务器，并只读取实际需要的模块。此举将工具目录从模型上下文迁移到代码中，Token 仅用于相关接口。

Progressive tool discovery: The agent no longer needs to preload every tool definition. It can inspect the generated filesystem, list servers, and read only the modules it actually needs. This shifts tool catalogs out of the model context and into code, so tokens are spent only on relevant interfaces.

高效数据处理：大型数据集留在执行环境内部。TypeScript 可以通过 MCP 包装器抓取一个大型电子表格，过滤行、计算汇总，然后只向模型返回摘要或少量示例。重数据搬运被隔离在模型上下文之外。

Efficient data handling: Large datasets stay inside the execution environment. TypeScript can fetch a big spreadsheet through an MCP wrapper, filter rows, compute aggregates, and return only summaries or small examples to the model. Heavy data movement stays out of the model context.

隐私保护操作：敏感字段可在执行环境内部进行标记化。模型仅看到占位符，而 MCP 客户端在调用下游工具时才映射与恢复真实值，使数据在服务器间流动时不暴露原始标识符。

Privacy preserving operations: Sensitive fields can be tokenized inside the execution environment. The model sees placeholders while the MCP client maps and restores real values only when calling downstream tools, letting data move between servers without exposing raw identifiers to the model.

状态与可复用技能：文件系统可存储中间文件与辅助脚本。转换器或报表生成器可以保存在 skills 目录中，并跨会话复用。Anthropic 将这一想法与 Claude Skills 关联，脚本与元数据集合形成更高层能力。

State and reusable skills: The filesystem can store intermediate files and helper scripts. Transformations or report generators can be saved in a skills directory and reused across sessions. Anthropic links this idea to Claude Skills, where collections of scripts and metadata form higher level capabilities.

## 安全与权衡(Security and trade offs)

将工作推入沙箱运行时降低 Token 成本与延迟，但带来运营关注点。团队必须严肃对待代码执行安全，控制隔离环境内的绑定与网络访问，并维护敏感映射的安全处理。将 MCP 转换为可执行 API 表面提高效率，但也为工程师与平台运营者带来新职责。

Pushing work into a sandboxed runtime reduces token costs and latency but raises operational concerns. Teams must treat code execution security seriously, control bindings and network access inside the isolate, and maintain secure handling of sensitive mappings. Converting MCP into an executable API surface improves efficiency but places new responsibilities on engineers and platform operators.

## 对代理构建者的启示(Implications for agent builders)

将 MCP 服务器转换为代码 API 是攻击基于上下文的代理核心扩展瓶颈的务实方式。它降低 Token 开销，局部化重数据处理，并启用渐进式发现与复用。对许多代理而言，这一模式在成本与延迟上提供即时收益，同时改变团队设计与保障模型集成的方式。

Converting MCP servers into code APIs is a pragmatic way to attack the core scaling limits of context based agents. It reduces token overhead, localizes heavy data processing, and enables progressive discovery and reuse. For many agents the pattern offers immediate cost and latency wins while changing how teams design and secure model integrations.
