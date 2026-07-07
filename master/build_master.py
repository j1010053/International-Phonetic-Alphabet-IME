# -*- coding: utf-8 -*-
"""P2: 由特徵字典程式化生成 IPA 輸入法 master 主資料來源 (CSV)。
依編碼方案規格 v0.4。描述式碼與中英描述由規則生成,確保一致。"""
import csv

# (code, en, zh)
PLACE = {
    'bilabial': ('bl', 'bilabial', '雙唇'),
    'labiodental': ('ld', 'labiodental', '唇齒'),
    'dental': ('dn', 'dental', '齒'),
    'alveolar': ('al', 'alveolar', '齒齦'),
    'postalveolar': ('pa', 'postalveolar', '後齒齦'),
    'retroflex': ('rx', 'retroflex', '捲舌'),
    'palatal': ('pj', 'palatal', '硬顎'),
    'velar': ('ve', 'velar', '軟顎'),
    'uvular': ('uv', 'uvular', '小舌'),
    'pharyngeal': ('ph', 'pharyngeal', '咽'),
    'glottal': ('gl', 'glottal', '聲門'),
    'epiglottal': ('eg', 'epiglottal', '會厭'),
    'labial-velar': ('lv', 'labial-velar', '唇軟顎'),
    'labial-palatal': ('lp', 'labial-palatal', '唇硬顎'),
    'alveolo-palatal': ('ap', 'alveolo-palatal', '齦顎'),
}
# (code, en, zh, is_obstruent)
MANNER = {
    'plosive': ('p', 'plosive', '塞音', True),
    'nasal': ('n', 'nasal', '鼻音', False),
    'trill': ('r', 'trill', '顫音', False),
    'tap': ('t', 'tap/flap', '閃音', False),
    'fricative': ('f', 'fricative', '擦音', True),
    'approximant': ('a', 'approximant', '近音', False),
    'lateral-approximant': ('l', 'lateral approximant', '邊近音', False),
    'lateral-fricative': ('lf', 'lateral fricative', '邊擦音', True),
    'lateral-flap': ('lx', 'lateral flap', '邊閃音', False),
    'affricate': ('af', 'affricate', '塞擦音', True),
}
HEIGHT = {
    'close': ('cl', 'close', '閉'),
    'near-close': ('nc', 'near-close', '次閉'),
    'close-mid': ('cm', 'close-mid', '半閉'),
    'mid': ('md', 'mid', '中'),
    'open-mid': ('om', 'open-mid', '半開'),
    'near-open': ('no', 'near-open', '次開'),
    'open': ('op', 'open', '開'),
}
BACK = {'front': ('f', 'front', '前'), 'central': ('c', 'central', '央'), 'back': ('b', 'back', '後')}

NO_VOICING_WORD = {'ʔ', 'ʡ'}  # 名稱不含清濁字

def cp(s):
    return ' '.join('U+%04X' % ord(c) for c in s)

def cons_desc(symbol, place, manner, voiced):
    pc, pen, pzh = PLACE[place]
    mc, men, mzh, obstr = MANNER[manner]
    code = ('v' if (obstr and voiced) else '') + pc + mc
    if symbol in NO_VOICING_WORD:
        en = f'{pen} {men}'
        zh = f'{pzh}{mzh}'
    elif obstr:
        en = f'{"voiced" if voiced else "voiceless"} {pen} {men}'
        zh = f'{"濁" if voiced else "清"}{pzh}{mzh}'
    else:
        en = f'{pen} {men}'
        zh = f'{pzh}{mzh}'
    return code, en, zh

def vowel_desc(height, back, rounded):
    hc, hen, hzh = HEIGHT[height]
    bc, ben, bzh = BACK[back]
    code = hc + bc + ('r' if rounded else '')
    en = f'{hen} {ben} {"rounded" if rounded else "unrounded"} vowel'
    zh = f'{hzh}{bzh}{"圓唇" if rounded else "不圓唇"}元音'
    return code, en, zh

