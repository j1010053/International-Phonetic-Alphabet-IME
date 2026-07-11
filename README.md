# IPA IME — 國際音標 Windows 輸入法

基於 [Rime 輸入法引擎](https://rime.im)（小狼毫 / Weasel）的 IPA 輸入方案。
授權：開源（GPL v3，與 Rime 相容）。

## 簡介

本專案為 2020 官方 IPA 表所列全部符號提供四層 ASCII 輸入碼：

| 層 | 範例 | 說明 |
|---|---|---|
| X-SAMPA | `S` → ʃ | 國際標準，最短 |
| 助記 | `sh` → ʃ | 英語直覺拼音，依 ARPABET 等 |
| 描述式 | `paf` → ʃ | 依部位/方法縮寫，可生成 |
| Praat | `\sh` → ʃ | 語音學軟體 Praat 的反斜線碼 |

輸入行為：**注音式**——打碼選字後累積在緩衝區，按 **Enter** 整串上屏。

## 目錄結構

```
ipa-ime/
├── master/          # 主資料來源 (IPA_master.csv) 與產生器
├── rime/            # Rime 方案資產 (schema / dict) 與產生器
├── spec/            # 系統規格書、編碼方案規格
└── docs/            # POC 測試指引等
```

## 快速安裝（Windows + 小狼毫）

**前提：** 已安裝 [小狼毫（Weasel）](https://github.com/rime/weasel/releases)。

1. 開啟使用者資料夾：系統匣右鍵小狼毫圖示 →「用戶文件夾」
   （路徑通常為 `%AppData%\Rime`）
2. 將 `rime/ipa.schema.yaml` 與 `rime/ipa.dict.yaml` 複製進去
3. 處理 `rime/default.custom.yaml`：
   - 若資料夾**沒有**此檔 → 直接複製整檔進去
   - 若**已有**此檔 → 把本檔 `patch:` 下的內容合併進既有的 `patch:` 段
4. 系統匣右鍵 →「重新部署」（首次較慢，請稍候）
5. 任意輸入框按 **F4** → 選「IPA 國際音標」

> 詳細安裝與測試步驟請見 [docs/IPA_P3_POC測試指引.md](docs/IPA_P3_POC測試指引.md)

## 從原始碼重新產生

修改碼表或描述式規則：

```bat
cd master
python build_master.py

cd ..\rime
python gen_rime.py --master ..\master\IPA_master.csv --outdir .
```

產生器內建全層撞名檢查，有衝突會直接中止並報告。

## 當前狀態

| 里程碑 | 狀態 |
|---|---|
| P0 鎖定 IPA 版本（2020） | ✅ |
| P1 編碼方案規格 v0.4 | ✅ |
| P2 Master 主資料來源（173 列） | ✅ |
| P3 Rime schema POC | ✅（V1–V8 全數通過） |
| P4 碼表完整化（全 2020 覆蓋、combo 預生成、1219 條） | ✅ |
| P5 候選說明 | ⬜ |
| P6 可選字型元件 | ⬜ |
| P7 打包與部署 | ⬜ |
| P8 測試 | ⬜ |
| P9 文件 | ⬜ |

## 已知限制（POC 階段）

- 候選視窗目前無符號說明（P5 補）
- 分次上屏的基底+組合附加符號無法跨次 NFC 合成（P4 預生成整列解決）
- Praat 碼 163/173 已填，連結弧（˩˥/˥˩）等組合式無單一碼屬設計預期
- 小句群 `|` 之 Praat 碼待對官方手冊覆核
