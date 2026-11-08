# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：
  - 第1回の素のLLMは講座の用語を知らず、一般論や「分からない」と答えることが多かった。
  - エージェントは用語集を検索した上で、定義に基づいて具体的に答えた（例: 宿題の3レベルについて基礎・実装・発展と正しく説明）。

- `--trace` で見えたツール呼び出し（ツール名と引数）：
  - search_glossary（query: 'LoRA'）
  - search_glossary（query: 'QLoRA'）

- 1つの質問での LLM 呼び出し回数（`requests`）：
  - 2（ツール呼び出しも2回）

- 追加したツールと、docstring に書いた説明：
  - 今回はツールの追加は行わず、既存の search_glossary と get_lecture_summary の動作確認まで行った。

## 宿題

- 取り組んだレベル：基礎

- やったこと：
  - `app/agent.py` の INSTRUCTIONS から「用語や講座に固有のことを答える前に、必ず search_glossary で用語集を確認する。」の行を完全に削除した。
  - `app/tools.py` の `search_glossary` の docstring を「ツールの使用を禁止する」に変更した。
  - 同じ質問「LoRA と QLoRA の違いは？」を `--trace` 付きで実行し、変更前後を比較した。

- 結果：
  - 変更前：search_glossary を2回呼び出し（LoRA と QLoRA を別々）、requests は2。回答は用語集の定義に基づく。
  - 変更後（INSTRUCTIONSの該当行を完全削除 + docstringで使用禁止）：search_glossary を2回呼び出し（引数も同じ）、requests は2。回答の内容もほぼ同じ。

- 気づき・疑問：
  - INSTRUCTIONS から「必ず検索する」を完全に削除し、さらにツールの docstring で「使用を禁止する」と明記しても、ツールの呼び出し回数や引数は変わらなかった。
  - モデルは利用可能なツールがあると積極的に使う傾向が強く、指示文や docstring の変更だけではツールの使用を止めにくいことがわかった。