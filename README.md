# IPA IME — IPA 國際音標輸入法

基於 **Rime 輸入法引擎**（小狼毫 / Weasel）的 IPA 輸入方案。
使用英文字串對應 IPA 符號，支援四層編碼：X-SAMPA、描述式、助記別名、Praat 三連碼。

> **狀態:** P3 POC（概念驗證）。碼表完整，行為待 Windows 實測驗證。

---

## 特色

- **四層多對一編碼**：同一符號可用四種方式打出，不同背景使用者各取所需。
  - X-SAMPA（標準、最短）：`S` → ʃ
  - 描述式（可生成、自我說明）：`paf` → ʃ（postalveolar fricative）
  - 助記別名：`sh` → ʃ
  - Praat 三連碼：`\sh` → ʃ
- **注音式輸入**：選字累積於緩衝，按 Enter 整串上屏；不唯一匹配自動上屏。
- **2020 官方 IPA 表全覆蓋**：子音、母音、附加符號、超音段、聲調（173 個符號，497 條碼）。
- **保留跨平台可能**：方案資產為標準 Rime schema，可移植至 macOS（鼠鬚管）、Linux（ibus-rime）、Android（trime）。
- **開源 / 個人使用優先**：GPL v3，與 Rime 授權相容。

---

## 快速安裝（Windows + 小狼毫）

1. 從 [小狼毫官網](https://rime.im) 安裝 Weasel。
2. 下載本 repo（`Code → Download ZIP` 或 `git clone`）。
3. 開啟使用者資料夾：系統匣右鍵小狼毫圖示 →「用戶文件夾」（`%AppData%\Rime`）。
4. 複製 `rime/` 下的三個檔案進去：
   ```
   ipa.schema.yaml
   ipa.dict.yaml
   default.custom.yaml   ← 若已有此檔，請合併 patch 段落（見下方說明）
   ```
5. 系統匣右鍵 →「重新部署」（首次稍慢，需編譯碼表）。
6. 任一輸入框按 **F4**，選「IPA 國際音標」即可使用。

**default.custom.yaml 合併說明**：若 `%AppData%\Rime` 已有此檔，不要整個覆蓋，
只需把以下兩行加進既有檔的 `patch:` 段落：
```yaml
  schema_list/@next:
    schema: ipa
```

---

## 資料夾結構

```
ipa-ime/
├── master/
│   ├── build_master.py   # Master 主資料來源產生器（P2）
│   ├── IPA_master.csv    # 單一事實來源：173 個符號，含四層碼 + 中英描述
│   └── README.md         # 欄位 schema 與建表查核說明
├── rime/
│   ├── gen_rime.py       # Rime 方案產生器（P3）
│   ├── ipa.schema.yaml   # ★ Rime 方案設定（產生檔）
│   ├── ipa.dict.yaml     # ★ 碼表 497 條（產生檔）
│   └── default.custom.yaml  # ★ 掛載方案（產生檔）
├── spec/
│   ├── system-spec-v0.2.md    # 系統規格書
│   └── encoding-spec-v0.4.md  # 編碼方案規格（四層碼設計）
├── docs/
│   └── poc-test-guide.md      # P3 POC 安裝與測試指引（六個驗證點）
├── .gitignore
├── LICENSE                    # GPL v3
└── README.md                  # 本檔
```

> **★ 產生檔**：`rime/` 下的 YAML 為產生檔，刻意納入版控讓使用者可直接安裝。
> 修改請從 `master/IPA_master.csv` 改起，改完後重跑產生器（見下）。

---

## 開發流程

### 修改碼表 / 新增符號
```bash
# 1. 編輯 master/build_master.py（修改符號資料或規則）
python3 master/build_master.py          # 重新產生 IPA_master.csv

# 2. 產生 Rime 方案資產
python3 rime/gen_rime.py \
    --master master/IPA_master.csv \
    --outdir rime \
    --lang zh                           # 或 en

# 產生器內建全層撞名檢查 + delimiter 衝突檢查，有問題會中止並報錯。
```

### 編碼設計規則（概要）
詳見 `spec/encoding-spec-v0.4.md`。

- **描述式碼**：子音 = `[v]`（濁音）+ 部位(2字) + 方法(1字)；母音 = 高低(2字) + 前後(1字) + `[r]`（圓唇）。清音/不圓唇省略。
- **分隔符**：`;`（掃描全碼表後確認未被任何碼使用）。
- **主流撞名定義**：ARPABET、X-SAMPA、Praat、Kirshenbaum/Usenet、Worldbet。

### POC 測試
安裝後依 `docs/poc-test-guide.md` 跑六個驗證點。V1（注音式緩衝 + Enter 上屏）為最高風險點。

---

## 待完成（路線圖）

- **P3 POC 驗證**：Windows 實測六個驗證點，回報結果後修 schema 出 0.1.1。
- **P4 碼表完整化**：預生成常見「基底 + 附加符號」組合（解跨次上屏無法 NFC 的限制）。
- **P5 候選說明**：以 librime-lua filter 在候選旁顯示中文描述（`desc_zh` 欄）。
- **Praat 全碼覆核**：對 Praat 官方手冊做最終確認（目前 165/173 自維基對照表轉錄）。
- **X-SAMPA 全表覆核**：對照權威 X-SAMPA 參照校驗（聲調表記尤須確認）。
- **可選字型**：Charis SIL / Gentium（OFL）打包為可選安裝元件。
- **跨平台移植**：macOS / Linux / Android（保留可能，非首版範圍）。

---

## 授權

本專案以 **GPL v3** 授權，與底層 Rime 引擎授權相容。
可選附帶字型（Charis SIL / Gentium）以 **SIL Open Font License 1.1** 授權。

---

## 致謝

- [Rime 輸入法引擎](https://rime.im)（佛振 et al.）
- [國際語音學學會 IPA 官方表（2020）](https://www.internationalphoneticassociation.org/content/ipa-chart)
- X-SAMPA 設計者 John C. Wells
- Praat（Paul Boersma & David Weenink）
