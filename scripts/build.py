"""Validate the Markdown wiki and produce an offline, GitHub Pages-ready site.
Python 3 standard library only. Run from any working directory.
"""
from pathlib import Path
import html
import json
import re
import shutil
from export_notes import export_all

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {'id','title','category','type','summary','tags','source_id','pages',
            'related','updated','question','options','answer','explanation'}
SECTIONS = ['核心概念','重點整理','教學實例（AI 自編）','易混淆提醒','來源與查證']

def inline(text):
    text = html.escape(text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    def link(m):
        label, target = m.groups()
        if target.endswith('.md'):
            slug = target.rsplit('/',1)[-1][:-3]
            anchor = '#source' if '/sources/' in target else '#coverage' if slug=='coverage' else '#issues' if slug=='open-questions' else '#history' if slug=='log' else '#note/'+slug
            return '<a href="'+anchor+'">'+label+'</a>'
        if target.startswith('https://'):
            return '<a rel="noopener" target="_blank" href="'+target+'">'+label+'</a>'
        return label
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,text)

def render_md(body):
    """Render the documented, deliberately small Markdown subset safely."""
    lines=body.splitlines(); out=[]; i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line: i+=1; continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                row=lines[i].strip().strip('|').split('|')
                if not all(re.fullmatch(r'\s*:?-+:?\s*',c) for c in row): rows.append(row)
                i+=1
            out.append('<div class="table-wrap"><table>')
            for j,row in enumerate(rows):
                tag='th' if j==0 else 'td'
                out.append('<tr>'+''.join('<'+tag+'>'+inline(c.strip())+'</'+tag+'>' for c in row)+'</tr>')
            out.append('</table></div>'); continue
        if line.startswith('- ') or re.match(r'^\d+\. ',line):
            out.append('<ul>')
            while i<len(lines) and (lines[i].strip().startswith('- ') or re.match(r'^\d+\. ',lines[i].strip())):
                item=re.sub(r'^(?:- |\d+\. )','',lines[i].strip())
                out.append('<li>'+inline(item)+'</li>'); i+=1
            out.append('</ul>'); continue
        if line.startswith('#'):
            level=min(len(line)-len(line.lstrip('#')),6)
            if level>1: out.append(f'<h{level}>'+inline(line[level:].strip())+f'</h{level}>')
        else: out.append('<p>'+inline(line)+'</p>')
        i+=1
    return '\n'.join(out)

