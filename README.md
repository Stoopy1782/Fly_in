# Fly_in

ドローン経路シミュレーション。マップファイルを読み込み、ゾーン・ルート・ドローンの状態を表示します。

## 必要なもの

- Python 3.10 以上
- [uv](https://docs.astral.sh/uv/)(Python パッケージマネージャ)

uv が未インストールの場合:

```sh
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## セットアップ

```sh
make install
```

`uv sync` で `uv.lock` から依存関係をインストールし、`.venv` を再生成します。

## 実行

```sh
make run            # medium/02 のマップで実行
```

任意のマップを指定する場合:

```sh
uv run python3 src/main.py --file_path=maps/easy/01_linear_path.txt
```

利用できるマップは `maps/easy`, `maps/medium`, `maps/hard`, `maps/challenger` にあります。

## その他のコマンド

```sh
make debug          # pdb 付きで起動
make lint           # flake8 + mypy
make lint-strict    # mypy --strict
make clean          # キャッシュ削除
```
