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

## [2026-11-16] ingest | nespresso-tw-coffee-types

- 來源：Nespresso 台灣三篇專文（咖啡種類、Flat White、拿鐵；簡稱 Nespresso 台灣，`raw/nespresso-tw-coffee-types.md`）。繁體中文品牌（膠囊機）教育文，建議量是膠囊定量，已略過機型與膠囊導購。
- 重點：(1) 10 款飲品的建議量（毫升）：濃縮 40、拿鐵 40:120＋奶泡、卡布奇諾 40:40:40、摩卡 40:40（熱可可）:20（奶泡）、拿鐵瑪奇朵 40＋牛奶奶泡 125、康寶藍 40:40 鮮奶油、阿芙加朵；(2) 台灣用詞：馥芮白／馥列白／平白／澳式白咖啡沒有標準用詞，拿鐵代表濃縮加牛奶與熱奶泡；(3) Flat White 咖啡:牛奶 1:2 或 1:3、薄奶泡約 0.5 公分，介於拿鐵與卡布奇諾之間；(4) 淺／中／深焙的風味方向，以及加牛奶時中至深焙較保留咖啡香；(5) 處理法（日曬、水洗、蜜處理、濕剝法）、三大豆種、海拔與環境；(6) 冷萃（>12 小時、1:16）與冰滴（≥2 小時、1:10）；(7) 拿鐵的優缺點（柔和適合入門，咖啡味較淡、熱量較高）。
- 新增頁面（2）：`sources/nespresso-tw-coffee-types.md`；`concepts/cold-brew.md`（冷萃與冰滴）。
- 更新頁面（13）：`concepts/espresso-drinks.md`（表三、台灣常見名稱、康寶藍與阿芙加朵、來源間的差異改寫成三來源）；七個飲品概念頁 `espresso`、`americano`、`macchiato`、`cappuccino`、`latte`、`mocha`、`flat-white`（加入此來源並更新來源間的差異；`cortado` 沒有動，此來源沒談）；`roast-level.md`（淺中深焙風味、搭配牛奶、來源間的差異改寫，補上原先「待補充」的缺口）、`processing-methods.md`（日曬／水洗／蜜處理細節、濕剝法）、`variety.md`（三大豆種）、`altitude.md`（低海拔與溫差說法）；`index.md`（來源 1 行、新增冷萃頁、更新數個概念頁摘要）。
- 矛盾／差異（皆並列「A 說…，B 說…」）：瑪奇朵（Seattle 與 La Marzocco 的濃縮加一點奶泡，對 Nespresso 的 125 毫升牛奶奶泡加 40 毫升濃縮，差別最大）；拿鐵牛奶倍數（Nespresso 1:3，La Marzocco 1:5+）；摩卡（拿鐵加巧克力，對 40:40:20 熱可可）；濃縮量（28–36 對 40）；萃取是「蒸氣」（Nespresso）還是「熱水加壓」（La Marzocco）；Nespresso 自己的文章裡美式一處說「減少苦韻」、一處說「苦韻較拿鐵明顯」，馥列白與拿鐵的牛奶比例在 1:3 時相同但說馥列白較少。單位（毫升對盎司、克）不換算；烘焙度、處理法、品種、海拔沒有直接衝突，只是層級或面向不同。
- 更正：前一筆 Seattle 飲品 ingest 的 log 與其間的頁面寫「ristretto／lungo 只在圖表文字被提到」。重看原文，這些名字也出現在文章開頭的正文（同樣只列名、沒有說明），所以結論（沒有說明、不立頁）不變，只有「只在圖表」不精確；log 為 append-only，在此更正。
- 判斷：Nespresso 的「拿鐵瑪奇朵」不併入 Seattle 的 Macchiato 頁內容，而是在同一頁並列；康寶藍、阿芙加朵各只有一小段，放在入口頁，不另立頁；冷萃與冰滴有定義、時間、比例，另立 `cold-brew.md`；空腹喝拿鐵與減重提醒屬健康建議，不收；膠囊、機型、食譜導購不收。
- 忠實度核對：發現 6 處，處理方式：(1) 冷萃頁定義原寫「菜單上常見為冰咖啡類」，原文沒有，刪除，並把「冷水或常溫水慢慢萃取」改為對兩者都成立的「低溫、長時間」；(2) 瑪奇朵頁原寫「台灣用『拿鐵瑪奇朵』稱呼」，原文只是 Nespresso 的用詞，改為「Nespresso 台灣把這款叫……」；(3) 摩卡頁一句「三者都有鮮奶油或奶泡的說法但不完全一致」太含糊，改為逐來源說明；(4) 濃縮頁原寫 40 毫升「比兩者的雙份量都大」，但兩者單位是毫升與克，改為「數字上比…範圍大」並註明不換算；(5) 馥列白頁原寫「三篇都說源自澳洲」，Seattle 與 La Marzocco 寫澳洲或紐西蘭，改為並列寫法；(6) 入口頁原寫 Seattle「只在圖表替代文字」提到 café con panna，原文正文也有，改為「提到圖表涵蓋」。其餘每個掛來源的句子都已對回原文；術語＊保留在入口頁與濃縮、瑪奇朵頁並有頁尾說明。
- 檢查：`python scripts/check_wiki.py` 結果 `OK: 25 pages`，一次通過，沒有失敗；index 與 log 已更新。

