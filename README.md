# Agent RP — 纯文字、轻量级的角色扮演 Skill 方案

> **定位**：纯文字、无状态、轻量级的 RP 演绎。只保留最基础的叙事与文风，自动剔除一切不可实现的机制。
> 
> **理念**：Skill = 渐进披露的静态指导上下文。RP 的「角色卡 / 预设 / 世界书」本质是静态设定，可炼成 Skill。独立干净 session + 把人设/文风放进常驻层 = 人设主导、文笔不被污染。
>
> ⚠️ **机制更正**：Skill **没有"钉住 / 强制常驻"功能**。正文是"被调用那一次加载、之后留在上下文"，不是"每轮自动命中"。本方案的"统一引导"靠**元启动器 `rp-launcher` 开场显式调用**那三个独立 skill 来实现，不是 pin。详见 [docs/05-loading-mechanism.md](docs/05-loading-mechanism.md)（全局唯一真相源，优先级高于本文其他描述）。
> 
> **核心约束**：
> - ✅ 纯文字：不生成图片、不渲染 UI、不执行代码
> - ✅ 无状态：无数值变化、无骰子、无战斗、无经济系统
> - ✅ 轻量级：小型世界书（< 10 条）、短会话（< 20 轮）
> - ✅ 自动审计：从外部卡片导入时，agent 自动剔除不可实现内容

---

## 快速开始

分两段，**必须用两个 session**。转换 session 是脏的——塞着原始卡全文（含被剔除的机制）、agent 拆解推理、converter 正文；在里面直接开演会污染文风、让角色"看见"本该删掉的机制（越权全知）。所以转换归转换，演绎另起干净 session。

### 第一段：转换（Session A）
```
1. 新建独立 session，调用 agent-rp-converter skill
2. 把你的卡（PNG / JSON / 文本）丢给 agent
3. agent 自动拆解 → 输出四件套：
     character-<name>/  preset-<name>/  worldbook-<name>/  rp-launcher-<name>/
   （机制自动剥离；剔除 >50% 时附降级声明）
4. 装好四件套，二选一：
   · 安装：每个写进 agent skills 目录（<name>/SKILL.md）→ 之后可 /<name> 调用
   · 临时：复制四份正文备用，不写盘
```

### 第二段：演绎（Session B，全新干净）
```
1. 新起一个干净 session（关闭 code/search/data 类 skill，避免污染文风）
2. 载入四件套：
   · 已安装 → /rp-launcher-<name>（它依次拉起 character / preset / worldbook）
   · 没安装 → 直接把四份正文粘进首轮上下文
3. 输入首句剧情（含具体场景 + 动作），开跑
4. 上下文被压缩后，重新 /rp-launcher-<name>
```

> 可选升级：若长会话里人设反复掉线，可把角色卡+预设额外写进 `CLAUDE.md` 保证每轮在线（非默认）。机制与"为什么没有钉住"见 [docs/05-loading-mechanism.md](docs/05-loading-mechanism.md)。完整 8 步工作流见 [docs/03-workflow.md](docs/03-workflow.md)。

---

## 项目结构

