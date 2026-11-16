# 教甄筆記

工作資料夾名稱：**LLM WIKI的工作資料**。

依使用者提供的老師課堂照片與 Karpathy LLM Wiki 方法，建立「先累積知識、再產生筆記與網頁」的個人教甄專案。中文 AI 工作規則在 AGENTS.md，實際操作順序在 WORKFLOW.md。

## 開始使用

1. 把 ZIP 全部解壓縮；最外層就是「LLM WIKI的工作資料」。
2. 直接用 Chrome 或 Edge 開啟根目錄的 **index.html**。
3. 點選主題，進入獨立 HTML 閱讀頁；也能下載該篇 Markdown 筆記。
4. 想逐步對照老師的做法，先讀 **WORKFLOW.md**。

不需 API 金鑰或額外網頁訂閱。單純閱讀不需安裝 Python；更新內容並重新產生網站時才需要 Python 3。

## 與老師相同的工作順序

1. 訂規則：AGENTS.md。
2. 收來源：raw，保留原始檔，不修改。
3. 建知識：wiki/sources、wiki/concepts、wiki/comparisons。
4. 維護知識：wiki/index.md、wiki/log.md、wiki/open-questions.md。
5. 產生複習筆記：notes/md，每篇依 Wiki 整理。
6. 產生 HTML：notes/html，每篇可獨立開啟。
7. 串起成果：根目錄 index.md 與 index.html。
8. 新增內容時沿用同一規則，更新規則、索引及日誌。

老師以 LLM 研究與簡報示範。本專案沿用流程，主題換成教育心理學，成果是適合個人複習的筆記閱讀頁。

## 資料夾

| 檔案或路徑 | 用途 |
| --- | --- |
| AGENTS.md | 中文 AI 專案規則 |
| README.md、WORKFLOW.md | 使用說明與課堂流程對照 |
| index.md | 所有層次檔案的總目錄 |
| index.html | 網站首頁，連到每個獨立 HTML |
| raw/ | 私人原始 PDF 與方法參考，不公開上傳 |
| wiki/sources/ | 來源摘要及頁碼，catalog.json 登錄來源 |
| wiki/concepts/ | 概念筆記，知識的維護位置 |
| wiki/comparisons/ | 跨主題比較與綜合 |
| wiki/index.md、wiki/log.md | 知識目錄與更新日誌 |
| wiki/open-questions.md | 待查證事項 |
| notes/md/ | 由 Wiki 產生的 Markdown 複習筆記 |
| notes/html/ | 由相同 Wiki 產生的獨立 HTML |
| notes/html/assets/ | HTML 同層共用樣式與互動程式 |
| web/、scripts/ | 原始網站版型與產生程式 |
| docs/ | 與根目錄閱讀成果一致，供 GitHub Pages 使用 |
| SUBMISSION.md | 繳交草稿，實際網址發布後再填 |

## 目前範圍

《2教育心理學.pdf》共 121 頁，現按全書主要章節整理，整理 47 篇概念、3 篇比較及 50 題 AI 自編檢核題，不是逐字重製。來源書目資訊與疑點保留於 Wiki。

網站支援搜尋、分類、收藏與已讀紀錄。紀錄只存在目前瀏覽器；file:// 下是否跨本機 HTML 共用紀錄由瀏覽器決定，公開網站同來源下可共用。沒有遠端同步。

## 後續新增內容

先請能操作專案的 AI 讀 AGENTS.md，提供新來源，再更新 Wiki、相關連結、目錄及日誌；不要只修改輸出的 HTML。

在專案根目錄執行：

```sh
python scripts/build.py
```

Windows 也可用 `py scripts/build.py`。只有 Python 3 標準函式庫，不需安裝額外套件。

程式檢查筆記格式、id、來源、頁碼、相關連結及孤立主題，再從 Wiki 產生 notes/md、notes/html、根目錄首頁和 docs。新增分類與筆記會自動顯示，無需為每一篇重做首頁。

這是 AI 維護檔案的 Wiki。網站負責閱讀，不會自行處理新 PDF 或在背景呼叫模型。ChatGPT 中更新的專案需要重新下載，才會進到自己的電腦；本聊天不會直接取得本機寫入權限。

## GitHub 上傳與網站公開

目前仍未登入你的 GitHub 上傳或發布。完成檔案確認後：

1. 在 GitHub 建立 Public Repository，例如 teacher-exam-wiki。
2. 上傳專案內容，讓 AGENTS.md、README.md、index.md、index.html、wiki、notes、web、scripts、docs 等位於 Repository 根目錄。
3. **不要上傳 raw 中的 PDF 或原始參考資料。** `.gitignore` 適用 Git 追蹤；GitHub 網頁拖曳上傳不會自動排除它們。raw 只上傳 README.md 即可。
4. Repository → Settings → Pages → Deploy from a branch，選 main 與 /docs，按 Save。
5. 等待 GitHub 顯示成功，再開啟它提供的網站網址；不要自行猜測公開網址。
6. 將 Repository 和網站的實際網址填入 SUBMISSION.md。

操作參考：[GitHub Pages 官方說明](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)。

## 方法參考

[Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)，以及使用者提供的課堂照片與 Markdown。原始方法檔保存在 raw/references/，未將課堂中其他人的題目、角色貼圖或專案成果複製為自己的作品。
