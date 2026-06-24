---
name: agent-rp-converter
description: 把外部角色扮演卡（SillyTavern / AIRP / Risu / 酒馆卡 PNG·JSON、预设、世界书 lorebook）拆解、剥离不可实现机制，重构成三个独立的纯文字 Skill（角色卡 / 预设 / 世界书）加一个统一调用的元启动器。当用户想"导入角色卡""把酒馆卡变成 skill""拆解预设/世界书""做一个角色扮演 skill""重构成三件套"时使用。仅产出最基础的对话演绎，自动剥离渲染/状态/骰子/代码等。
---

# Agent RP 转换器

把一张外部 RP 卡，转成**三个独立 Skill + 一个元启动器**。产物只做**最基础的纯文字对话演绎**——卡里自带的渲染面板、数值状态、骰子、脚本等**一律剥离**，不保留、不降级。

## 何时用

用户带来 SillyTavern / AIRP / Risu 角色卡（PNG/JSON）、预设、世界书（lorebook），想把它跑成 skill。

## 产物（固定四件）

| 文件 | 内容 | 装载 |
|------|------|------|
| `character-<name>/SKILL.md` | 人设/外观/性格/说话风格 + **few-shot 范例** | 元启动器调用 |
| `preset-<name>/SKILL.md` | 文风/格式规则（**只取文风**，丢采样参数） | 元启动器调用 |
| `worldbook-<name>/SKILL.md` | 小型背景条目（≤10 条 / <1000 token） | 元启动器调用（懒加载） |
| `rp-launcher/SKILL.md` | 元启动器：开场统一调用上面三个，不带内容 | 用户开场调用一次 |

> **架构是三个独立 skill**，由元启动器统一引导——不合并、不塞 CLAUDE.md（那只是可选的"保证在线"升级，见 [docs/05](docs/05-loading-mechanism.md)）。

## ⚠️ 先验机制（必读，否则做了也白做）

Skill 是**静态**的，且**没有"钉住 / 强制常驻 / 每轮自动注入"**。正文是"被调用那一次进上下文、之后留到压缩"。元启动器靠**指示 agent 去调用**那三个 skill 来"统一引导"，不是 pin。完整机制与负向验收见 **[docs/05-loading-mechanism.md](docs/05-loading-mechanism.md)（唯一真相源）**。

只适合：短会话 / 无数值状态 / 小世界 / 单角色。命中下表任一 → 超出本方案，转动态层（MCP / AIRP / tavern2agent），不要硬塞：
- 活体状态（HP/MP/EXP/好感度每轮变）
- 跨会话记忆 / 封卷归档
- 大世界书逐轮关键词门控
- 长战役（>20 轮）/ 战斗 / 骰子 / 经济
边界详表见 [docs/02-boundaries.md](docs/02-boundaries.md)。

## 转换流程（agent 执行）

1. **接收 + 解包**：把卡内容拆成四块——角色设定 / 文风格式 / 世界观 / 机制。
2. **机制块 → 整段删除**：数值表、骰子、战斗、经济、时间推进、文生图 tags、HTML/CSS 面板、`{{char}}`/`{{user}}` 宏、JSON Patch、COT 标签、多 agent/NPC 调度、秘密边界门控、记忆/归档、可执行代码、采样参数。不提示、不降级、直接删。
3. **设定块 → 静态化清洗**：
   - 角色：删 `{{user}}` 开场白与自指宏；好感度数值→性格描述；保留外貌/性格/背景/说话风格/纯对话范例。
   - 文风：删门控（"紧张时切短句"→默认短句）、删元叙述、删多角色切换；保留句式/节奏/修辞/前后缀/反例。
   - 世界：删门控语句（保留内容为静态条目）、删纯百科、嵌套压到 1-2 层、数值设定→描述性设定。
4. **重组**：填入 `templates/` 三个模板 → 写出 `character-<name>/SKILL.md`、`preset-<name>/SKILL.md`、`worldbook-<name>/SKILL.md`。命名：前缀 + 无空格后缀（`character-elara` / `preset-whimsical` / `worldbook-coven`）。
5. **生成元启动器**：复制 `templates/meta-launcher-SKILL.md`，填入三个 skill 名。
6. **检查**（全过才输出）：
   - 角色卡含 ≥3 组 few-shot；预设含文风锚；世界书 ≤10 条 / <1000 token。
   - 三个 skill 的 `description` 都写了**触发场景 + 专名**（角色名/世界专名）——否则元启动器调不动它们。见 [docs/05 §4](docs/05-loading-mechanism.md)。
   - 无任何机制残留（对照 [docs/04 自检清单](docs/04-audit-guide.md)）。
7. **输出 + 声明**：每份开头加审计声明；若剔除 >50%，加降级声明（模板见 [docs/04](docs/04-audit-guide.md)）。
8. **跑负向验收**：越权全知 / 出戏诱导 / 压缩后存活（清单见 [docs/05 §6](docs/05-loading-mechanism.md)）。

## 详细参考

- 机制 / 装载 / 验收：[docs/05-loading-mechanism.md](docs/05-loading-mechanism.md) ← 唯一真相源
- 硬边界 / 何时翻车：[docs/02-boundaries.md](docs/02-boundaries.md)
- 完整剔除清单 + ST 卡片节映射：[docs/04-audit-guide.md](docs/04-audit-guide.md)
- 为什么拆三份：[ARCHITECTURE.md](ARCHITECTURE.md)
- 模板：[templates/](templates/)　完整示例：[examples/](examples/)
