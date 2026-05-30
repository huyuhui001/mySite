# 构建自我进化的公司 Building the self-improving company

Tom Blomfield 是硅谷顶尖创业加速器 Y Combinator (YC) 的核心合伙人之一，同时也是一位成功的连续创业者。他目前负责领导 YC 的企业软件和人工智能投资方向。下面是他关于构建自我进化的公司的发言内容，他认为 AI 将彻底改变传统公司的组织形态。

## 摘要

Tom Blomfield 认为 AI 将颠覆传统的层级化公司组织形态。他提出"自我进化的公司"核心理念：将公司每个职能构建为递归的 AI 自我改进循环，包含传感器层、策略层、工具层、质量门控和学习机制五个环节，使系统在无需人工干预的情况下持续迭代优化。

YC 的实践案例证明了这一可行性：监控 Agent 自动检测查询失败，通宵完成代码修复、提交 PR、审核、合并、部署，次日即可成功响应同类请求。类似地，YC 利用 2000 小时 Office Hours 录音自动生成并持续更新用户手册，将 16 位合伙人的智慧汇聚为可随时调用的 AI 知识库。

对于公司建设的实践建议：

1. **燃烧 Token，而非人头数**：过去 18 个月，YC 投资组合公司人均收入提升约 5 倍，未来瓶颈将是 Token 用量而非员工数。
2. **中层管理已终结**：AI 可以承担信息协调职能，公司只需 IC（独立贡献者）加上明确的直接责任人。
3. **让组织对 AI 可见**：记录一切——邮件、Slack、会议——未被记录的信息对 AI 等于不存在，再通过日志化与摘要提炼为 AI 可用的上下文。
4. **数据珍贵，软件可弃**：业务数据与领域理解是核心资产，内部软件可随时用 AI 重新生成。
5. **人类活在边缘**：人类负责处理模型尚无法涉足的高风险、高情绪、需要伦理判断的现实场景，其余交由 AI 循环自主运转。

## 发言稿

Where human beings are the conduit for information flowing up and down... And this underlying assumption that hierarchically organized companies are the way we should be organizing our economic units of value — I think AI basically breaks that.

人类作为信息自下而上、自上而下流动的媒介……而这种基本假设——层级化组织的公司是组织经济价值单元的正确方式——我认为 AI 基本上颠覆了这一点。

If you talked to people a year ago about how AI was useful, they talked about productivity — co-pilots, making engineers 20% more productive. But I think you can re-imagine what a company is: as a set of recursive, self-improving AI loops. I think this is really, really important. Because when it gets there, the company starts to self-improve even when you're sleeping.

如果你一年前跟人们聊 AI 有什么用，他们会谈论生产力——副驾驶、让工程师效率提升 20%。但我认为你可以重新想象公司的形态：作为一套递归的、自我改进的 AI 循环。我认为这非常重要。因为一旦做到这一点，公司就会在你睡觉时自我改进。

So let me give you an example. This AI loop: you start with a sensor layer — that's a fancy word, but really it might be emails from your customers, support tickets, code changes, people cancelling their subscription, product telemetry. It's sensor data to get information from the outside world.

让我举个例子。这个 AI 循环：你从传感器层开始——这是个花哨的词，但实际上可能是你客户的邮件、支持工单、代码变更、取消订阅的用户、产品遥测数据。这是传感器数据，用来从外部世界获取信息。

And then a policy layer: decision rules about what the AI can do, what it has to ask a human permission for, what it must log.

然后是策略层：关于 AI 能做什么、需要人类授权什么、必须记录什么的决策规则。

Then a tool layer — deterministic APIs, things like query my database or look at my calendar. A set of tools that the AI can call.

然后是工具层——确定性 API，比如查询数据库或查看日历。一组 AI 可以调用的工具。

Then a quality gate — that might be evals, deterministic checks, safety filters, human review for high-risk stuff.

然后是质量门控——可能是评估、确定性检查、安全过滤器、高风险事项的人工审核。