## [2026-11-16] check | 批次A 審查

- 做法：審查者抽查約 40 處陳述，對照 `raw/` 原文。
- 結果：所有數字與比例都對得上原文；發現 2 處跨來源綜合句過度概括（皆在 `concepts/espresso-drinks.md`）：(1) 重點把 La Marzocco 寫成說「差別在牛奶的量與質地」，原文只問各飲品的本質差在哪，已改為「在卡布奇諾與拿鐵的說明中以牛奶與濃縮比例區分」；(2) 來源間的差異開頭「三篇一致：由濃縮、牛奶、奶泡組成」沒有引用，且 La Marzocco 與 Nespresso 沒有這樣陳述，已改為中性開場。另有 4 處較小的措辭問題，暫緩處理。
- 錯誤源頭節點：N3 ingest（第 6 步自我核對漏掉）。規律：跨來源綜合句最容易過度概括。
- 規則修改：CLAUDE.md N3 第 6 步加一句，並在第 10 節記錄修改前後與原因。
- 檢查：`python scripts/check_wiki.py` 結果 `OK: 25 pages`。

## [2026-11-16] ingest | hk01-pour-over-five-things

- 來源：香港01〈咖啡冷知識｜手沖咖啡必知5件事〉（轉載 GQ Taiwan；簡稱 HK01 手沖，`raw/hk01-pour-over-five-things.md`）。文章開頭的「五件事」圖卡沒有擷取到，只依文字整理，未推測圖卡內容。
- 重點：(1) 焙度最直接影響風味：淺焙酸甜、深焙苦；(2) 日曬（Dry）／水洗（Wet）最大宗，依產地水源與日照決定；日曬飽滿濃甜、水洗乾淨明亮口感偏酸；蜜處理又稱半水洗；(3) 最基本標示為產區、焙度、處理法，進階有微產區、莊園、海拔、批次、預期風味、生產履歷；(4) 挑豆看大小均勻與聞香；(5) 杯測評分項目與 COE 為例的分數區間（69 以下、70–74、75–79、80+ 精品、86+ 優勝、90+）。
- 新增頁面（2）：`sources/hk01-pour-over-five-things.md`；`concepts/cupping-score.md`（杯測分數與精品等級；HK01 手沖已有完整區間與評分項目，故另立）。
- 更新頁面（6）：`processing-methods`（日曬水洗蜜處理說法、來源間的差異）、`roast-level`（淺深焙風味、深焙與好豆的說法、差異）、`reading-coffee-bags`（基本與進階標示、挑豆、差異）、`origin`、`altitude`、`tasting-notes`（各補一兩條與差異）；`index.md`（來源 1 行、新概念 1 行）。`variety`、`roast-date` 不動（此來源未談）。
- 差異（並列「A 說…，B 說…」）：水洗風味，HK01 手沖說「口感偏酸」，Nespresso 台灣說「酸度較明亮」，Seattle 豆袋只說乾淨明亮；蜜處理，HK01 手沖稱半水洗並只講做法，Nespresso 台灣分白黃紅黑蜜；處理法名稱 Dry／Wet、Natural／Washed、乾式／濕式；基本標示，HK01 手沖列焙度為最基本，Seattle 豆袋說不是每包都標烘焙度；杯測 69 與 70 分之間原文留有間隙，照列。海拔、品種沒有衝突（HK01 手沖不談門檻與品種）。
- 判斷：酸甜與苦的描述不與 Nespresso 合併成「多來源一致」，只並列；SCAA 只被點名為杯測方法，沒有給分數，不補；沖煮技巧、咖啡營養文章連結不收。
- 忠實度核對：發現 2 處，處理方式：(1) 來源頁原寫「處理法、焙度與 Seattle 豆袋、Nespresso 台灣大致同向」，但 Seattle 豆袋並未談焙度風味，改為只指向概念頁；(2) 來源頁原寫分數區間是「本 Wiki 唯一給出具體數字的來源」，是對整個 Wiki 的主張，改為「目前只有這篇給出」。處理法差異段的跨來源敘述逐一對回 Seattle、Nespresso、HK01 原文（水洗酸度、日曬口感、Dry/Wet 與乾式/濕式用詞）後保留。
- 檢查：`python scripts/check_wiki.py` 結果 `OK: 27 pages`；index 與 log 已更新。

