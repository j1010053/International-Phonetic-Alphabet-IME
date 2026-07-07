# IPA 輸入法 — 編碼方案規格

**版本：** v0.4
**依據：** 2020 官方 IPA 表
**對應主規格：** 系統規格書 v0.2 第 2.3、5（P1）節
**前次版本：** v0.3

**v0.4 變更摘要：**
- **聲調兩種形式皆收**（§5.7）：調符（combining）以 `td*` 碼、調値字母（Chao staff letter）以 `tl*` 碼，兩族分立。`tl` 前綴 + Chao 數字（含連調數字串）既保留 Chao 慣例，又避開「裸數字撞 X-SAMPA」之問題。
- **塞擦音**（§5.8）：預收常見 5 個，並新增專屬描述式方法碼 **affricate `af`**（§3.1），與「塞音+連結弧+擦音」組合式並存。
- 本版自含完整附加符號、超音段、聲調表（不再參照前版）。
- 聲調與塞擦音由「待確認」移入「已鎖定」；偏好項僅餘「ʔ 是否日後補助記」（視頻率）。

---

## 1. 目的與四層編碼

每個 IPA 符號可由四種輸入碼擇一打出，全部為「多對一」，指向同一 Unicode 輸出：

1. **X-SAMPA（主碼）** — 既有標準，最短、可互通。
2. **描述式碼** — 依發音學描述的固定縮寫，可生成、自我說明。
3. **助記別名** — 於存在自然助記時提供，依「不撞主流」規則收錄（§4）。
4. **Praat 三連碼** — 語音學軟體 Praat 的反斜線碼，規則化、全 IPA 覆蓋（§5A）。

四層皆以「碼表一列指向同一輸出」實作。

---

## 2. 通用設計原則

- **預設值省略：** 子音清音省略、濁音前綴 `v`（僅阻礙音）；母音不圓唇省略、圓唇後綴 `r`。
- **以「產生」取代「即時解析」：** 合法碼於建表階段機械式產生、逐列收錄；引擎只做精確比對。欄寬不齊、跨層同形不影響解析。
- **前綴共存由輸入行為承接：** 採注音式、關閉唯一匹配自動上屏（主規格 2.4）。
- **大小寫：** X-SAMPA 區分大小寫；描述式、助記一律小寫；Praat 依其原樣。

---

## 3. 描述式縮寫字典（已鎖定）

### 3.1 子音：清濁 / 部位 / 方法
碼 = `[v]` + 部位(2) + 方法(1，複合方法為 2)。清音省略、濁音前綴 `v`。

**部位（2 字母）：** bilabial `bl`｜labiodental `ld`｜dental `dn`｜alveolar `al`｜postalveolar `pa`｜retroflex `rx`｜palatal `pj`｜velar `ve`｜uvular `uv`｜pharyngeal `ph`｜glottal `gl`｜epiglottal `eg`｜labial-velar `lv`｜labial-palatal `lp`｜alveolo-palatal `ap`

**方法（1 字母；複合方法 2 字母）：** plosive `p`｜nasal `n`｜trill `r`｜tap/flap `t`｜fricative `f`｜approximant `a`｜lateral approximant `l`｜lateral fricative `lf`｜lateral flap `lx`｜**affricate `af`**

> `af`（塞擦音）並非官方 IPA 表上的 manner 列（官方以「塞音+擦音」序列表示）；此碼為**預收塞擦音的便利描述式**，輸出仍為帶連結弧的序列（見 §5.8）。表外罕見塞擦音仍用組合式（§6）。

**已知外觀瑕疵：** velar=`ve`，故濁軟顎阻礙音呈雙 v（ɡ=`vvep`、ɣ=`vvef`）。可讀、不歧義。

### 3.2 母音：高低 / 前後 / 圓唇
碼 = 高低(2) + 前後(1) + `[r]`。不圓唇省略、圓唇後綴 `r`。

