'use strict';
(() => {
 const notes=window.WIKI.notes;
 const $=s=>document.querySelector(s);
 const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const storageKey='teacher-notes-v1';
 let state={bookmarks:[],read:[]},storageOK=true;
 try{const saved=JSON.parse(localStorage.getItem(storageKey)||'null');if(saved)for(const k of ['bookmarks','read'])if(Array.isArray(saved[k]))state[k]=saved[k].filter(id=>notes.some(n=>n.id===id));}catch(e){storageOK=false;}
 let view='all',category='all',query='',lastFocus=null,toastTimer;
 const dialog=$('#detail');
 function notify(msg){$('#toast').textContent=msg;$('#toast').classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').classList.remove('show'),2200);}
 function save(){try{localStorage.setItem(storageKey,JSON.stringify(state));}catch(e){storageOK=false;}if(!storageOK)notify('此瀏覽器無法保存紀錄，本次操作仍可使用。');}
 function updateCounts(){const read=notes.filter(n=>state.read.includes(n.id)).length;$('#readCount').textContent=read;$('#allCount').textContent=notes.length;$('#noteCount').textContent=notes.length;$('#comparisonCount').textContent=notes.filter(n=>n.type==='comparison').length;$('#bookmarkCount').textContent=state.bookmarks.length;$('#unreadCount').textContent=notes.length-read;const p=Math.round(read/notes.length*100);$('#percent').textContent=p+'%';$('#progressBar').style.width=p+'%';}
 function toggleBookmark(id){const i=state.bookmarks.indexOf(id);if(i<0)state.bookmarks.push(id);else state.bookmarks.splice(i,1);save();render();if(location.hash==='#note/'+id)renderNote(id);notify(i<0?'已加入收藏':'已取消收藏');}
 function render(){
  updateCounts();
  const filtered=notes.filter(n=>(category==='all'||n.category===category)&&(view!=='bookmarks'||state.bookmarks.includes(n.id))&&(view!=='unread'||!state.read.includes(n.id))&&(!query||[n.title,n.summary,n.search,...n.tags].join(' ').toLowerCase().includes(query.toLowerCase())));
  $('#viewTitle').textContent={all:'今天，想弄懂哪個概念？',bookmarks:'把重要的概念，留在手邊。',unread:'還有這些新知識，等你探索。'}[view];
  $('#resultCount').textContent=`顯示 ${filtered.length} / ${notes.length} 篇筆記`;
  $('#cards').innerHTML=filtered.map(n=>`<article class="card"><div class="card-top"><span class="category ${n.type==='comparison'?'compare':''}">${escape(n.category)}</span>${state.read.includes(n.id)?'<span class="read-tag">✓ 已讀</span>':''}<button class="bookmark ${state.bookmarks.includes(n.id)?'saved':''}" data-bookmark="${n.id}" aria-label="${state.bookmarks.includes(n.id)?'取消收藏':'收藏'}：${escape(n.title)}" aria-pressed="${state.bookmarks.includes(n.id)}">${state.bookmarks.includes(n.id)?'★':'☆'}</button></div><h3><a class="title-button" href="notes/html/${n.id}.html">${escape(n.title)}</a></h3><p>${escape(n.summary)}</p><div class="tags">${n.tags.slice(0,3).map(t=>'<span># '+escape(t)+'</span>').join('')}</div><div class="card-bottom"><span>講義 p.${n.pages[0]}${n.pages.length>1?' 等':''}</span><a class="read-link" href="notes/html/${n.id}.html">閱讀筆記 ↗</a></div></article>`).join('');
  $('#empty').hidden=!!filtered.length;
  $('#emptyMessage').textContent=view==='bookmarks'&&!state.bookmarks.length?'點筆記右上角的星號，即可加入收藏。':view==='unread'&&state.read.length===notes.length?'這一版筆記都讀過了，可以回到全部筆記複習。':'試試不同的關鍵字或分類。';
  document.querySelectorAll('[data-view]').forEach(b=>{b.classList.toggle('active',b.dataset.view===view);b.setAttribute('aria-pressed',b.dataset.view===view);});
  document.querySelectorAll('[data-category]').forEach(b=>{b.classList.toggle('active',b.dataset.category===category);b.setAttribute('aria-pressed',b.dataset.category===category);});
 }
 function renderNote(id){
  const n=notes.find(n=>n.id===id);if(!n){$('#detailBody').innerHTML='<h1 id="detailTitle">找不到這篇筆記</h1><p>請關閉視窗，回到筆記目錄選擇。</p>';return;}
  $('#dialogLabel').textContent=n.category+' / '+(n.type==='comparison'?'比較統整':'概念筆記');
  const bookmarked=state.bookmarks.includes(id),read=state.read.includes(id);
  $('#detailBody').innerHTML=`<div class="article-meta">EDUCATIONAL PSYCHOLOGY · 更新 ${n.updated}</div><h1 id="detailTitle">${escape(n.title)}</h1><p class="article-summary">${escape(n.summary)}</p><div class="article-actions"><button class="secondary" data-bookmark="${id}" aria-pressed="${bookmarked}">${bookmarked?'★ 已收藏':'☆ 收藏筆記'}</button><button class="secondary" data-read="${id}" aria-pressed="${read}">${read?'✓ 已讀過（點擊取消）':'標記為已讀'}</button></div><div class="article-content">${n.html}</div><section class="quiz" aria-labelledby="quizTitle"><div class="eyebrow">CHECK YOUR UNDERSTANDING</div><h3 id="quizTitle">自我檢核 · AI 自編題</h3><p>${escape(n.question)}</p><div class="quiz-options">${n.options.map((o,i)=>`<button data-answer="${i}" data-note="${id}">${String.fromCharCode(65+i)}. ${escape(o)}</button>`).join('')}</div><div class="quiz-feedback" role="status" aria-live="polite"></div></section><h3>把知識連起來</h3><div class="related">${n.related.map(r=>{const related=notes.find(x=>x.id===r);return `<button data-open="${r}">${escape(related.title)} ↗</button>`;}).join('')}</div><p class="article-meta">來源：edu-psych-01 · PDF 第 ${n.pages.join('、')} 頁 · <a href="#source">查看來源與限制</a></p>`;
 }
 function renderSource(kind='source'){
  $('#dialogLabel').textContent='知識庫來源與維護';
  const title={source:'有來源，也有更新的脈絡。',issues:'待查證與後續整理',history:'Wiki 更新紀錄',coverage:'PDF 章節與筆記對照'}[kind];
  const content={source:window.WIKI.sourcesHtml,issues:window.WIKI.issuesHtml,history:window.WIKI.historyHtml,coverage:window.WIKI.coverageHtml}[kind];
  $('#detailBody').innerHTML=`<h1 id="detailTitle">${title}</h1><div class="related"><a class="secondary" href="#coverage">PDF 章節對照</a><a class="secondary" href="#source">來源摘要</a><a class="secondary" href="#issues">待查證清單</a><a class="secondary" href="#history">更新紀錄</a></div><div class="article-content">${content}</div><div class="source-block"><h3>下一次怎麼繼續？</h3><p>先讓能操作專案檔案的 AI 閱讀 AGENTS.md，再整理新資料、更新筆記與日誌，執行 <code>python scripts/build.py</code>。此網站是閱讀器，不會自行呼叫 LLM 或讀取新放入的 PDF。</p><p>收藏與已讀紀錄只保留在目前瀏覽器。方法參考：<a href="https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f" target="_blank" rel="noopener">Karpathy 的 LLM Wiki 構想 ↗</a>。</p></div>`;
 }

 function route(){const hash=location.hash;if(hash.startsWith('#note/')||['#source','#issues','#history','#coverage'].includes(hash)){
  if(!dialog.open){lastFocus=document.activeElement;dialog.showModal();}
  if(['#source','#issues','#history','#coverage'].includes(hash))renderSource(hash.slice(1));else renderNote(decodeURIComponent(hash.slice(6)));
  dialog.scrollTop=0;$('#closeDetail').focus();
 }else if(dialog.open){dialog.close();if(lastFocus&&lastFocus.isConnected)lastFocus.focus();}}
 function close(){history.replaceState(null,'',location.pathname+location.search+'#library');route();}
 document.addEventListener('click',e=>{
  const b=e.target.closest('button');if(!b)return;
  if(b.dataset.open){location.href='notes/html/'+b.dataset.open+'.html';return;}
  if(b.dataset.bookmark){toggleBookmark(b.dataset.bookmark);return;}
  if(b.dataset.read){const id=b.dataset.read,i=state.read.indexOf(id);if(i<0)state.read.push(id);else state.read.splice(i,1);save();render();renderNote(id);notify(i<0?'已標記為讀過':'已取消已讀標記');return;}
  if(b.dataset.answer!==undefined){const n=notes.find(x=>x.id===b.dataset.note),choice=Number(b.dataset.answer);document.querySelectorAll('[data-answer]').forEach(x=>{x.disabled=true;const i=Number(x.dataset.answer);x.classList.toggle('correct',i===n.answer);x.classList.toggle('wrong',i===choice&&choice!==n.answer);});$('.quiz-feedback').textContent=(choice===n.answer?'答對了！':'再記住這個差異：')+n.explanation;return;}
  if(b.dataset.view){view=b.dataset.view;category='all';query='';$('#search').value='';render();$('#library').scrollIntoView();}
  if(b.dataset.category){category=b.dataset.category;render();}
 });
 $('#search').addEventListener('input',e=>{query=e.target.value.trim();render();});
 $('#reset').addEventListener('click',()=>{view='all';category='all';query='';$('#search').value='';render();});
 $('#closeDetail').addEventListener('click',close);
 dialog.addEventListener('cancel',e=>{e.preventDefault();close();});
 dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)close();}});
 window.addEventListener('hashchange',route);
 window.addEventListener('pageshow',()=>{try{const saved=JSON.parse(localStorage.getItem(storageKey)||'null');if(saved)for(const k of ['bookmarks','read'])if(Array.isArray(saved[k]))state[k]=saved[k].filter(id=>notes.some(n=>n.id===id));}catch(e){}render();});
 document.addEventListener('keydown',e=>{if(e.key==='/'&&!dialog.open&&!['INPUT','TEXTAREA'].includes(document.activeElement.tagName)){e.preventDefault();$('#search').focus();}});
 $('.filter-row').innerHTML='<button class="chip active" data-category="all" aria-pressed="true">全部主題</button>'+[...new Set(notes.map(n=>n.category))].map(c=>`<button class="chip" data-category="${escape(c)}" aria-pressed="false">${escape(c)}</button>`).join('');
 render();route();
})();
