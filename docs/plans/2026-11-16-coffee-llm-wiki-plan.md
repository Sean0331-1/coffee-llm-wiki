# 咖啡入門 LLM Wiki ＋ 教學簡報：實作計畫

> **給執行者：** 逐項執行，用 `- [ ]` 追蹤。所有節點的執行結果與檢查（通過／失敗＋原因＋修正）都要寫進 `wiki/log.md`。

**Goal：** 建立咖啡入門 LLM Wiki（≥5 篇來源），並以它為唯一知識來源產生教學 HTML 簡報與繳交報告。

**Architecture：** Claude Code 依 `CLAUDE.md` 的規則執行 8 節點 graph；兩支小型 Python 檢查腳本把「連結有效、事實有引用、簡報每頁有 wiki 出處」變成可機械判斷的檢查；三個人工檢查點加上大綱確認。

**Tech Stack：** Markdown（標準相對連結＋YAML frontmatter）、Python 3.12 標準函式庫（檢查腳本）、單一 HTML／CSS／SVG／原生 JS（簡報）、git＋GitHub Pages。環境中沒有 `gh` CLI，repo 由使用者在 GitHub 網頁建立。

**Spec：** `docs/specs/2026-11-16-coffee-llm-wiki-design.md`

## Global Constraints

- 根目錄：`C:\SEAN\政大\大四上\gen ai\tenth week\`
- 語言：繁體中文，保留英文術語（Washed、Flat White…）。
- 連結格式：`[文字](相對路徑.md)`，禁止 `[[ ]]`。
- frontmatter 欄位：`title`、`type`（source｜concept｜overview｜output｜synthesis）、`sources`、`updated`。
- log 格式：`## [YYYY-MM-DD] <discuss|fetch|ingest|lint|query|outline|generate|check|report> | <標題>`，append-only。
- `raw/*.md` 全文不進 git，只有 `raw/SOURCES.md` 公開。
- 簡報圖片全部自繪 SVG/CSS，不複製外部圖片。
- 推送 GitHub、開 Pages 前要先取得使用者確認；目標 11/22 前完成推送。
- 反思只能根據 `log.md` 的實際紀錄撰寫。

## Review Focus

1. 相對連結在 GitHub 網頁上壞掉（路徑大小寫、空格、中文檔名）→ 檔名一律英文小寫加連字號；`check_wiki.py` 要驗證每個連結都指向存在的檔案。
2. 概念頁出現沒有標來源的段落 → `check_wiki.py` 檢查每個 concept 頁的 frontmatter `sources` 非空，且內文至少有一個指向 `sources/` 的連結。
3. 簡報頁的事實不在引用的 wiki 頁中 → N7 逐頁人工（LLM）核對，並記錄每頁的結果；`check_slides.py` 只負責驗證引用存在。
4. 簡報在手機寬度（375px）爆版或無法翻頁 → Task 8 用瀏覽器 mobile preset 實測，並測試觸控滑動與方向鍵。
5. 某個來源被擋或只抓到摘要 → N2 檢查記錄抓到的正文字數與是否涵蓋預定區塊，不通過就換來源。

---

### Task 1：建立骨架與 schema

**Files：** Create `CLAUDE.md`、`README.md`、`.gitignore`、`raw/SOURCES.md`、`wiki/index.md`、`wiki/log.md`、`wiki/overview.md`（先放占位）、`scripts/check_wiki.py`

**Produces：**
- `CLAUDE.md`：寫入三層架構、頁面慣例（Global Constraints）、8 個節點與各自的檢查規則、三個人工檢查點、出錯時的退回路徑。
- `python scripts/check_wiki.py` → 掃描 `wiki/**/*.md`，輸出並以非零碼結束，當出現：(a) 指向不存在檔案的連結；(b) 缺少 frontmatter 必要欄位；(c) concept 頁 `sources` 為空或內文沒有 `sources/` 連結；(d) 孤兒頁（除 `index.md`、`log.md` 外，沒有任何其他頁連入）。全部通過時輸出 `OK: N pages`。

