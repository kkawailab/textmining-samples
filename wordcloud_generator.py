#!/usr/bin/env python3
"""
単語頻度データからワードクラウドを生成するスクリプト
"""

import csv
from pathlib import Path

try:
    from wordcloud import WordCloud
except ImportError:
    print("wordcloudをインストールしてください: pip install wordcloud")
    exit(1)

try:
    import matplotlib.pyplot as plt
    import japanize_matplotlib
except ImportError:
    print("matplotlibをインストールしてください: pip install matplotlib japanize-matplotlib")
    exit(1)


def load_word_frequencies(csv_path: str) -> dict:
    """CSVファイルから単語頻度データを読み込む"""
    word_freq = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            word = row['単語']
            count = int(row['出現回数'])
            word_freq[word] = count
    return word_freq


def find_japanese_font() -> str:
    """利用可能な日本語フォントを探す"""
    # 一般的な日本語フォントのパス
    font_paths = [
        # ChromeOS / Linux (Noto CJK fonts)
        '/usr/share/fonts/chromeos/notocjk/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/chromeos/notocjk/NotoSansCJK-Bold.ttc',
        '/usr/share/fonts/chromeos/notocjk/NotoSansCJK-Light.ttc',
        # Linux (Noto fonts)
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
        # Linux (IPAフォント)
        '/usr/share/fonts/ipa-gothic/ipag.ttf',
        '/usr/share/fonts/truetype/ipa-gothic/ipag.ttf',
        '/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf',
        '/usr/share/fonts/ipa-mincho/ipam.ttf',
        # Linux (Takaoフォント)
        '/usr/share/fonts/truetype/takao-gothic/TakaoGothic.ttf',
        # Linux (VLゴシック)
        '/usr/share/fonts/truetype/vlgothic/VL-Gothic-Regular.ttf',
        # Ubuntu/Debian
        '/usr/share/fonts/truetype/fonts-japanese-gothic.ttf',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        # macOS
        '/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc',
        '/System/Library/Fonts/Hiragino Sans GB.ttc',
        '/Library/Fonts/Arial Unicode.ttf',
        # Windows
        'C:/Windows/Fonts/msgothic.ttc',
        'C:/Windows/Fonts/meiryo.ttc',
    ]

    for font_path in font_paths:
        if Path(font_path).exists():
            return font_path

    return None


def generate_wordcloud(word_freq: dict, output_path: str, font_path: str = None) -> None:
    """ワードクラウドを生成して保存"""

    # 日本語フォントの設定
    if font_path is None:
        font_path = find_japanese_font()

    if font_path is None:
        print("警告: 日本語フォントが見つかりません。文字が正しく表示されない可能性があります。")
        font_path = None

    # ワードクラウドの設定
    wc = WordCloud(
        font_path=font_path,
        width=1200,
        height=800,
        background_color='white',
        max_words=100,
        max_font_size=150,
        min_font_size=10,
        colormap='viridis',  # カラーマップ
        prefer_horizontal=0.7,  # 横書きの割合
        relative_scaling=0.5,  # 頻度と文字サイズの関係
        random_state=42,  # 再現性のため
    )

    # ワードクラウド生成
    wc.generate_from_frequencies(word_freq)

    # 画像として保存（タイトルなしでシンプルに）
    plt.figure(figsize=(16, 10))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white', pad_inches=0.1)
    plt.close()

    print(f"ワードクラウドを保存しました: {output_path}")


def main():
    base_dir = Path(__file__).parent

    # 入力ファイル（頻度分析結果）
    input_csv = base_dir / "word_frequency_results.csv"

    if not input_csv.exists():
        print(f"エラー: {input_csv} が見つかりません")
        print("先に word_frequency_analysis.py を実行してください")
        return

    # 出力ファイル
    output_image = base_dir / "wordcloud.png"

    print("=" * 50)
    print("ワードクラウド生成")
    print("=" * 50)

    # 1. 単語頻度データを読み込み
    print("\n[1/2] 単語頻度データを読み込み中...")
    word_freq = load_word_frequencies(str(input_csv))
    print(f"     読み込み単語数: {len(word_freq)} 語")

    # 上位10語を表示
    print("\n     上位10語:")
    for i, (word, count) in enumerate(sorted(word_freq.items(), key=lambda x: -x[1])[:10], 1):
        print(f"     {i:2}. {word}: {count}回")

    # 2. ワードクラウド生成
    print("\n[2/2] ワードクラウドを生成中...")
    generate_wordcloud(word_freq, str(output_image))

    print("\n" + "=" * 50)
    print("完了!")
    print("=" * 50)


if __name__ == "__main__":
    main()
