# master/

IPA 輸入法的**單一事實來源**。所有碼表、描述與語言資料均從這裡產生。

## 檔案說明

| 檔案 | 說明 |
|---|---|
| `IPA_master.csv` | 主資料表（173 列，含 Unicode/X-SAMPA/描述式/助記/Praat/中英描述） |
| `build_master.py` | 主資料產生器（特徵字典 → 描述式碼 → CSV） |
| `IPA_master_README.md` | 欄位 schema、設計說明、待查核項 |

## 修改流程

- **改碼表規則**（描述式/特徵字典）→ 改 `build_master.py` 中的字典 → 重跑
- **改助記/X-SAMPA/Praat**（逐符號資料）→ 直接改 `build_master.py` 對應列
- 跑完後再跑 `../rime/gen_rime.py` 重新產生 Rime 方案資產

```bat
python build_master.py
cd ..\rime
python gen_rime.py --master ..\master\IPA_master.csv --outdir .
```
