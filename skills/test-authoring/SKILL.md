---
name: "test-authoring"
description: "为 tgoskits/ArceOS/StarryOS 编写“可跑通、可维护、可复现”的测试：选型（Rust/C/脚本）、目录落点、配置文件、成功/失败断言与常见坑。"
---

# Test Authoring（测试写作技能）

## 目标

把“写一个测例”落到一个可复现的交付：

- 能被 `cargo xtask ... test qemu` 跑起来
- 有稳定的 success/fail 断言（regex），并能在日志里给出证据
- 不把“平台/构建链路的坑”隐式留在测试里

## 选型：Rust 还是 C/脚本？

- **ArceOS**：`test-suit/arceos/rust/**` 与 `test-suit/arceos/c/**` 都是主流写法。优先选择与你要验证的模块最贴近的那一种。
  - 验证 ArceOS 运行时/库接口/内核侧能力（例如 backtrace 输出块）→ Rust 测试更自然。
  - 验证 POSIX/ulib 行为或 pthread 行为 → C 测试更自然。
- **StarryOS**：大量用例位于 `test-suit/starryos/normal/test-*` / `bug-*`，常见形式是 **C + CMake + prebuild.sh** 或脚本（例如 busybox）。

## ArceOS Rust 测试落点与骨架

- 目录：`test-suit/arceos/rust/<topic>/`
- 文件：
  - `Cargo.toml`：只放本测试需要的依赖；避免为了测试方便而启用“额外模块 feature”。
  - `build-<target>.toml`：构建特性与 env。注意 `env` 是必填字段，至少要有一个空的 `[env]` 表，否则 axbuild 解析会报 `missing field env`。
    - 推荐最小模板：
      - `features = ["ax-std"]`
      - `log = "Warn"`
      - `max_cpu_num = 4`
      - `[env]`
  - `qemu-<arch>.toml`：运行参数与 success/fail regex。
- `main.rs` 最小约束：
  - 需要在 ArceOS 侧导出 `main`：`#[cfg_attr(feature = "ax-std", unsafe(no_mangle))] fn main() { ... }`
  - 结束方式明确：打印关键证据 → 打印 `test pass` → `ax_hal::power::system_off()`

## regex 断言写法（建议）

- success_regex 应包含：
  - “能力证据”：例如 backtrace 的 `BACKTRACE_BEGIN` + 至少两行 `BT`。
  - “用例完成标记”：例如 `^test pass$`。
- fail_regex 只放高置信失败信号（panic、abort、assert 等），避免把无关日志误判为失败。

## 常见坑（必须规避）

- **feature 名称写错**：启用上游模块 feature 时，用 `ax-std/<feature>` 或 `ax-feat/<feature>`，不要写裸 `backtrace` 这类在 app 包里不存在的 feature。
- **构建链路 flag 覆盖**：不要在测试配置里硬塞 `RUSTFLAGS` 去“凑出来能编译”，应让构建工具统一注入目标侧 flags（否则容易把 link args 覆盖掉，导致不同架构下行为不一致）。
- **复用/拷贝错用例**：避免把 `exception` 之类的测试骨架直接复制到 `backtrace` 包里，导致“包名/断言/目标能力”错位。

## 交付清单（完成一次测试的最小闭环）

- 新增/修改的测试目录能在至少一个 arch 上跑通
- `qemu-<arch>.toml` 的 success_regex 能匹配到证据与 `test pass`
- 给出一条最短可复现命令（build+run 或 test）
- **PR 绑定测试**：若该用例将随 PR 交付，必须满足 `pr-workflow` 的 E2E 要求（用例与功能同 PR；Test plan 含命令 + 期望输出）
- **Rust host 代码**：若改动 `scripts/axbuild/` 等 host crate，交付前运行 `cargo fmt --all -- --check`（失败则 `cargo fmt --all` 后 re-check，与功能变更同 commit）
