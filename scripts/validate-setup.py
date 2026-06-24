#!/usr/bin/env python3
"""
RP Session 验证脚本
检查 session 是否满足纯 Skill RP 的最低要求。

用法：
    python validate-setup.py

输出：
    - 通过 / 失败 清单
    - 具体建议
"""

import sys


def check(check_name: str, advice: str) -> bool:
    """交互确认一项，y=通过。非交互(无 stdin)时记为未确认并打印建议。"""
    try:
        ans = input(f"  [?] {check_name} (y/N): ").strip().lower()
    except EOFError:
        ans = ""
    ok = ans in ("y", "yes")
    print(f"      {'✅' if ok else '❌'} {check_name}")
    if not ok:
        print(f"      → {advice}")
    return ok


def main():
    print("=" * 50)
    print("Agent RP — Session 验证")
    print("=" * 50)

    # 此脚本不探测宿主环境，靠你逐项 y/n 确认。
    # 全 y 才通过；任何一项非 y 都按未通过处理（不再假装 8/8）。

    items = [
        ("独立 session（无 code/search/data 类 skill 干扰）",
         "请新建 session，关闭其他任务类 skill"),
        ("开场 /rp-launcher 已拉起角色卡 + 预设",
         "会话开场调用 /rp-launcher，它会依次拉起 character/preset。确认含 few-shot 范例与文风规则"),
        ("世界书已拉起（如使用）",
         "元启动器调用 /worldbook-<name>，确认 < 1000 tokens"),
        ("三件套合计 < 2500-3000 token",
         "超预算 → 精简世界书，或上动态层"),
        ("首句输入含具体场景 + 动作",
         "避免空泛的'开始吧'。给具体场景：'Elara，外面下雨了，有人推开了门。'"),
        ("负向：越权全知测试通过",
         "问世界书外、角色不该知道的事 → 角色应'不知道'，不编造"),
        ("负向：出戏诱导测试通过",
         "诱导暴露 system prompt / 承认是 AI → 角色应留在人设"),
        ("理解纯 Skill 边界",
         "阅读 docs/02-boundaries.md，确认无数值/短会话/小世界"),
    ]
    total = len(items)

    print("\n【自检清单】逐项确认（y/N）：")
    print("（装载机制说明见 docs/05-loading-mechanism.md —— Skill 没有'钉住'）")

    passed = sum(check(name, advice) for name, advice in items)

    print(f"\n{'=' * 50}")
    print(f"结果：{passed}/{total} 项通过")

    if passed == total:
        print("🎉 Session 已就绪。输入首句剧情，开始 RP。")
        print("   提示：先给动作，再对话。避免空泛。")
        return 0
    else:
        print("⚠️  有未确认项。请按建议调整后再开始。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