# Praat 反斜線碼,自維基「Comparison of ASCII encodings of the IPA」對照表轉錄(2025)。
# 鍵為符號字元(子音/母音/擊音/內爆音/擠喉標記/其他)。
PRAAT = {
    'p':'p','b':'b','t':'t','d':'d','ʈ':r'\t.','ɖ':r'\d.','c':'c','ɟ':r'\j-','k':'k','ɡ':r'\gs','q':'q','ɢ':r'\gc','ʔ':r'\?g',
    'm':'m','ɱ':r'\mj','n':'n','ɳ':r'\n.','ɲ':r'\nj','ŋ':r'\ng','ɴ':r'\nc',
    'ʙ':r'\bc','r':'r','ʀ':r'\rc','ⱱ':r'\V^','ɾ':r'\fh','ɽ':r'\f.',
    'ɸ':r'\ff','β':r'\bf','f':'f','v':'v','θ':r'\tf','ð':r'\dh','s':'s','z':'z','ʃ':r'\sh','ʒ':r'\zh','ʂ':r'\s.','ʐ':r'\z.','ç':r'\c,','ʝ':r'\jc','x':'x','ɣ':r'\gf','χ':r'\cf','ʁ':r'\ri','ħ':r'\h-','ʕ':r'\9e','h':'h','ɦ':r'\h^',
    'ɬ':r'\l-','ɮ':r'\lz',
    'ʋ':r'\vs','ɹ':r'\rt','ɻ':r'\r.','j':'j','ɰ':r'\ml',
    'l':'l','ɭ':r'\l.','ʎ':r'\yt','ʟ':r'\lc',
    'ʍ':r'\wt','w':'w','ɥ':r'\ht','ʜ':r'\hc','ʢ':r'\9-','ʡ':r'\?-','ɕ':r'\cc','ʑ':r'\zc','ɺ':r'\rl','ɧ':r'\hj',
    'ʘ':r'\O.','ǀ':r'\|1','ǃ':'!','ǂ':r'\|-','ǁ':r'\|2',
    'ɓ':r'\b^','ɗ':r'\d^','ʄ':r'\j^','ɠ':r'\g^','ʛ':r'\G^','ʼ':r'\ap',
    'i':'i','y':'y','ɨ':r'\i-','ʉ':r'\u-','ɯ':r'\mt','u':'u',
    'ɪ':r'\ic','ʏ':r'\yc','ʊ':r'\hs',
    'e':'e','ø':r'\o/','ɘ':r'\e-','ɵ':r'\o-','ɤ':r'\rh','o':'o',
    'ə':r'\sw',
    'ɛ':r'\ef','œ':r'\oe','ɜ':r'\er','ɞ':r'\kb','ʌ':r'\vt','ɔ':r'\ct',
    'æ':r'\ae','ɐ':r'\at',
    'a':'a','ɶ':r'\Oe','ɑ':r'\as','ɒ':r'\ab',
}
# 依描述式碼查(附加符號 token / 超音段 / 聲調)。空字串=該系統未提供或為組合式。
PRAAT_BY_CODE = {
    'dev':r'\0v','voi':r'\vv','asp':r'\^h','rou+':r'\3v','rou-':r'\cv','adv':r'\+v','ret':r'\-v','cen':r'\:^','mce':r'\x^','syl':r'\|v','nsy':r'\nv','rho':r'\hr','bre':r'\:v','cre':r'\~v','lgl':r'\mv','lab':r'\^w','pzd':r'\^j','vzd':r'\^G','pha':r'\^9','vph':r'\~/','rai':r'\T^','low':r'\Tv','atr':r'\T(','rtr':r'\T)','dnt':r'\Nv','api':r'\Uv','lam':r'\Dv','nas':r'\~^','nrl':r'\^n','lrl':r'\^l','nor':r'\cn',
    'str1':r"\'1",'str2':r"\'2",'lng':r'\:f','hln':r'\.f','xsh':r'\N^','grp1':'','grp2':'||','sbr':'.','lnk':r'\_u',
    'dstep':r'\|d','ustep':r'\|u','grise':r'\NE','gfall':r'\SE',
    'tie':r'\li','tieb':r'\LI',
}

rows = []
def add(category, symbol, xsampa, descriptive, mnemonic, mnem_src, desc_en, desc_zh, notes='', codepoint=None):
    rows.append({
        'id': '', 'category': category, 'symbol': symbol,
        'codepoint': codepoint if codepoint is not None else cp(symbol),
        'xsampa': xsampa, 'descriptive': descriptive,
        'mnemonic': mnemonic, 'mnemonic_source': mnem_src,
        'praat': PRAAT.get(symbol, '') or PRAAT_BY_CODE.get(descriptive, ''), 'desc_en': desc_en, 'desc_zh': desc_zh, 'notes': notes,
    })