- [ ] **Step 1：** `git init`；`.gitignore` 內容為 `raw/*` 與 `!raw/SOURCES.md`。
- [ ] **Step 2：** 寫 `CLAUDE.md`、`README.md`（作業說明＋之後要填的三個連結）、`wiki/index.md`（分類：概覽／來源／概念／產出）。
- [ ] **Step 3：** `wiki/log.md` 第一筆：`## [2026-11-16] discuss | 需求與設計討論`，如實摘要主題、學習目標、內容比重、參與程度、做法 A＋A，註明「依當日對話整理」。
- [ ] **Step 4：** 寫 `scripts/check_wiki.py`；先放一個故意壞掉的連結測試頁，執行確認它回報錯誤，再刪除該測試頁。
- [ ] **Step 5：** 執行 `python scripts/check_wiki.py`，預期 `OK`。
- [ ] **Step 6：** Commit `chore: wiki 骨架、schema 與檢查腳本`。

### Task 2：N1 找候選來源 → 檢查點 1

- [ ] **Step 1：** 上網搜尋，提出 6–7 篇可信、公開的來源，合起來要涵蓋：菜單飲品、豆子標籤（產區／海拔／處理法／品種）、烘焙度、風味輪、沖煮方式。每篇附「標題、網址、它補哪一塊」。
- [ ] **Step 2：** 交給使用者挑選（**停下等待**）。
- [ ] **Step 3：** 把使用者的選擇與理由記入 log（`discuss | 檢查點1：選定來源`）。

### Task 3：N2 擷取到 raw/

- [ ] **Step 1：** 每篇抓取後存為 `raw/<slug>.md`，開頭記錄網址、擷取日期、擷取方式。
- [ ] **Step 2：** 檢查：正文有涵蓋預定區塊、不是付費牆或錯誤頁。不通過就換來源（回 Task 2，必要時再問使用者）。每篇結果寫一筆 `fetch` log。
- [ ] **Step 3：** 更新 `raw/SOURCES.md`。Commit `feat: 擷取來源`（全文不會進 git）。

### Task 4：N3 Ingest 第一篇 → 檢查點 2

- [ ] **Step 1：** 讀第一篇，列 5–8 個重點；寫 `wiki/sources/<slug>.md`；建立或更新相關 `wiki/concepts/*.md`（每個事實都要標來源連結）；更新 `index.md`。
- [ ] **Step 2：** 執行 `python scripts/check_wiki.py`，預期 `OK`；失敗就修，並把失敗記入 log。
- [ ] **Step 3：** 給使用者看來源頁與一個概念頁，確認格式、深度、用詞（**停下等待**）。依回饋調整，必要時把新規則寫進 `CLAUDE.md`。
- [ ] **Step 4：** log 記錄 `ingest` 與 `discuss | 檢查點2`。Commit。

### Task 5：N3 Ingest 其餘來源（loop）

- [ ] **Step 1：** 逐篇依第一篇的標準執行。遇到與既有頁面矛盾時，在概念頁寫出「A 說…，B 說…」。
- [ ] **Step 2：** 每篇完成後執行 `check_wiki.py`，失敗就修，並寫一筆 `ingest` log（含「這篇動到哪些頁」）。
- [ ] **Step 3：** 寫好 `wiki/overview.md`。每篇一個 commit。

### Task 6：N4 Lint → 檢查點 3

- [ ] **Step 1：** 執行 `check_wiki.py`，加上 LLM 檢查：來源之間的矛盾、缺頁的概念、學習目標（看懂菜單、看懂標籤、知道點什麼）有沒有被 wiki 完整支撐。
- [ ] **Step 2：** 把 lint 報告交給使用者決定處理方式（**停下等待**）。
- [ ] **Step 3：** 依決定補資料（回 Task 2/3/5）或標註矛盾。log 記錄 `lint` 與 `discuss | 檢查點3`。Commit。

