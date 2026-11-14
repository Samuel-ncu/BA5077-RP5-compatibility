"""把 部落格版/ 的 Markdown 文章轉成 digithouse.net 部落格草稿用的 Payload Lexical bundle（JSON）。

用法：python3 -I tools/md2lexical.py <repo> <out.json> NN [NN ...] [--seo]

- 只產生網站已能顯示的節點：heading、paragraph、text、link、list/listitem、quote、code、upload。
- 網站編輯器沒有表格功能，Markdown 表格會轉成項目清單；表格中跳脫的 \\| 不算欄位分隔。
- 圖片必須是 raw.githubusercontent.com 外連；檔案以 base64 放進 bundle，上傳時以檔名重複使用。
- 站內互連改成 https://digithouse.net/blog/<slug>，slug 取自 部落格版/新舊課號對照表.md。
- 加 --seo 時，從 部落格版/網站SEO與分類標籤.md 帶入每篇的 SEO 標題、描述、圖片與主題標籤，
  並加上共同分類與基本標籤，產出可直接交給平台一次性草稿腳本的 bundle。
- 只轉換，不連線、不寫入網站；建立草稿由平台端腳本處理，發佈由編輯在後台按「發佈」。
"""
import base64, json, re, sys
from pathlib import Path
from urllib.parse import unquote

args = [a for a in sys.argv[1:] if a != '--seo']; with_seo = '--seo' in sys.argv[1:]
repo = Path(args[0]); out = Path(args[1]); wanted = args[2:]
blog = repo / '部落格版'
RAW = 'https://raw.githubusercontent.com/Samuel-ncu/BA5077-RP5-compatibility/main/'
GH_BLOB = 'https://github.com/Samuel-ncu/BA5077-RP5-compatibility/blob/main/部落格版/'
SITE = 'https://digithouse.net/blog/'
BOLD, ITALIC, CODE = 1, 2, 16


SLUGS = {m.group(1).zfill(2): m.group(2) for m in re.finditer(r'^\| *(\d+) *\|.*`(ba5077-[a-z0-9-]+)` *\| *$', (blog / '新舊課號對照表.md').read_text(encoding='utf-8'), re.M)}


def slug_for(nn):
    return SLUGS[nn]


def text(t, fmt=0):
    return {'detail': 0, 'format': fmt, 'mode': 'normal', 'style': '', 'text': t, 'type': 'text', 'version': 1}


def block(kind, children, **extra):
    node = {'children': children, 'direction': 'ltr', 'format': '', 'indent': 0, 'type': kind, 'version': 1}
    node.update(extra)
    return node


def map_href(href):
    if href.startswith('http'):
        return href
    name = unquote(href[2:] if href.startswith('./') else href)
    m = re.match(r'(\d\d)-', name)
    if m:
        return SITE + slug_for(m.group(1)) + '?locale=zh-TW'
    return GH_BLOB + href.lstrip('./')


INLINE = re.compile(r'\[((?:[^\[\]]|`[^`]*`)+)\]\(([^)\s]+)\)|\*\*(.+?)\*\*|`([^`]+)`|\*([^*\s][^*]*?)\*')


def inline(s, fmt=0):
    nodes, pos = [], 0
    for m in INLINE.finditer(s):
        if m.start() > pos:
            nodes.append(text(s[pos:m.start()], fmt))
        if m.group(1) is not None:
            nodes.append({'children': inline(m.group(1), fmt), 'direction': 'ltr', 'format': '', 'indent': 0,
                          'type': 'link', 'version': 3,
                          'fields': {'linkType': 'custom', 'newTab': not map_href(m.group(2)).startswith(SITE), 'url': map_href(m.group(2))}})
        elif m.group(3) is not None:
            nodes.extend(inline(m.group(3), fmt | BOLD))
        elif m.group(4) is not None:
            nodes.append(text(m.group(4), fmt | CODE))
        else:
            nodes.extend(inline(m.group(5), fmt | ITALIC))
        pos = m.end()
    if pos < len(s):
        nodes.append(text(s[pos:], fmt))
    return nodes