# ---- 5.1 肺氣流子音: (symbol, xsampa, place, manner, voiced, mnemonic, mnem_src) ----
PULMONIC = [
    ('p','p','bilabial','plosive',False,'',''),
    ('b','b','bilabial','plosive',True,'',''),
    ('t','t','alveolar','plosive',False,'',''),
    ('d','d','alveolar','plosive',True,'',''),
    ('ʈ','t`','retroflex','plosive',False,'',''),
    ('ɖ','d`','retroflex','plosive',True,'',''),
    ('c','c','palatal','plosive',False,'',''),
    ('ɟ','J\\','palatal','plosive',True,'',''),
    ('k','k','velar','plosive',False,'',''),
    ('ɡ','g','velar','plosive',True,'',''),
    ('q','q','uvular','plosive',False,'',''),
    ('ɢ','G\\','uvular','plosive',True,'',''),
    ('ʔ','?','glottal','plosive',False,'',''),
    ('m','m','bilabial','nasal',True,'',''),
    ('ɱ','F','labiodental','nasal',True,'',''),
    ('n','n','alveolar','nasal',True,'',''),
    ('ɳ','n`','retroflex','nasal',True,'',''),
    ('ɲ','J','palatal','nasal',True,'ny','西班牙語 ñ 羅馬化'),
    ('ŋ','N','velar','nasal',True,'ng','ARPABET（亦英語拼寫）'),
    ('ɴ','N\\','uvular','nasal',True,'',''),
    ('ʙ','B\\','bilabial','trill',True,'',''),
    ('r','r','alveolar','trill',True,'',''),
    ('ʀ','R\\','uvular','trill',True,'',''),
    ('ⱱ','','labiodental','tap',True,'',''),
    ('ɾ','4','alveolar','tap',True,'',''),
    ('ɽ','r`','retroflex','tap',True,'',''),
    ('ɸ','p\\','bilabial','fricative',False,'',''),
    ('β','B','bilabial','fricative',True,'',''),
    ('f','f','labiodental','fricative',False,'',''),
    ('v','v','labiodental','fricative',True,'',''),
    ('θ','T','dental','fricative',False,'th','ARPABET（亦英語拼寫）'),
    ('ð','D','dental','fricative',True,'dh','ARPABET'),
    ('s','s','alveolar','fricative',False,'',''),
    ('z','z','alveolar','fricative',True,'',''),
    ('ʃ','S','postalveolar','fricative',False,'sh','ARPABET（亦英語拼寫）'),
    ('ʒ','Z','postalveolar','fricative',True,'zh','ARPABET'),
    ('ʂ','s`','retroflex','fricative',False,'',''),
    ('ʐ','z`','retroflex','fricative',True,'',''),
    ('ç','C','palatal','fricative',False,'',''),
    ('ʝ','j\\','palatal','fricative',True,'',''),
    ('x','x','velar','fricative',False,'',''),
    ('ɣ','G','velar','fricative',True,'gh','阿拉伯/希臘語轉寫'),
    ('χ','X','uvular','fricative',False,'',''),
    ('ʁ','R','uvular','fricative',True,'',''),
    ('ħ','X\\','pharyngeal','fricative',False,'',''),
    ('ʕ','?\\','pharyngeal','fricative',True,'',''),
    ('h','h','glottal','fricative',False,'',''),
    ('ɦ','h\\','glottal','fricative',True,'',''),
    ('ɬ','K','alveolar','lateral-fricative',False,'',''),
    ('ɮ','K\\','alveolar','lateral-fricative',True,'',''),
    ('ʋ','v\\','labiodental','approximant',True,'',''),
    ('ɹ','r\\','alveolar','approximant',True,'',''),
    ('ɻ','r\\`','retroflex','approximant',True,'',''),
    ('j','j','palatal','approximant',True,'',''),
    ('ɰ','M\\','velar','approximant',True,'',''),
    ('l','l','alveolar','lateral-approximant',True,'',''),
    ('ɭ','l`','retroflex','lateral-approximant',True,'',''),
    ('ʎ','L','palatal','lateral-approximant',True,'',''),
    ('ʟ','L\\','velar','lateral-approximant',True,'',''),
]
for sym, xs, pl, mn, vd, mnem, src in PULMONIC:
    d, en, zh = cons_desc(sym, pl, mn, vd)
    add('pulmonic', sym, xs, d, mnem, src, en, zh)

