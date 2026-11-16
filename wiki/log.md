---
title: 操作紀錄
type: overview
sources: []
updated: 2026-11-16
---

# 操作紀錄

只增不改（append-only）。格式：`## [YYYY-MM-DD] <操作> | <標題>`。回到[目錄](index.md)。

## [2026-11-16] discuss | 需求與設計討論

（依當日對話整理）

- 作業與參考：使用者提供作業要求（用「先討論、後生成」建立 LLM Wiki、ingest 至少 5 篇來源、再產生教學型 HTML 簡報、說明 loop／graph、反思），以及 Karpathy 的「LLM Wiki」構想檔作為參考架構。
- 主題：使用者一開始沒有想法。Claude 先提出 AI 相關主題，再應要求提出非 AI 主題（投資、租屋、睡眠科學、求職、讀研究所 vs 工作、咖啡、地方歷史、行為經濟學）。使用者喜歡咖啡和睡眠，擔心「沒有論文」；Claude 說明公開文章與官方網站即可。最後使用者選定「咖啡入門」。
- 學習目標（使用者原話）：走進咖啡店看得懂菜單和豆子標籤、知道自己點什麼。
- 內容比重（Claude 提議、使用者接受）：菜單飲品（重）、豆子標籤（重）、烘焙度（中）、風味輪（中）、沖煮方式（輕，不教操作）、收尾的點餐決策樹。
- 參與程度：使用者選「介於逐篇與批次之間」，形成三個人工檢查點（選來源、檢視第一篇 ingest、檢視 lint 結果），另加簡報大綱確認後才生成 HTML。
- 做法：使用者選 A＋A，即由 Claude Code 依 `CLAUDE.md` 規則執行 graph（不用 LangGraph／API key），簡報為手寫單檔 HTML。
- 獨立審查後的決定：`raw/` 全文只留本機（gitignore），公開的只有 `raw/SOURCES.md`；當日討論記為「先討論」階段；點餐指南為 synthesis 頁，其底層事實引用 concept 頁；繳交預設貼上 GitHub 連結，PDF 匯出為選項。
- 結果：使用者核准設計文件，並選擇以 subagent 逐任務執行並審查。

## [2026-11-16] discuss | 檢查點1：選定來源

- 候選：Claude 提出 7 篇候選：#1 Seattle Coffee Gear〈Espresso Drinks: A Written and Visual Guide〉、#2 La Marzocco〈The Beginner's Guide to Espresso Drinks〉、#3 Seattle Coffee Gear〈How to Read a Specialty Coffee Bag〉、#4 香港01〈咖啡冷知識｜手沖咖啡必知5件事〉、#5 Wikipedia〈Coffee roasting〉、#6 About Coffee（NCA）〈Roasts〉及沖煮分頁、#7 SCA〈How to Use the Coffee Taster's Flavor Wheel in Eight Steps〉。
- 使用者決定：回覆「照建議 6 篇」，選定 #1 #2 #3 #4 #6 #7；未選 #5 Wikipedia Coffee roasting（保留為備選）。
- 已知風險：#7 SCA 頁面在 N1 用 WebFetch 只取得導覽列，正文待確認；#1、#3 是器材商的教學頁、#4 是香港媒體文章，皆非標準文件，留待 lint 交叉比對；風味輪目前只有一篇來源。

## [2026-11-16] fetch | seattle-espresso-drinks-guide

- 網址：https://www.seattlecoffeegear.com/blogs/learning-center/espresso-drinks-guide
- 方式：curl 取原始 HTML，再用 Python 標準庫轉成文字，存為 `raw/seattle-espresso-drinks-guide.md`（已略過選單與購物車文字）。
- 字數：約 3,640 字元（正文，不含檔頭）。
- 涵蓋區塊：菜單飲品。Espresso、Americano、Macchiato、Cortado、Cappuccino、Flat White、Latte、Mocha 皆有說明與比例；16 款圖表只有 alt text。
- 檢查結果：通過。不是付費牆或錯誤頁，涵蓋被選用的區塊。註：ristretto、lungo 只出現在圖片 alt 中，沒有說明。

## [2026-11-16] fetch | la-marzocco-espresso-drinks

- 網址：https://home.lamarzoccousa.com/the-beginners-guide-to-espresso-drinks-2/
- 方式：同上，存為 `raw/la-marzocco-espresso-drinks.md`（已略過「Latest news」等頁尾區塊）。
- 字數：約 11,444 字元。
- 涵蓋區塊：菜單飲品。Espresso、Macchiato、Cortado、Cappuccino、Latte、Flat White、Mocha、Americano 皆出現。
- 檢查結果：通過。

## [2026-11-16] fetch | seattle-read-coffee-bag

- 網址：https://www.seattlecoffeegear.com/blogs/learning-center/how-to-read-a-coffee-bag
- 方式：同上，存為 `raw/seattle-read-coffee-bag.md`。
- 字數：約 5,544 字元。
- 涵蓋區塊：豆子標籤。Origin、Variety、Processing、Elevation、Tasting Notes、Roast Date、Roast Level、Producer Info 皆有獨立段落。
- 檢查結果：通過。

## [2026-11-16] fetch | hk01-pour-over-five-things

- 網址：https://www.hk01.com/教煮/548664/咖啡冷知識-手沖咖啡必知5件事-日曬水洗分別-咖啡豆杯測分級
- 方式：第一次用未編碼的中文網址 curl，回傳 404 錯誤頁（頁面內容為「頁面不存在」）；改用百分比編碼網址後 HTTP 200，正文完整。存為 `raw/hk01-pour-over-five-things.md`（已略過延伸閱讀與相關文章清單）。
- 字數：約 2,380 字元。
- 涵蓋區塊：豆子標籤與處理法（焙度、日曬／水洗、標示資訊、產區、海拔、批次、杯測分級，80 分以上為精品）。
- 檢查結果：通過。註：文章原作者為 GQ Taiwan，由香港01 轉載；5 點中有圖片版內容，圖片文字沒有擷取。

## [2026-11-16] fetch | about-coffee-roasts-and-brewing

- 網址：https://www.aboutcoffee.org/beans/roasts/；沖煮頁 https://www.aboutcoffee.org/brewing/ 與其子頁 drip-coffee、pour-over-coffee、espresso、cold-brew-coffee（網址都在檔內各頁標題處）。
- 方式：同上，存為兩個檔：`raw/about-coffee-roasts.md`（約 3,851 字元）與 `raw/about-coffee-brewing.md`（總覽加 4 個子頁，約 54,148 字元，各頁約 1,281／13,252／15,300／11,600／12,687 字元）。
- 涵蓋區塊：烘焙度（Light、Medium、Dark roast 與常見名稱）；沖煮方式（drip、pour-over、espresso、cold brew）。
- 檢查結果：通過。註：沖煮子頁篇幅長且偏操作步驟與器材，ingest 時只取菜單差異相關的部分（不教操作）。

## [2026-11-16] fetch | sca-flavor-wheel-eight-steps

- 網址：https://sca.coffee/sca-news/how-to-use-the-flavor-wheel-in-eight-steps-ab2hy
- 方式：用 curl 取原始 HTML 即含完整正文（N1 時 WebFetch 只拿到導覽列，這次不需要瀏覽器），存為 `raw/sca-flavor-wheel-eight-steps.md`。
- 字數：約 7,169 字元。
- 涵蓋區塊：風味輪。Step 1 到 Step 8 完整，含「從中心往外」「果味分為莓果、乾果、柑橘…」的使用說明。風味輪圖本身不在正文內。
- 檢查結果：通過。
