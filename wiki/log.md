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

## [2026-11-16] ingest | seattle-read-coffee-bag

- 來源：`raw/seattle-read-coffee-bag.md`（Seattle Coffee Gear〈How to Read a Specialty Coffee Bag〉）。這是第一篇 ingest，作為之後各篇的校準範本。選它的理由：最貼近「看得懂豆子標籤」的學習目標，且一篇就涵蓋最多欄位。
- 先列出的重點（7 項）：
  1. 豆袋常見八個欄位：產區、品種、處理法、海拔、風味描述、烘焙日期、烘焙度、生產者資訊；逐欄讀懂就能挑到喜歡的豆子。
  2. 產區可細到國家／產區／合作社／水洗站，越細越可追溯；衣索比亞、哥倫比亞、肯亞的風味傾向只是起點，不是規則。
  3. 處理法是影響風味最大的因素之一：水洗乾淨明亮、日曬厚實果味重、蜜處理居中；另有厭氧等實驗處理。
  4. 高海拔（約 1,500 公尺以上）因氣溫低、果實熟得慢，豆子較密、風味較複雜；標籤常用 MASL。
  5. 風味描述是杯測時的印象，不是添加物；只是方向，不是保證。
  6. 烘焙日期可能是最重要的數字：一般烘焙後約 2–4 週最好喝（濃縮約 2–4 週、濾泡約 1–2 週）；賞味期限不等於烘焙日期；充氮包裝是例外。
  7. 烘焙度淺到深，有 City／Full City／French／Italian 等舊稱；各烘焙商標準不同，只有 Agtron 數值可客觀比較。初學者先看產區與處理法，品種之後再研究。
- 新增頁面（9）：`sources/seattle-read-coffee-bag.md`；`concepts/reading-coffee-bags.md`（入口頁，含八欄速查表）、`concepts/origin.md`、`concepts/processing-methods.md`、`concepts/altitude.md`、`concepts/variety.md`、`concepts/tasting-notes.md`、`concepts/roast-date.md`、`concepts/roast-level.md`。
- 更新頁面：`index.md`（來源 1 行、概念 8 行，概念分「豆子標籤」「烘焙度」兩組）；`overview.md`（仍為占位，只加一行連到豆袋入口頁）。
- 判斷：「生產者資訊」原文只有一小段，沒有另立概念頁，併入 `reading-coffee-bags.md`。原文中導購自家商品的句子（依風味方向選購）沒有收錄。每個概念頁都有「相關概念」與「來源間的差異」（目前皆寫「目前僅一個來源」），並註記待其他來源補充的缺口（處理法流程、淺中深焙風味差異、風味輪）。
- 檢查：(1) 逐句核對每個概念頁的事實陳述都對得上原文，且都有行內來源連結，通過；(2) `python scripts/check_wiki.py` 第一次執行即為 `OK: 12 pages`，沒有失敗；(3) index 與 log 已更新，通過。
- 下一步：檢查點2（CP2），請使用者確認格式、深度、用詞後，再批次 ingest 其餘來源。

## [2026-11-16] check | 第一篇 ingest 審查

- 做法：獨立審查者（reviewer subagent）逐句對照 `raw/seattle-read-coffee-bag.md` 與新寫的 wiki 頁。
- 結果：沒有捏造的事實；結論為核可，但列出以下 Minor 問題，因為第一篇是範本，要求修正後才往下做：
  - 5 處來源沒有的補充解釋掛在來源連結旁：處理法定義的「紅色的小果實」、品種頁的「不是變質的酸」、烘焙度頁 Agtron 的「用儀器測量」、烘焙日期頁充氮包裝的「把袋內空氣換成氮氣以減緩氧化」、來源頁 direct trade 的「烘焙商直接向農民採購」。
  - 3 處推論寫在「相關概念」：origin.md「產區風味傾向會反映在風味描述上」、processing-methods.md「日曬豆的風味描述常偏果味」、tasting-notes.md「這些欄位都會影響風味描述會出現什麼詞」（原文只說沖煮方式、研磨、水、味覺會影響喝到的味道）。
  - 1 處推論出的層級排序：origin.md 用「合作社或農場 → 水洗站」箭頭排出原文沒有的由粗到細順序。
  - 1 處缺來源：reading-coffee-bags.md 的定義沒有行內來源，速查表各列也沒有。
  - 1 行寫壞：來源頁用途行「（第 7 節「重」區塊）」語意不清。
- 錯誤源頭節點：N3 ingest。發現時機：ingest 完成後的審查（若沒有這次審查，要到 N4 lint 或 N7 事實核對才會浮現）。

## [2026-11-16] discuss | 檢查點2：第一篇格式確認

