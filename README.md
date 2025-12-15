# 外交青書2025 テキストマイニング分析

外務省が発行する「外交青書2025」第1章「国際情勢認識と日本外交の展望」を対象としたテキストマイニング分析のサンプルプロジェクトです。

## 概要

このリポジトリでは、日本語PDFドキュメントに対して以下のテキストマイニング手法を実装しています：

- **形態素解析**: Janomeを使用した日本語テキストの単語分解
- **単語頻度分析**: 出現頻度の高いキーワードの特定
- **共起分析**: 同時に出現する単語ペアの分析とネットワーク可視化
- **ワードクラウド**: 単語頻度の視覚化

## ファイル構成

```
textmining-samples/
├── 1_2_1.pdf                      # 分析対象PDF（外交青書2025 第1章）
├── text_mining_analysis.ipynb     # Python版 Jupyterノートブック（実行結果付き）
├── text_mining_analysis_r.ipynb   # R版 Jupyterノートブック
├── word_frequency_analysis.py     # 単語頻度分析スクリプト
├── wordcloud_generator.py         # ワードクラウド生成スクリプト
├── word_frequency_results.csv     # 単語頻度分析結果
├── cooccurrence_results.csv       # 共起分析結果
├── wordcloud.png                  # ワードクラウド画像
├── stop_words.csv                 # ストップワード一覧
├── abstract.md                    # PDF要約
└── README.md                      # このファイル
```

## 必要環境

### Python版
- Python 3.8以上
- 日本語フォント（Noto Sans CJK等）

### R版（オプション）
- R 4.0以上
- MeCab（日本語形態素解析エンジン）
- IRkernel（JupyterでRを実行するためのカーネル）

## インストール

### 1. リポジトリのクローン

```bash
git clone https://github.com/kkawailab/textmining-samples.git
cd textmining-samples
```

### 2. 仮想環境の作成（推奨）

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# または
.\venv\Scripts\activate   # Windows
```

### 3. 依存パッケージのインストール

```bash
pip install pdfplumber janome wordcloud matplotlib japanize-matplotlib networkx jupyter
```

### 4. R環境のセットアップ（R版を使用する場合）

#### MeCabのインストール

**Ubuntu/Debian:**
```bash
sudo apt-get install mecab libmecab-dev mecab-ipadic-utf8
```

**macOS:**
```bash
brew install mecab mecab-ipadic
```

#### Rパッケージのインストール

```r
install.packages(c("pdftools", "RMeCab", "dplyr", "tidyr", "ggplot2",
                   "igraph", "wordcloud2", "stringr", "htmlwidgets"))