**高低：** close `cl`｜near-close `nc`｜close-mid `cm`｜mid `md`｜open-mid `om`｜near-open `no`｜open `op`
**前後：** front `f`｜central `c`｜back `b`

### 3.3 非肺氣流與標記類
擊音 click：部位 + `ck`；內爆音 implosive：部位 + `im`；擠喉音 ejective：基底阻礙音碼 + `ej`（見 §6）。

---

## 4. 助記別名收錄規則（已鎖定）

一個碼可收為助記別名，當且僅當：(1) 內部不撞（無兩符號共用同碼）；且 (2) 不與主流系統（X-SAMPA、ARPABET、Praat、Kirshenbaum、SAMPA 等）的既有意義牴觸。符合者即收（不撞就收，允許一符多碼）；牴觸者剔除或改用該系統之碼。每個助記須於來源表（§5B）標明出處。

---

## 5. 完整編碼表

> 欄位：符號 ｜ Unicode ｜ X-SAMPA ｜ 描述式碼 ｜ 助記別名（若有）
> Praat 碼見 §5A；助記來源見 §5B。「—」表示該層不提供。

### 5.1 肺氣流子音

| 符號 | Unicode | X-SAMPA | 描述式 | 助記 |
|---|---|---|---|---|
| p | U+0070 | p | blp | — |
| b | U+0062 | b | vblp | — |
| t | U+0074 | t | alp | — |
| d | U+0064 | d | valp | — |
| ʈ | U+0288 | t` | rxp | — |
| ɖ | U+0256 | d` | vrxp | — |
| c | U+0063 | c | pjp | — |
| ɟ | U+025F | J\ | vpjp | — |
| k | U+006B | k | vep | — |
| ɡ | U+0261 | g | vvep | — |
| q | U+0071 | q | uvp | — |
| ɢ | U+0262 | G\ | vuvp | — |
| ʔ | U+0294 | ? | glp | — |
| m | U+006D | m | bln | — |
| ɱ | U+0271 | F | ldn | — |
| n | U+006E | n | aln | — |
| ɳ | U+0273 | n` | rxn | — |
| ɲ | U+0272 | J | pjn | ny |
| ŋ | U+014B | N | ven | ng |
| ɴ | U+0274 | N\ | uvn | — |
| ʙ | U+0299 | B\ | blr | — |
| r | U+0072 | r | alr | — |
| ʀ | U+0280 | R\ | uvr | — |
| ⱱ | U+2C71 | — | ldt | — |
| ɾ | U+027E | 4 | alt | — |
| ɽ | U+027D | r` | rxt | — |
| ɸ | U+0278 | p\ | blf | — |
| β | U+03B2 | B | vblf | — |
| f | U+0066 | f | ldf | — |
| v | U+0076 | v | vldf | — |
| θ | U+03B8 | T | dnf | th |
| ð | U+00F0 | D | vdnf | dh |
| s | U+0073 | s | alf | — |
| z | U+007A | z | valf | — |
| ʃ | U+0283 | S | paf | sh |
| ʒ | U+0292 | Z | vpaf | zh |
| ʂ | U+0282 | s` | rxf | — |
| ʐ | U+0290 | z` | vrxf | — |
| ç | U+00E7 | C | pjf | — |
| ʝ | U+029D | j\ | vpjf | — |
| x | U+0078 | x | vef | — |
| ɣ | U+0263 | G | vvef | gh |
| χ | U+03C7 | X | uvf | — |
| ʁ | U+0281 | R | vuvf | — |
| ħ | U+0127 | X\ | phf | — |
| ʕ | U+0295 | ?\ | vphf | — |
| h | U+0068 | h | glf | — |
| ɦ | U+0266 | h\ | vglf | — |
| ɬ | U+026C | K | allf | — |
| ɮ | U+026E | K\ | vallf | — |
| ʋ | U+028B | v\ | lda | — |
| ɹ | U+0279 | r\ | ala | — |
| ɻ | U+027B | r\` | rxa | — |
| j | U+006A | j | pja | — |
| ɰ | U+0270 | M\ | vea | — |
| l | U+006C | l | all | — |
| ɭ | U+026D | l` | rxl | — |
| ʎ | U+028E | L | pjl | — |
| ʟ | U+029F | L\ | vel | — |