def build():
    sources=json.loads((ROOT/'wiki/sources/catalog.json').read_text(encoding='utf-8'))
    source_counts={s['id']:s['page_count'] for s in sources}
    notes=[]
    for path in sorted((ROOT/'wiki').glob('*/*.md')):
        if path.parent.name not in ('concepts','comparisons'): continue
        raw=path.read_text(encoding='utf-8')
        assert raw.startswith('---\n'), f'{path}: missing frontmatter'
        front,body=raw[4:].split('\n---\n',1)
        meta={}
        for line in front.splitlines():
            key,value=line.split(':',1); meta[key]=json.loads(value.strip())
        assert REQUIRED<=meta.keys(), f'{path}: missing fields {REQUIRED-meta.keys()}'
        assert meta['id']==path.stem and re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',path.stem)
        assert meta['type'] in ('concept','comparison')
        assert meta['source_id'] in source_counts, 'unknown source'
        assert isinstance(meta['pages'],list) and meta['pages'] and all(type(p)==int and 1<=p<=source_counts[meta['source_id']] for p in meta['pages'])
        assert len(meta['options'])==4 and len(set(meta['options']))==4
        assert type(meta['answer'])==int and 0<=meta['answer']<4
        assert meta['related'] and isinstance(meta['tags'],list)
        assert (ROOT/'wiki/sources'/(meta['source_id']+'.md')).is_file()
        positions=[body.index('## '+heading) for heading in SECTIONS]
        assert positions==sorted(positions), f'{path}: section order'
        meta['html']=render_md(body)
        meta['search']=re.sub(r'\s+',' ',body)
        meta['path']=str(path.relative_to(ROOT))
        notes.append(meta)
    order={name:i for i,name in enumerate(['教育心理基礎','人格與社會發展','道德與性別','認知發展','學習理論','認知與記憶','課程與教學','人本與生態','學習動機','智力與資優','比較統整'])}
    notes.sort(key=lambda n:(order.get(n['category'],9),n['id']))
    ids=[n['id'] for n in notes]
    assert len(ids)==len(set(ids)), 'duplicate IDs'
    index=(ROOT/'wiki/index.md').read_text(encoding='utf-8')
    for n in notes:
        assert n['id']+'.md' in index, 'index missing '+n['id']
        assert all(x in ids and x!=n['id'] for x in n['related']), 'broken related link'
        assert any(n['id'] in other['related'] for other in notes if other['id']!=n['id']), 'orphan note: '+n['id']
    # Check every local Markdown link in the wiki, including source and index pages.
    for path in (ROOT/'wiki').rglob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
            if target.startswith(('https://','http://','#')): continue
            assert (path.parent/target.split('#')[0]).is_file(), f'broken link: {path}: {target}'
    target=ROOT/'docs'; target.mkdir(exist_ok=True)
    sources_html=''.join('<h2>'+html.escape(s['title'])+'</h2>'+render_md((ROOT/'wiki/sources'/s['file']).read_text(encoding='utf-8')) for s in sources)
    payload=json.dumps({'notes':notes, 'sourcesHtml':sources_html,
        'issuesHtml':render_md((ROOT/'wiki/open-questions.md').read_text(encoding='utf-8')),
        'coverageHtml':render_md((ROOT/'wiki/coverage.md').read_text(encoding='utf-8')),
        'historyHtml':render_md((ROOT/'wiki/log.md').read_text(encoding='utf-8'))},ensure_ascii=False).replace('<','\\u003c')
    (target/'data.js').write_text('window.WIKI = '+payload+';\n',encoding='utf-8')
    for name in ['index.html','style.css','app.js']: shutil.copyfile(ROOT/'web'/name,target/name)
    (target/'.nojekyll').touch()
    standalone=(target/'index.html').read_text(encoding='utf-8')
    standalone=standalone.replace('<link rel="stylesheet" href="style.css">','<style>'+(target/'style.css').read_text(encoding='utf-8')+'</style>')
    standalone=standalone.replace('<script defer src="data.js"></script>','<script>'+(target/'data.js').read_text(encoding='utf-8')+'</script>')
    standalone=standalone.replace('<script defer src="app.js"></script>','<script defer>'+ (target/'app.js').read_text(encoding='utf-8')+'</script>')
    # Inline script must run after DOM parsing, since defer does not affect inline scripts.
    standalone=standalone.replace('<script defer>','<script>document.addEventListener("DOMContentLoaded",()=>{').replace('</script>\n</head>','});</script>\n</head>')
    (ROOT/'START-HERE.html').write_text(standalone,encoding='utf-8')
    (ROOT/'index.html').write_text(standalone,encoding='utf-8')
    (target/'single-file.html').write_text(standalone,encoding='utf-8')
    export_all(ROOT,notes)
    root_index='# LLM WIKI的工作資料｜總索引\n\n[AI 工作規則](AGENTS.md) · [操作順序](WORKFLOW.md) · [網站首頁](index.html)\n\n## 知識庫\n\n[Wiki 主題索引](wiki/index.md) · [更新日誌](wiki/log.md) · [待查證事項](wiki/open-questions.md)\n\n## Wiki → 複習筆記 → HTML\n\n| 主題 | Wiki | Markdown 筆記 | HTML 閱讀頁 |\n| --- | --- | --- | --- |\n'
    for n in notes:
        root_index+=f'| {n["title"]} | [知識頁]({n["path"]}) | [複習筆記](notes/md/{n["id"]}.md) | [閱讀頁](notes/html/{n["id"]}.html) |\n'
    (ROOT/'index.md').write_text(root_index,encoding='utf-8')
    print(f'PASS: {len(notes)} notes, unique IDs, sources, page ranges, sections, quiz answers, related links and wiki links. Built docs/index.html.')

if __name__=='__main__': build()