- Claude 提出的 3 個問題：(1) 頁面粒度：每個標籤欄位一頁（8 頁，生產者資訊併入入口頁），或合併成大頁？(2) 來源標註：每條重點都行內標註，較冗長，可否接受？(3) 術語白話解釋的深度是否合適？另提出上面審查的忠實度修正，並建議把忠實度核對從 N4／N7 前移到 N3。
- 使用者決定：回覆「照你的建議」，即 (1) 維持 8 個概念頁＋入口頁；(2) 維持逐條行內標註，但連結文字改用來源簡稱，例如「Seattle 豆袋」；(3) 維持第一次出現時的白話解釋；並核准忠實度修正與 graph 修改。
- 頁面修改：
  - 8 個概念頁：來源連結文字由「來源：Seattle Coffee Gear 豆袋指南」改為「Seattle 豆袋」；「相關概念」全部改為純導覽（連結＋一句該頁講什麼）。
  - processing-methods.md：定義刪「紅色的小果實」，「取出、乾燥」改為「把裡面的咖啡豆取出」（原文只在日曬處提到乾燥）。
  - variety.md：刪 acidity 的括號解釋。roast-level.md：Agtron 改為「本 Wiki 補充說明：一種表示烘焙深淺的數值」。roast-date.md：刪充氮包裝的機制解釋。
  - origin.md：拿掉箭頭排序，改為「也可細到……」。
  - reading-coffee-bags.md：定義加來源、「貼紙」改「小標籤」、速查表每列加來源；刪「因為它決定豆子新不新鮮」這句推論。
  - sources/seattle-read-coffee-bag.md：frontmatter 加 `short_name: Seattle 豆袋`；用途行改寫；刪 direct trade 與充氮的機制解釋、「紅色果實」與「乾燥」；刪「美國」與「點單品咖啡」兩處原文沒有的說法。`index.md` 該行加上簡稱。
- 忠實度核對（依新規則自我再核一次）：除審查列出的項目外，另發現 8 處術語白話解釋不是原文內容（cooperative、wash station、single origin、stone fruit、body、cupping、rest，以及 filter 的「例如手沖」），依使用者決定 (3) 保留，但改標「（英文；本 Wiki 補充說明：……）」且不掛來源；origin.md 肯亞的「酸質鮮明」改回原文的 bright。
- CLAUDE.md 修改：第 3 節加入來源簡稱（`short_name`）、concept 頁結構、「相關概念只做導覽」、「本 Wiki 補充說明」標記四條規則；第 5 節 N3 新增第 6 步「忠實度自我核對」（在 `check_wiki.py` 之前），ingest log 固定寫「忠實度核對：發現 N 處，處理方式……」；新增第 10 節「Graph 修改紀錄」，寫明修改前後、原因與代價。
- 檢查：`python scripts/check_wiki.py` 為 `OK: 12 pages`，一次通過。

## [2026-11-16] check | 補充說明標記簡化

- 依 controller 對檢查點2 後續的裁定：術語白話解釋（只說明詞義、不含事實主張）由「（英文；本 Wiki 補充說明：……）」改為括號內解釋結尾加全形 ＊，並在用到的頁面頁尾加一行說明；「（本 Wiki 補充說明）」只保留給原文沒有的事實補充。共改 16 處 ＊（origin 4、processing-methods 1、roast-date 2、roast-level 1、tasting-notes 1、來源頁 7），6 個頁面加頁尾說明；目前 wiki 內沒有事實補充標記。CLAUDE.md 第 3 節、N3 第 6 步與第 10 節 Graph 修改紀錄同步更新。原因：嚴格版標記讓解釋長度約變三倍，而術語定義不是來源主張。`python scripts/check_wiki.py` 為 `OK: 12 pages`。

## [2026-11-16] ingest | seattle-espresso-drinks-guide