And then a learning mechanism: the system interacts with the real world, picks up where it doesn't work, and loops back to the top again. And if you can run every single step of that without human intervention — with minimal human intervention — your system gets better and better and better while you're sleeping.

然后是学习机制：系统与现实世界交互，发现不奏效的地方，然后回到顶部重新循环。如果你能够运行这个闭环的每一步而无需人类干预——或者说最少的人类干预——你的系统就会在你睡觉时变得越来越好。

Right now we started with an agent that you can ask, and it has deterministic tools to query our database. Pretty simple — like, "When did we last have office hours with this company?" Then it got a little bit smarter, which was like: "For this company I'm doing office hours with right now, they need introductions for anyone in petrochemicals." And it could query the database in different ways and use RAG and all sorts of stuff to come up with five relevant founders for you to meet. But again, this is a sidekick. This is an agent. And the first version of how AI is making me better as a group partner — making me 20 or 30% more effective.

现在我们从这样一个 Agent 开始：你可以问它问题，它有确定性工具来查询我们的数据库。很简单——比如"我们上次和这家公司做 Office Hours 是什么时候？"然后它变得更聪明了一点："对于这家我正在做 Office Hours 的公司，他们需要化工行业的人脉介绍。"它可以用不同的方式查询数据库，使用 RAG 和各种技术，为你找到五位相关的创始人见面。但 Again，这只是一个副驾驶。这还是一个 Agent。这是 AI 让我作为一个合伙人对接人变得更好的第一个版本——让我效率提升 20% 或 30%。

The aha moment for me came when we put a monitoring agent on top of that, which looked at every single query every single YC employee was doing, and saw when it worked and when it did not work. When it didn't work, it's like: "Oh, why not? What would have made this query work? Do we need different deterministic tools? Do we need to update the skills file? Do we need to update the database for you? Do we need a new index?" And this literally happens overnight now — it writes code, puts in a merge request to the YC codebase, has an agent review it, merge it, and deploy it. So when a human comes the next day to ask the same query, it will now succeed. For me, that was like the holy shit moment. That's not just AI making you 20 or 30% more valuable — it is the AI going through this loop to figure out how to self-improve.

我的顿悟时刻是，当我们在那之上放了一个监控 Agent，它审视每一个 YC 员工所做的每一次查询，看看什么时候成功、什么时候失败。当它失败时，它会想："哦，为什么失败？怎样才能让这个查询成功？我们需要不同的确定性工具吗？我们需要更新技能文件吗？我们需要为你更新数据库吗？我们需要一个新索引吗？"而这现在真的可以通宵发生——它写代码、向 YC 代码库提交合并请求、由 Agent 审核、合并、部署。所以当一个人第二天来问同样的查询时，它现在就能成功了。对我来说，那是一个"卧槽"时刻。这不仅仅是 AI 让你增值 20% 或 30%——而是 AI 正在通过这个循环来弄清楚如何自我改进。

And by parts of your company that work like this, you can eliminate as much of the human monitoring and supervisory capacity. You can just throw tokens at this problem and your company will get better.

通过让你的公司各部分按这种方式运作，你可以消除大量的人类监控和监督能力。你只需要在这方面投入 Token，你的公司就会变得更好。

Other examples: if you have product analytics, having an agent go through your product analytics to figure out what part of your sales funnel is presenting the highest amount of friction, researching best practices, putting in an A/B test, and deploying it — again and again for your product to have a self-optimizing product loop. Or you do it with customer service queries. You have customer suggestions coming in and in and in, and then you triage with an agent that acts like your chief product officer and chief technology officer, making judgment calls. "Okay, this is a suggestion we just don't want to do — we'll discard it." But "no, this is a suggestion that is now in line with our roadmap" — without a human being involved.

其他例子：如果你有产品分析，让一个 Agent 遍历你的产品分析，找出销售漏斗中哪部分阻力最大，研究最佳实践、放入 A/B 测试、部署它——一遍又一遍，让你的产品拥有一个自我优化的产品循环。或者你用客户服务的查询做这件事。客户建议不断涌入，然后你用一个 Agent 进行分类，它像你的首席产品官和首席技术官一样，做判断决策。"好吧，这个建议我们就是不想做——我们丢弃它。"但"不，这个建议现在符合我们的路线图"——这整个过程没有人类参与。