```
agent-rp-converter/          ← 整个文件夹即此 skill（name=agent-rp-converter）
├── SKILL.md                  ← ⭐ 转换器入口：引导 agent 拆卡→三件套+元启动器
├── README.md                 ← 你在这里
├── ARCHITECTURE.md           ← 架构设计（为什么拆三份）
├── docs/
│   ├── 01-concept.md        ← 理念与核心假设
│   ├── 02-boundaries.md     ← 硬边界：什么时候翻车 + 自动剔除清单
│   ├── 03-workflow.md     ← 完整工作流（创建→安装→使用→卸载）
│   ├── 04-audit-guide.md  ← 导入审计：从外部卡片到纯 Skill + 生命周期管理
│   └── 05-loading-mechanism.md ← ⚠️ 加载机制（唯一真相源：为什么没有"钉住"）
├── templates/               ← 空白模板，复制即用
│   ├── character-SKILL.md   ← 含自动剔除约束
│   ├── preset-SKILL.md      ← 含自动剔除约束
│   ├── worldbook-SKILL.md   ← 含自动剔除约束
│   └── meta-launcher-SKILL.md
├── examples/                ← 两个完整示例（标准输出形态：每个 skill 一个 <name>/SKILL.md）
│   ├── witch-cafe/
│   │   ├── character-elara/SKILL.md
│   │   ├── preset-whimsical/SKILL.md
│   │   ├── worldbook-coven/SKILL.md
│   │   └── rp-launcher-witch-cafe/SKILL.md
│   └── cyber-noir/
│       ├── character-vance/SKILL.md
│       ├── preset-hardboiled/SKILL.md
│       ├── worldbook-neocity/SKILL.md
│       └── rp-launcher-cyber-noir/SKILL.md
├── skills/                  ← 可直接使用的 production skill
│   ├── rp-character/SKILL.md
│   ├── rp-preset/SKILL.md
│   ├── rp-worldbook/SKILL.md
│   └── rp-launcher/SKILL.md
└── scripts/
    └── validate-setup.py   ← 验证脚本：检查 session 是否合规
```

---

## 三件套各司其职

| 组件 | 职责 | 装载方式 | 体积建议 |
|------|------|-----------|----------|
| **角色卡** | 人设/外观/性格/说话风格 + few-shot 范例 | 元启动器开场调用 | 500-1500 tokens |
| **预设** | 文风规则、格式指令、前缀/后缀 | 元启动器开场调用 | 200-500 tokens |
| **世界书** | 背景知识条目（仅限小型） | 元启动器开场调用（懒加载） | < 1000 tokens |
| **rp-launcher** | 元启动器：开场统一拉起上面三个，不带内容 | 用户开场调用一次 | 极小 |

