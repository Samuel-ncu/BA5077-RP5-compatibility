"""檢查 56 篇教材的本機連結與 Python 語法；不執行範例或宣稱實機驗收。"""
import ast
import json
from pathlib import Path
import re
import textwrap
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def links(markdown):
    text = re.sub(r'```.*?```', '', markdown, flags=re.S)
    for match in re.finditer(r'\]\(', text):
        start = match.end()
        depth = 1
        end = start
        while end < len(text) and depth:
            if text[end] == '(':
                depth += 1
            elif text[end] == ')':
                depth -= 1
            end += 1
        if depth == 0:
            yield text[start:end - 1].strip('<>')


def check():
    lessons = sorted(p for p in (ROOT / '教材').glob('*.md')
                     if p.name.startswith(('第 ', '補充 ', '使用 Flask')))
    issues = []
    blocks = 0
    for path in lessons:
        source = path.read_text(encoding='utf-8-sig')
        for target in links(source):
            if target.startswith(('https:', 'http:', 'mailto:', '#')):
                continue
            filename = unquote(target.split('#')[0])
            if not (path.parent / filename).exists():
                issues.append({'file': path.name, 'missing_file': target})
        for number, code in enumerate(re.findall(r'```python\n(.*?)```', source, re.S), 1):
            blocks += 1
            try:
                ast.parse(textwrap.dedent(code))
            except SyntaxError as exc:
                issues.append({'file': path.name, 'python_block': number,
                               'error': exc.msg, 'line': exc.lineno})
    scripts = sorted((ROOT / '教材/範例程式').glob('*.py'))
    for path in scripts:
        try:
            ast.parse(path.read_text(encoding='utf-8-sig'))
        except SyntaxError as exc:
            issues.append({'script': path.name, 'error': exc.msg, 'line': exc.lineno})
    result = {'lessons': len(lessons), 'python_blocks': blocks,
              'python_scripts': len(scripts), 'issues': issues,
              'scope': 'local file links and syntax only; no installation or hardware validation'}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return len(lessons) == 56 and not issues


if __name__ == '__main__':
    raise SystemExit(0 if check() else 1)