So I think if you can think about each part of your company as a self-improving, recursive AI loop, it becomes very, very different from this hierarchically organized, Roman-legion-style company.

所以我认为，如果你能把公司的每个部分都看作一个自我改进的、递归的 AI 循环，它就会变得与这种层级化组织的、罗马军团式的公司非常、非常不同。

So what are the implications if you want to do this? One is: burn tokens, not headcount. We're seeing companies get to Demo Day with about 5x more revenue per employee than they did 18 months ago, and I think that's going to continue through Series A and Series B. So I think you're going to be constrained on token usage, not on headcount, really, really soon.

那么如果你想这样做，意味着什么？一个是：燃烧 Token，而不是人头数。我们看到公司到达 Demo Day 时，人均收入大概是 18 个月前的 5 倍，而且我认为这种情况会延续到 A 轮和 B 轮。所以我认为你很快就会受到 Token 使用的约束，而不是人头数的约束，真的。

The blunt measure now is just measuring everyone's token usage, which is obviously dumb and gameable at the extreme. But directionally, I think it's correct. We're in the phase of what is possible right now, so everyone should be experimenting to the max to figure out what we can even do with this crazy new intelligence we have. As soon as you turn it into a leaderboard and people get promoted or fired based on it, obviously it gets gamed — obviously that's dumb. But I think directionally, figuring out who in the organization is token-maxing, who is not, is a good way to think about which employees you should be spending your time with.

现在粗暴的衡量方法就是测量每个人的 Token 使用量，这显然很蠢，而且在极端情况下是可以被操纵的。但从方向上说，我认为这是对的。我们现在处于探索可能性的阶段，所以每个人都应该最大程度地做实验，看看我们用这种疯狂的新智能到底能做什么。一旦你把它变成排行榜、人们根据它获得晋升或被解雇，它显然就会被操纵——这显然很蠢。但我认为从方向上说，找出组织中谁在最大化 Token 使用、谁没有，是思考你应该把时间花在哪些员工身上的好方法。

I think middle management is done. I just don't think you need middle management for this coordination problem. I think AI should be doing it.

我认为中层管理已经结束了。我不认为你还需要中层管理来解决这个协调问题。我认为 AI 应该来做这件事。

And for me, there are two roles that really, really matter. Everyone just has to be an IC now — a builder, an operator. And I think crucially, having directly responsible individuals to get anything done. I think you need a named human, not a committee, not a group of people — just a single person. And I think you can build companies based on ICs effectively. Middle management is over.

对我来说，有两个角色真的非常非常重要。每个人现在都只是一个 IC——一个建设者、一个运营者。我认为关键的是，要有一个直接责任人（直接负责人）来完成任何事情。我认为你需要一个具名的个人，而不是一个委员会、一群人——就只是一个人。而且我认为你可以有效地建立在 IC 之上的公司来运营。中层管理已经结束了。

Building the self-improving company — that's the dream.

构建自我改进的公司——这就是梦想。

And by the way, I think people are at the bleeding edge of this right now. I'd be interested to see where you all are, but it feels like people are exploring the boundaries. I'm not sure anyone has a truly self-improving company in every function. I might be wrong — you might prove me wrong.

顺便说一句，我认为人们现在正处于这件事的最前沿。我很有兴趣看看你们都在什么阶段，但感觉人们正在探索边界。我不确定是否有人真正做到了每个职能都有自我改进的公司。我可能错了——你们可能会证明我错了。

What would I do? First of all, I would make the entire organization legible to AI. What does that mean? It means you've got to record everything. All of our partner emails — if you email a YC partner, that email is in the YC database. Every Slack message, every DM. Every office hour we've started recording for the last three or four months. Every single thing that happens — if it is recorded, it happened to the AI. If it did not get recorded, it did not happen to your intelligence.