## [2026-11-16] ingest | coffee-hero-processing-methods

- 來源：Coffee Hero〈Coffee Processing Methods: Washed, Natural and Honey Explained〉（簡稱 Coffee Hero，`raw/coffee-hero-processing-methods.md`），澳洲烘焙商的英文教學文。
- 重點：(1) 處理法是採收後去除果肉的方式，決定果實糖分與風味轉移多少；(2) 水洗：去果肉機、水槽發酵 24–72 小時、洗淨乾燥，風味乾淨明亮酸度高；(3) 日曬：整顆果實乾燥 3–6 週，口感厚、酸度低、果味強；(4) 蜜處理：黃蜜（去除最多、近水洗）、紅蜜、黑蜜（留最多、近日曬）三級；(5) 比較表（口感、酸度、甜感、用水量）；(6) 各處理法的常見產地與適合的沖法；(7) 豆袋上的寫法（washed、fully washed、natural、pulped natural、yellow honey 等），沒寫就問烘焙商。
- 新增頁面（1）：`sources/coffee-hero-processing-methods.md`。
- 更新頁面（5）：`concepts/processing-methods.md`（新增流程、色階表、比較表、選豆建議、袋上寫法；來源間的差異重寫為四來源並列）；`origin`（處理法與常見產地對應）、`reading-coffee-bags`（處理法袋上寫法與詢問）、`tasting-notes`（處理法對應的風味詞）；`index.md`（來源 1 行、處理法摘要）。`roast-level`、`altitude`、`variety`、`cupping-score` 不動（此來源未談）。
- 差異（皆並列「A 說…，B 說…」，沒有選邊）：蜜處理分級，Nespresso 台灣四種（含白蜜）對 Coffee Hero 三種（黃紅黑）；蜜處理口感，Seattle 豆袋說「比日曬更有結構」、Coffee Hero 表中說中到厚；水洗酸度的各家說法；常見產地，Nespresso 台灣說日曬常見於肯亞，Coffee Hero 把肯亞列在水洗產地；處理法的決定因素，HK01 手沖說由產地水源與日照決定，Coffee Hero 沒談。Coffee Hero 把哥倫比亞歸在中美洲，照原文轉述。
- 判斷：選豆建議（水洗從衣索比亞或肯亞開始等）屬單一來源建議，標明「該文」；文末導向自家文章的句子不收；沒有新增概念頁（處理法已有頁）。
- 忠實度核對：發現 1 處，處理方式：來源間的差異段原有「前三個來源之間原有的比較」一句舊的比較，在加入 HK01 手沖後標題已不準確，改標為「前三個來源的原有比較」。其餘跨來源句（水洗酸度、日曬酸與果味、產地、蜜處理色階）逐一對回四個來源原文：Seattle 豆袋與 HK01 手沖未談日曬酸度、Seattle 豆袋未談水洗酸，都明寫為「沒有提」，沒有寫成多來源一致。
- 檢查：`python scripts/check_wiki.py` 結果 `OK: 28 pages`；index 與 log 已更新。

