#!/usr/bin/env python3
"""Run questions in separate Codex sessions and return observable results as JSON."""
import argparse
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from urllib.parse import urlparse


def check(answer, brand):
    names = [str(x).strip().lower() for x in [brand.get('name', ''), *(brand.get('aliases') or [])] if str(x).strip()]
    domains = [str(x).strip().lower().removeprefix('www.') for x in brand.get('official_domains', []) if str(x).strip()]
    text = answer.lower()
    first = re.split(r'\n\s*\n', answer, maxsplit=1)[0][:300].lower()
    titles = {url: title for title, url in re.findall(r'\[([^\]]+)\]\((https?://[^\s)]+)\)', answer)}
    urls = list(dict.fromkeys(u.rstrip('。，、；：.,;:)]】') for u in re.findall(r'https?://[^\s<>"\']+', answer)))
    def domain_matches(url, domain):
        host = (urlparse(url).hostname or '').lower().removeprefix('www.')
        return host == domain or host.endswith('.' + domain)
    return {'mentioned': any(name in text for name in names),
            'is_first_position': any(name in first for name in names),
            'website_cited': any(domain in text for domain in domains) or any(domain_matches(url, domain) for url in urls for domain in domains),
            'answer_links': [{'url': url, 'title': titles.get(url, '')} for url in urls]}


def main():
    parser = argparse.ArgumentParser(description='用当前登录的 Codex 独立会话检测品牌。输入 JSON 从 stdin 读取。')
    parser.add_argument('--search', action='store_true', help='允许 Codex 使用实时网页搜索')
    args = parser.parse_args()
    try:
        data = json.load(sys.stdin)
        brand = data['brand']
        questions = data['prompts']
        if not isinstance(brand, dict) or not isinstance(brand.get('name'), str) or not brand['name'].strip():
            raise ValueError('请提供品牌名称')
        if not isinstance(questions, list) or not 1 <= len(questions) <= 3 or not all(isinstance(q, str) and q.strip() for q in questions):
            raise ValueError('请提供一至三个非空问题')
    except (ValueError, KeyError, TypeError) as exc:
        parser.error(str(exc))
    results = []
    with tempfile.TemporaryDirectory(prefix='aissgc-codex-') as cwd:
        for question in questions:
            command = ['codex'] + (['--search'] if args.search else ['-c', 'web_search="disabled"']) + [
                'exec', '--ephemeral', '--skip-git-repo-check', '--sandbox', 'read-only', '--json', '-']
            try:
                proc = subprocess.run(command, input=question, text=True, capture_output=True, cwd=cwd, timeout=600)
                events = []
                for line in proc.stdout.splitlines():
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
                messages = [e['item']['text'] for e in events if e.get('type') == 'item.completed'
                            and e.get('item', {}).get('type') == 'agent_message' and e['item'].get('text')]
                if proc.returncode or not messages or not any(e.get('type') == 'turn.completed' for e in events):
                    errors = [e.get('message') or e.get('item', {}).get('message') for e in events
                              if e.get('type') in ('error', 'turn.failed') or e.get('item', {}).get('type') == 'error']
                    results.append({'prompt': question, 'error': next((x for x in reversed(errors) if x), 'Codex 未返回完整回答，请检查登录和网络。')})
                    continue
                answer = messages[-1]
                results.append({'prompt': question, 'answer': answer, **check(answer, brand)})
            except (OSError, subprocess.TimeoutExpired) as exc:
                results.append({'prompt': question, 'error': str(exc)})
    print(json.dumps({'channel': 'Codex 独立会话', 'model': '以 Codex 配置为准', 'web_search': '实时搜索已启用，是否使用取决于回答' if args.search else '已关闭',
                      'time': datetime.now(timezone.utc).isoformat(), 'results': results}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
