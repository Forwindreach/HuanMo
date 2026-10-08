# Security Policy

## Supported versions

Security fixes target the latest published release and the `main` branch.

## Reporting a vulnerability

请不要通过公开 Issue 报告尚未修复的安全漏洞。优先使用 GitHub 仓库 **Security** 页面中的 **Report a vulnerability** 私下提交；如果该入口不可用，请通过维护者的 GitHub 主页联系。

Please do not disclose an unpatched vulnerability in a public issue. Use **Report a vulnerability** under the repository's **Security** tab when available, or contact the maintainer through their GitHub profile.

报告中请包括：

- 受影响的版本与操作系统
- 最小复现步骤或概念验证
- 可能的影响范围
- 已知的缓解方式

请勿附带真实用户的敏感文档。维护者会尽快确认报告，在修复可用前请给予合理的协调披露时间。

## Security model

HuanMo binds to `127.0.0.1` and performs document processing locally. It is not designed to be exposed to a public network or run as a multi-user server. Do not change the bind address to `0.0.0.0` on an untrusted network.