## [2026-11-16] ingest | wikipedia-coffee-varieties

- 來源：Wikipedia〈List of coffee varieties〉（Coffee varieties 轉址；簡稱 Wikipedia 品種，`raw/wikipedia-coffee-varieties.md`）。條目長而偏育種史，只收初學者看豆袋用得上的部分。
- 重點：(1) variety 與 cultivar 的詞彙，專業咖啡界熟知的品種大多是 cultivar，Bourbon、Typica 最知名；(2) 杯測品質是農民選品種最重視的特性；(3) 阿拉比卡約占全球產量 61%（2004–2010），羅巴斯塔高產抗病但品質較低，越南是最大羅巴斯塔產國；(4) Bourbon、Typica、Caturra、Geisha（Gesha）、SL28／SL34 的來歷；(5) 名字不一定是品種（Java、Sulawesi、Lintong、Santos、Mocha；Yirgacheffe、Sidamo、Harar 是衣索比亞商標名）；(6) Timor 為阿拉比卡與羅巴斯塔的雜交種。
- 新增頁面（2）：`sources/wikipedia-coffee-varieties.md`；`concepts/species.md`（豆種：阿拉比卡與羅巴斯塔；Nespresso 台灣與 Wikipedia 品種都有實質內容，原本放在品種頁，移出另立並兩來源並列）。
- 更新頁面（3）：`concepts/variety.md`（三個豆種的 bullet 移到 species，新增詞彙、品種來歷、名字不是品種；來源間的差異重寫為三來源）、`concepts/origin.md`（Yirgacheffe 等名字與歸類並列）；`index.md`（來源 1 行、新增 species、品種摘要更新）。`altitude`、`tasting-notes`、`reading-coffee-bags`、`roast-level` 沒有動：條目沒有給海拔門檻或風味描述，沒有可併入的內容。
- 差異（並列「A 說…，B 說…」）：品種層級（Seattle 豆袋的栽培品種、Nespresso 台灣的三大豆種、Wikipedia 品種的 variety／cultivar 詞彙，層級不同不衝突）；Geisha 風味（Seattle 豆袋說花香，Wikipedia 品種沒給風味，只說價格與拍賣）；Geisha 拼法 Geisha／Gesha／藝妓；阿拉比卡產量（Nespresso 台灣說最多，Wikipedia 品種給 61%）；羅巴斯塔（Nespresso 台灣說苦、咖啡因高，Wikipedia 品種說高產抗病但品質較低，面向不同）；Yirgacheffe 的歸類（Wikipedia 品種列在品種表並說是商標名稱，Seattle 豆袋當國內產區、HK01 手沖當菜單標示例）。沒有發現直接矛盾。杯測分數、海拔門檻本篇沒有談。
- 判斷：不收 40 多個品種的完整清單與育種史；Brutte、Starmaya 等罕見品種不收；原文標 citation needed 的句子（SL28 的選育年份與來源、Bergendal）不收；Geisha 拍賣價只收「條目稱最貴品種」，不寫每磅金額。
- 忠實度核對：發現 4 處，處理方式：(1) 豆種頁與品種頁原寫「更上一層的分類」，是階層推論、原文沒有，改為只引兩來源的各自用詞（Nespresso 稱三大品種、Wikipedia 在 Species 標題下用學名）；(2) Caturra 原寫「Bourbon 的天然突變」，原文是「由 Bourbon Red 天然突變出的兩個品種發展而來」，改為原文說法；(3) 原寫「Mandheling 與 Lintong 是地區」，原文只有 Lintong 說是地區，Mandheling 是名稱由來，改為只寫 Lintong；(4) 豆種頁差異原寫「兩者都沒有給對方那一種說法」，語意不清，改為「說法不同，並列」。其餘跨來源句（Bourbon／Typica／Geisha 都是阿拉比卡、Yirgacheffe 的三種歸類）已逐一對回 Seattle 豆袋、Nespresso 台灣、HK01 手沖與 Wikipedia 品種原文。
- 檢查：`python scripts/check_wiki.py` 結果 `OK: 30 pages`；index 與 log 已更新。