> 三个独立 skill，由元启动器统一引导——可单独替换复用（换世界书不动角色）。为什么不合并见 [docs/05 §3](docs/05-loading-mechanism.md#3-为什么是三份独立而不是合并)。

---

## 核心约束：自动剔除不可实现内容

本方案是**纯文字的轻量 RP**。从外部卡片（SillyTavern / AIRP / 其他）导入时，agent 必须**自动剔除**以下内容：

- 数值状态系统（HP/MP/好感度/经济/经验值）
- 骰子/战斗/经济/时间推进系统
- 文生图提示词（Stable Diffusion tags）
- HTML/CSS/前端面板（状态栏、进度条）
- ST 宏/运行时补丁（`{{char}}`、`{{user}}` 替换语法）
- JSON Patch / 状态更新格式
- COT 标签（显式思考链）
- 多 agent / NPC 协同指令
- 秘密边界/视角隔离机制
- 记忆/封卷/跨会话归档
- 可执行代码/脚本
- 采样参数（temperature、top_p 等）

详见 `docs/04-audit-guide.md` 的完整审计清单和导入流程。

---

## 硬边界（必看）

纯 Skill 方案**只适合**：
- ✅ 短会话（单次或几轮，< 20 轮）
- ✅ 无数值状态（HP/MP/EXP 不变，无骰子）
- ✅ 小型世界书（< 10 条背景知识）
- ✅ 纯文字（无图片、无 UI、无代码）

**不适合**（需要动态数据层 MCP/AIRP）：
- ❌ 活体状态（HP/MP 每轮变化）
- ❌ 跨会话记忆
- ❌ 大世界书（关键词门控）
- ❌ 长战役（> 20 轮）
- ❌ 战斗/骰子/经济系统

---

## 示例预览

### 女巫咖啡馆（Witch Cafe）
- **角色**：Elara，300 岁女巫，开咖啡馆，毒舌但心软
- **文风**： whimsical，比喻丰富，带一点黑色幽默
- **世界**：现代架空，魔法隐藏在凡人视线之外，咖啡是施法媒介

### 赛博黑色电影（Cyber Noir）
- **角色**：Detective Vance，半机械人私家侦探，说话简短，带复古俚语
- **文风**： hardboiled，短句，比喻粗粝， rain-soaked 意象
- **世界**：2088 年 Neo-City，霓虹与酸雨，企业统治

---

## 从外部卡片导入

如果你有 SillyTavern 角色卡（PNG/JSON）、AIRP 配置或其他格式的 RP 设定，使用 `docs/04-audit-guide.md` 中的审计流程：

1. 接收原始卡片 → 2. 自动解包分类 → 3. 机制块直接删除 → 4. 设定块静态化清洗 → 5. 重组为三件套 → 6. 规模检查 → 7. 输出 + 审计声明

agent 会自动完成，无需用户手动过滤。

---

## 生命周期管理

### 安装

生成三件套 skill 后，保存到 agent 的 skills 目录下：

```
<agent-skills-dir>/
├── character-elara/
│   └── SKILL.md
├── preset-whimsical/
│   └── SKILL.md
└── worldbook-coven/
    └── SKILL.md
```

每个 skill 一个独立目录，目录名即 skill 名。使用前缀 `character-` / `preset-` / `worldbook-` + 无空格后缀（如 `elara` / `whimsical`），避免与其他 skill 冲突。

### 使用

在独立 session 中开场 `/rp-launcher-<name>` 拉起三件套（见上方"快速开始"），然后输入首句剧情即可开跑。正文进上下文后留存；上下文被压缩后重新 `/rp-launcher-<name>`。

> 没有"持续钉住、每轮命中"这回事 —— 那是早期文档的错误描述。统一引导靠元启动器显式调用。真相见 [docs/05](docs/05-loading-mechanism.md)。

### 临时使用（不安装）

如果只想跑一次、不想留文件：将三件套内容直接粘贴到 session 作为 system prompt 或首轮输入。零残留，但无法复用，session 结束即丢失。

### 卸载

不需要时，直接删除对应 skill 目录即可：
- 删除 `<agent-skills-dir>/character-<name>/`
- 删除 `<agent-skills-dir>/preset-<name>/`
- 删除 `<agent-skills-dir>/worldbook-<name>/`

删除后该 skill 不再可被调用。若额外用了 CLAUDE.md 升级，则从 CLAUDE.md 删掉对应段落即可。

### 更新/替换

直接覆盖原目录中的 `SKILL.md` 文件，或创建新版本目录（如 `character-elara-v2/`）后删除旧版。建议先备份再替换。

---

## 与 tavern2agent 的关系

[Xerxes-2/tavern2agent](https://github.com/Xerxes-2/tavern2agent) 是一个完整的卡片语义提取 + evented runtime 生成工具，支持状态机、战斗、骰子、多 agent、秘密边界等。

**纯 Skill 方案只借鉴其"解包"和"审计"思路，不采用其 runtime**：
- 借鉴：提取卡片结构、分类机制与设定、识别不可实现内容
- 不采用：state schema、reducers、event packs、CodeAct、subagents、两段式渲染
- 本质差异：`tavern2agent` 是**动态层**（runtime），纯 Skill 是**静态层**（prompt-only 退化形态）

如果用户需要完整机制（战斗、经济、多 agent、长战役），应直接迁移到 `tavern2agent`，而非在本项目硬塞机制。

---

## 贡献

角色卡模板、预设风格、世界书条目都欢迎 PR。遵循 `templates/` 中的格式，保持：
- 纯文字（无图片/UI/代码）
- 零占位（自包含，不依赖外部文件）
- 自动剔除（模板中已含约束，导入时 agent 自动执行）

---

## 参考文献

- [Xerxes-2/tavern2agent](https://github.com/Xerxes-2/tavern2agent)（MIT）—— 把 SillyTavern 卡编译成 evented runtime 的动态层方案。本项目的"解包 / 审计 / 机制识别"思路受其启发；其术语（card-ir、reducers、event packs、CodeAct、两段式渲染、秘密边界）在 [docs/04](docs/04-audit-guide.md) 中用于对比说明。本项目是其**静态退化形态**，不复用其 runtime 代码。

---

## 许可

[MIT](LICENSE) © 2026 GhostXia
