---
name: rp-launcher-witch-cafe
description: 开始女巫咖啡馆（Elara）RP 时使用。开场依次拉起 character-elara / preset-whimsical / worldbook-coven。薄壳层，不带内容。
---

# RP 启动器 · 女巫咖啡馆

> ⚠️ Skill 无"钉住"。本 launcher 靠**指示 agent 调用**三件套把正文拉进上下文（留存到压缩）。机制见 docs/05-loading-mechanism.md。

## 动作
1. 确认独立 session（无 code/search/data 类 skill）
2. 调用 `character-elara`、`preset-whimsical`
3. 调用 `worldbook-coven`
4. 输出启动确认，提示输入首句剧情

## 执行流程
```
拉起三件套（依次调用）：
  → /character-elara
  → /preset-whimsical
  → /worldbook-coven
全部到位 → 启动确认
压缩后重新调用本 launcher。
```

## 启动确认语
```
[RP 就绪]
角色：Elara（character-elara）
文风：奇趣 whimsical（preset-whimsical）
世界：女巫咖啡馆（worldbook-coven）
状态：三件套已拉进上下文，session 干净

请给首句剧情（含具体场景+动作）。例：
"Elara，外面下着雨，一个浑身湿透的年轻人推开了咖啡馆的门。"
```