# ---- 5.3 其他符號 (以 place/manner 生成者) ----
OTHER = [
    ('ʍ','W','labial-velar','fricative',False,'wh','英語拼寫（Worldbet 等亦用）'),
    ('w','w','labial-velar','approximant',True,'',''),
    ('ɥ','H','labial-palatal','approximant',True,'',''),
    ('ʜ','H\\','epiglottal','fricative',False,'',''),
    ('ʢ','<\\','epiglottal','fricative',True,'',''),
    ('ʡ','>\\','epiglottal','plosive',False,'',''),
    ('ɕ','s\\','alveolo-palatal','fricative',False,'',''),
    ('ʑ','z\\','alveolo-palatal','fricative',True,'',''),
]
for sym, xs, pl, mn, vd, mnem, src in OTHER:
    d, en, zh = cons_desc(sym, pl, mn, vd)
    add('other', sym, xs, d, mnem, src, en, zh)
# 其他符號 (特殊,直接給)
add('other', 'ɺ', 'l\\', 'allx', '', '', 'voiced alveolar lateral flap', '濁齒齦邊閃音')
add('other', 'ɧ', 'x\\', '', '', '', 'simultaneous ʃ and x', 'ʃ 與 x 同時')

# ---- 5.2 非肺氣流子音 ----
CLICKS = [  # symbol, xsampa, descriptive, desc_en, desc_zh
    ('ʘ','O\\','blck','bilabial click','雙唇擊音'),
    ('ǀ','|\\','dnck','dental click','齒擊音'),
    ('ǃ','!\\','pack','postalveolar click','後齒齦擊音'),
    ('ǂ','=\\','pjck','palatal click','硬顎擊音'),
    ('ǁ','|\\|\\','allck','alveolar lateral click','齒齦邊擊音'),
]
for sym, xs, d, en, zh in CLICKS:
    add('nonpulmonic', sym, xs, d, '', '', en, zh)
IMPLOSIVES = [
    ('ɓ','b_<','blim','voiced bilabial implosive','濁雙唇內爆音'),
    ('ɗ','d_<','alim','voiced alveolar implosive','濁齒齦內爆音'),
    ('ʄ','J\\_<','pjim','voiced palatal implosive','濁硬顎內爆音'),
    ('ɠ','g_<','veim','voiced velar implosive','濁軟顎內爆音'),
    ('ʛ','G\\_<','uvim','voiced uvular implosive','濁小舌內爆音'),
]
for sym, xs, d, en, zh in IMPLOSIVES:
    add('nonpulmonic', sym, xs, d, '', '', en, zh)
add('nonpulmonic', 'ʼ', '_>', 'ej', '', '', 'ejective marker', '擠喉音標記', notes='附加於基底阻礙音之後')

# ---- 5.4 母音 ----
VOWELS = [
    ('i','i','close','front',False,'',''),
    ('y','y','close','front',True,'',''),
    ('ɨ','1','close','central',False,'',''),
    ('ʉ','}','close','central',True,'',''),
    ('ɯ','M','close','back',False,'',''),
    ('u','u','close','back',True,'',''),
    ('ɪ','I','near-close','front',False,'',''),
    ('ʏ','Y','near-close','front',True,'',''),
    ('ʊ','U','near-close','back',True,'',''),
    ('e','e','close-mid','front',False,'',''),
    ('ø','2','close-mid','front',True,'eu','法語拼寫'),
    ('ɘ','@\\','close-mid','central',False,'',''),
    ('ɵ','8','close-mid','central',True,'',''),
    ('ɤ','7','close-mid','back',False,'',''),
    ('o','o','close-mid','back',True,'',''),
    ('ə','@','mid','central',False,'ax','ARPABET'),
    ('ɛ','E','open-mid','front',False,'eh','ARPABET'),
    ('œ','9','open-mid','front',True,'oe','符號本名 o-e ligature（亦法/德語）'),
    ('ɜ','3','open-mid','central',False,'',''),
    ('ɞ','3\\','open-mid','central',True,'',''),
    ('ʌ','V','open-mid','back',False,'',''),
    ('ɔ','O','open-mid','back',True,'ao','ARPABET'),
    ('æ','{','near-open','front',False,'ae','ARPABET'),
    ('ɐ','6','near-open','central',False,'',''),
    ('a','a','open','front',False,'',''),
    ('ɶ','&','open','front',True,'',''),
    ('ɑ','A','open','back',False,'aa','ARPABET'),
    ('ɒ','Q','open','back',True,'',''),
]
for sym, xs, ht, bk, rd, mnem, src in VOWELS:
    d, en, zh = vowel_desc(ht, bk, rd)
    add('vowel', sym, xs, d, mnem, src, en, zh)

