# IPA 輸入法 — Master 主資料來源 (P2)

**檔案：** `IPA_master.csv`（資料）、`build_master.py`（產生器）
**依據：** 編碼方案規格 v0.4
**用途：** 單一事實來源（single source of truth）。P3 之產生器依語言參數讀取此檔，輸出 Rime 方案資產（schema/碼表）。

## 內容統計
共 **171 列**：肺氣流子音 59、其他符號 10、非肺氣流 11、母音 28、塞擦音 5、附加符號 31、超音段 9、聲調（調符 7 + 調値字母 7 + 其他 4）。

## 欄位 schema

| 欄位 | 說明 |
|---|---|
| `id` | 列識別碼（類別前綴 + 序號，如 PUL002） |
| `category` | 類別：pulmonic / other / nonpulmonic / vowel / affricate / diacritic / suprasegmental / tone_diacritic / tone_letter / tone_other |
| `symbol` | IPA 符號（組合附加符號以 ◌ U+25CC 示意；塞擦音為帶連結弧序列） |
| `codepoint` | Unicode 碼點（序列以空白分隔） |
| `xsampa` | X-SAMPA 主碼（唇齒閃音 ⱱ 留空；調値字母無標準 X-SAMPA） |
| `descriptive` | 描述式碼（緊湊版；規則見下） |
| `mnemonic` | 助記別名；多值以 `;` 分隔（如 `jh;dj`） |
| `mnemonic_source` | 助記來源（ARPABET / 符號本名 / 某語言拼寫 等） |
| `praat` | Praat 反斜線碼；**已轉錄 163/171**（自維基對照表）。空白 8 列：5 塞擦音 + 2 連調字母為組合式（無單一 Praat 碼）、小句群 1 列待確認 |
| `desc_en` | 英文描述（由特徵生成） |
| `desc_zh` | 中文描述（由特徵生成） |
| `notes` | 備註（如 spacing / combining） |

## 描述式碼規則（由 `build_master.py` 程式化生成）
- 子音：`[v]` + 部位(2) + 方法(1，複合方法 2)。清音省略、濁音前綴 `v`（僅阻礙音）。
- 母音：高低(2) + 前後(1) + `[r]`。不圓唇省略、圓唇後綴 `r`。
- 聲調：調符 `td*`、調値字母 `tl*`（Chao 數字串）。
- 多對一：同一符號的 xsampa／descriptive／mnemonic（可多個）／praat 全部指向同一輸出。

## 來源關係（重要）
- `descriptive`、`desc_en`、`desc_zh` 為**衍生欄**，由 `build_master.py` 中的特徵字典（部位/方法/高低/前後）生成。要改這些，請改規則/特徵後重跑產生器，**勿**直接手改 CSV，以維持一致性。
- `mnemonic`、`mnemonic_source`、`praat`、`xsampa` 可於資料層直接維護。
- i18n：`desc_en`/`desc_zh` 即語言欄；新增語言＝加一欄描述，碼不變。

## 內部一致性
已通過內部撞名檢查：`xsampa`、`descriptive`、`mnemonic` 各層及「描述式×助記」跨層，**零**「不同符號共用同碼」。

## 待完成（建表查核，承接編碼規格 v0.4 §8）
1. **Praat 轉錄（大致完成）**：163/171 已自維基「Comparison of ASCII encodings of the IPA」對照表轉錄（2025）。剩 8 列：5 塞擦音與 2 連調字母（˩˥/˥˩）為**組合式**（成分碼 + 連結 `\li`，無單一 Praat 碼）、小句群 `|` 一列**待對 Praat 官方手冊確認**。建議全表最終對 Praat 手冊覆核一次（本轉錄來源為維基對照表，非一手）。
2. **主流撞名掃描（已完成，裁定 A）**：助記碼對**現行主流**（ARPABET、X-SAMPA、Praat、Kirshenbaum/Usenet、Worldbet）**零撞名**。三處對冷僻/舊系統的邊界撞名（`dj`↔UPSID 之 ɟ、`oe`↔PHONASCII 之 ø、`ao`↔PHONASCII 之 ɒ）經裁定：UPSID（語音資料庫）與 PHONASCII（1988 年舊系統）**不視為現行主流輸入記法**，三碼**全部保留**。收錄規則 §4 之「主流」自此明確界定為：ARPABET、X-SAMPA、Praat、Kirshenbaum/Usenet、Worldbet。
3. **X-SAMPA 全表覆核**：對照權威 X-SAMPA 參照最後校驗（聲調 `_T/_H…` 尤須確認）。
4. 偏好項：ʔ 是否補助記（視頻率）。

## 下一步（P3）
撰寫產生器：讀本 CSV，依指定語言輸出 Rime `schema.yaml` / 碼表 / `default.yaml`，並驗證注音式行為（`auto_select=false`、Enter 上屏、候選確認）與 Praat 標點納入 alphabet 之優先序。