## [2026-11-16] check | 批次B 審查

- 做法：審查者抽查 25 處陳述，對照 `raw/` 原文。
- 結果：24 處屬實；1 處為錯誤的跨來源負面句：`processing-methods` 寫「Coffee Hero 給了發酵與乾燥時間，其他來源沒有給數字」，但 Nespresso 台灣原文有衣索比亞日曬例子「長達四週」。另有 1 處 markdown 格式破損：`index.md` 的 Wikipedia 來源行黏在 Coffee Hero 行尾，且 `## 概念` 前的空行被刪掉；`check_wiki.py` 偵測不到這類問題。其餘較小的措辭問題暫緩。
- 錯誤源頭節點：N3 ingest（第 6 步）。新規則（第 3 批前加的）只涵蓋「多個來源一致」的肯定句，沒涵蓋「其他來源沒有提／唯一來源」這類負面句。
- 修正：processing-methods 該句改為並列 Coffee Hero 與 Nespresso 台灣的時間；另把 `cupping-score` 的「目前只有 HK01 給出分數區間」同類負面表述改為肯定句；index.md 還原換行與空行，逐行確認每個條目各自一行。
- 規則修改：CLAUDE.md N3 第 6 步加負面句必須逐一核對每個已 ingest 來源，並在第 10 節記錄修改前後與原因。
- 檢查：`python scripts/check_wiki.py` 結果 `OK: 30 pages`。

## [2026-11-16] ingest | about-coffee-roasts

- 來源：About Coffee（美國國家咖啡協會）〈Roasts〉（簡稱 NCA 烘焙，`raw/about-coffee-roasts.md`），英文教育頁。
- 重點：(1) 烘焙是用熱把生豆變成咖啡豆，烘後放 2 到 3 天可沖，建議烘後約 2 到 7 天內沖煮；(2) Espresso roast 不是特定烘焙度，常見中到深焙；(3) 淺、中、深三個顏色類別，各家顏色與名稱不一；(4) 淺焙較酸、表面無油；中焙稱美式烘焙、表面不油；深焙黑亮有油、苦味明顯、較不酸；(5) 淺焙咖啡因略高，深焙不比較強；(6) 包裝上由淺到深的名稱：Blonde／Cinnamon、City、Full City、Vienna、French、Italian。
- 新增頁面（1）：`sources/about-coffee-roasts.md`。
- 更新頁面（4）：`concepts/roast-level.md`（新增 NCA 的各級說法、名稱、咖啡因、Espresso roast；新增並列段）、`concepts/roast-date.md`（烘後沖煮時機，與 Seattle 豆袋並列）、`concepts/espresso.md`（Espresso roast 一條）；`index.md`（來源 1 行、烘焙度摘要）。
- 差異（並列「A 說…，B 說…」）：烘焙後最佳飲用時機，Seattle 豆袋說約 2–4 週（濃縮 2–4 週、濾泡 1–2 週），NCA 烘焙說烘後 2–3 天可沖、建議 2–7 天內，差距大，未選邊；分級四級（Seattle 豆袋）對三級（NCA 烘焙、Nespresso 台灣、HK01 手沖）；酸度與苦味方向，NCA 烘焙與 Nespresso 台灣、HK01 手沖逐一並列；中焙，NCA 烘焙談外觀與強度，Nespresso 台灣談甜味與焦糖，面向不同；「深焙比較強」，NCA 烘焙說與咖啡因無關，Nespresso 台灣說口感濃郁醇厚，面向不同。沒有直接矛盾。
- 判斷：文末導向沖煮頁的句子不收；不另立各烘焙度的概念頁（roast-level 已涵蓋）。
- 忠實度核對：發現 3 處，處理方式：(1) 來源頁初稿加了華氏轉攝氏，是本 Wiki 補充，刪除；(2) 並列段中 HK01 手沖的「淺焙保留香氣」初稿漏了原文前提，補上（傳統上好豆不太選深焙，因為高溫焙容易帶走獨特味道）；(3) 順手發現 `espresso.md` 既有負面句「壓力、咖啡與水的比例，只有 La Marzocco 提到」不實（Nespresso 台灣也提到 bar 與比例），改為肯定句，只說 9 bar 與 1:2 是 La Marzocco 飲品給的數字。跨來源句（酸度、深焙苦、淺焙保留原味、烘焙度因店而異）逐一對回 NCA 烘焙、Nespresso 台灣、HK01 手沖、Seattle 豆袋原文；HK01 手沖沒有講深焙酸度，明寫「沒有講」；新寫內容沒有「其他來源沒有」的負面句。
- 檢查：`python scripts/check_wiki.py` 結果 `OK: 31 pages`；index 與 log 已更新，已重讀 roast-level、roast-date、espresso、index 改過的清單與標題。

