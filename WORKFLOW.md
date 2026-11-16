# 照老師示範，完成自己的教甄筆記 Wiki

你的工作資料夾名稱是 **LLM WIKI的工作資料**。

## 與老師九張照片的對應

| 老師示範的動作 | 教甄筆記的實際檔案／做法 |
| --- | --- |
| 建立工作資料夾 | 保留「LLM WIKI的工作資料」名稱 |
| 給 AI Karpathy LLM Wiki 方法說明 | 參考你傳來的 Markdown；原檔保留在 raw/references/ |
| 先寫中文 AGENTS.md、README.md、index.md | 根目錄均已建立，規定檔案結構和後續新增方式 |
| 放入第一篇原始文章 | 你提供的教育心理學 PDF 放在 raw，不改寫原檔 |
| 整理來源並向多個主題擴展 | wiki/sources、wiki/concepts、wiki/comparisons，建立相關連結 |
| 維護目錄、日誌與矛盾 | wiki/index.md、wiki/log.md、wiki/open-questions.md |
| 依 Wiki 產生主題筆記 | notes/md，每篇標示對應 Wiki 和來源頁碼 |
| 從筆記產生 HTML 成果 | notes/html，每主題一個 HTML 閱讀頁 |
| 圖片和 HTML 的相對路徑 | 共用檔固定在 notes/html/assets；目前不需要外部圖片 |
| 在根目錄做首頁串連成果 | index.html 連到每篇 HTML；index.md 連到各層檔案 |
| 之後變更也沿用同一規則 | 修改格式或風格時同步更新 AGENTS.md |

老師照片用 LLM 研究主題和 HTML 簡報示範。這裡使用相同的知識累積與產出流程，主題換成教甄教育心理學，成果選擇適合複習的 HTML 閱讀頁。課堂示範的日系風格、角色貼圖與簡報題目沒有直接複製。

## 你現在先做這一步

1. 下載新版 ZIP，按「全部解壓縮」。
2. 裡面的最外層資料夾名稱就是「LLM WIKI的工作資料」。
3. 如果電腦已經有同名工作資料夾，先保留你自行新增的檔案，再把新版內容放進去；避免外面又套一層同名資料夾。
4. 開啟根目錄 `index.html`，點一篇主題，確認能看到筆記與「下載 Markdown 筆記」。

這個聊天中的 AI 負責建立可下載的專案；把檔案放進自己的電腦後，就是老師示範的本機資料夾形式。

## 第一次練習：對照現成的完整流程

以「皮亞傑的認知發展論」為例，依序查看：

1. `raw/2教育心理學.pdf` 的第 55–58、60 頁。
2. `wiki/sources/edu-psych-01.md` 的來源摘要。
3. `wiki/concepts/piaget-cognitive-development.md` 的知識頁。
4. `notes/md/piaget-cognitive-development.md` 的複習筆記。
5. `notes/html/piaget-cognitive-development.html` 的 HTML 閱讀頁。
6. 根目錄 `index.html` 的主題入口與 `index.md` 的檔案連結。

這些層次呈現的是同一批資料如何被整理，不應把每一層都當成不同的文獻來源。

## 下一次新增：可直接交給 AI 的指令

### 1. 加入新資料（ingest）

「請先讀 AGENTS.md、根目錄 index.md 和 Wiki 日誌。我新增了一份原始資料，請保留原檔，整理來源摘要，再更新相關概念、比較頁、目錄和日誌。發現矛盾時列出來源與頁碼，不要直接覆蓋。」

實際檔名要用你新增的檔案；不要聲稱某份未提供的資料已經在資料夾內。

### 2. 提問並累積答案（query）

「請依目前 Wiki 比較皮亞傑與維高斯基，說明在國小教學中的差異。請列來源頁碼，並把可保存的結果更新到比較頁，再更新索引及日誌。」

### 3. 從 Wiki 產生新成果

「請完全依照 Wiki，將指定主題整理成 notes/md 的複習筆記，再產生 notes/html 的獨立閱讀頁；沿用既有風格，將新頁面加入根目錄首頁。如果需要新資料，先提出建議並完成來源整理，不能直接編造內容。」

### 4. 檢查（lint）

「請依 AGENTS.md 檢查未標來源、論點矛盾、過時表述、孤立頁面與失效連結。核對 notes 與 Wiki 是否一致，最後執行建置，回報實際完成的檢查與仍待確認之處。」

## AI 在哪裡操作？

- 在本聊天裡：你上傳新資料，我更新專案包，你再下載到電腦。
- 在可讀寫本機資料夾的 AI 工具裡：開啟「LLM WIKI的工作資料」，讓該工具讀規則並更新檔案。

兩者都可以使用同一份 AGENTS.md。這個聊天不會因為你在其他工具選了資料夾，就自動取得電腦的寫入權限。

## 最後才完成 GitHub 發布

網站檔案已備妥，但 GitHub 尚未上傳。依 README.md 上傳專案、以 main 的 /docs 發布，再把實際網址填到 SUBMISSION.md。
