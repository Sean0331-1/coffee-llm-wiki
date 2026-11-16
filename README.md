# 咖啡入門 LLM Wiki

政大 大四上 Gen AI 第十週作業。依 Karpathy 的「LLM Wiki」構想：先討論、後生成。先把公開的咖啡資料 ingest 成一個互相連結的 markdown Wiki（由 Claude Code 依 `CLAUDE.md` 維護），再以 Wiki 為唯一知識來源，產生一份教學型 HTML 簡報，並附上 loop／graph 設計、執行紀錄與反思。

**主題：咖啡入門。** 學習目標：看完的人走進精品咖啡店，看得懂菜單和豆子標籤，知道怎麼點到自己會喜歡的咖啡。

## 資料夾

```
CLAUDE.md        schema：頁面格式、各節點流程與檢查規則
raw/SOURCES.md   公開的來源清單（raw/ 其餘全文因版權不上傳）
wiki/            LLM 維護的 Wiki：index.md、log.md、overview.md、sources/、concepts/、outputs/
scripts/         check_wiki.py：Wiki 檢查腳本（python scripts/check_wiki.py）
slides/          教學簡報（單一 HTML）
report.md        繳交報告
docs/specs/      設計文件
```

## 連結

- Wiki（GitHub repo）：https://github.com/Sean0331-1/coffee-llm-wiki（入口：https://github.com/Sean0331-1/coffee-llm-wiki/blob/main/wiki/index.md）
- 簡報（GitHub Pages）：https://sean0331-1.github.io/coffee-llm-wiki/slides/
- 報告：https://github.com/Sean0331-1/coffee-llm-wiki/blob/main/report.md
