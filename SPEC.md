# Meetnote 規格書（SPEC）

> 狀態：草稿 v0.2 ・ 最後更新：2026-11-23
> 標記 `TBD` 或列在「10. 待決問題」的項目，需要進一步討論後才定案。

## 1. 專案概述
- **名稱**：Meetnote
- **一句話描述**：把會議錄音／影片／即時錄音轉成「逐字稿 + 重點筆記 + 可回溯的引用 + 名詞解釋」的會議記錄。
- **目標使用者**：需要整理會議、報告、討論內容的人（TBD：個人使用 / 團隊使用）
- **要解決的問題**：
  1. 會議內容中英夾雜、專有名詞多，一般轉錄工具辨識不準。
  2. 多人發言，事後很難知道「誰說了什麼」。
  3. 正事與閒聊混在一起，人工整理重點很花時間；而閒聊中偶爾也有重要資訊。
  4. 筆記和原始內容脫節，無法快速回去查證原話。

## 2. 會議情境
| 情境 | 描述 | 筆記重點 |
|------|------|----------|
| **報告型** | 1 位或多位主講人報告，其他人提問、討論 | 報告大綱與重點、Q&A（誰問、問什麼、怎麼回答）、後續討論結論 |
| **討論型** | 所有人彼此討論，沒有固定主講人 | 討論議題、各方觀點、共識與分歧、決議、待辦事項 |

- 系統應能自動判斷情境（或由使用者指定），並套用對應的筆記結構。
- 同一場會議可能混合兩種情境（例：先報告、後自由討論）。

## 3. 範圍
### 3.1 In Scope（v1）
- [ ] 輸入：語音檔、影片檔、即時錄音
- [ ] 中英混合語音辨識，含英文專有名詞
- [ ] 講者分離（Speaker Diarization）
- [ ] 帶時間戳的逐字稿
- [ ] 重點筆記（區分正事／閒聊，閒聊中的相關資訊需甄別保留）
- [ ] 引用（Reference）：筆記每一條都能對應回逐字稿與原始媒體時間點
- [ ] 名詞解釋（Glossary）：一兩句白話解釋

### 3.2 Out of Scope（v1 暫不做，待討論）
- 中英以外語言
- 多人即時協作編輯
- 自動寄送會議記錄／整合行事曆

## 4. 處理流程
```
 ┌───────────┐   ┌──────────┐   ┌──────────────┐   ┌────────────┐
 │ 輸入        │──>│ 前處理     │──>│ 語音辨識 ASR  │──>│ 講者分離     │
 │ 音檔/影片/  │   │ 抽音軌、   │   │ 中英混合 +    │   │ 對齊講者與   │
 │ 即時錄音    │   │ 轉格式、切段│   │ 專有名詞詞庫  │   │ 時間戳       │
 └───────────┘   └──────────┘   └──────────────┘   └─────┬──────┘
                                                          v
 ┌───────────┐   ┌──────────────────────────────────────────────┐
 │ 輸出        │<──│ 內容分析（LLM）                                │
 │ 會議記錄    │   │ 1. 逐字稿校正（專有名詞、標點）                 │
 │            │   │ 2. 情境判斷（報告型/討論型）                     │
 │            │   │ 3. 段落分類（正事 / 閒聊 / 閒聊但相關）          │
 │            │   │ 4. 重點筆記 + Reference                          │
 │            │   │ 5. 名詞解釋 Glossary                             │
 └───────────┘   └──────────────────────────────────────────────┘
```

## 5. 功能需求（Functional Requirements）

### 5.1 輸入
| ID | 需求 | 優先級 | 驗收條件 | 對應測試 |
|----|------|--------|----------|----------|
| FR-IN-01 | 支援語音檔輸入 | Must | 可讀取 wav / mp3 / m4a（TBD：其他格式） | `tests/unit/test_input.py` |
| FR-IN-02 | 支援影片檔輸入 | Must | 可從 mp4 / mov / mkv 抽出音軌後處理 | `tests/unit/test_input.py` |
| FR-IN-03 | 支援即時錄音 | Must | 可從麥克風錄音，結束後產出記錄（TBD：是否需邊錄邊出逐字稿） | `tests/integration/test_live.py` |
| FR-IN-04 | 使用者可提供專有名詞詞庫 | Should | 提供詞表後，詞表內名詞辨識正確率提升 | `tests/unit/test_vocab.py` |
| FR-IN-05 | 使用者可提供會議背景資訊 | Could | 可輸入會議主題、與會者姓名、簡報檔等，作為辨識與筆記的提示 | TBD |

