#!/usr/bin/env python3
"""
外交青書PDF 形態素解析・単語頻度分析スクリプト
"""

import re
from collections import Counter
from pathlib import Path

# PDF読み込み用
try:
    import pdfplumber
except ImportError:
    print("pdfplumberをインストールしてください: pip install pdfplumber")
    exit(1)

# 形態素解析用（Janomeを使用 - 純粋Pythonで依存関係が少ない）
try:
    from janome.tokenizer import Tokenizer
except ImportError:
    print("Janomeをインストールしてください: pip install janome")
    exit(1)


def extract_text_from_pdf(pdf_path: str) -> str:
    """PDFからテキストを抽出"""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def clean_text(text: str) -> str:
    """テキストのクリーニング"""
    # 数字、英字、記号などを除去
    text = re.sub(r'[0-9０-９]+', '', text)
    text = re.sub(r'[a-zA-Zａ-ｚＡ-Ｚ]+', '', text)
    text = re.sub(r'[（）()【】「」『』・、。：；！？\s\n]+', ' ', text)
    text = re.sub(r'[^\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\s]', '', text)
    return text


def analyze_morphology(text: str, target_pos: list = None) -> list:
    """
    形態素解析を実行し、指定した品詞の単語を抽出

    Args:
        text: 解析対象のテキスト
        target_pos: 抽出対象の品詞リスト（デフォルト: 名詞、動詞、形容詞）

    Returns:
        抽出された単語のリスト
    """
    if target_pos is None:
        target_pos = ['名詞', '動詞', '形容詞']

    tokenizer = Tokenizer()
    words = []

    # ストップワード（除外する一般的な単語）
    stopwords = {
        'こと', 'もの', 'ため', 'よう', 'これ', 'それ', 'あれ',
        'ここ', 'そこ', 'あそこ', 'どこ', 'どれ', 'なに', '何',
        'する', 'いる', 'ある', 'なる', 'れる', 'られる', 'せる',
        'できる', 'おる', 'くる', '来る', '行く', 'いく',
        'この', 'その', 'あの', 'どの', 'ない', 'なく',
        '等', '的', '化', '性', '上', '中', '下', '内', '外',
        '年', '月', '日', '号', '第', '章', 'ほか', 'また',
        'および', 'かつ', 'ただし', 'なお', 'または'
    }

    for token in tokenizer.tokenize(text):
        pos = token.part_of_speech.split(',')[0]  # 品詞の大分類
        pos_detail = token.part_of_speech.split(',')[1] if ',' in token.part_of_speech else ''

        # 指定した品詞かつストップワードでない場合
        if pos in target_pos:
            # 名詞の場合、非自立・代名詞・数は除外
            if pos == '名詞' and pos_detail in ['非自立', '代名詞', '数']:
                continue

            word = token.base_form if token.base_form != '*' else token.surface

            # 1文字の単語とストップワードを除外
            if len(word) > 1 and word not in stopwords:
                words.append(word)

    return words


def display_frequency(word_counts: Counter, top_n: int = 30) -> None:
    """頻度分析結果を表示"""
    print("\n" + "=" * 60)
    print(f"単語頻度分析結果（上位{top_n}語）")
    print("=" * 60)
    print(f"{'順位':<6}{'単語':<20}{'出現回数':<10}{'棒グラフ'}")
    print("-" * 60)

    max_count = word_counts.most_common(1)[0][1] if word_counts else 1

    for rank, (word, count) in enumerate(word_counts.most_common(top_n), 1):
        bar_length = int(count / max_count * 30)
        bar = "█" * bar_length
        print(f"{rank:<6}{word:<20}{count:<10}{bar}")


def save_results(word_counts: Counter, output_path: str) -> None:
    """結果をCSVファイルに保存"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("順位,単語,出現回数\n")
        for rank, (word, count) in enumerate(word_counts.most_common(), 1):
            f.write(f"{rank},{word},{count}\n")
    print(f"\n結果を {output_path} に保存しました")


def main():
    # PDFファイルのパス
    pdf_path = Path(__file__).parent / "1_2_1.pdf"

    if not pdf_path.exists():
        print(f"エラー: {pdf_path} が見つかりません")
        return

    print("=" * 60)
    print("外交青書PDF 形態素解析・単語頻度分析")
    print("=" * 60)

    # 1. PDFからテキスト抽出
    print("\n[1/4] PDFからテキストを抽出中...")
    raw_text = extract_text_from_pdf(str(pdf_path))
    print(f"     抽出文字数: {len(raw_text):,} 文字")

    # 2. テキストクリーニング
    print("\n[2/4] テキストをクリーニング中...")
    cleaned_text = clean_text(raw_text)
    print(f"     クリーニング後: {len(cleaned_text):,} 文字")

    # 3. 形態素解析
    print("\n[3/4] 形態素解析を実行中...")
    words = analyze_morphology(cleaned_text)
    print(f"     抽出単語数: {len(words):,} 語")
    print(f"     ユニーク単語数: {len(set(words)):,} 語")

    # 4. 頻度分析
    print("\n[4/4] 頻度分析を実行中...")
    word_counts = Counter(words)

    # 結果表示
    display_frequency(word_counts, top_n=30)

    # 結果をCSVに保存
    output_path = Path(__file__).parent / "word_frequency_results.csv"
    save_results(word_counts, str(output_path))

    # 品詞別の統計
    print("\n" + "=" * 60)
    print("品詞別分析")
    print("=" * 60)

    tokenizer = Tokenizer()
    pos_counts = Counter()
    for token in tokenizer.tokenize(cleaned_text):
        pos = token.part_of_speech.split(',')[0]
        pos_counts[pos] += 1

    print(f"{'品詞':<15}{'出現回数':<10}")
    print("-" * 25)
    for pos, count in pos_counts.most_common(10):
        print(f"{pos:<15}{count:<10}")


if __name__ == "__main__":
    main()
