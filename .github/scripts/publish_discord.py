import json
import os
import re
import sys
import urllib.request
from pathlib import Path

webhook = os.environ.get('DISCORD_WEBHOOK_URL', '')
version = os.environ.get('RELEASE_VERSION', '').strip()
if not webhook.startswith('https://discord.com/api/webhooks/') and not webhook.startswith('https://discordapp.com/api/webhooks/'):
    sys.exit('Missing or invalid DISCORD_WEBHOOK_URL repository secret.')
if not version:
    sys.exit('Missing release version.')
releases = json.loads(Path('changelog.json').read_text(encoding='utf-8'))
if not isinstance(releases, list):
    sys.exit('changelog.json must contain an array.')
matches = [r for r in releases if str(r.get('version', '')).strip().casefold() == version.casefold()]
if len(matches) != 1:
    sys.exit(f'Expected exactly one release for {version!r}, found {len(matches)}.')
r = matches[0]
slug = re.sub(r'(^-|-$)', '', re.sub(r'[^a-z0-9]+', '-', str(r.get('id') or r.get('version') or r.get('title') or 'release').strip().lower()))
from urllib.parse import quote
url = 'https://tjofw.github.io/beroxity-music-app/#release/' + quote(slug)
embed = {
    'title': str(r.get('title') or 'BEROXITY MUSIC — ' + version)[:256],
    'url': url,
    'description': str(r.get('summary') or 'View the full changelog on our website.')[:4096],
    'color': 0xA855F7,
    'fields': [{'name': 'Full changelog', 'value': f'[View release notes]({url})'}],
    'footer': {'text': 'BEROXITY MUSIC • Your Music. Your Library. Your Rules.'}
}
if re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(r.get('date', ''))):
    embed['timestamp'] = r['date'] + 'T12:00:00Z'
body = json.dumps({'embeds': [embed], 'allowed_mentions': {'parse': []}}).encode('utf-8')
req = urllib.request.Request(webhook, data=body, headers={'Content-Type': 'application/json', 'User-Agent': 'BeroxityMusicChangelog/1.0'}, method='POST')
try:
    with urllib.request.urlopen(req, timeout=20) as response:
        print('Discord announcement published:', response.status)
except Exception as exc:
    sys.exit(f'Discord publishing failed: {type(exc).__name__}. Check webhook and workflow logs.')