### 5.2 非肺氣流子音

| 符號 | Unicode | X-SAMPA | 描述式 | 助記 |
|---|---|---|---|---|
| ʘ | U+0298 | O\ | blck | — |
| ǀ | U+01C0 | \|\ | dnck | — |
| ǃ | U+01C3 | !\ | pack | — |
| ǂ | U+01C2 | =\ | pjck | — |
| ǁ | U+01C1 | \|\\|\ | allck | — |
| ɓ | U+0253 | b_< | blim | — |
| ɗ | U+0257 | d_< | alim | — |
| ʄ | U+0284 | J\_< | pjim | — |
| ɠ | U+0260 | g_< | veim | — |
| ʛ | U+029B | G\_< | uvim | — |
| ʼ | U+02BC | _> | （見 §6 ejective） | — |

### 5.3 其他符號

| 符號 | Unicode | X-SAMPA | 描述式 | 助記 |
|---|---|---|---|---|
| ʍ | U+028D | W | lvf | wh |
| w | U+0077 | w | lva | — |
| ɥ | U+0265 | H | lpa | — |
| ʜ | U+029C | H\ | egf | — |
| ʢ | U+02A2 | <\ | vegf | — |
| ʡ | U+02A1 | >\ | egp | — |
| ɕ | U+0255 | s\ | apf | — |
| ʑ | U+0291 | z\ | vapf | — |
| ɺ | U+027A | l\ | allx | — |
| ɧ | U+0267 | x\ | （特殊：ʃ+x，見 §6） | — |

### 5.4 母音

