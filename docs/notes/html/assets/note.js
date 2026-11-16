"use strict";
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
