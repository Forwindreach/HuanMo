# 参与贡献 / Contributing

感谢你愿意帮助换墨变得更好。Bug 报告、功能建议、文档改进、测试和代码贡献都很有价值。

Thank you for helping improve HuanMo. Bug reports, feature proposals, documentation, tests, and code contributions are all welcome.

## 提交问题

- Bug 请使用 Bug 模板，并附上系统版本、换墨版本、复现步骤和错误信息。
- 功能建议请描述真实使用场景，而不仅是期望的实现方式。
- 涉及隐私或安全的问题请按 [SECURITY.md](SECURITY.md) 私下报告，不要创建公开 Issue。
- 请勿上传包含个人信息、证件、合同或其他敏感数据的示例文件；优先使用脱敏或人工构造的样例。

## 本地开发

需要 Python 3.9+。建议使用虚拟环境：

```bash
git clone https://github.com/Forwindreach/HuanMo.git
cd HuanMo
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r md2pdf_app/requirements.txt
python -m pip install pytest
python md2pdf_app/app.py
```

浏览器访问 <http://127.0.0.1:5199>。

## 测试

提交前请至少运行：

```bash
python -m py_compile md2pdf_app/app.py build_app.py
python -m pytest -q
```

涉及界面时，请手动验证三个模式；涉及扫描算法时，请覆盖彩色、黑白、横向、透视和无明显纸张边缘的图片。

## Pull Request

1. 从 `main` 创建范围清晰的分支。
2. 保持提交聚焦，避免把无关格式化混入功能改动。
3. 更新相关文档与测试。
4. 在 PR 中说明问题、方案、验证方式和可见变化。
5. 确认没有提交真实用户文档、密钥、构建产物或临时文件。

维护者会重点关注隐私边界、跨平台行为、输出兼容性和发布包体积。
