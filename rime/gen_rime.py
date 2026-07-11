# -*- coding: utf-8 -*-
"""P3: 由 IPA_master.csv 產生 Rime 方案資產。
輸出: ipa.dict.yaml(碼表) / ipa.schema.yaml(方案) / default.custom.yaml(掛載方案)
用法: python3 gen_rime.py [--lang zh] [--outdir DIR]
語言參數目前影響方案名稱/說明(i18n 載體);碼不隨語言變。"""
import csv, argparse, sys

VERSION = '0.2.0'
LAYER_WEIGHT = {'xsampa': 500, 'mnemonic': 400, 'descriptive': 300, 'praat': 200}

def parse_codepoints(cp_field):
    """'U+0074 U+0361 U+0073' -> 't͡s' 實際輸出字串"""
    return ''.join(chr(int(tok[2:], 16)) for tok in cp_field.split())

def load(master_path):
    rows = list(csv.DictReader(open(master_path, encoding='utf-8-sig')))
    entries = []  # (output_text, code, weight, layer, row_id)
    # 標點自指候選(0.1.2 通則化):
    # 高權重 999(字面排第一): 使用者指定的 . | \ + 無獨立碼意義的標點(打得出字面)
    # 低權重 50(字面為後位候選): 本身是 X-SAMPA/Praat 碼者(? ~ = : 等),IPA 符號仍排第一
    # HIGH: 自指字面排第一。僅列 initials 內可達者;
    # , ( ) ' / + 不在此列——它們無真實碼起首,將自動排除於 initials 外,冷按直接上屏字面。
    PUNCT_HIGH = ['.', '|', '\\', '<', '>', '-']
    PUNCT_LOW  = ['?', '~', '=', ':', '%', '"', '@', '&', '{', '}', '`', '_', '!']
    for ch in PUNCT_HIGH:
        entries.append((ch, ch, 999, 'punct_self', 'PUNCT'))
    for ch in PUNCT_LOW:
        entries.append((ch, ch, 50, 'punct_self', 'PUNCT'))
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
    """去重(同輸出同碼) + 全層撞名檢查(同碼異輸出即失敗)。
    例外: punct_self 的低權重字面候選為刻意多候選(如 ? -> ʔ 與字面 ?),不視為撞名。"""
    code_map = {}          # code -> (out, layer)
    clashes = []
    seen = set()
    result = []
    for out, code, w, layer, rid in entries:
        if code in code_map:
            prev_out, prev_layer = code_map[code]
            if prev_out != out and 'punct_self' not in (prev_layer, layer):
                clashes.append((code, prev_out, out))
        code_map.setdefault(code, (out, layer))
        key = (out, code)
        if key in seen:
            continue
        seen.add(key)
        result.append((out, code, w, layer, rid))
    return result, clashes

def build_alphabet(entries):
    chars = set()
    starts = set()
    for _, code, _, layer, _ in entries:
        chars.update(code)
        if layer != 'punct_self':   # 自指候選不算「真實碼」,不賦予起始資格
            starts.add(code[0])
    if ' ' in chars:
        sys.exit('錯誤: 碼含空白,與 delimiter 衝突')
    if ';' in chars:
        sys.exit('錯誤: 碼含分號 ; ,與 delimiter 衝突')
    order = [c for c in map(chr, range(33, 127)) if c in chars]
    alphabet = ''.join(order)
    # initials: 只有這些鍵能「開始」組字(仿官方 rime-ipa)。
    # 自動規則: 有任何碼以該字元起首者才列入;再手動排除 '.'
    # 使冷按 . 直接上屏字面句號(音節界符號即 . 本身,無損)。碼中 . 照常有效。
    UX_EXCLUDE = {'.'}
    initials = ''.join(c for c in order if c in starts and c not in UX_EXCLUDE)
    return alphabet, initials

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

# 0.1.3: 結構仿官方 rime-ipa(rime/rime-ipa)——符號密集 alphabet 的正解:
# 整條標點管線(punctuator/recognizer/matcher/punct_segmentor/punct_translator)拆除,
# 標點鍵一律走 speller/碼表。punct_segmentor 搶走 . 形成無候選死段即 V3-b 元凶。
engine:
  processors:
    - ascii_composer
    - key_binder
    - speller
    - selector
    - navigator
    - fluid_editor        # 語句流編輯器: 選字累積於緩衝, Enter 整串上屏
  segmentors:
    - ascii_segmentor
    - abc_segmentor
    - fallback_segmentor
  translators:
    - echo_translator     # 無任何候選時, 以原始輸入碼為候選(未匹配段可見、可上屏)
    - table_translator

speller:
  alphabet: '{alphabet}'
  # initials: 僅這些鍵能「開始」組字(自動生成=有碼以其起首者, 手動排除 .)。
  # 冷按 . 直接上屏字面句號; 碼中的 . (如 \\t.) 照常有效。仿官方 rime-ipa。
  initials: '{initials}'
  delimiter: " {delim}"
  auto_select: false      # 注音式: 唯一匹配不自動上屏

translator:
  dictionary: ipa
  enable_completion: true # 前綴補全候選
  enable_sentence: true
  enable_encoder: false
  enable_user_dict: false

menu:
  page_size: 9

# 0.2.0 關鍵修正(使用者診斷): default key_binder 將 . 綁為翻頁鍵
# (when: has_menu, accept: period, send: Page_Down),組字中 . 被吃去翻頁
# 而未進 speller —— 即 V3-b 元凶。故不 import default,只留 numpad 綁定。
key_binder:
  bindings:
    - {{ when: always, accept: KP_0, send: 0 }}
    - {{ when: always, accept: KP_1, send: 1 }}
    - {{ when: always, accept: KP_2, send: 2 }}
    - {{ when: always, accept: KP_3, send: 3 }}
    - {{ when: always, accept: KP_4, send: 4 }}
    - {{ when: always, accept: KP_5, send: 5 }}
    - {{ when: always, accept: KP_6, send: 6 }}
    - {{ when: always, accept: KP_7, send: 7 }}
    - {{ when: always, accept: KP_8, send: 8 }}
    - {{ when: always, accept: KP_9, send: 9 }}
    - {{ when: always, accept: KP_Decimal, send: period }}
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

    alphabet, initials = build_alphabet(entries)
    # YAML 單引號字串: 內部單引號需雙寫(build_alphabet 已保證無單引號)
    entries.sort(key=lambda e: (-e[2], e[1]))

    with open(f'{a.outdir}/ipa.dict.yaml', 'w', encoding='utf-8', newline='\n') as f:
        f.write(DICT_HEADER.format(ver=VERSION))
        for out, code, w, layer, rid in entries:
            f.write(f'{out}\t{code}\t{w}\n')

    t = I18N[a.lang]
    with open(f'{a.outdir}/ipa.schema.yaml', 'w', encoding='utf-8', newline='\n') as f:
        f.write(SCHEMA_TMPL.format(lang=a.lang, name=t['name'], ver=VERSION,
                                   desc=t['desc'], alphabet=alphabet.replace("'", "''"),
                                   initials=initials.replace("'", "''"), delim=';'))

    with open(f'{a.outdir}/default.custom.yaml', 'w', encoding='utf-8', newline='\n') as f:
        f.write(CUSTOM)

    print(f'symbols: {len(rows)}  dict entries: {len(entries)}')
    print(f'alphabet ({len(alphabet)}): {alphabet}')
    from collections import Counter
    print('layers:', dict(Counter(e[3] for e in entries)))
    print('撞名: 0;輸出:', a.outdir)

if __name__ == '__main__':
    main()