我会做什么？首先，我会让整个组织对 AI 可见。这意味着什么？这意味着你必须记录一切。我们所有合伙人的邮件——如果你给 YC 合伙人发邮件，那封邮件就在 YC 数据库里。每条 Slack 消息、每条 DM。我们过去三四个月开始记录每次 Office Hours。每一个发生的事情——如果它被记录了，它就发生在了 AI 身上。如果没有记录，它就没有发生到你的智能上。

And so I was talking with some founders over here just now, and we're having really good conversations about their company. But every conversation I had, I was like: "Fuck, I need to be recording this conversation." Because some guy wanted an introduction to — I can't even remember who the introduction was now. I was talking to someone about — I promised you an introduction, I said yes, and I said email me afterwards because I'm going to forget this, I'm going to talk to 20 people. So it needs to be my phone, or a clip, or smart glasses, or we deck out every room with microphones. But basically, everything needs to be recorded so it can be legible to the AI.

所以我刚才和这里的一些创始人聊天，我们关于他们的公司进行了非常好的对话。但我每次对话时，我都想："妈的，我需要记录这次对话。"因为有人想要一个介绍——我现在甚至记不清那个介绍是给谁的了。我在和一个人谈——我答应给你做介绍，我说好，然后我说之后给我发邮件，因为我可能会忘记这件事，我接下来要和 20 个人聊。所以它需要是我的手机、或者一个夹子、或者智能眼镜、或者我们在每个房间都装满麦克风。但基本上，一切都需要被记录，这样才能让 AI 可见。

And then, as Gary talked about — diarization. You cannot pump in 100,000 hours of recordings into a context window. So you have to diarize it. You have to basically aggregate it down, synthesize it into the important parts, and then give the AI breadcrumbs.

然后，正如 Gary 所说的——日志化。你不可能把 10 万小时的录音塞进一个上下文窗口。所以你必须对它进行日志化。你基本上需要把它聚合起来综合到重要的部分，然后给 AI 面包屑（给 AI 关键线索）。

So here's an example: who's read the YC user manual? Hopefully everyone in this room has at least opened it at some point. It's fine, but it was written five to ten years ago, most of it. It's kind of out of date.

所以这里有一个例子：谁读过 YC 用户手册？希望这个房间里的每个人都至少在某个时候打开过。它还行，但它大部分是五到十年前写的。它有点过时了。

So we thought last weekend: since now we've got about 2,000 hours of recorded office hours from the last three months, why don't we regenerate the user manual? You give it a set of instructions, you basically diarize it down, synthesize it, categorize it into certain areas — fundraising, hiring, co-founder, disputes, whatever — and then write me a new user manual. And by the end of the weekend, it had a 150-page user manual, which was dramatically better than the existing one. And now we can also update it every single month. So our user manual becomes self-improving. Every new piece of advice we give is compared with the existing user manual, and either incorporates it or whatever. So the user manual becomes this up-to-date, living brain of the advice we give. And obviously it doesn't stop as a user manual — you then pump it in as context to an AI agent, and suddenly you can ask a super-intelligent AI and get the combined wisdom of 16 YC partners in one — but only if it's legible. So you have to record everything.

所以上周末我们想：既然现在我们有了过去三个月大约 2000 小时的 Office Hours 录音，为什么不重新生成用户手册？你给它一组指令，你基本上把它日志化、综合、分类到特定领域——融资、招聘、联合创始人、纠纷等等——然后给我写一个新的用户手册。到周末结束时，它有了一份 150 页的用户手册，比现有的那份明显好得多。而且现在我们也可以每个月更新它。所以我们的用户手册变成了自我改进的。我们给出的每一个新建议都与现有的用户手册进行比较，要么将其纳入、要么做其他处理。所以这本用户手册成为了我们给出的建议的最新活的脑袋。而且很明显它不止于用户手册——然后你把它作为上下文输送给 AI Agent，突然你就可以问一个超级智能的 AI，获得 16 位 YC 合伙人的综合智慧——但前提是它是可见的。所以你必须记录一切。

