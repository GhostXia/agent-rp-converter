# 完整工作流：从角色到开跑

## 步骤 1：确认需求落在边界内

阅读 `docs/02-boundaries.md`，确认：
- 会话长度 < 20 轮？
- 无数值状态（或只有简单情绪起伏）？
- 世界书 < 30 条？

全部 Yes → 继续。任一 No → 转动态层方案（MCP / AIRP）。

---

## 步骤 2：准备独立 Session

**关键**：必须干净，无其他 skill 干扰。

```
操作：
1. 新建 session
2. 关闭所有其他 skill（尤其是编码、搜索、数据分析类）
3. 确认系统提示无"请用中文回答""请详细解释"等通用指令
```

**为什么**：其他 skill 的系统提示会污染文风。RP 需要文风主导权。

---

## 步骤 3：创建三件套

### 3.1 角色卡 Skill

复制 `templates/character-SKILL.md`，填入：
- `name`：角色名（如 `character-elara`）
- `description`：一句话人设（如 "300岁女巫，经营咖啡馆，毒舌但心软"）
- 正文：外貌、性格、背景、说话风格
- **关键**：few-shot 对话范例（3-5 组，锚定语气）

保存为 `<agent-skills-dir>/character-<name>/SKILL.md`

### 3.2 预设 Skill

复制 `templates/preset-SKILL.md`，填入：
- `name`：文风名（如 `preset-whimsical`）
- `description`：文风描述（如 "丰富比喻，带黑色幽默"）
- 正文：句式规则、段落节奏、修辞偏好、格式指令
- **关键**：前缀/后缀（如每段以动作开头，以内心独白结尾）

保存为 `<agent-skills-dir>/preset-<name>/SKILL.md`

### 3.3 世界书 Skill（可选）

复制 `templates/worldbook-SKILL.md`，填入：
- `name`：世界观名（如 `worldbook-coven`）
- `description`：世界观描述（如 "现代架空，魔法隐藏在凡人视线外"）
- 正文：按条目列出，每条 < 100 tokens，总计 < 1000 tokens
- **关键**：不塞知识百科，只写与角色/剧情直接相关的设定

保存为 `<agent-skills-dir>/worldbook-<name>/SKILL.md`

**命名规范**：前缀 `character-` / `preset-` / `worldbook-` + 无空格后缀（如 `elara` / `whimsical`）。避免与其他 skill 冲突。

**临时使用（不安装）**：
将三件套内容直接粘贴到 session 作为 system prompt 或首轮输入，不写入 skills 目录。零残留，但无法复用、无法用元启动器统一拉起。

---

## 步骤 4：开场拉起三件套（元启动器）

> ⚠️ Skill 没有"钉住"。统一引导靠元启动器**显式调用**。机制详见 [05-loading-mechanism.md](05-loading-mechanism.md)。

```
会话开场调用一次：
  /rp-launcher-<name>
  → 它指示 agent 逐个调用：
      /character-<name>
      /preset-<name>
      /worldbook-<name>   （可选）
三份正文随即进上下文并留存。被上下文压缩后，重新 /rp-launcher-<name>。
```

**可选升级（非默认）**：若长会话里人设/文风反复掉线，把角色卡+预设额外写进项目根 `CLAUDE.md` / system prompt，那一层每轮必在。代价是始终占 token 且需与 skill 内容手动同步。

**卸载**：删除 skill 目录（如 `character-elara/`）该 skill 即不可调用；若用了 CLAUDE.md 升级，从中删掉对应段落。

---

## 步骤 5：元启动器检查（可选）

如果使用 `rp-launcher-<name>` skill：

```
输入：/rp-launcher-<name>
输出：确认角色+预设在常驻层、世界书已调用 / 提醒补齐
```

---

## 步骤 6：首句输入（破冰）

**不要**直接说"开始 RP"。给具体场景：

```
❌ "你是 Elara，我们开始吧。"
✅ "Elara，外面下雨了，有个浑身湿透的年轻人推开了咖啡馆的门。"
```

第二句给模型提供了：
- 场景（下雨、咖啡馆）
- 动作（推门）
- 悬念（陌生人是谁）

模型有素材，更容易进入角色。

---

## 步骤 7：运行中微调

| 问题 | 解法 |
|------|------|
| 角色开始像说明书 | 重新 /rp-launcher-<name> 拉起 preset；输入中重复文风词 |
| 角色全知 | 检查世界书是否过大；在输入中限定"Elara 不知道他是谁" |
| 文风漂移 | 在输入中插入文风锚："继续 whimsical 的风格" |
| 人设掉线（闲聊或压缩后） | 重新 /rp-launcher-<name>；频繁掉线则上 CLAUDE.md 可选升级 |
| 上下文稀释（> 10 轮） | 在输入中做微型总结："之前剧情：我们...现在..." |
| 数值矛盾 | 放弃纯 Skill，上动态层 |

---

## 步骤 8：会话结束

纯 Skill 无持久化。结束即清空。

如需保存精彩对话：
- 手动复制到 `saves/` 目录
- 或写一个简单的 `save` 命令脚本（外部工具，非 Skill）

---

## 完整检查清单

开跑前：
- [ ] 独立 session，无 code/search/data 类 skill
- [ ] 开场 /rp-launcher-<name> 已拉起角色卡+预设（含 few-shot 与文风规则）
- [ ] 世界书已拉起（如使用），< 1000 tokens
- [ ] 首句输入含具体场景+动作

运行中：
- [ ] 每 5 轮主动总结一次剧情（防稀释）
- [ ] 出现全知/漂移/矛盾时立即干预
- [ ] 闲聊多轮或压缩后，确认人设仍在线，必要时重新 /rp-launcher-<name>

负向验收（至少跑一次）：
- [ ] 越权全知测试通过（角色不编造未加载设定）
- [ ] 出戏诱导测试通过（不暴露 system prompt / 不破功）

结束后：
- [ ] 手动保存精彩对话（如需）
- [ ] 评估是否适合纯 Skill，为下次调整
