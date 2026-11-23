# Meetnote 規格書（SPEC）

> 狀態：草稿 v0.1 ・ 最後更新：2026-11-23
> 標記為 `TBD` 的欄位請依實際需求補上。

## 1. 專案概述
- **名稱**：Meetnote
- **一句話描述**：TBD（例：將會議錄音／逐字稿整理成結構化會議記錄的 Python 工具）
- **目標使用者**：TBD
- **要解決的問題**：TBD

## 2. 範圍
### 2.1 In Scope（這一版要做）
- [ ] TBD

### 2.2 Out of Scope（這一版不做）
- TBD

## 3. 功能需求（Functional Requirements）
| ID | 需求 | 優先級 | 驗收條件 | 對應測試 |
|----|------|--------|----------|----------|
| FR-01 | TBD | Must | TBD | `tests/unit/test_xxx.py` |
| FR-02 | TBD | Should | TBD | TBD |

## 4. 非功能需求（Non-Functional Requirements）
| ID | 類別 | 要求 |
|----|------|------|
| NFR-01 | 相容性 | Python >= 3.10 |
| NFR-02 | 品質 | 單元測試覆蓋率 >= 80% |
| NFR-03 | 效能 | TBD |
| NFR-04 | 隱私／安全 | TBD |

## 5. 系統架構
```
輸入 ──> 解析 ──> 處理 ──> 輸出
 TBD      TBD      TBD      TBD
```
- 主要模組放在 `src/meetnote/`

## 6. 資料模型
```python
# TBD：例
# @dataclass
# class Meeting:
#     title: str
#     date: datetime
#     attendees: list[str]
#     notes: list[str]
#     action_items: list[ActionItem]
```

## 7. 介面（CLI / API）
| 指令／函式 | 輸入 | 輸出 | 說明 |
|-----------|------|------|------|
| TBD | TBD | TBD | TBD |

## 8. 測試策略
| 層級 | 位置 | 說明 | 執行方式 |
|------|------|------|----------|
| 單元測試 | `tests/unit/` | 單一函式／類別，不碰外部資源 | `pytest -m "not integration"` |
| 整合測試 | `tests/integration/` | 多模組串接、檔案 I/O、外部服務 | `pytest -m integration` |
| 測試資料 | `tests/fixtures/` | 範例輸入檔、預期輸出 | — |

- 每條 FR 至少對應一個測試，並填入第 3 節的「對應測試」欄位。
- 共用 fixture 放在 `tests/conftest.py`。

## 9. 里程碑
| 版本 | 內容 | 目標日期 |
|------|------|----------|
| v0.1 | 專案骨架、SPEC、測試環境 | 2026-11-23 |
| v0.2 | TBD | TBD |

## 10. 待決問題（Open Questions）
- [ ] TBD