### 5.2 逐字稿
| ID | 需求 | 優先級 | 驗收條件 | 對應測試 |
|----|------|--------|----------|----------|
| FR-TR-01 | 中英混合辨識 | Must | 中文句中夾英文詞（例：「這個 API 的 latency 太高」）能正確保留英文 | `tests/integration/test_asr.py` |
| FR-TR-02 | 英文專有名詞正確拼寫 | Must | 專有名詞以正確大小寫與拼法呈現（例：Kubernetes、PyTorch） | `tests/integration/test_asr.py` |
| FR-TR-03 | 講者標記 | Must | 每段標示講者（Speaker A/B/…），可由使用者改成真實姓名 | `tests/unit/test_diarization.py` |
| FR-TR-04 | 時間戳 | Must | 每段有開始／結束時間（`HH:MM:SS`） | `tests/unit/test_transcript.py` |
| FR-TR-05 | 段落編號 | Must | 每段有唯一 ID（例：`T-0042`），供 Reference 使用 | `tests/unit/test_transcript.py` |
| FR-TR-06 | 標點與分段 | Should | 逐字稿有合理標點，依講者與語意分段 | TBD |
| FR-TR-07 | 中文輸出字體 | Must | 輸出繁體中文（TBD：是否需可切換簡體） | `tests/unit/test_transcript.py` |

### 5.3 筆記
| ID | 需求 | 優先級 | 驗收條件 | 對應測試 |
|----|------|--------|----------|----------|
| FR-NT-01 | 會議摘要 | Must | 3–5 句說明會議在講什麼、結論是什麼 | `tests/unit/test_notes.py` |
| FR-NT-02 | 報告型筆記結構 | Must | 包含：報告大綱、各段重點、Q&A（提問者／問題／回答者／回答） | `tests/unit/test_notes.py` |
| FR-NT-03 | 討論型筆記結構 | Must | 包含：議題、各方觀點、共識／分歧、決議 | `tests/unit/test_notes.py` |
| FR-NT-04 | 決議與待辦事項 | Must | 列出決議與 Action Items（負責人、期限，若會議中有提到） | `tests/unit/test_notes.py` |
| FR-NT-05 | 正事／閒聊分類 | Must | 每段逐字稿標記為「正事」「閒聊」「閒聊但相關」；閒聊不進主要筆記 | `tests/unit/test_classify.py` |
| FR-NT-06 | 閒聊中的有用資訊 | Must | 「閒聊但相關」的內容（例：玩笑中帶出的期限、顧慮）另列一區，並註明出處 | `tests/unit/test_classify.py` |
| FR-NT-07 | 重點優先 | Should | 筆記依重要性排序，最重要的放最前面 | TBD |

### 5.4 Reference（引用）
| ID | 需求 | 優先級 | 驗收條件 | 對應測試 |
|----|------|--------|----------|----------|
| FR-RF-01 | 筆記可回溯逐字稿 | Must | 每條筆記附上來源段落 ID 與時間（例：`[T-0042 @ 00:12:35]`） | `tests/unit/test_reference.py` |
| FR-RF-02 | 引用可點擊跳轉 | Should | 點擊引用可跳到逐字稿對應段落 | TBD |
| FR-RF-03 | 引用可跳到原始媒體 | Should | 點擊引用可從該時間點播放原音／影片 | TBD |
| FR-RF-04 | 引用正確性 | Must | 引用的段落確實包含支持該筆記的內容（不可捏造） | `tests/unit/test_reference.py` |

### 5.5 名詞解釋（Glossary）
| ID | 需求 | 優先級 | 驗收條件 | 對應測試 |
|----|------|--------|----------|----------|
| FR-GL-01 | 自動挑出需解釋的名詞 | Must | 挑出專有名詞、縮寫、行話、不易理解的概念 | `tests/unit/test_glossary.py` |
| FR-GL-02 | 白話解釋 | Must | 每個名詞 1–2 句、精準且白話；以這場會議的語境解釋 | `tests/unit/test_glossary.py` |
| FR-GL-03 | 名詞出處 | Should | 標示名詞在逐字稿中首次出現的位置 | `tests/unit/test_glossary.py` |
| FR-GL-04 | 延伸閱讀 | Could | 附上可查證的外部參考連結（TBD：是否需要、來源為何） | TBD |

## 6. 非功能需求（Non-Functional Requirements）
| ID | 類別 | 要求 |
|----|------|------|
| NFR-01 | 相容性 | Python >= 3.10 |
| NFR-02 | 品質 | 單元測試覆蓋率 >= 80% |
| NFR-03 | 準確度 | TBD：逐字稿字錯誤率（CER）目標 |
| NFR-04 | 效能 | TBD：1 小時會議的處理時間上限 |
| NFR-05 | 會議長度 | TBD：最長支援幾小時 |
| NFR-06 | 隱私 | TBD：音檔是否可上傳雲端，或必須在本機處理 |
| NFR-07 | 成本 | TBD：每場會議可接受的 API 費用 |

