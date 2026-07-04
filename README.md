# Stock Master

個人股票交易紀錄系統，使用 Python 與 SQLite 建構，透過終端機選單操作。適合用來記錄買賣交易、查詢歷史紀錄、查看目前持股狀況，以及依 FIFO（先進先出）計算已實現損益。

## 功能列表

- **新增買進交易**：記錄股票代號、股數、單價、日期、手續費與備註
- **新增賣出交易**：記錄股票代號、股數、單價、日期、手續費、交易稅與備註
  - 賣出時會檢查目前持股，避免新增超賣交易
- **查看所有交易紀錄**：依交易日期列出全部買賣紀錄
- **查看目前持股**：依 `trades` 資料表計算各股票的淨持有股數
  - 買進增加股數、賣出減少股數
  - 已賣清（股數 = 0）不顯示
- **查看已實現損益**：依 FIFO 配對買進與賣出交易，計算各股票已實現損益
  - 買進成本會包含手續費與交易稅
  - 賣出收入會扣除手續費與交易稅

## 安裝方式

### 需求

- Python 3.9 或以上
- 無需額外安裝第三方套件（僅使用 Python 標準函式庫）

### 取得專案

```bash
git clone <repository-url>
cd Stock_master
```

## 執行方式

在專案根目錄執行：

```bash
python3 main.py
```

啟動後會看到主選單：

```
=== 股票交易紀錄系統 ===
1. 新增買進
2. 新增賣出
3. 查看所有交易紀錄
4. 查看目前持股
5. 查看 Realized PnL
0. 離開
```

### 操作提示

- 交易日期可直接按 Enter，預設為今天（格式：`YYYY-MM-DD`）
- 手續費、交易稅可直接按 Enter 略過，預設為 `0`
- 備註為選填
- 資料庫會在首次執行時自動建立於 `data/stock.db`

### 初始化資料庫（選用）

若只需建立資料庫而不進入選單，可執行：

```bash
python3 -m db.connection
```

## 測試方式

本專案使用 Python 標準函式庫 `unittest`，不需額外安裝套件。

```bash
python3 -m unittest discover -s tests
```

也可以執行 FIFO 損益計算示範腳本：

```bash
python3 scripts/test_pnl_fifo.py
```

## 系統設計

架構圖與主要流程圖請參考：[docs/system_design.md](docs/system_design.md)

## 專案結構

```
Stock_master/
├── main.py                 # 程式進入點
├── config.py               # 資料庫路徑設定
├── cli/                    # 終端機介面
│   ├── menu.py             # 主選單與功能流程
│   ├── prompts.py          # 使用者輸入提示
│   └── display.py          # 表格格式化輸出
├── services/               # 業務邏輯
│   ├── trade_service.py    # 新增買進／賣出交易
│   ├── holdings_service.py # 計算目前持股
│   └── pnl_service.py      # FIFO 已實現損益計算
├── models/                 # 資料結構
│   ├── trade.py            # 交易紀錄
│   ├── holding.py          # 持股彙總
│   └── realized_pnl.py     # 已實現損益彙總
├── db/                     # 資料庫層
│   ├── schema.sql          # trades 資料表定義
│   └── connection.py       # SQLite 連線與初始化
├── docs/                   # 系統設計文件
│   └── system_design.md    # 架構圖與主要流程圖
├── tests/                  # 單元測試
│   ├── test_pnl_service.py # FIFO 損益計算測試
│   └── test_trade_service.py # 交易寫入與超賣防護測試
└── data/                   # SQLite 資料庫（執行後自動產生）
    └── stock.db
```

### 資料表：`trades`

| 欄位 | 說明 |
|------|------|
| `id` | 主鍵 |
| `symbol` | 股票代號 |
| `side` | 交易方向（`buy` / `sell`） |
| `quantity` | 股數 |
| `price` | 成交單價 |
| `fee` | 手續費 |
| `tax` | 交易稅 |
| `trade_date` | 交易日期 |
| `note` | 備註 |
| `created_at` | 建立時間 |

## 未來規劃

- [x] **已實現損益計算**：依 FIFO（先買先賣）配對買賣交易，計算各股票已實現損益
- [x] **單元測試**：為 FIFO 損益邏輯建立基本測試
- [x] **超賣防護**：賣出時檢查持股是否足夠，避免異常負持股
- [x] **系統設計文件**：補充架構圖與主要流程圖
- [ ] **平均成本**：顯示各股票的平均持有成本
- [ ] **交易紀錄管理**：支援查詢、修改、刪除既有交易
- [ ] **資料匯入**：支援從券商 CSV 匯入交易紀錄
- [ ] **測試覆蓋擴充**：為交易寫入、持股計算、輸入驗證建立更多測試
