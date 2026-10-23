"""Combine published release JSON files into the static changelog index."""
import json
from pathlib import Path
root = Path(__file__).parent
entries = []
for path in sorted((root / 'releases').glob('*.json')):
    release = json.loads(path.read_text(encoding='utf-8'))
    if release.get('status', 'Published').lower() == 'published':
        entries.append(release)
entries.sort(key=lambda x: (x.get('date') or '', x.get('title') or ''), reverse=True)
(root / 'changelog.json').write_text(json.dumps(entries, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print(f'Generated changelog.json with {len(entries)} published releases')
