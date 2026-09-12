# GST Pragyan, professional GST workbench

A lightweight static website for GST reference, calculators, articles and the GST Pragyan Windows desktop application.

## Publishing articles from the browser

GST Pragyan now uses Decap CMS as the browser editor for articles.

Open:

    https://pragyan-gst.github.io/admin/

The editor creates Markdown files under `content/articles/`. Each article has structured fields for title, publication date, last review date, topics, audience, legal basis, common pitfalls, related references and related calculators.

The public site remains static. Decap CMS writes the article content to GitHub, and the GitHub Actions workflow in `.github/workflows/build-articles.yml` generates the public article HTML, article manifest and search index.

## Authentication setup

The public website remains on GitHub Pages. The Decap GitHub backend requires GitHub authentication through an OAuth service or proxy. Decap's current documentation explains that the GitHub backend needs a server-side authentication step and supports an edge-worker or serverless OAuth proxy.

The supplied `admin/config.yml` already points `base_url` at this site's deployed OAuth proxy:

    base_url: https://gst-pragyan-cms-auth.pragyangst.workers.dev

If the proxy is ever redeployed elsewhere, update `base_url` to the new proxy's domain. Do not put a GitHub client secret in `config.yml` or in any website file.

The OAuth application callback should point to the `/callback` route of that proxy, and the Decap admin page is:

    https://pragyan-gst.github.io/admin/

For a simpler hosted authentication route, Decap also supports Git Gateway with Netlify. That option can be used if the site is later moved to Netlify.

## Editorial workflow

The CMS is configured with `editorial_workflow` and GitHub PR support. A saved article is treated as a draft, then can be reviewed and approved before publication. Squash merging is enabled so published article work stays tidy in the repository history.

## Local article build

From the website root:

    python3 -m pip install -r requirements.txt
    python3 scripts/build_articles.py

The build generates:

    articles/<slug>.html
    articles.json
    search-index.json

It also updates the static article list in `articles.html` and the recent article entries in `whats-new.html`, so the public index and search stay aligned even when JavaScript is disabled.

## Site structure

    index.html        task-oriented home page and application glimpse
    compliance.html   GST reference
    calculators.html  GST calculators
    app.html          desktop application page
    articles.html     article index
    content/articles/ CMS-managed article source files
    articles/         generated article HTML files
    about.html        About GST Pragyan
    contact.html      Contact Us
    privacy.html      Privacy policy
    search.html       site search
    quick-reference.html printable GST quick reference
    admin/             Decap CMS editor
    scripts/           article build script
    .github/workflows/ GitHub Actions workflow

## House style

Use commas, full stops or parentheses instead of em-dashes or en-dashes.

Keep substantive GST figures dated and tied to the relevant legal provision.

Do not present illustrative graphics as statutory data.

Keep the distinction between a working aid and an official or legal conclusion clear.

## Privacy and performance

The public website uses system fonts and does not use analytics, advertising or tracking scripts. The Decap CMS editor is an authenticated administrative interface and is the only part of the site that loads the CMS application from an external package source.