# ---- 5.8 預收塞擦音 ----
AFFR = [
    ('t͡s','ts','alaf','','voiceless alveolar affricate','清齒齦塞擦音'),
    ('t͡ʃ','tS','paaf','ch','voiceless postalveolar affricate','清後齒齦塞擦音'),
    ('d͡ʒ','dZ','vpaaf','jh;dj','voiced postalveolar affricate','濁後齒齦塞擦音'),
    ('t͡ɕ','ts\\','apaf','','voiceless alveolo-palatal affricate','清齦顎塞擦音'),
    ('d͡ʑ','dz\\','vapaf','','voiced alveolo-palatal affricate','濁齦顎塞擦音'),
]
for sym, xs, d, mnem, en, zh in AFFR:
    src = 'ARPABET / 直覺英語' if mnem else ''
    add('affricate', sym, xs, d, mnem, src, en, zh)

# ---- 5.5 附加符號: (name_en, name_zh, codepoint_int, is_spacing, xsampa, token) ----
DIAC = [
    ('voiceless','清化',0x0325,False,'_0','dev'),
    ('voiced','濁化',0x032C,False,'_v','voi'),
    ('aspirated','送氣',0x02B0,True,'_h','asp'),
    ('more rounded','較圓',0x0339,False,'_O','rou+'),
    ('less rounded','較展',0x031C,False,'_c','rou-'),
    ('advanced','前移',0x031F,False,'_+','adv'),
    ('retracted','後移',0x0320,False,'_-','ret'),
    ('centralized','央化',0x0308,False,'_"','cen'),
    ('mid-centralized','央化(中)',0x033D,False,'_x','mce'),
    ('syllabic','成音節',0x0329,False,'=','syl'),
    ('non-syllabic','非成節',0x032F,False,'_^','nsy'),
    ('rhoticity','兒化',0x02DE,True,'`','rho'),
    ('breathy voiced','氣聲',0x0324,False,'_t','bre'),
    ('creaky voiced','嘎裂聲',0x0330,False,'_k','cre'),
    ('linguolabial','舌唇',0x033C,False,'_N','lgl'),
    ('labialized','唇化',0x02B7,True,'_w','lab'),
    ('palatalized','顎化',0x02B2,True,'_j','pzd'),  # X-SAMPA 允許 ' 或 _j;採 _j,' 留作 Rime delimiter
    ('velarized','軟顎化',0x02E0,True,'_G','vzd'),
    ('pharyngealized','咽化',0x02E4,True,'_?\\','pha'),
    ('velarized or pharyngealized','軟顎化或咽化',0x0334,False,'_e','vph'),
    ('raised','升',0x031D,False,'_r','rai'),
    ('lowered','降',0x031E,False,'_o','low'),
    ('advanced tongue root','舌根前',0x0318,False,'_A','atr'),
    ('retracted tongue root','舌根後',0x0319,False,'_q','rtr'),
    ('dental','齒化',0x032A,False,'_d','dnt'),
    ('apical','舌尖',0x033A,False,'_a','api'),
    ('laminal','舌葉',0x033B,False,'_m','lam'),
    ('nasalized','鼻化',0x0303,False,'~','nas'),
    ('nasal release','鼻除阻',0x207F,True,'_n','nrl'),
    ('lateral release','邊除阻',0x02E1,True,'_l','lrl'),
    ('no audible release','無聲除阻',0x031A,False,'_}','nor'),
]
for en, zh, code, spacing, xs, token in DIAC:
    ch = chr(code)
    disp = ch if spacing else '\u25CC' + ch
    note = 'spacing modifier' if spacing else 'combining'
    add('diacritic', disp, xs, token, '', '', en, zh, notes=note, codepoint='U+%04X' % code)

