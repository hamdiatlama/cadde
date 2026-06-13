import re, os

with open('raw.txt', 'r', encoding='utf-8-sig') as f:
    text = f.read()

categories = [
    {
        'dir': '💰 İş ve Finans',
        'header': 'İş ve Finans',
        'pos': 2376,
    },
    {
        'dir': '🎨 Sanat, Medya ve Eğlence',
        'header': 'Sanat, Medya ve Eğlence',
        'pos': 2745,
    },
    {
        'dir': '🏭 Sanayi ve Üretim',
        'header': 'Sanayi ve Üretim',
        'pos': 3317,
    },
    {
        'dir': '🌾 Tarım ve Hayvancılık',
        'header': 'Tarım ve Hayvancılık',
        'pos': 3903,
    },
]

# Find end positions
for i, cat in enumerate(categories):
    if i < len(categories) - 1:
        cat['end'] = categories[i+1]['pos']
    else:
        remaining = text[cat['pos'] + len(cat['header']):]
        emoji_pattern = r'[\U0001F300-\U0001F9FF\U00002600-\U000026FF\U00002700-\U000027BF]'
        match = re.search(emoji_pattern, remaining)
        if match:
            cat['end'] = cat['pos'] + len(cat['header']) + match.start()
        else:
            cat['end'] = len(text)

for cat in categories:
    full_text = text[cat['pos']:cat['end']].strip()
    prof_text = full_text[len(cat['header']):].strip()
    # Remove trailing emoji if any leaked
    prof_text = re.sub(r'[\U0001F300-\U0001F9FF\U00002600-\U000026FF\U00002700-\U000027BF].*$', '', prof_text).strip()
    professions = [p.strip() for p in prof_text.split(',') if p.strip()]
    
    os.makedirs(cat['dir'], exist_ok=True)
    md_path = os.path.join(cat['dir'], 'tablo.md')
    
    lines = [f'# {cat["dir"]} - Meslek Listesi', '', '| # | Meslek |', '|---|--------|']
    for i, p in enumerate(professions, 1):
        lines.append(f'| {i} | {p} |')
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    
    # Print summary to a file since console has encoding issues
    with open('_output_log.txt', 'a', encoding='utf-8') as log:
        log.write(f'Created: {md_path} with {len(professions)} professions\n')
        for i, p in enumerate(professions, 1):
            log.write(f'  {i}. {p}\n')
        log.write('\n')

with open('_output_log.txt', 'a', encoding='utf-8') as log:
    log.write('=== DONE ===\n')