### Task 7：N5 Query ＋ N6 大綱

**Produces：** `wiki/outputs/slide-outline.md`（每頁：標題、重點、引用的 wiki 頁路徑）、`wiki/outputs/ordering-guide.md`（`type: synthesis`）

- [ ] **Step 1：** 讀 `index.md`，依學習目標挑出相關頁面，記錄 `query` log。
- [ ] **Step 2：** 寫點餐決策指南（synthesis 頁，底層事實都引用 concept 頁）與 15–20 頁大綱，結構依 spec 5.5。
- [ ] **Step 3：** 檢查：每頁 ≥1 個 wiki 引用、術語第一次出現時有解釋、三個學習目標都有涵蓋。不通過就重寫，並記錄。
- [ ] **Step 4：** 交給使用者確認大綱（**停下等待**）。執行 `check_wiki.py`。Commit。

### Task 8：N7 生成 HTML 簡報

**Files：** Create `slides/index.html`、`scripts/check_slides.py`

**Produces：**
- 每頁是 `<section class="slide" data-wiki="wiki/concepts/latte.md wiki/…">`，頁尾顯示引用並連到 GitHub 上的該頁（repo 網址未知前，先用相對路徑 `../wiki/...`）。
- `python scripts/check_slides.py` → 驗證每個 `.slide` 都有 `data-wiki`，且每個路徑都存在；頁數介於 15–20 之間。通過時輸出 `OK: N slides`。

- [ ] **Step 1：** 寫 `check_slides.py`，用一個缺少 `data-wiki` 的測試頁確認它會回報錯誤。
- [ ] **Step 2：** 依大綱生成 `slides/index.html`：方向鍵、點擊、觸控滑動翻頁，顯示頁碼，咖啡色系，自繪 SVG（飲品剖面、烘焙色階、簡化風味輪、標籤拆解、決策樹）。
- [ ] **Step 3：** 執行 `check_slides.py`，預期 `OK`。
- [ ] **Step 4：** 事實核對：逐頁比對簡報陳述與引用頁，不符的頁重新生成，每頁結果記入 `check` log。
- [ ] **Step 5：** 在瀏覽器打開：桌面與 mobile（375px）各翻完全部頁面，確認 console 沒有錯誤、沒有爆版。問題記入 log 並修正。
- [ ] **Step 6：** Commit。

### Task 9：N8 報告

**Files：** Create `report.md`

- [ ] **Step 1：** 依 spec 5.6 寫作業 6 項：mermaid 流程圖、文字說明、從 log 摘錄一次完整的執行與檢查紀錄、從 log 統計各節點失敗次數後寫反思（最常出錯的節點、檢查往前移到哪、`CLAUDE.md` 或 graph 改了什麼、為什麼）。
- [ ] **Step 2：** 如果執行中修改過 graph，`CLAUDE.md` 和報告都要寫出修改前後的差異。
- [ ] **Step 3：** 執行 `check_wiki.py` 與 `check_slides.py`，皆預期 `OK`。Commit。

### Task 10：發佈（對外動作，需確認）

- [ ] **Step 1：** 請使用者在 GitHub 建立公開 repo，並提供網址（**停下等待**）。
- [ ] **Step 2：** 推送前執行 `git ls-files raw/`，預期只出現 `raw/SOURCES.md`。
- [ ] **Step 3：** 使用者確認後 `git push`；請使用者在 repo 設定開啟 Pages（branch main、根目錄）。
- [ ] **Step 4：** 把簡報頁尾的引用換成 GitHub 絕對網址，填好 `README.md`、`report.md` 的三個連結，再推送一次。
- [ ] **Step 5：** 用瀏覽器打開 Pages 網址與 repo 頁面，確認簡報能翻頁、引用連結能點開。
- [ ] **Step 6：** 提醒繳交標題格式；若課程平台要求上傳檔案，再匯出 PDF。