## [2026-11-16] ingest | about-coffee-brewing

- 來源：About Coffee（美國國家咖啡協會）〈Brewing methods〉五頁（總覽、drip-coffee、pour-over-coffee、espresso、cold-brew-coffee；簡稱 NCA 沖煮，`raw/about-coffee-brewing.md`，約 55k 字元）。每頁都有器材、研磨、步驟、清潔，依「輕比重、不教操作」只收菜單上看得出的差別。
- 重點：(1) 沖煮過程與品種、烘焙度同樣影響杯中風味，最好的方式是沖出你最愛那杯的方式；(2) 滴濾是機器自動、穩定明亮；手沖是人手倒水、可客製、更突顯風味、適合單一產區；(3) 義式濃縮不是豆子或烘焙度，是以方法命名的飲品，高壓近沸水、約 20–30 秒，有 crema，也是拿鐵等的基底；味道更濃，但咖啡因不一定更多（文章引 USDA：一份約 63 毫克、沖煮咖啡每盎司 12–16 毫克）；(4) 冷萃用室溫或更冷的水、浸泡幾分鐘到 12–18 小時以上、更順更柔和，也可做濃縮液；冷萃不等於冰咖啡（冰咖啡是熱沖後降溫）；(5) 大約接觸時間：滴濾約 5 分鐘、濃縮 20–30 秒、冷萃約 12 小時。法式濾壓壺與即溶只有總覽一句形容，沒有子頁。
- 新增頁面（3）：`sources/about-coffee-brewing.md`（列出五個網址）；`concepts/brewing-methods.md`（入口頁：沖煮方式在菜單上的差別，含比較表）；`concepts/pour-over.md`（手沖與滴濾差別、點手沖選豆；NCA 沖煮、HK01 手沖、Coffee Hero 三來源皆有實質內容）。
- 更新頁面（3）：`concepts/cold-brew.md`（冷萃名稱、浸泡時間、冷萃與冰咖啡；差異段改為並列）、`concepts/espresso.md`（定義為沖煮方式、crema、咖啡因、差異段）、`index.md`（來源 1 行、沖煮方式新小節 2 行、冷萃摘要）。`roast-level`、`processing-methods` 不動。
- 差異（並列「A 說…，B 說…」）：冷萃浸泡時間，Nespresso 台灣說超過 12 小時，NCA 沖煮說幾分鐘到 12–18 小時以上，典型約 12 小時；冷萃口感，Nespresso 台灣說酸苦都偏低，NCA 沖煮說更順更柔和、比冰咖啡不苦；義式做法，NCA 沖煮說高壓近沸水 20–30 秒，La Marzocco 飲品說 9 bar、雙份 25–30 秒，Nespresso 台灣說高壓 bar 數蒸氣；crema 的形容，NCA 沖煮說絲絨般金棕色上層，La Marzocco 飲品說光亮；冷萃對照的對象不同（冰滴對冰咖啡）。沒有直接矛盾。
- 判斷：器材、濾紙、研磨粗細表、步驟、清潔、家用比例不收；咖啡因數字照轉述、標明是文章引用 USDA；法式濾壓壺、即溶不立頁（來源只有一句形容）；滴濾不另立頁（併入入口頁與手沖頁的對照）。
- 忠實度核對：發現 3 處，處理方式：(1) 入口頁差異段初稿寫「兩者都沒有把冷萃說成更濃或更烈」，但 NCA 沖煮原文有「可做較強的冷萃濃縮液」，這句是錯的跨來源負面句，改為「兩者都用柔和、偏低的苦來描述」；(2) 冷萃頁差異段初稿有「沒有談冰滴」「沒有說更酸」兩個負面句，無法對照全文確認，刪除，改為只寫兩篇各自對照的對象；(3) 手沖頁初稿「NCA 沖煮沒有談手沖的冰熱」同為負面句，刪除。另外定義句首句原把「同一種豆可用不同方式沖」掛在 NCA 沖煮下，原文沒有，改為術語解釋加 ＊。其餘跨來源句（HK01 手沖與 NCA 沖煮都談單品豆與手沖、Nespresso 台灣與 NCA 沖煮的冷萃口感）逐一對回原文後保留。
- 檢查：`python scripts/check_wiki.py` 結果 `OK: 34 pages`；index 與 log 已更新，已重讀 index 沖煮方式與冷萃、烘焙度相鄰清單與標題，每個條目各自一行。

