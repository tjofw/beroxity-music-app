# BEROXITY MUSIC — Changelog Website

Free static website for GitHub Pages. No build tools or paid hosting required.

## Publish

1. Sign in to GitHub and create a **public** repository named `beroxity-music-changelog`.
2. Select **Add file → Upload files**, then upload `index.html` and `changelog.json` from this folder. Commit them to the `main` branch at the repository root.
3. In the repository, open **Settings → Pages**.
4. Under **Build and deployment**, select **Deploy from a branch**.
5. Choose `main` and `/ (root)`; save.
6. Once GitHub finishes publishing, your site will be at `https://YOUR-USERNAME.github.io/beroxity-music-changelog/`.

## Add future updates

Edit `changelog.json` on GitHub. Add a new release object at the **top** of the JSON array, separated from the next release by a comma. Use the existing release as a template. The website updates after you commit changes.

The initial entry is based on the development notes supplied in chat. Its date is deliberately blank because no release date was specified. Set it to a real date in `YYYY-MM-DD` format if you wish.

Note: GitHub Pages sites and repository contents are publicly accessible. Do not commit private keys, tokens, or secrets.
