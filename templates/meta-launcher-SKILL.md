---
name: rp-launcher-<name>
description: 开始某角色的 RP 会话、做开场统一拉起时使用。依次调用 character/preset/worldbook 三个独立 skill，把正文拉进上下文。薄壳层，不携带内容。（<name> 用世界/角色名，如 rp-launcher-witch-cafe，避免装多套时 launcher 重名。）
---

# RP 启动器

> ⚠️ Skill 没有"钉住 / 强制常驻"。本 launcher 的"统一引导" = **指示 agent 去调用**那三个独立 skill，把它们的正文拉进上下文（调用一次留存到压缩）。不是 pin。机制见 `docs/05-loading-mechanism.md`。

## 功能

当本 skill 被调用时，执行以下动作：

1. 确认当前 session 为独立 session（无 code/search/data 类 skill 干扰）
2. **调用** `character-<name>` 与 `preset-<name>`，把角色+文风正文拉进上下文
3. 若使用世界书，**调用** `worldbook-<name>`
4. 输出启动确认 + 提示输入首句剧情

## 执行流程

```
检查 session 干净度：
  → 发现其他 skill（如 code、search、data）→ 提醒用户关闭
  → 干净 → 继续

拉起三件套（依次调用）：
  → /character-<name>   （必需）
  → /preset-<name>      （必需）
  → /worldbook-<name>   （可选）
  任一 skill 不存在 → 提示用户先用 agent-rp-converter 生成

全部到位 → 输出启动确认 + 提示输入首句剧情

注：上下文被压缩后，重新调用本 launcher 即可重新拉起。
若长会话仍频繁掉线 → 把角色+预设额外写进 CLAUDE.md（可选升级，见 docs/05）。
```

## 启动确认语

```
[RP 就绪]
角色：<角色名>（来自 <character skill name>）
文风：<文风名>（来自 <preset skill name>）
世界：<世界观名>（来自 <worldbook skill name>）
状态：三件套已拉进上下文，session 干净

请给出首句剧情输入（含具体场景+动作）：
```

## 故障排查

| 问题 | 诊断 |
|------|------|
| 角色不像 | 检查 character 是否含 few-shot 范例 |
| 文风僵硬 | 重新调用本 launcher 拉起 preset；输入文风关键词 |
| 角色全知 | 检查 worldbook 是否过大；检查角色知道的程度设定 |
| 人设掉线（闲聊/压缩后） | 重新调用本 launcher；频繁掉线则上 CLAUDE.md 可选升级 |
| 上下文稀释 | 手动在输入中做微型总结 |

## 免责声明

本 launcher 不携带任何 RP 内容，只负责依次拉起三件套。实际 RP 质量取决于：
- 三件套 skill 的质量
- 模型遵循指令的能力
- 用户的输入质量（场景具体度）

纯 Skill 方案有硬边界，详见 `docs/02-boundaries.md`；装载机制见 `docs/05-loading-mechanism.md`。