## [2026-11-16] discuss | 精簡來源

- 使用者說：「好 加速 然後把你覺得可以不需要的文章刪掉 減少一點」。
- Claude 提議刪掉兩篇尚未 ingest 的來源：Urnex〈Reinventing the Coffee Taster's Flavor Wheel〉（廠商部落格，與 Trade 內容重疊、權威性較低）、World Coffee Research〈Sensory Lexicon〉（只擷取到簡介，詞彙表本體是另外下載的檔案，對初學者太技術）。已 ingest 的來源保留，因為移除會需要重做既有頁面的連結與引用。
- 處理：從 `raw/SOURCES.md` 刪除這兩列；`raw/` 內的擷取檔留在硬碟上（已被 gitignore）。刪除後 SOURCES.md 共 11 列（已 ingest 9 篇加待 ingest 的 SCA 與 Trade 2 篇；其中 Nespresso 一列含三篇專文）。
- 流程變更：從本批次起，每批次只做一次審查，較小的措辭問題延後到 lint 處理。

## [2026-11-16] ingest | sca-flavor-wheel-eight-steps

- 來源：SCA〈How to Use the Coffee Taster’s Flavor Wheel in Eight Steps〉（簡稱 SCA 風味輪，`raw/sca-flavor-wheel-eight-steps.md`），英文官方使用說明。
- 重點：(1) 風味輪是 SCAA 與 WCR 合作的品嚐工具；(2) 可用在隨意品嚐或杯測，依序觀察乾香、注水香氣、入口風味；(3) 風味是味道加氣味，輪上涵蓋純味覺到純香氣；(4) 由中心往外，越外越具體，可隨時停下，衣索比亞果香→柑橘→葡萄柚的例子；(5) 輪以 WCR Sensory Lexicon 為基礎，詞彙表每個屬性有定義與參照物；(6) 參照物可嚐可聞，香氣類不可入口；(7) 格子相連表示專業品嚐者認為關係近；(8) 共同語言與顏色的用途。
- 新增頁面（2）：`sources/sca-flavor-wheel-eight-steps.md`；`concepts/flavor-wheel.md`（風味輪，目前一個來源）。
- 更新頁面（2）：`concepts/tasting-notes.md`（新增風味輪一條與相關概念連結，並改寫差異段最後一句）、`index.md`（來源 1 行、新增風味輪小節）。
- 差異：目前概念頁只有一個來源，無衝突；與 Seattle 豆袋的風味描述面向不同（SCA 談品嚐者用輪描述，沒有談豆袋標示）。
- 判斷：詞彙表參照物的取得與嗅聞方式只收一句；步驟 4 到 6 屬進階，不細寫；沒有輪上詞彙的完整清單。
- 忠實度核對：發現 1 處，處理方式：來源頁初稿在「與其他來源的關係」寫了尚未存在的 Trade 頁連結與「兩者說法不同」，在 Trade ingest 前屬於預寫，刪除，留待 Trade 那篇再補。其餘句子逐句對回原文；「風味輪（flavor wheel）」概念頁「杯測」用 ＊ 並加頁尾說明；沒有跨來源肯定或負面句。
- 檢查：`python scripts/check_wiki.py` 結果 `OK: 36 pages`；index 與 log 已更新，已重讀 tasting-notes 重點與相關概念清單、index 新增的清單與標題。