## 7. 資料模型（初稿）
```python
@dataclass
class Segment:                 # 逐字稿一段
    id: str                    # "T-0042"
    speaker: str               # "Speaker A" 或真實姓名
    start: float               # 秒
    end: float
    text: str
    category: Literal["business", "chitchat", "chitchat_relevant"]

@dataclass
class Reference:
    segment_ids: list[str]
    start: float               # 供跳轉原始媒體

@dataclass
class NoteItem:
    text: str
    references: list[Reference]

@dataclass
class GlossaryEntry:
    term: str
    explanation: str           # 1–2 句白話解釋
    first_seen: Reference

@dataclass
class MeetingRecord:
    source: str                # 原始檔路徑
    mode: Literal["presentation", "discussion", "mixed"]
    speakers: dict[str, str]   # "Speaker A" -> "王小明"
    transcript: list[Segment]
    summary: list[NoteItem]
    notes: dict[str, list[NoteItem]]   # 依情境的章節
    decisions: list[NoteItem]
    action_items: list[NoteItem]
    side_notes: list[NoteItem]         # 閒聊但相關
    glossary: list[GlossaryEntry]
```

## 8. 輸出格式（初稿，待討論）
```markdown
# 會議記錄：<主題>
日期／時長／與會者／會議型態

## 摘要
- ……[T-0003 @ 00:01:12]

## 報告重點 / 討論議題
## Q&A
## 決議
## 待辦事項
## 閒聊中的相關資訊
## 名詞解釋
- **RAG**（Retrieval-Augmented Generation）：先從資料庫找出相關資料，再交給 AI 參考後回答，讓回答更有根據。[T-0010]

## 逐字稿
[T-0001] 00:00:05 Speaker A：……
```

## 9. 測試策略
| 層級 | 位置 | 說明 | 執行方式 |
|------|------|------|----------|
| 單元測試 | `tests/unit/` | 單一函式／類別，ASR 與 LLM 以 mock 取代 | `pytest -m "not integration"` |
| 整合測試 | `tests/integration/` | 實際跑 ASR／LLM、檔案 I/O | `pytest -m integration` |
| 測試資料 | `tests/fixtures/` | 範例音檔（中英夾雜、多講者、含閒聊）、預期逐字稿 | — |

- 每條 FR 至少對應一個測試，並填入第 5 節的「對應測試」欄位。
- 需要準備的測試樣本：
  - [ ] 單講者、中英夾雜、含專有名詞的短音檔
  - [ ] 報告型：主講人 + 2 位提問者
  - [ ] 討論型：3 人以上自由討論
  - [ ] 含閒聊、玩笑（其中有一句與會議相關）的片段
  - [ ] 短影片檔

## 10. 待決問題（Open Questions）
- [ ] **Q1 本機 vs 雲端**：音檔能否上傳到雲端服務（ASR、LLM）？會影響技術選型與隱私。
- [ ] **Q2 即時錄音的要求**：錄完再處理即可，還是要邊錄邊出逐字稿／筆記？
- [ ] **Q3 使用介面**：CLI、桌面 App、網頁？
- [ ] **Q4 輸出格式**：Markdown、HTML（可點擊跳轉、可播放）、Word、Notion…？
- [ ] **Q5 講者姓名**：自動用 Speaker A/B，事後手動改名即可？還是需要聲紋辨識固定成員？
- [ ] **Q6 筆記語言**：一律繁中？專有名詞保留英文？
- [ ] **Q7 名詞解釋來源**：只靠 LLM 知識，還是需要上網查證並附連結？
- [ ] **Q8 硬體**：本機是否有 GPU？（影響能否在本機跑 Whisper / 講者分離）
- [ ] **Q9 會議規模**：一般會議長度與人數？
- [ ] **Q10 人工校正**：使用者是否需要在產出前後修改逐字稿，並讓筆記重新生成？

## 11. 里程碑（初稿）
| 版本 | 內容 | 目標日期 |
|------|------|----------|
| v0.1 | 專案骨架、SPEC、測試環境 | 2026-11-23 |
| v0.2 | SPEC 定案（解決第 10 節待決問題） | TBD |
| v0.3 | 音檔／影片 → 帶講者與時間戳的逐字稿 | TBD |
| v0.4 | 筆記、正事／閒聊分類、Reference | TBD |
| v0.5 | 名詞解釋、輸出格式 | TBD |
| v0.6 | 即時錄音 | TBD |
