# BEROXITY MUSIC — Website v2

Live site: https://tjofw.github.io/beroxity-music-app/

## Installation

1. Extract this ZIP.
2. Upload **all files and folders**, including the hidden `.pages.yml` and `.github/workflows` folders, into the root of your existing `tjofw/beroxity-music-app` GitHub repository. Overwrite `index.html` and `changelog.json`. Keep the repository public and GitHub Pages on main/root.
3. In repository **Settings → Actions → General → Workflow permissions**, select **Read and write permissions** if the changelog-index workflow cannot push.
4. Go to https://app.pagescms.org/ and sign in with GitHub. Install/authorize the Pages CMS GitHub App for **only** `tjofw/beroxity-music-app`.
5. Open the repository in Pages CMS. Choose **Changelog releases**, create a release, and save it. Choose **Published** for a public release, or **Draft** to hide it.
6. GitHub Actions automatically regenerates `changelog.json` after changes under `releases/`. Check **Actions → Build changelog index** if it does not update. Pages redeploys after the generated index is committed.

## How this works

- `releases/*.json`: source files managed by Pages CMS.
- `.pages.yml`: editor configuration, including sections and item lists.
- `build_changelog.py`: generates the public JSON index from **Published** entries only.
- `.github/workflows/update-changelog.yml`: regenerates and commits the index.
- `changelog.json`: public index loaded by the site; do not edit manually once CMS is active.

## Security

The site's Login and Admin links open the **external** Pages CMS editor. GitHub OAuth is handled by Pages CMS; the public GitHub Pages site does **not** authenticate anyone or store passwords/tokens. The Admin page is a public instruction page, not a private dashboard. Actual edit rights are controlled by GitHub repository permissions. No GitHub token should be added to public files.

## Notes

The site retains the existing published changelog. Release dates can be filled in when known. The hosted Pages CMS UI may change. The workflow needs repository write permissions to commit the generated JSON. If your repository uses protected branches, workflow pushes may require different settings.