The second point is kind of the same: if it creates an artifact that can self-improve, it's legible. If it doesn't, you throw it away.

第二点大致相同：如果它产生了一个可以自我改进的产物，它就是可见的。如果不能，你就把它扔掉。

The third point: every function can generate this kind of dashboard. It's not just dashboards — it's on-demand software. Codex is now good enough. You can one-shot most simple internal software dashboards to a pretty high level of quality. I tried it over the weekend on a bunch of our stuff — it's just unreal. So all of your internal operations teams should be sitting on this layer of kind of intelligence and understanding, and then creating their own dashboards and their own workflows. And I would see those as entirely disposable. I would very preciously store all the data. So as Gary said, he puts all of his emails in markdown, never throw anything away. But then treat the software as disposable. You can generate it, you can regenerate it. The valuable part is the comprehension inside people's heads — like, "this is how the function works, this is how we run a YC event." Whatever the software to actually run the event — you can generate it for the event. The models get smarter in a month or two. Throw this software away, give it your original set of instructions, and regenerate the software. So I think the business context and skills are the valuable part. The software on top of it is disposable.

第三点：每个职能都可以生成这种仪表板。它不仅仅是仪表板——它是按需软件。Codex 现在已经足够好了。你可以一次性生成大多数简单的内部软件仪表板，达到相当高的质量水平。我周末在我们的很多东西上试过了——简直不可思议。所以你所有的内部运营团队都应该坐在这层智能和理解之上，然后创建他们自己的仪表板和工作流。而且我会认为这些完全是可任意处置的。我会非常珍惜地存储所有数据。正如 Gary 所说，他把所有邮件都转成 markdown，从不丢弃任何东西。但然后把软件当作可任意处置的。你可以生成它，你可以重新生成它。有价值的部分是人头脑中的理解——比如"这个职能是怎么运作的，这就是我们如何运行一个 YC 活动。"无论什么软件来实际运行这个活动——你可以在活动时生成它。模型在一两个月后会变得更聪明。扔掉这个软件，给它你的原始指令集，重新生成软件。所以我认为业务上下文和技能是有价值的部分。在其之上的软件是可任意处置的。

So what are humans for in this world? I think basically we're talking about a company brain. I know a bunch of people in this room are building this. But the bit in the middle — all of your data, all of your emails, your DMs, the skills, the know-how — that is like the company brain. And I think the humans sit around the edge of this, interfacing with the real world. It's where this intelligence makes contact with reality. Human beings reach into places the models can't go yet — that might be a conference, or novel situations, ethical considerations, high-stakes moments. It's where the founder comes to us and is thinking about breaking up with their co-founder. Those are the real high-stakes, high-emotion moments where you really want a human being. I think that's where the human fits. For all of you with sales conversations — I think that's a human being in the room for the next 20 years.

那么在这个世界上人类是为了什么？我认为我们基本上在谈论一个公司大脑。我知道这个房间里有很多人正在构建这个。但中间的那部分——你所有的数据、你所有的邮件、你的 DM、技能、诀窍——那就是公司大脑。而我认为人类坐落在这个的边缘，与现实世界接口。这是这种智能接触现实的地方。人类伸入模型还去不了的地方——那可能是一个会议、或者 novel 的情况、伦理考量、高风险时刻。这是创始人来找我们、思考与他们的联合创始人分手的时候。那些是真正高风险、高情绪的时刻，你真的想要一个人类在场。我认为这就是人类的位置。对于所有在做销售对话的人——我认为未来 20 年房间里都需要一个人类。

So the humans live around the edge.

所以人类生活在边缘。

And I'll leave you with this one question: if you were building your company today, would you start it in this shape? For most of you who are small enough to build it right, I don't think you have any excuse. And I know there are a few of you who are in the process of ripping up and rebuilding your company.

我会留给你们这个问题：如果你今天在建立你的公司，你会以这种形态开始吗？对于你们大多数人来说，小到足以正确构建它，我不认为你有什么借口。我知道你们有些人在撕掉并重建你们的公司的过程中。