- 來源：Seattle Coffee Gear〈Espresso Drinks: A Written and Visual Guide〉（簡稱 Seattle 飲品，`raw/seattle-espresso-drinks-guide.md`）。16 款飲品圖表在擷取時只剩替代文字，圖內比例看不到。
- 重點：(1) 義式飲品由濃縮、蒸奶、奶泡三組件構成，差別在比例與牛奶質地；(2) 文字詳述八款：濃縮咖啡、美式、瑪奇朵、Cortado、卡布奇諾、馥列白、拿鐵、摩卡；(3) 雙份濃縮 14–18 克粉、約 28–36 毫升；(4) 各款杯量（oz）：美式 6–8、瑪奇朵約 2、卡布奇諾 5–6、馥列白 5–6、拿鐵 8–12 以上；(5) 傳統瑪奇朵與星巴克式焦糖瑪奇朵是不同飲品；(6) ristretto、lungo 等只在圖表文字被提到，沒有說明。
- 新增頁面（10）：`sources/seattle-espresso-drinks-guide.md`；`concepts/espresso-drinks.md`（入口頁，含比較表）、`espresso.md`、`americano.md`、`macchiato.md`、`cortado.md`、`cappuccino.md`、`flat-white.md`、`latte.md`、`mocha.md`。
- 更新頁面：`index.md`（來源 1 行、新增「菜單飲品」概念組 9 行）。沒有更動既有概念頁（此來源不談烘焙度或豆子標籤）。`overview.md` 依指示暫不寫（批次 D）。
- 判斷：ristretto／lungo 未另立頁，因來源沒有解釋它們；「在家做」段落不收（非目標）；盎司不換算。
- 忠實度核對：發現 3 處，處理方式：(1) 美式頁「倒水到濃縮是美式」原文只說兩種倒法不同、後者像 long black，改為原文說法；(2) 7 處「相關概念」寫了比較性的主張（如「奶量更少」「杯量相近」），改為中性的一句導覽；(3) 入口頁術語「蒸奶」「奶泡」加 ＊ 標記與頁尾說明，並把馥列白／拿鐵奶泡的差別改為原文說法（融在蒸奶裡／蓋薄薄一層）。其餘每個掛來源的句子都已對回原文。
- 檢查：`python scripts/check_wiki.py`、index 與 log 更新，結果 `OK: 22 pages`，一次通過，沒有失敗。

## [2026-11-16] ingest | la-marzocco-espresso-drinks

- 來源：La Marzocco Home〈The Beginner's Guide to Espresso Drinks〉（簡稱 La Marzocco 飲品，`raw/la-marzocco-espresso-drinks.md`），義式咖啡機廠商的部落格文章，2020 年刊登。
- 重點：(1) espresso 是一種沖煮方式，咖啡與水約 1:2（濾泡約 1:15）；(2) 瑪奇朵義大利式是濃縮加一點奶泡，現代店常加蒸奶；(3) 卡布奇諾傳統三等分，現代精品店約 6 oz、牛奶:濃縮約 1:4、奶泡很少；(4) 拿鐵約 8–12 oz，牛奶:濃縮約 1:5+，latte 在歐洲只是加牛奶的濃縮；(5) 馥列白奶泡層不超過約 0.5 公分、拿鐵約 1 公分；(6) Cortado 等量濃縮與牛奶、4.5 oz gibraltar 杯；(7) 摩卡、美式（雙份加約 8 oz 水）、café au lait；(8) 蒸奶質地與 dry 卡布奇諾。
- 新增頁面（1）：`sources/la-marzocco-espresso-drinks.md`。
- 更新頁面（10）：`concepts/espresso-drinks.md`（新增表二、牛奶質地、café au lait、來源間的差異）；`espresso`、`americano`、`macchiato`、`cortado`、`cappuccino`、`flat-white`、`latte`、`mocha` 八個概念頁（加入 La Marzocco 事實，改寫「來源間的差異」，frontmatter 的 sources 加入此來源）；`index.md`（來源 1 行，入口頁摘要更新）。沒有更動烘焙度等既有概念頁（此來源不談）。
- 矛盾／差異（皆並列「A 說…，B 說…」，沒有選邊或平均）：雙份粉量 14–18 克／毫升（Seattle）對 18 克／克（La Marzocco）；美式總量 6–8 oz 對水約 8 oz；瑪奇朵傳統 vs 現代加蒸奶；卡布奇諾厚奶泡三等分 vs 現代奶泡很少；Cortado 1 份 vs 雙份濃縮。
- 判斷：蒸奶溫度、操作步驟、課程推廣、Sprudge 引文不收；café au lait 只放在入口頁，不另立頁（原文只有一小段且自稱不屬濃縮系）。
- 忠實度核對：發現 4 處，處理方式：(1) 馥列白原寫「兩篇都說比拿鐵咖啡味強」，La Marzocco 並沒有比較強度，改為只說兩篇都說源自澳洲／紐西蘭；(2) 濃縮頁原寫「所以味道濃」是推論，改成分開陳述；(3) 卡布奇諾差異段原有一句我自己的杯量比較與一句雜訊，改為各自說法；(4) 入口頁表二標題原寫「配方皆以雙份濃縮計」，但瑪奇朵配方只寫一份，改為「除瑪奇朵外」並註明現代店未說份數。美式「以稀釋濃縮聞名」改為原文的「加牛奶是拿鐵、加水是美式」。無來源的術語（bar、crema、demitasse）已用 ＊ 並加頁尾說明。
- 檢查：`python scripts/check_wiki.py` 結果 `OK: 23 pages`，一次通過，沒有失敗；index 與 log 已更新。
