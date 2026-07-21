# 张微青的金融科技项目

这是一个用于学习金融科技开发的 Python 项目。当前示例使用 `Decimal` 计算单利，避免浮点数处理金额时的精度问题。

## 目录结构

```text
project1/
├── .env.example
├── .gitignore
├── requirements.txt
├── src/
│   ├── __init__.py
│   └── main.py
└── tests/
    ├── __init__.py
    └── test_main.py
```

## 运行示例

```bash
python -m src.main
```

预期输出：

```text
Simple interest: 350.00
```

## 运行测试

```bash
python -m unittest discover -s tests -v
```

## 密钥安全

1. 复制 `.env.example` 为 `.env`。
2. 只在本地 `.env` 中填写真实 API Key。
3. `.env` 已被 `.gitignore` 排除，不应提交到 GitHub。
4. 提交前先执行 `git status` 检查文件清单。
