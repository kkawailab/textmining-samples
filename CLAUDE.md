# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Japanese text mining analysis project for "Diplomatic Bluebook 2025" (外交青書2025). Implements morphological analysis, word frequency analysis, co-occurrence analysis, and word cloud generation for Japanese PDF documents.

## Commands

### Environment Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install pdfplumber janome wordcloud matplotlib japanize-matplotlib networkx jupyter
```

### Run Analysis Scripts
```bash
# Word frequency analysis (generates word_frequency_results.csv)
python word_frequency_analysis.py

# Word cloud generation (requires word_frequency_results.csv first)
python wordcloud_generator.py
```

### Run Jupyter Notebook
```bash
jupyter notebook text_mining_analysis.ipynb
```

### Execute Notebook and Save Outputs
```bash
python -m jupyter nbconvert --to notebook --execute --inplace text_mining_analysis.ipynb
```

## Architecture

### Data Flow
1. PDF (`1_2_1.pdf`) → pdfplumber extracts text
2. Text → clean_text() removes numbers, English, symbols
3. Cleaned text → Janome tokenizer performs morphological analysis
4. Tokens → filter by POS (名詞/動詞/形容詞), remove stopwords
5. Words → Counter for frequency analysis, combinations for co-occurrence
6. Results → CSV files, word cloud image, network visualization

### Key Components

**word_frequency_analysis.py**: Standalone script for morphological analysis
- `extract_text_from_pdf()`: PDF text extraction
- `clean_text()`: Text preprocessing with regex
- `analyze_morphology()`: Janome tokenization with POS filtering
- Outputs: console ranking + `word_frequency_results.csv`

**wordcloud_generator.py**: Word cloud from frequency CSV
- `find_japanese_font()`: Auto-detects CJK fonts across OS
- `generate_wordcloud()`: Creates visualization
- Requires: `word_frequency_results.csv` from frequency analysis

**text_mining_analysis.ipynb**: Complete analysis pipeline with outputs
- All functionality from both scripts
- Co-occurrence analysis with networkx
- Pre-executed cells with results

### Stopwords
Defined in scripts as `STOPWORDS` set. Categories:
- 形式名詞: こと, もの, ため, よう
- 補助動詞: する, いる, ある, なる
- 指示詞: この, その, あの
- 接尾辞: 等, 的, 化, 性

Also available in `stop_words.csv` for reference.

### Japanese Font Detection
Scripts auto-detect fonts in order: ChromeOS Noto → Linux Noto → IPA Gothic → macOS Hiragino → Windows Meiryo
