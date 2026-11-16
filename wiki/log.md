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

## [2026-11-16] discuss | 檢查點1b：追加來源

- 起因：檢查點1之後，使用者表示「多找一些再找四篇」。這是一次由使用者觸發、從 N2 回到 N1（再找來源）的迴圈。
- 第二輪搜尋：Claude 提出 6 篇候選 #8–#13：#8 Trade〈The Coffee Taster's Flavor Wheel, Explained〉、#9 Urnex〈Reinventing the Coffee Taster's Flavor Wheel〉、#10 World Coffee Research〈Sensory Lexicon〉、#11 Coffee Hero〈Coffee Processing Methods: Washed, Natural and Honey Explained〉、#12 維基百科〈Coffee varieties〉（原先列的 WCR 品種目錄疑為 JS 動態載入，改用維基百科）、#13 Nespresso 台灣的三篇專文（咖啡種類、Flat White、拿鐵）。
- 建議：subagent 建議 #8 #10 #11 #13；Claude 建議 #8 #11 #12 #13，把 #10 換成 #12。理由是缺口分析（gap analysis）發現沒有任何來源涵蓋豆子標籤的「品種」欄位，而 SCA 風味輪頁已經成功擷取，不再需要 WCR Sensory Lexicon 來頂替。
- 使用者決定：回覆「全部都納進來」，6 篇全數加入，來源總數變成 12 篇。
- 接下來：依 N2 擷取這 6 篇。

## [2026-11-16] fetch | trade-flavor-wheel-explained

- 網址：https://drinktrade.com/blog/education/coffee-tasters-flavor-wheel
- 方式：curl 取原始 HTML，再用 Python 標準庫轉成文字，存為 `raw/trade-flavor-wheel-explained.md`（已略過選單、購物與 FAQ 區塊）。
- 字數：約 7,476 字元。
- 涵蓋區塊：風味輪。風味輪的歷史（1995 年首版、2016 年改版）、「由中心往外」的讀法、各層級舉例、缺陷區，並提到品種與處理法對風味的影響（Gesha、Bourbon、Washed、Natural）。
- 檢查結果：通過。註：發文日為 2020-10-07；來源是訂閱平台的教育文，屬商業來源。

## [2026-11-16] fetch | urnex-reinventing-flavor-wheel

- 網址：https://urnex.com/blog/reinventing-the-coffee-tasters-flavor-wheel
- 方式：同上，存為 `raw/urnex-reinventing-flavor-wheel.md`。
- 字數：約 8,544 字元。
- 涵蓋區塊：風味輪。2016 年改版的過程（WCR 詞彙表是基礎、110 個詞、每個詞有參照配方）、center-out 讀法、用途，可與 Trade 那篇交叉驗證。
- 檢查結果：通過。註：來源是清潔用品廠商的部落格，權威性低於 WCR，當作第二來源。

## [2026-11-16] fetch | wcr-sensory-lexicon

- 網址：https://worldcoffeeresearch.org/resources/sensory-lexicon；另一頁 https://worldcoffeeresearch.org/work/sensory-lexic 實測會 302 轉址到同一頁，內容完全相同，所以只存一個檔 `raw/wcr-sensory-lexicon.md`。
- 方式：同上。依指示只取簡介文字，沒有下載詞彙表 PDF。
- 字數：約 1,698 字元。
- 涵蓋區塊：風味輪／品飲詞彙的官方背景。Lexicon 2.0（2017 年 10 月出版）、110 個風味／香氣／質地屬性、由 Kansas State University 的 Sensory Analysis Center 建立、是新版風味輪的基礎。
- 檢查結果：通過，但篇幅短。簡介頁沒有詞彙表本體，只能當官方背景與交叉驗證用。

## [2026-11-16] fetch | coffee-hero-processing-methods

- 網址：https://coffeehero.com.au/blogs/news/coffee-processing-methods-washed-natural-honey-explained
- 方式：同上。原始 HTML 約 2.9 MB，轉成文字後正文乾淨可用（約 200 行），不需要改用備選的 Attendant Coffee。已略過導覽、相關文章與購物區塊。
- 字數：約 6,404 字元。
- 涵蓋區塊：處理法。Washed、Natural、Honey 的流程與風味、Yellow／Red／Black Honey 色階、比較表、怎麼在豆袋上找到處理法。
- 檢查結果：通過。註：來源是澳洲烘焙商，用英式拼法 flavour。

## [2026-11-16] fetch | wikipedia-coffee-varieties

- 網址：https://en.wikipedia.org/wiki/Coffee_varieties（轉址到 List of coffee varieties）
- 方式：同上，存為 `raw/wikipedia-coffee-varieties.md`（已略過 See also 與參考文獻）。
- 字數：約 19,474 字元。
- 涵蓋區塊：豆子標籤的「品種」欄。Variety 與 cultivar 的術語、選種標準、C. arabica 與 C. canephora（robusta）、品種清單（Bourbon、Typica 等及其由來）。
- 檢查結果：通過。註：內容偏技術且很長，ingest 時只取初學者需要的部分；維基百科內容可能被編輯，以擷取日為準。
- 另記：計畫中原本的 WCR 品種目錄（varieties.worldcoffeeresearch.org）疑為 JS 動態載入，N1 時已改用維基百科，所以沒有擷取它。

## [2026-11-16] fetch | nespresso-tw-coffee-types

- 網址：https://www.nespresso.com/tw/zh/blog-coffee-type 、 https://www.nespresso.com/tw/zh/blog-flat-white 、 https://www.nespresso.com/tw/zh/blog-latte-feature
- 方式：同上，三頁合併存為 `raw/nespresso-tw-coffee-types.md`，各頁標題處標有網址（已略過文末的機型推薦區塊）。
- 字數：約 12,707 字元（三頁約 7,322／2,965／2,402）。
- 涵蓋區塊：台灣菜單用語（繁體中文）。10 款飲品與濃縮咖啡／牛奶比例、Flat White 的中文名稱（馥芮白、馥列白、平白咖啡、澳式白咖啡）及與拿鐵、卡布奇諾的差異、拿鐵與美式的比較；第一篇另有品種、處理法、烘焙度的簡短說明。
- 檢查結果：通過。註：品牌（膠囊機）教育文，比例偏向膠囊機，ingest 時要與 Seattle Coffee Gear、La Marzocco 交叉比對；文內含食譜與機型推薦，只取飲品知識。
