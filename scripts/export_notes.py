"""Export study notes and independent HTML pages from the maintained wiki."""
from pathlib import Path
import html
import json
import re


def export_all(root, notes):
    by_id = {n['id']: n for n in notes}
    for base in (root, root/'docs'):
        md_dir = base/'notes/md'
        html_dir = base/'notes/html'
        assets = html_dir/'assets'
        for directory in (md_dir, html_dir, assets):
            directory.mkdir(parents=True, exist_ok=True)
        css = (root/'web/style.css').read_text(encoding='utf-8')
        css += '''
body.note-page{background:#f8f7f3}.note-shell{max-width:900px;margin:0 auto;padding:30px 30px 65px}.note-nav{display:flex;gap:15px;justify-content:space-between;align-items:center;font-size:12px;border-bottom:1px solid #dce3d7;padding-bottom:18px}.note-nav>a{font-weight:600}.note-article{background:#fffefb;border:1px solid #dfe5d8;border-radius:10px;padding:35px 42px;margin-top:24px}.note-article h1{font-size:32px;line-height:1.5;letter-spacing:1px;margin:15px 0}.breadcrumb{font-size:11px;color:#829077}.workflow-tag{font-size:10px;letter-spacing:1px;color:#829077;margin:20px 0}.note-provenance{background:#eff3e9;padding:18px;border-radius:6px;margin-top:30px;font-size:12px;overflow-wrap:anywhere}.note-provenance a{text-decoration:underline}.note-foot{font-size:11px;color:#7a8b73;margin-top:25px}.source-link{font-size:12px}.local-status{font-size:11px;color:#8b6b4c}.note-actions{display:flex;gap:10px;flex-wrap:wrap}.note-actions a{display:inline-flex;align-items:center}.note-toc{display:flex;gap:8px;flex-wrap:wrap;margin:20px 0}.note-toc a{font-size:11px;border:1px solid #e0e5d9;padding:4px 9px;border-radius:4px}.diagram-text{font-size:12px;color:#6a7e65}.quiz-options button[aria-pressed="true"]{font-weight:600}.print-only{display:none}@media(max-width:600px){.note-shell{padding:20px 12px 40px}.note-article{padding:25px 20px}.note-article h1{font-size:26px}.note-nav{font-size:11px}.note-nav span{display:none}.note-toc a{font-size:10px}.note-article .article-content{font-size:14px}}@media print{body.note-page{background:white}.note-shell{max-width:none;padding:0}.note-nav,.note-actions,.quiz-options,.note-toc,.related,.local-status{display:none!important}.note-article{border:0;padding:0;margin:0}.quiz{break-inside:avoid}.print-only{display:block}.article-content{font-size:12px}.note-article h1{font-size:24px}}
'''
        (assets/'style.css').write_text(css,encoding='utf-8')
        (assets/'note.js').write_text(NOTE_JS,encoding='utf-8')
        for note in notes:
            slug = note['id']
            # Produce a reading note only from the wiki body, without adding new theory.
            source_text=(root/note['path']).read_text(encoding='utf-8')
            body=source_text[4:].split('\n---\n',1)[1].strip()
            body=re.sub(r'^# [^\n]+\n*','',body)
            body=re.sub(r'\[([^\]]+)\]\(\.\./sources/[^)]+\)',r'[\1](../../index.html#source)',body)
            md=(f'# {note["title"]}\n\n'
                f'> 依 Wiki 整理的教甄複習筆記；不是新增資料來源。\n\n'
                f'- 整理依據：`{note["path"]}`\n'
                f'- 摘要：{note["summary"]}\n'
                f'- 更新日期：{note["updated"]}\n'
                '\n'+body+'\n\n'
                '## 自我檢核（AI 自編）\n\n'+note['question']+'\n\n'+
                '\n'.join(f'- {chr(65+i)}. {o}' for i,o in enumerate(note['options']))+'\n\n'+
                f'**答案：{chr(65+note["answer"])}。** {note["explanation"]}\n\n'
                '## 延伸閱讀\n\n'+
                '\n'.join(f'- [{by_id[r]["title"]}]({r}.md)' for r in note['related'])+'\n')
            (md_dir/(slug+'.md')).write_text(md,encoding='utf-8')
            body_html=note['html']
            body_html=re.sub(r'href="#note/([a-z0-9-]+)"',r'href="\1.html"',body_html)
            body_html=body_html.replace('href="#source"','href="../../index.html#source"')
            # Fixed headings become accessible anchors without depending on JavaScript.
            headings=['核心概念','重點整理','教學實例（AI 自編）','易混淆提醒','來源與查證']
            for i,title in enumerate(headings,1):
                body_html=body_html.replace('<h2>'+title+'</h2>',f'<h2 id="section-{i}">{title}</h2>')
            related=''.join('<a class="secondary" href="'+r+'.html">'+html.escape(by_id[r]['title'])+' ↗</a>' for r in note['related'])
            options=''.join(f'<button type="button" data-choice="{i}">{chr(65+i)}. {html.escape(o)}</button>' for i,o in enumerate(note['options']))
            payload=json.dumps({k:note[k] for k in ['id','answer','explanation']},ensure_ascii=False).replace('<','\\u003c')
            text=f'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(note['title'])}｜教甄筆記</title><link rel="icon" href="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMiAzMiIgZmlsbD0ibm9uZSI+PHBhdGggZD0iTTE2IDhDMTIgNSA3IDUgMyA3djE5YzQtMiA5LTIgMTMgMSA0LTMgOS0zIDEzLTFWN2MtNC0yLTktMi0xMyAxWiIgc3Ryb2tlPSIjMzQ2ZDY0IiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz48cGF0aCBkPSJNMTYgOHYxOU03IDExYzItMSA0LTEgNiAwTTE5IDExYzItMSA0LTEgNiAwTTcgMTZjMi0xIDQtMSA2IDBNMTkgMTZjMi0xIDQtMSA2IDAiIHN0cm9rZT0iIzM0NmQ2NCIgc3Ryb2tlLXdpZHRoPSIxLjYiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPjwvc3ZnPg=="><meta name="description" content="{html.escape(note['summary'],quote=True)}">