| 符號 | Unicode | X-SAMPA | 描述式 | 助記 |
|---|---|---|---|---|
| i | U+0069 | i | clf | — |
| y | U+0079 | y | clfr | — |
| ɨ | U+0268 | 1 | clc | — |
| ʉ | U+0289 | } | clcr | — |
| ɯ | U+026F | M | clb | — |
| u | U+0075 | u | clbr | — |
| ɪ | U+026A | I | ncf | — |
| ʏ | U+028F | Y | ncfr | — |
| ʊ | U+028A | U | ncbr | — |
| e | U+0065 | e | cmf | — |
| ø | U+00F8 | 2 | cmfr | eu |
| ɘ | U+0258 | @\ | cmc | — |
| ɵ | U+0275 | 8 | cmcr | — |
| ɤ | U+0264 | 7 | cmb | — |
| o | U+006F | o | cmbr | — |
| ə | U+0259 | @ | mdc | ax |
| ɛ | U+025B | E | omf | eh |
| œ | U+0153 | 9 | omfr | oe |
| ɜ | U+025C | 3 | omc | — |
| ɞ | U+025E | 3\ | omcr | — |
| ʌ | U+028C | V | omb | — |
| ɔ | U+0254 | O | ombr | ao |
| æ | U+00E6 | { | nof | ae |
| ɐ | U+0250 | 6 | noc | — |
| a | U+0061 | a | opf | — |
| ɶ | U+0276 | & | opfr | — |
| ɑ | U+0251 | A | opb | aa |
| ɒ | U+0252 | Q | opbr | — |

### 5.5 附加符號（Diacritics）
> 作為 token 附加於基底符號碼之後（見 §6）。標（間隔）者為間隔修飾字母（spacing），其餘為組合字元（combining），影響 NFC 與顯示。

| 名稱 | 符號 | Unicode | X-SAMPA | 描述式 token |
|---|---|---|---|---|
| voiceless 清化 | ◌̥ | U+0325 | _0 | dev |
| voiced 濁化 | ◌̬ | U+032C | _v | voi |
| aspirated 送氣 | ◌ʰ（間隔） | U+02B0 | _h | asp |
| more rounded 較圓 | ◌̹ | U+0339 | _O | rou+ |
| less rounded 較展 | ◌̜ | U+031C | _c | rou- |
| advanced 前移 | ◌̟ | U+031F | _+ | adv |
| retracted 後移 | ◌̠ | U+0320 | _- | ret |
| centralized 央化 | ◌̈ | U+0308 | _" | cen |
| mid-centralized 央化(中) | ◌̽ | U+033D | _x | mce |
| syllabic 成音節 | ◌̩ | U+0329 | = | syl |
| non-syllabic 非成節 | ◌̯ | U+032F | _^ | nsy |
| rhoticity 兒化 | ◌˞（間隔） | U+02DE | ` | rho |
| breathy 氣聲 | ◌̤ | U+0324 | _t | bre |
| creaky 嘎裂聲 | ◌̰ | U+0330 | _k | cre |
| linguolabial 舌唇 | ◌̼ | U+033C | _N | lgl |
| labialized 唇化 | ◌ʷ（間隔） | U+02B7 | _w | lab |
| palatalized 顎化 | ◌ʲ（間隔） | U+02B2 | _' | pzd |
| velarized 軟顎化 | ◌ˠ（間隔） | U+02E0 | _G | vzd |
| pharyngealized 咽化 | ◌ˤ（間隔） | U+02E4 | _?\ | pha |
| velar/pharyngealized | ◌̴ | U+0334 | _e | vph |
| raised 升 | ◌̝ | U+031D | _r | rai |
| lowered 降 | ◌̞ | U+031E | _o | low |
| ATR 舌根前 | ◌̘ | U+0318 | _A | atr |
| RTR 舌根後 | ◌̙ | U+0319 | _q | rtr |
| dental 齒化 | ◌̪ | U+032A | _d | dnt |
| apical 舌尖 | ◌̺ | U+033A | _a | api |
| laminal 舌葉 | ◌̻ | U+033B | _m | lam |
| nasalized 鼻化 | ◌̃ | U+0303 | ~ | nas |
| nasal release 鼻除阻 | ◌ⁿ（間隔） | U+207F | _n | nrl |
| lateral release 邊除阻 | ◌ˡ（間隔） | U+02E1 | _l | lrl |
| no audible release 無聲除阻 | ◌̚ | U+031A | _} | nor |

### 5.6 超音段（Suprasegmentals）

| 名稱 | 符號 | Unicode | X-SAMPA | 描述式 |
|---|---|---|---|---|
| primary stress 主重音 | ˈ | U+02C8 | " | str1 |
| secondary stress 次重音 | ˌ | U+02CC | % | str2 |
| long 長 | ː | U+02D0 | : | lng |
| half-long 半長 | ˑ | U+02D1 | :\ | hln |
| extra-short 極短 | ◌̆ | U+0306 | _X | xsh |
| minor group 小句群 | \| | U+007C | \| | grp1 |
| major group 大句群 | ‖ | U+2016 | \|\| | grp2 |
| syllable break 音節界 | . | U+002E | . | sbr |
| linking 連音 | ‿ | U+203F | -\ | lnk |

### 5.7 聲調與字調（Tones & word accents）— 兩形式皆收
> **調符**（combining，疊於母音）以 `td*`；**調値字母**（Chao staff letter，獨立）以 `tl*`。調符之 X-SAMPA 為 `_T/_H/_M/_L/_B`；調値字母無標準 X-SAMPA，故僅以 `tl` 碼承載。

**位準調（level）：**
| 階 | 調符 | 調符 U+ | `td` 碼 | 調値字母 | 字母 U+ | `tl` 碼 |
|---|---|---|---|---|---|---|
| extra high 超高 | ◌̋ | U+030B | td5 | ˥ | U+02E5 | tl5 |
| high 高 | ◌́ | U+0301 | td4 | ˦ | U+02E6 | tl4 |
| mid 中 | ◌̄ | U+0304 | td3 | ˧ | U+02E7 | tl3 |
| low 低 | ◌̀ | U+0300 | td2 | ˨ | U+02E8 | tl2 |
| extra low 超低 | ◌̏ | U+030F | td1 | ˩ | U+02E9 | tl1 |

**連調（contour）：** 調符提供常見二者；調値字母以 `tl` + Chao 數字串組合（高=5…低=1）。
| 類 | 調符 | 調符 U+ | `td` 碼 | 調値字母例 | `tl` 碼例 |
|---|---|---|---|---|---|
| rising 升 | ◌̌ | U+030C | tdr | ˩˥ | tl15 |
| falling 降 | ◌̂ | U+0302 | tdf | ˥˩ | tl51 |
| 其他連調 | — | — | — | ˨˩˦ 等 | tl214 等（數字串） |

**其他調號（單一標記，無雙形式）：**
| 名稱 | 符號 | Unicode | X-SAMPA | 描述式 |
|---|---|---|---|---|
| downstep 降階 | ꜜ | U+A71C | <D> | dstep |
| upstep 升階 | ꜛ | U+A71B | <U> | ustep |
| global rise 全升 | ↗ | U+2197 | <R> | grise |
| global fall 全降 | ↘ | U+2198 | <F> | gfall |

### 5.8 預收塞擦音（Affricates）
> 輸出為帶連結弧（U+0361）之序列；提供專屬描述式 `af`（§3.1）、X-SAMPA 序列式、與助記。表外罕見塞擦音用組合式（§6）。

| 塞擦音 | Unicode 序列 | X-SAMPA | 描述式 | 助記 |
|---|---|---|---|---|
| t͡s | U+0074 U+0361 U+0073 | ts | alaf | — |
| t͡ʃ | U+0074 U+0361 U+0283 | tS | paaf | ch |
| d͡ʒ | U+0064 U+0361 U+0292 | dZ | vpaaf | jh / dj |
| t͡ɕ | U+0074 U+0361 U+0255 | ts\ | apaf | — |
| d͡ʑ | U+0064 U+0361 U+0291 | dz\ | vapaf | — |

> 註：t͡ʃ、d͡ʒ 嚴格為「齒齦塞音+後齒齦擦音」之異部位組合，沿用通用名「後齒齦塞擦音」（部位 `pa`），屬約定俗成之簡化。

---

## 5A. Praat 三連碼層

**收錄決定：** 納為第四層輸入別名。命名空間獨立——Praat 碼全部以 `\` 起首，其他三層均不以 `\` 起首（X-SAMPA 雖含 `\` 但僅在非開頭位置），故與各層皆不撞名。

**命名規則（Praat 文件）：** 第一字母取最接近的英文字母；第二字母標變形（t=turned、c=capital/curled、s=script、r=reversed、-=barred、/=slashed、i=inverted、j=left-tail）；部分用傳統名拼寫（eng=ŋ、eth=ð、esh=ʃ、yogh=ʒ、schwa=ə 等）。

**已查證範例：** ɡ=`\gs`、ʈ=`\t.`、ɖ=`\d.`、ɟ=`\j-`。

**設定需求（Rime）：** 將 `\` 及 Praat 標點（`. / - < > =`）納入 `speller/alphabet`；`.`/`|` 等亦為超音段碼，須設為「組字中視為碼、不當字面標點上屏」，**POC 實測**。

**建表工作（P2）：** Praat 全碼自官方手冊逐一轉錄，**不於本規格臆造**。

---

## 5B. 助記別名來源

| 符號 | 助記 | 來源 |
|---|---|---|
| ʃ | sh | ARPABET（亦英語拼寫） |
| t͡ʃ | ch | ARPABET（亦英語拼寫） |
| θ | th | ARPABET（亦英語拼寫） |
| ð | dh | ARPABET |
| ŋ | ng | ARPABET（亦英語拼寫） |
| ʒ | zh | ARPABET |
| æ | ae | ARPABET |
| ɛ | eh | ARPABET |
| ɑ | aa | ARPABET |
| ɔ | ao | ARPABET |
| ə | ax | ARPABET |
| d͡ʒ | jh | ARPABET |
| d͡ʒ | dj | 直覺英語（不撞，併收） |
| ɲ | ny | 西班牙語 ñ 羅馬化 |
| ʍ | wh | 英語拼寫（Worldbet 等亦用） |
| ɣ | gh | 阿拉伯/希臘語轉寫 |
| ø | eu | 法語拼寫 |
| œ | oe | 符號本名 o-e ligature（亦法/德語） |

---

## 6. 組合與特殊處理

- 附加符號疊加：基底碼 + diacritic token；常見組合預生成整列，罕見保留自由疊加；輸出 **NFC 正規化**。
- 送氣/清化等：tʰ = `alp`+`asp`（描述式）/ `t_h`（X-SAMPA）。
- 擠喉音：pʼ = `blp`+`ej`（X-SAMPA `p_>`）。
- 塞擦音：預收 5 個見 §5.8（含專屬 `af` 描述式）；**表外塞擦音**用「塞音碼 + 連結弧 + 擦音碼」自由組合，例 t͡ɬ = `alp`+tie+`allf`。連結弧 ◌͡◌（U+0361，上）/ ◌͜◌（U+035C，下）。
- ɧ：單列收錄（X-SAMPA `x\`）。

---

## 7. 多對一彙整
每個符號於碼表中可能對應多列：X-SAMPA、描述式、助記（可多個）、Praat。聲調另有 `td`/`tl` 兩族對應兩種不同輸出。全部依設計指向各自正確的 Unicode 輸出。

---

## 8. 審查狀態

**已鎖定：**
- 描述式縮寫字典（緊湊版、voiced=`v`、清音/不圓唇省略；含 affricate `af`）。
- 唇齒閃音 ⱱ：X-SAMPA 留空。ɺ：`l\`。正規化：NFC。velar=`ve`。
- 助記收錄規則（§4）與來源（§5B）；ah/aw/uh→aa/ao/ax；d͡ʒ 收 jh+dj；移除 gt。
- Praat 收錄與設定需求（§5A）。
- **聲調**：調符 `td*` + 調値字母 `tl*` 兩形式皆收（§5.7）。
- **塞擦音**：預收常見 5 個 + 專屬 `af` 描述式（§5.8）。

**建表工作 / 待查核（P2 階段）：**
1. Praat 全碼自官方手冊轉錄填入 master 表。
2. 主流撞名掃描：每個自訂碼對照 X-SAMPA、ARPABET、Praat、Kirshenbaum、SAMPA（用維基「Comparison of ASCII encodings of the IPA」一表）。
3. 標點優先序 POC：`\` 與標點納入 alphabet 後，`.`/`|` 在組字中不被當字面標點上屏。
4. X-SAMPA 全表覆核（聲調 `_T/_H…` 表記尤須確認）。

**仍待確認（偏好項，不阻擋進 P2）：**
- ʔ 是否日後補助記（視使用頻率）。

---

## 9. 交付與後續
本規格各表即 P2「Master 主資料來源」之列，欄位含 符號／Unicode／X-SAMPA／描述式／助記／助記來源／Praat／說明(zh)[／en…]。聲調以 `td`/`tl` 兩列、塞擦音以 `af` 列併入。§8 建表工作完成後，由產生器輸出 Rime 方案資產。

*本文件為編碼方案 v0.4。編碼設計實質定版；餘項為建表階段之資料轉錄與查核。*
