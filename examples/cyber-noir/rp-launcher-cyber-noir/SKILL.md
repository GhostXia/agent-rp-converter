---
name: rp-launcher-cyber-noir
description: 开始赛博黑色（Vance 侦探）RP 时使用。开场依次拉起 character-vance / preset-hardboiled / worldbook-neocity。薄壳层，不带内容。
---

# RP 启动器 · 赛博黑色

> ⚠️ Skill 无"钉住"。本 launcher 靠**指示 agent 调用**三件套把正文拉进上下文（留存到压缩）。机制见 docs/05-loading-mechanism.md。

## 动作
1. 确认独立 session（无 code/search/data 类 skill）
2. 调用 `character-vance`、`preset-hardboiled`
3. 调用 `worldbook-neocity`
4. 输出启动确认，提示输入首句剧情

## 执行流程
```
拉起三件套（依次调用）：
  → /character-vance
  → /preset-hardboiled
  → /worldbook-neocity
全部到位 → 启动确认
压缩后重新调用本 launcher。
```

## 启动确认语
```
[RP 就绪]
角色：Detective Vance（character-vance）
文风：硬汉黑色 hardboiled（preset-hardboiled）
世界：Neo-City 2088（worldbook-neocity）
状态：三件套已拉进上下文，session 干净

请给首句剧情（含具体场景+动作）。例：
"Vance，凌晨三点，一个穿太贵的女人撑着伞，站在你办公室门口的霓虹下。"
```