<link rel="stylesheet" href="assets/style.css"><script type="application/json" id="noteData">{payload}</script><script defer src="assets/note.js"></script></head>
<body class="note-page"><div class="note-shell"><nav class="note-nav" aria-label="頁面導覽"><a href="../../index.html#library">← 回到教甄筆記首頁</a><span>教甄筆記</span><a href="../../index.html#source">來源與更新</a></nav>

<article class="note-article"><div class="breadcrumb">教育心理學 / {html.escape(note['category'])}</div><h1>{html.escape(note['title'])}</h1><p class="article-summary">{html.escape(note['summary'])}</p>

<div class="article-actions note-actions"><button class="secondary" id="readToggle" aria-pressed="false">標記為已讀</button><button class="secondary" id="bookmarkToggle" aria-pressed="false">☆ 收藏筆記</button><a class="secondary" href="../md/{slug}.md" download>下載 Markdown 筆記</a><button class="secondary" id="printNote">列印筆記</button></div>
<p class="local-status" id="saveStatus" role="status" aria-live="polite"></p>
<nav class="note-toc" aria-label="筆記章節">{''.join(f'<a href="#section-{i}">{title}</a>' for i,title in enumerate(headings,1))}</nav>
<div class="article-content">{body_html}</div>
<section class="quiz" aria-labelledby="quizTitle"><div class="eyebrow">CHECK YOUR UNDERSTANDING</div><h2 id="quizTitle">自我檢核 · AI 自編</h2><p>{html.escape(note['question'])}</p><div class="quiz-options">{options}</div><p id="quizFeedback" role="status" aria-live="polite"></p><p class="print-only">答案 {chr(65+note['answer'])}：{html.escape(note['explanation'])}</p></section>
<h2>相關筆記</h2><div class="related">{related}</div>
<div class="note-provenance"><strong>這篇筆記從哪裡來？</strong><br>原始資料：教育心理學講義，PDF 第 {'、'.join(map(str,note['pages']))} 頁。<br>對應 Wiki：<code>{html.escape(note['path'])}</code><br>此頁與 Markdown 筆記依 Wiki 內容產生，修改理論內容時先回到 Wiki，再重新產生兩種成果。<br><a href="../../index.html#source">來源摘要</a> · <a href="../../index.html#issues">待查證事項</a> · <a href="../../index.html#history">更新紀錄</a></div>
</article><footer class="note-foot">資料夾：LLM WIKI的工作資料 · 更新 {html.escape(note['updated'])} · 個人教甄複習</footer></div></body></html>'''
            (html_dir/(slug+'.html')).write_text(text,encoding='utf-8')
    # A visible Markdown index for the derivatives (not another knowledge source).
    index='# Wiki 衍生的教甄複習筆記\n\n先更新 Wiki，再重新產生這些成果；不可反過來把筆記輸出當成獨立來源。\n\n'
    index+='\n'.join(f'- [{n["title"]}](md/{n["id"]}.md) · [HTML 閱讀頁](html/{n["id"]}.html)' for n in notes)+'\n'
    (root/'notes/index.md').write_text(index,encoding='utf-8')
    (root/'docs/notes/index.md').write_text(index,encoding='utf-8')


NOTE_JS=r'''"use strict";
(()=>{
 const note=JSON.parse(document.getElementById('noteData').textContent);
 const key='teacher-notes-v1';
 let state={read:[],bookmarks:[]};
 const $=id=>document.getElementById(id);
 try{const s=JSON.parse(localStorage.getItem(key)||'null');if(s)for(const k of ['read','bookmarks'])if(Array.isArray(s[k]))state[k]=s[k];}catch(e){}
 function render(){
  const read=state.read.includes(note.id), saved=state.bookmarks.includes(note.id);
  $('readToggle').textContent=read?'✓ 已讀過（點擊取消）':'標記為已讀';
  $('readToggle').setAttribute('aria-pressed',read);
  $('bookmarkToggle').textContent=saved?'★ 已收藏（點擊取消）':'☆ 收藏筆記';
  $('bookmarkToggle').setAttribute('aria-pressed',saved);
 }
 function toggle(k){const i=state[k].indexOf(note.id);if(i<0)state[k].push(note.id);else state[k].splice(i,1);try{localStorage.setItem(key,JSON.stringify(state));$('saveStatus').textContent='已更新閱讀紀錄；只儲存在這個瀏覽器。';}catch(e){$('saveStatus').textContent='目前只能暫存，這個瀏覽器未允許保存紀錄。';}render();}
 $('readToggle').addEventListener('click',()=>toggle('read'));
 $('bookmarkToggle').addEventListener('click',()=>toggle('bookmarks'));
 $('printNote').addEventListener('click',()=>window.print());
 document.querySelectorAll('[data-choice]').forEach(b=>b.addEventListener('click',()=>{
  const c=Number(b.dataset.choice);document.querySelectorAll('[data-choice]').forEach(x=>{const i=Number(x.dataset.choice);x.disabled=true;x.classList.toggle('correct',i===note.answer);x.classList.toggle('wrong',i===c&&c!==note.answer);});
  $('quizFeedback').textContent=(c===note.answer?'答對了！':'再記住這個差異：')+note.explanation;
 }));render();
})();
'''
