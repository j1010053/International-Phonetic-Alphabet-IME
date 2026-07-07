# rime/

Rime 方案資產。由 `gen_rime.py` 自 `../master/IPA_master.csv` 產生。

**⚠️ 這些是生成檔。** 若需修改碼表或規則，請從 `master/` 改起再重跑產生器，
勿直接手改這裡的 YAML——下次重跑會覆蓋。

## 檔案說明

| 檔案 | 說明 |
|---|---|
| `ipa.schema.yaml` | 方案主設定（speller / translator / engine） |
| `ipa.dict.yaml` | 碼表（497 條，四層編碼） |
| `default.custom.yaml` | 將本方案掛入 Rime 方案清單的補丁 |
| `gen_rime.py` | 產生器腳本 |

## 重新產生

```bat
python gen_rime.py --master ..\master\IPA_master.csv --outdir .
python gen_rime.py --master ..\master\IPA_master.csv --outdir . --lang en
```
