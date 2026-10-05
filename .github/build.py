"""The sandbox's locales build: source/*.po plus translations/<lang>/*.json -> branches/..."""
import json
import os
import re
import sys

uid, branch = sys.argv[1], sys.argv[2]
UNESCAPE = {'\\\\': '\\', '\\"': '"', '\\t': '\t', '\\n': '\n'}


def unescape(text):
    return re.sub(r'\\[\\"tn]', lambda m: UNESCAPE[m.group(0)], text)


def parse(path):
    strings, key, field = {}, None, None
    for line in open(path, encoding='utf-8').read().split('\n'):
        if m := re.match(r'^msgctxt "(.*)"$', line):
            key, field = unescape(m.group(1)), None
        elif m := re.match(r'^(msgid|msgstr) "(.*)"$', line):
            field = m.group(1)
            if field == 'msgid' and key is not None:
                strings[key] = unescape(m.group(2))
        elif (m := re.match(r'^"(.*)"$', line)) and field == 'msgid' and key is not None:
            strings[key] += unescape(m.group(1))
        elif line.strip() == '':
            key = None if field == 'msgstr' else key
    return strings


def as_built(value):
    """The real converter json_decodes every value: "2.10" -> 2.1, "true" -> true."""
    try:
        return json.loads(value)
    except ValueError:
        return value


languages = {'de'} | ({d for d in os.listdir('translations')} if os.path.isdir('translations') else set())
for po in sorted(os.listdir('source')):
    if not po.endswith('.po'):
        continue
    name = po[:-3]
    english = parse(os.path.join('source', po))
    for language in ['en'] + sorted(languages - {'en'}):
        translated = {}
        path = os.path.join('translations', language, name + '.json')
        if language != 'en' and os.path.exists(path):
            translated = json.load(open(path, encoding='utf-8'))
        data = {key: as_built(translated.get(key, text)) for key, text in english.items()}
        out = os.path.join('branches', branch, uid, language)
        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, name + '.json'), 'w', encoding='utf-8') as f:
            json.dump({'data': data, 'meta': {'context': name, 'language': language}}, f, ensure_ascii=False)
        print(f'{out}/{name}.json: {len(data)} keys')
