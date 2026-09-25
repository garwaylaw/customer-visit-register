# 版本管理

技能版本保存在 `skills/customer-visit-register/SKILL.md` 的 `version` 字段中，并遵循语义化版本规则。

- `major`：不兼容的字段语义、确认流程或写入行为变更。
- `minor`：新增向后兼容的平台、字段映射或工作能力。
- `patch`：规则修正、勘误词、文档和兼容性修复。

推送到 `main` 后，GitHub Actions 根据提交信息自动更新版本：

- `feat!:` 或正文含 `BREAKING CHANGE:`：升级主版本。
- `feat:`：升级次版本。
- 其他提交：升级修订版本。
- 提交信息含 `[skip version]`：不更新版本。

也可以在本地显式执行：

```bash
python3 tools/bump_version.py --level major
python3 tools/bump_version.py --level minor
python3 tools/bump_version.py --level patch
```
