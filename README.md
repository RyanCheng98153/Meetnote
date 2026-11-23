# Meetnote

規格請見 [SPEC.md](SPEC.md)。

## 開發環境

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## 測試

```bash
pytest                       # 全部
pytest -m "not integration"  # 只跑單元測試
pytest -m integration        # 只跑整合測試
pytest --cov=meetnote        # 覆蓋率
```

## 結構

```
src/meetnote/        主程式
tests/unit/          單元測試
tests/integration/   整合測試
tests/fixtures/      測試資料
SPEC.md              規格書
```
