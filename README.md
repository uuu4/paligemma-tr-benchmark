# PaliGemma 2 on Turkish text: 224 vs 448

Companion code for the blog post *What Happens If You Give Eyes to a Language Model?* (reading Google's PaliGemma 2 paper, testing it on Turkish text).

11 photos I took myself (7 receipts, 3 cigarette boxes, 1 sign), `paligemma2-3b-mix-224` and `-448`, greedy decoding, `max_new_tokens=100`. The photos are not in this repo.

## Files

| File | What it is |
|---|---|
| `paligemma2_tr_ocr_v3.ipynb` | Current notebook (Colab, T4): 5 prompts, targets, full texts, scoring, tables. Notebook text is in Turkish. |
| `results/sonuclar_v3.csv` | Raw outputs of the v3 session (3 repeats, 330 rows). |
| `results/sonuclar_v3_puanli.csv` | Same, with the word-match score and the invented-word count. |
| `results/sonuclar_v2.csv` | Raw outputs of the v2 session (5 prompts, 110 rows). Table 1 in the post was computed from this. |
| `results/sonuclar_v1.csv` | Raw outputs of the first session (3 prompts, 66 rows). |
| `compare_sessions.py` | Compares the three sessions (`python compare_sessions.py`, no dependencies). |
| `paligemma2_tr_ocr.ipynb` | The first notebook (v1, 3 prompts). Kept for reference. |

## Things to know

- **Targets were corrected.** In v1/v2 the target for receipt 1 was `gürme`; the photo says `GURME`. Receipt 5's target was `ŞTİ`; the photo says `STI`. The fixed targets change the receipt rows of Table 1 and Table 2 (receipt `ocr`: 74/75 became 70/78 in the v2 session).
- **Repeats inside one session are identical.** Three repeats in the v3 session gave the same text in 110 of 110 cells. The variation is **between Colab sessions** (28 to 46 of the outputs differ between any two sessions).
- **Metric:** the share of the first words of the text (receipt: business name; box and sign: start of the warning) that appear exactly in the output, Turkish characters included. It ignores order.
- **Invented words:** words in the output that are not on the photo and not similar (ratio < 0.7) to any word on it, so a one-letter slip is not counted. The full texts (`TAM_METIN` in the notebook) are my own reading of the photos; very small print and mirrored text on the back of receipts are not included. Card digits were removed from the published copy (digits are not counted anyway).
- N=11, three boxes of one brand and one sign. This is a hint, not a result.
