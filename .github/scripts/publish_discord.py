"""Publish newly added changelog entries after a successful Build Changelog run.

Manual dispatch accepts an exact version. A tracked ledger prevents reposts.
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

LEDGER = Path('.github/discord-announced.json')
CHANGELOG = Path('changelog.json')
WEBHOOK = os.getenv('DISCORD_WEBHOOK_URL', '')
MODE = os.getenv('PUBLISH_MODE', 'manual')
VERSION = os.getenv('RELEASE_VERSION', '').strip()


def releases_from(raw):
    data = json.loads(raw)
    if not isinstance(data, list):
        raise ValueError('changelog.json must contain an array')
    return data


def key(release):
    return str(release.get('version', '')).strip().casefold()


def prior_versions(sha):
    if not re.fullmatch(r'[0-9a-fA-F]{40}', sha or ''):
        raise ValueError('Missing or invalid originating build commit SHA')
    try:
        raw = subprocess.check_output(
            ['git', 'show', f'{sha}:changelog.json'], stderr=subprocess.DEVNULL
        ).decode('utf-8')
        return {key(r) for r in releases_from(raw)}
    except subprocess.CalledProcessError:
        # A repository with no prior changelog should be treated as a baseline.
        print('No prior changelog at build commit; skipping initial automatic backfill.')
        return None


def slug(release):
    text = str(release.get('id') or release.get('version') or release.get('title') or 'release').strip().lower()
    return re.sub(r'^-+|-+$', '', re.sub(r'[^a-z0-9]+', '-', text))


def make_embed(release):
    url = 'https://tjofw.github.io/beroxity-music-app/#release/' + quote(slug(release))
    version = str(release.get('version') or 'Development update')
    summary = str(release.get('summary') or 'Read the full changelog on our website.').strip()
    if len(summary) > 350:
        summary = summary[:347].rsplit(' ', 1)[0] + '…'
    embed = {
        'title': f'Beroxity Music — {version}'[:256],
        'url': url,
        'description': summary,
        'color': 0xA855F7,
        'fields': [{'name': 'Full changelog', 'value': f'[View release notes]({url})'}],
        'footer': {'text': 'BEROXITY MUSIC • Your Music. Your Library. Your Rules.'},
    }
    date = str(release.get('date') or '')
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', date):
        try:
            datetime.fromisoformat(date)
            embed['timestamp'] = date + 'T12:00:00Z'
        except ValueError:
            pass
    return embed


def post(release):
    payload = json.dumps({'embeds': [make_embed(release)], 'allowed_mentions': {'parse': []}}).encode()
    req = urllib.request.Request(
        WEBHOOK, data=payload,
        headers={'Content-Type': 'application/json', 'User-Agent': 'BeroxityMusicChangelog/2.0'},
        method='POST',
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=25) as response:
                print(f"Published {release.get('version')} to Discord: HTTP {response.status}")
                return
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < 2:
                try:
                    delay = min(float(json.loads(exc.read()).get('retry_after', 2)), 20)
                except (ValueError, TypeError):
                    delay = 2
                time.sleep(delay)
                continue
            raise RuntimeError(f'Discord returned HTTP {exc.code}') from exc
    raise RuntimeError('Discord rate limit retries exhausted')


def main():
    if not WEBHOOK.startswith(('https://discord.com/api/webhooks/', 'https://discordapp.com/api/webhooks/')):
        sys.exit('Missing or invalid DISCORD_WEBHOOK_URL repository secret.')
    releases = releases_from(CHANGELOG.read_text(encoding='utf-8'))
    ledger = json.loads(LEDGER.read_text(encoding='utf-8')) if LEDGER.exists() else {'versions': []}
    announced = {str(v).casefold() for v in ledger.get('versions', [])}

    if MODE == 'manual':
        if not VERSION:
            sys.exit('Missing release version.')
        matches = [r for r in releases if key(r) == VERSION.casefold()]
        if len(matches) != 1:
            sys.exit(f'Expected one release for {VERSION!r}, found {len(matches)}')
        candidates = matches
    elif MODE == 'auto':
        old = prior_versions(os.getenv('BUILD_HEAD_SHA', ''))
        if old is None:
            return
        candidates = [r for r in reversed(releases) if key(r) and key(r) not in old]
    else:
        sys.exit(f'Unknown publishing mode: {MODE}')

    for release in candidates:
        version = str(release.get('version', '')).strip()
        if not version or version.casefold() in announced:
            print(f'Skipping already announced or unversioned release: {version!r}')
            continue
        post(release)
        ledger.setdefault('versions', []).append(version)
        announced.add(version.casefold())
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        LEDGER.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