```

#### IRkernelのインストール（JupyterでR使用）

```r
install.packages("IRkernel")
IRkernel::installspec()
```

## 使い方

### Jupyterノートブックで実行（推奨）

統合ノートブックには全ての分析が含まれており、実行結果も確認できます。

```bash
jupyter notebook text_mining_analysis.ipynb
```

ノートブックの構成：

| セクション | 内容 |
|-----------|------|
| 1. 環境設定 | ライブラリのインポート |
| 2. 設定とパラメータ | 分析パラメータの定義 |
| 3. PDFからテキスト抽出 | pdfplumberでテキスト抽出 |
| 4. テキストの前処理 | クリーニング処理 |
| 5. 形態素解析 | Janomeで単語分解 |
| 6. 単語頻度分析 | 出現回数カウント・可視化 |
| 7. 共起分析 | 単語ペア分析・ネットワーク描画 |
| 8. 品詞別分析 | 品詞構成の分析 |
| 9. ワードクラウド生成 | 視覚化 |
| 10. 結果の保存 | CSV出力 |
| 11. 分析結果のまとめ | サマリー表示 |

### R版ノートブックで実行

R環境とMeCabが設定済みの場合、R版でも同様の分析が可能です。

```bash
jupyter notebook text_mining_analysis_r.ipynb
```

R版ノートブックの構成：

| セクション | 内容 |
|-----------|------|
| 1. 環境設定 | ライブラリの読み込み |
| 2. 設定とパラメータ | 分析パラメータの定義 |
| 3. PDFからテキスト抽出 | pdftoolsでテキスト抽出 |
| 4. テキストの前処理 | クリーニング処理 |
| 5. 形態素解析 | RMeCabで単語分解 |
| 6. 単語頻度分析 | 出現回数カウント・可視化 |
| 7. 共起分析 | 単語ペア分析・igraphでネットワーク描画 |
| 8. 品詞別分析 | 品詞構成の分析 |
| 9. ワードクラウド生成 | wordcloud2で視覚化 |
| 10. 結果の保存 | CSV出力 |
| 11. 分析結果のまとめ | サマリー表示 |

### 個別スクリプトで実行

#### 単語頻度分析

```bash
python word_frequency_analysis.py
```

出力：
- コンソールに上位30語のランキング表示
- `word_frequency_results.csv` に全単語の頻度データを保存

#### ワードクラウド生成

```bash
python wordcloud_generator.py
```

出力：
- `wordcloud.png` にワードクラウド画像を保存

## 分析結果

### 基本統計

| 項目 | 値 |
|------|-----|
| 抽出文字数 | 6,547文字 |
| 総単語数 | 1,387語 |
| ユニーク単語数 | 586語 |
| 共起ペア数 | 445ペア |

### 単語頻度ランキング（上位10語）

| 順位 | 単語 | 出現回数 |
|------|------|----------|
| 1 | 国際 | 56 |
| 2 | 社会 | 29 |
| 3 | 経済 | 20 |
| 4 | 日本 | 17 |
| 5 | 安全 | 16 |
| 6 | 秩序 | 15 |
| 7 | 課題 | 15 |
| 8 | 含む | 15 |
| 9 | 重要 | 14 |
| 10 | 情勢 | 13 |

### 共起頻度ランキング（上位5ペア）

| 順位 | 単語ペア | 共起回数 |
|------|----------|----------|
| 1 | 国際 - 社会 | 24 |
| 2 | 国際 - 秩序 | 12 |
| 3 | 保障 - 安全 | 11 |
| 4 | 国際 - 情勢 | 9 |
| 5 | 国際 - 日本 | 8 |

### ワードクラウド

![ワードクラウド](wordcloud.png)

## カスタマイズ

### ストップワードの変更

`stop_words.csv` または各スクリプト内の `STOPWORDS` 変数を編集してください。

```python
STOPWORDS = {
    'こと', 'もの', 'ため', 'よう',  # 形式名詞
    'する', 'いる', 'ある', 'なる',  # 補助動詞
    # ... 追加・削除
}
```

### 抽出品詞の変更

デフォルトでは名詞・動詞・形容詞を抽出しています。

```python
TARGET_POS = ['名詞', '動詞', '形容詞']
```

### ワードクラウドのスタイル変更

```python
WORDCLOUD_CONFIG = {
    'width': 1200,           # 画像幅
    'height': 800,           # 画像高さ
    'background_color': 'white',
    'max_words': 100,        # 最大単語数
    'colormap': 'viridis',   # カラーマップ（plasma, inferno, magma等）
}
```

## 使用ライブラリ

### Python版

| ライブラリ | 用途 |
|-----------|------|
| pdfplumber | PDFからテキスト抽出 |
| Janome | 日本語形態素解析 |
| wordcloud | ワードクラウド生成 |
| matplotlib | グラフ・画像表示 |
| japanize-matplotlib | matplotlib日本語対応 |
| networkx | 共起ネットワーク可視化 |

### R版

| ライブラリ | 用途 |
|-----------|------|
| pdftools | PDFからテキスト抽出 |
| RMeCab | 日本語形態素解析（MeCab使用） |
| dplyr, tidyr | データ操作 |
| ggplot2 | グラフ・画像表示 |
| igraph | 共起ネットワーク可視化 |
| wordcloud2 | ワードクラウド生成 |
| stringr | 文字列処理 |

## ライセンス

このプロジェクトはサンプルコードとして公開しています。
分析対象のPDFファイル（外交青書）の著作権は外務省に帰属します。

## 参考資料

### Python版
- [外務省 外交青書](https://www.mofa.go.jp/mofaj/gaiko/bluebook/)
- [Janome ドキュメント](https://mocobeta.github.io/janome/)
- [wordcloud ドキュメント](https://amueller.github.io/word_cloud/)

### R版
- [RMeCab ドキュメント](https://sites.google.com/site/rmaborakaba/)
- [pdftools ドキュメント](https://docs.ropensci.org/pdftools/)
- [igraph for R](https://r.igraph.org/)
- [wordcloud2 ドキュメント](https://github.com/Lchiffon/wordcloud2)

---

## 更新履歴

### 2025-12-15

#### v1.2.0
- R版Jupyterノートブック（`text_mining_analysis_r.ipynb`）を追加
  - pdftoolsによるPDFテキスト抽出
  - RMeCabによる形態素解析
  - igraphによる共起ネットワーク可視化
  - wordcloud2によるワードクラウド生成
- READMEにR環境セットアップ手順を追加
- 使用ライブラリ一覧をPython版/R版に分離

#### v1.1.0
- Jupyterノートブック形式（`text_mining_analysis.ipynb`）を追加
- 共起分析機能を追加
  - 文単位での共起頻度計算
  - networkxによる共起ネットワーク可視化
  - キーワード別共起単語分析
- 共起分析結果（`cooccurrence_results.csv`）を追加
- ノートブックに実行結果を含めて保存

#### v1.0.0
- 初回リリース
- PDFテキスト抽出機能
- 形態素解析（Janome）
- 単語頻度分析
- ワードクラウド生成
- ストップワード定義
- PDF要約（`abstract.md`）
