# -*- coding: utf-8 -*-
"""P3: 由 IPA_master.csv 產生 Rime 方案資產。
輸出: ipa.dict.yaml(碼表) / ipa.schema.yaml(方案) / default.custom.yaml(掛載方案)
用法: python3 gen_rime.py [--lang zh] [--outdir DIR]
語言參數目前影響方案名稱/說明(i18n 載體);碼不隨語言變。"""
import csv, argparse, sys

VERSION = '0.1.1'
LAYER_WEIGHT = {'xsampa': 500, 'mnemonic': 400, 'descriptive': 300, 'praat': 200}

def parse_codepoints(cp_field):
    """'U+0074 U+0361 U+0073' -> 't͡s' 實際輸出字串"""
    return ''.join(chr(int(tok[2:], 16)) for tok in cp_field.split())

def load(master_path):
    rows = list(csv.DictReader(open(master_path, encoding='utf-8-sig')))
    entries = []  # (output_text, code, weight, layer, row_id)
    # V3-a: 既是碼又是標點者,補「指向自己」的最高權重候選,使字面標點排第一。
    # 先加入,dedupe 保留先見者(即高權重版),覆蓋碼表中同 (out,code) 的較低權重列。
    for ch in ('.', '|', '\\'):
        entries.append((ch, ch, 999, 'punct_self', 'PUNCT'))
    for r in rows:
        out = parse_codepoints(r['codepoint'])
        for layer in ('xsampa', 'descriptive', 'praat'):
            code = r[layer].strip()
            if code and not code.startswith('('):
                entries.append((out, code, LAYER_WEIGHT[layer], layer, r['id']))
        for m in r['mnemonic'].split(';'):
            m = m.strip()
            if m:
                entries.append((out, m, LAYER_WEIGHT['mnemonic'], 'mnemonic', r['id']))
    return rows, entries

def dedupe_and_check(entries):
    """去重(同輸出同碼) + 全層撞名檢查(同碼異輸出即失敗)"""
    code_map = {}
    clashes = []
    seen = set()
    result = []
    for out, code, w, layer, rid in entries:
        if code in code_map and code_map[code] != out:
            clashes.append((code, code_map[code], out))
        code_map.setdefault(code, out)
        key = (out, code)
        if key in seen:
            continue
        seen.add(key)
        result.append((out, code, w, layer, rid))
    return result, clashes

def build_alphabet(entries):
    chars = set()
    for _, code, _, _, _ in entries:
        chars.update(code)
    if ' ' in chars:
        sys.exit('錯誤: 碼含空白,與 delimiter 衝突')
    if ';' in chars:
        sys.exit('錯誤: 碼含分號 ; ,與 delimiter 衝突')
    order = [c for c in map(chr, range(33, 127)) if c in chars]
    return ''.join(order)

DICT_HEADER = """# Rime dictionary: IPA
# encoding: utf-8
# 由 gen_rime.py 自 IPA_master.csv 產生,勿手改;修改請改 master 後重跑產生器。
---
name: ipa
version: "{ver}"
sort: by_weight
use_preset_vocabulary: false
...
"""

