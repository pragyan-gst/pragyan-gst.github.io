# GST Pragyan, Decap CMS setup

The article editor is installed at `/admin/` and writes article source files to `content/articles/`.

## One-time authentication setup

The public site stays on GitHub Pages. Decap's GitHub backend needs an authentication service or OAuth proxy because the browser must not contain a GitHub client secret.

1. Create a GitHub OAuth application for the GST Pragyan repository.
2. Deploy a supported Decap OAuth proxy or edge worker.
3. Configure the proxy with the GitHub OAuth client ID and client secret.
4. Set the OAuth callback to the `/callback` route of that proxy.
5. In `admin/config.yml`, replace:

       base_url: https://YOUR-OAUTH-PROXY.example.com

   with the proxy base URL.
6. Keep `auth_endpoint: auth` unless the selected proxy uses a different path.
7. Open `https://pragyan-gst.github.io/admin/` and sign in with the authorised GitHub account.

Do not place a GitHub client secret in the repository, the CMS config or any public JavaScript file.

## Publishing an article

1. Sign in at `/admin/`.
2. Open **Articles**.
3. Select **New Article**.
4. Fill in the title, date, review date, summary, topic, audience and legal basis.
5. Add the article body using the Markdown editor.
6. Use the preview to check headings, tables, notes and links.
7. Save the draft.
8. Use the editorial workflow to review and approve it.
9. Publish by merging the generated pull request.

After the article is merged into `main`, GitHub Actions runs `scripts/build_articles.py`. The workflow generates the article HTML page, `articles.json`, the search index and the static article list. The public GitHub Pages site then serves the generated files.

## Local testing

From the website root:

    python3 -m pip install -r requirements.txt
    python3 scripts/build_articles.py
    python3 -m http.server 8000

For local CMS development, use the Decap local proxy documented by Decap. The editorial workflow is not supported by that local proxy, so normal draft and review testing should be done against the hosted repository workflow.
