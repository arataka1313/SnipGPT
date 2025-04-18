# SnipGPT

[![Python CI](https://github.com/arataka1313/SnipGPT/actions/workflows/python.yml/badge.svg)](https://github.com/arataka1313/SnipGPT/actions/workflows/python.yml)

スクリーンショットから問題をキャプチャし、ChatGPT に送信して自動で解答・保存するツールです。

## セットアップ

1. `.env.example` を `.env` にコピーし、`OPENAI_API_KEY=sk-○△×` の `sk-` 以下を自分の OpenAI APIキーに書き換えてください。
2. 必要ライブラリをインストール：
   ```bash
   pip install -r requirements.txt
   ```
3. `SnipGPT.py` を実行してスタート！

## 使用方法

- 実行すると即座に画面キャプチャが始まります。
- ChatGPTが画像を読み取り、回答を `answer/` に保存します。
- 画像は `problems/` に自動で整理されます。

## 注意事項

- このツールが提供する解答はあくまでAIによる自動出力であり、**100%の正確性は保証されません**。
- 出力結果を鵜呑みにせず、**自ら検証することを推奨します**。

## 免責事項

- このプログラムの利用によって発生したいかなる損害・損失に対しても、作成者は一切の責任を負いません。
- 利用は自己責任でお願いします。

## ライセンス

このリポジトリは [MIT License](LICENSE) のもとで公開されています。

## CI/CD（GitHub Actions 例）

`.github/workflows/python.yml` に以下のような設定を追加することで、CI環境でLintチェックなどが行えます：

```yaml
name: Python CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Lint with flake8
        run: |
          pip install flake8
          flake8 .
```

---

🚀 ご自由にフォーク・改善・提案してください！