def cells(row):
    # GitHub tables escape a literal pipe as \|; it is not a column separator.
    return [c.strip().replace('\\|', '|') for c in re.split(r'(?<!\\)\|', row.strip().strip('|'))]


def table_to_list(rows):
    header = cells(rows[0])
    items = []
    for row in rows[2:]:
        c = cells(row)
        kids = inline(c[0], BOLD)
        rest = ['%s：%s' % (header[i], c[i]) if len(header) > 2 else c[i] for i in range(1, len(c))]
        if rest:
            kids += [text('：' if len(header) == 2 else '｜')] + inline('；'.join(rest))
        items.append(kids)
    return make_list(items, 'bullet')


def make_list(items, kind, start=1):
    children = [block('listitem', kids, value=i + start) for i, kids in enumerate(items)]
    return block('list', children, listType=kind, start=start, tag='ul' if kind == 'bullet' else 'ol')


def convert(md, images):
    lines = md.splitlines()
    nodes, i = [], 0
    title = None
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        if s.startswith('```'):
            lang = s[3:].strip() or 'text'
            j = i + 1
            indent = len(line) - len(line.lstrip())
            buf = []
            while not lines[j].strip().startswith('```'):
                buf.append(lines[j][indent:] if lines[j][:indent].strip() == '' else lines[j])
                j += 1
            nodes.append(block('code', [text('\n'.join(buf))], language=lang))
            i = j + 1
            continue
        m = re.match(r'^(#{1,6})\s+(.*)$', s)
        if m:
            if len(m.group(1)) == 1 and title is None:
                title = m.group(2)
            else:
                nodes.append(block('heading', inline(m.group(2)), tag='h%d' % min(max(len(m.group(1)), 2), 4)))
            i += 1
            continue
        m = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)$', s)
        if m:
            fname = unquote(m.group(2).rsplit('/', 1)[-1])
            assert m.group(2).startswith(RAW), m.group(2)
            images.setdefault(fname, m.group(1))
            nodes.append({'type': 'upload', 'version': 3, 'format': '', 'relationTo': 'media',
                          'value': '__MEDIA__:' + fname, 'fields': None, 'id': 'img-%s' % fname})
            i += 1
            continue
        if s.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                rows.append(lines[i]); i += 1
            nodes.append(table_to_list(rows))
            continue
        if s.startswith('>'):
            paras, cur = [], []
            while i < len(lines) and lines[i].strip().startswith('>'):
                body = lines[i].strip()[1:].strip()
                if body:
                    cur.append(body)
                elif cur:
                    paras.append(' '.join(cur)); cur = []
                i += 1
            if cur:
                paras.append(' '.join(cur))
            kids = []
            for n, p in enumerate(paras):
                if n:
                    kids.append({'type': 'linebreak', 'version': 1})
                kids.extend(inline(p))
            nodes.append(block('quote', kids))
            continue
        m = re.match(r'^(\d+)\.\s+(.*)$', s) or re.match(r'^[-*]\s+(.*)$', s)
        if m and line == line.lstrip():
            numbered = s[0].isdigit()
            start = int(m.group(1)) if numbered else 1
            items = []
            while i < len(lines):
                ls = lines[i]
                mm = (re.match(r'^(\d+)\.\s+(.*)$', ls) if numbered else re.match(r'^[-*]\s+(.*)$', ls))
                if not mm:
                    break
                items.append(inline(mm.group(mm.lastindex)))
                i += 1
                while i < len(lines) and lines[i].startswith('   ') and not lines[i].strip().startswith(('```', '![')):
                    items[-1] += [text(' ')] + inline(lines[i].strip()); i += 1
                if i < len(lines) and not lines[i].strip() and i + 1 < len(lines) and lines[i + 1].startswith('   '):
                    break  # indented block (code/image) follows: close the list, render it top-level
                if i < len(lines) and not lines[i].strip() and i + 1 < len(lines) and (re.match(r'^\d+\.\s', lines[i + 1]) if numbered else re.match(r'^[-*]\s', lines[i + 1])):
                    i += 1
            nodes.append(make_list(items, 'number' if numbered else 'bullet', start))
            continue
        buf = [s]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#|```|\||>|!\[|[-*]\s|\d+\.\s)', lines[i].strip()):
            buf.append(lines[i].strip()); i += 1
        nodes.append(block('paragraph', inline(' '.join(buf))))
    return title, nodes