SCHEMA_TMPL = """# Rime schema: IPA
# encoding: utf-8
# 由 gen_rime.py 產生 (lang={lang})
schema:
  schema_id: ipa
  name: "{name}"
  version: "{ver}"
  author:
    - "IPA IME 專案"
  description: |
    {desc}

switches:
  - name: ascii_mode
    reset: 0
    states: [ "IPA", "ABC" ]

engine:
  processors:
    - ascii_composer
    - recognizer
    - key_binder
    - speller
    - punctuator
    - selector
    - navigator
    - fluid_editor        # 語句流編輯器: 選字累積於緩衝, Enter 整串上屏 (POC 驗證點 1)
  segmentors:
    - ascii_segmentor
    - matcher
    - abc_segmentor
    - punct_segmentor
    - fallback_segmentor
  translators:
    - punct_translator
    - table_translator

speller:
  alphabet: '{alphabet}'
  delimiter: " {delim}"
  auto_select: false      # 注音式: 唯一匹配不自動上屏 (POC 驗證點 2)

translator:
  dictionary: ipa
  enable_completion: true # 前綴補全候選
  enable_sentence: true
  enable_encoder: false
  enable_user_dict: false

menu:
  page_size: 9

# numpad 綁為選字鍵(主鍵盤數字列送字面數字供 | / ^ 碼使用) (POC 驗證點 7)
key_binder:
  import_preset: default
  bindings:
    - {{ when: has_menu, accept: KP_1, send: 1 }}
    - {{ when: has_menu, accept: KP_2, send: 2 }}
    - {{ when: has_menu, accept: KP_3, send: 3 }}
    - {{ when: has_menu, accept: KP_4, send: 4 }}
    - {{ when: has_menu, accept: KP_5, send: 5 }}
    - {{ when: has_menu, accept: KP_6, send: 6 }}
    - {{ when: has_menu, accept: KP_7, send: 7 }}
    - {{ when: has_menu, accept: KP_8, send: 8 }}
    - {{ when: has_menu, accept: KP_9, send: 9 }}

# 自訂標點:僅保留少數「非碼」標點即時上屏;. | \\ 等已在 alphabet 中者不列入,
# 讓 speller 於組字時取用(修 V3-b: \\t. 尾端 . 不再延遲) (POC 驗證點 3)
punctuator:
  half_shape:
    ",": {{commit: ", "}}
    "?": {{commit: "? "}}
    "!": {{commit: "! "}}

recognizer:
  import_preset: default
  patterns:
    # 保證以 \\ 起首的 Praat 碼(含 \\t. 等含標點者)全段落入 speller
    ipa_code: "^\\\\[a-zA-Z0-9].*$"
"""

CUSTOM = """# default.custom.yaml — 將 IPA 方案掛入方案清單
patch:
  schema_list/@next:
    schema: ipa
"""

I18N = {
    'zh': {'name': 'IPA 國際音標',
           'desc': '國際音標(IPA)輸入方案(POC)。四層編碼:X-SAMPA、描述式、助記、Praat。注音式:候選確認、Enter 上屏。'},
    'en': {'name': 'IPA Phonetic',
           'desc': 'IPA input schema (POC). Four code layers: X-SAMPA, descriptive, mnemonic, Praat. Buffer-and-confirm input; Enter commits.'},
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lang', default='zh', choices=list(I18N))
    ap.add_argument('--master', default='/mnt/user-data/outputs/IPA_master.csv')
    ap.add_argument('--outdir', default='.')
    a = ap.parse_args()

    rows, entries = load(a.master)
    entries, clashes = dedupe_and_check(entries)
    if clashes:
        print('全層撞名(同碼異輸出),中止:')
        for code, o1, o2 in clashes:
            print(f'  {code!r}: {o1!r} vs {o2!r}')
        sys.exit(1)

    alphabet = build_alphabet(entries)
    # YAML 單引號字串: 內部單引號需雙寫(build_alphabet 已保證無單引號)
    entries.sort(key=lambda e: (-e[2], e[1]))

    with open(f'{a.outdir}/ipa.dict.yaml', 'w', encoding='utf-8', newline='\n') as f:
        f.write(DICT_HEADER.format(ver=VERSION))
        for out, code, w, layer, rid in entries:
            f.write(f'{out}\t{code}\t{w}\n')

    t = I18N[a.lang]
    with open(f'{a.outdir}/ipa.schema.yaml', 'w', encoding='utf-8', newline='\n') as f:
        f.write(SCHEMA_TMPL.format(lang=a.lang, name=t['name'], ver=VERSION,
                                   desc=t['desc'], alphabet=alphabet.replace("'", "''"), delim=';'))

    with open(f'{a.outdir}/default.custom.yaml', 'w', encoding='utf-8', newline='\n') as f:
        f.write(CUSTOM)

    print(f'symbols: {len(rows)}  dict entries: {len(entries)}')
    print(f'alphabet ({len(alphabet)}): {alphabet}')
    from collections import Counter
    print('layers:', dict(Counter(e[3] for e in entries)))
    print('撞名: 0;輸出:', a.outdir)

if __name__ == '__main__':
    main()