# ---- 5.6 超音段 ----
SUPRA = [
    ('primary stress','主重音',0x02C8,'"','str1'),
    ('secondary stress','次重音',0x02CC,'%','str2'),
    ('long','長',0x02D0,':','lng'),
    ('half-long','半長',0x02D1,':\\','hln'),
    ('extra-short','極短',0x0306,'_X','xsh'),
    ('minor (foot) group','小句群',0x007C,'|','grp1'),
    ('major (intonation) group','大句群',0x2016,'||','grp2'),
    ('syllable break','音節界',0x002E,'.','sbr'),
    ('linking','連音',0x203F,'-\\','lnk'),
]
for en, zh, code, xs, c in SUPRA:
    ch = chr(code)
    disp = ch if code not in (0x0306,) else '\u25CC' + ch
    add('suprasegmental', disp, xs, c, '', '', en, zh, codepoint='U+%04X' % code)

# ---- 5.7 聲調 ----
# 組合調符沿用 X-SAMPA _T/_H/_M/_L/_B(不另設描述式碼,見 OTHERTONE 註)。
# 調値字母(Chao staff letter): 碼 = '|' + 1~3 位數字, 每位 1-5 逐位映射 ˩˨˧˦˥。
CHAO = {1: 0x02E9, 2: 0x02E8, 3: 0x02E7, 4: 0x02E6, 5: 0x02E5}  # 1..5 -> ˩˨˧˦˥
CHAO_ZH = {1:'超低',2:'低',3:'中',4:'高',5:'超高'}
import itertools
for n in (1, 2, 3):
    for combo in itertools.product('12345', repeat=n):
        digits = ''.join(combo)
        letters = ''.join(chr(CHAO[int(d)]) for d in combo)
        code = '|' + digits
        cps = ' '.join('U+%04X' % CHAO[int(d)] for d in combo)
        zh = ''.join(CHAO_ZH[int(d)] for d in combo)
        en = 'Chao tone letter ' + '-'.join(combo)
        add('tone_letter', letters, '', code, '', '', en, f'調値 {digits}({zh})', codepoint=cps)

# 上標數字(superscript): 碼 = '^' + 數字。1~2 位允許 0-9;3 位限 1-5(調值連調語境)。
SUP = {0:0x2070,1:0x00B9,2:0x00B2,3:0x00B3,4:0x2074,5:0x2075,6:0x2076,7:0x2077,8:0x2078,9:0x2079}
for n in (1, 2, 3):
    pool = '0123456789' if n < 3 else '12345'
    for combo in itertools.product(pool, repeat=n):
        digits = ''.join(combo)
        sup = ''.join(chr(SUP[int(d)]) for d in combo)
        cps = ' '.join('U+%04X' % SUP[int(d)] for d in combo)
        add('superscript', sup, '', '^' + digits, '', '', f'superscript {digits}', f'上標數字 {digits}', codepoint=cps)

# 其他調號
OTHERTONE = [
    ('downstep','降階',0xA71C,'<D>','dstep'),
    ('upstep','升階',0xA71B,'<U>','ustep'),
    ('global rise','全升',0x2197,'<R>','grise'),
    ('global fall','全降',0x2198,'<F>','gfall'),
]
for en, zh, code, xs, c in OTHERTONE:
    add('tone_other', chr(code), xs, c, '', '', en, zh, codepoint='U+%04X' % code)

# ---- 連結弧 (tie bar, v0.4 §6) ----
add('tie', '\u25CC\u0361\u25CC', '_', 'tie', '', '', 'tie bar (above)', '連結弧（上）', notes='combining;塞擦/雙重調音', codepoint='U+0361')
add('tie', '\u25CC\u035C\u25CC', '', 'tieb', '', '', 'tie bar (below)', '連結弧（下）', notes='combining', codepoint='U+035C')

# ---- 指派 id ----
for i, r in enumerate(rows, 1):
    r['id'] = f'{r["category"][:3].upper()}{i:03d}'

cols = ['id','category','symbol','codepoint','xsampa','descriptive','mnemonic','mnemonic_source','praat','desc_en','desc_zh','notes']
out = '/mnt/user-data/outputs/IPA_master.csv'
with open(out, 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for r in rows:
        w.writerow(r)

# 統計
from collections import Counter
cnt = Counter(r['category'] for r in rows)
praat_filled = sum(1 for r in rows if r['praat'])
print('total rows:', len(rows))
for k, v in cnt.items():
    print(f'  {k}: {v}')
print('praat filled:', praat_filled, '/ rest pending manual transcription')
print('written:', out)