def plain(nodes):
    out = []
    for n in nodes:
        if n.get('type') == 'text':
            out.append(n['text'])
        out.append(plain(n.get('children', [])))
    return ''.join(out)


bundle = {'images': [], 'posts': []}
images = {}
for nn in wanted:
    path = next(blog.glob(nn + '-*.md'))
    title, nodes = convert(path.read_text(encoding='utf-8'), images)
    assert title, path
    paras = [plain(n['children']) for n in nodes if n['type'] == 'paragraph' and not plain(n['children']).startswith(('digithouse.net 原文', '原始課程目錄'))]
    excerpt = paras[0]
    if len(excerpt) > 160:
        cut = max(excerpt.rfind(p, 0, 160) for p in '。？！')
        excerpt = excerpt[:cut + 1] if cut > 40 else excerpt[:157] + '…'
    bundle['posts'].append({'nn': nn, 'slug': slug_for(nn), 'title': title, 'excerpt': excerpt,
                            'content': {'root': block('root', nodes)}})
for fname, alt in images.items():
    data = (repo / '教材/圖檔' / fname).read_bytes()
    bundle['images'].append({'filename': fname, 'alt': alt, 'mimetype': 'image/png' if fname.endswith('.png') else 'image/jpeg',
                             'b64': base64.b64encode(data).decode()})
TAGS = {'AI': 'digithouse-ai', 'Camera': 'digithouse-camera', 'Libcamera': 'digithouse-libcamera', 'Linux': 'digithouse-linux',
        'OpenCV': 'digithouse-opencv', 'Picamera2': 'digithouse-picamera2', 'Python': 'digithouse-python'}
if with_seo:
    table = (blog / '網站SEO與分類標籤.md').read_text(encoding='utf-8')
    rows = {m.group(1): m for m in re.finditer(r'^\| (\d\d) \| `([^`]+)` \| ([^|]+) \| ([^|]+?) \| DigitHouse \| ([^|]+?) \| `?([^`|]+?)`? \|$', table, re.M)}
    names = {image['filename'] for image in bundle['images']} | set(images)
    for post in bundle['posts']:
        row = rows[post['nn']]
        assert row.group(2) == post['slug'], (row.group(2), post['slug'])
        image = row.group(6).strip()
        image = None if image == '—' else image
        assert image is None or image in names, image
        tags = [] if row.group(3).strip() == '—' else [TAGS[t] for t in row.group(3).split('、')]
        post['seo'] = {'title': row.group(4) + ' | DigitHouse', 'description': row.group(5), 'image': image}
        post['extraTags'] = tags
    bundle['categories'] = ['course-ba5077', 'digithouse-technical-articles']
    bundle['baseTags'] = ['digithouse-aiot', 'digithouse-aiot-product-development', 'digithouse-raspberry-pi']
out.write_text(json.dumps(bundle, ensure_ascii=False), encoding='utf-8')
print('posts', [(p['slug'], p['title'], len(p['content']['root']['children'])) for p in bundle['posts']])
print('images', [(x['filename'], len(x['b64']) * 3 // 4) for x in bundle['images']])
print('excerpts'); [print(' ', p['slug'], p['excerpt'][:90]) for p in bundle['posts']]
