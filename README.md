# GST Pragyan — website

Static pages. No framework, no build step, no dependencies.

    index.html        home page, visual overview, latest articles and the desktop tool
    compliance.html   12 chart sections + 3 calculators — late fee and interest since
    about.html        why GST Pragyan exists, design principles and who it is for
    contact.html      contact details, corrections and feedback
                      01.07.2017, notice/order limitation dates, and the rate structure
    articles.html     the article index, built from articles.json
    articles/         one HTML file per article, plus _TEMPLATE.html
    articles.json     the article manifest — the only file to edit when publishing
    privacy.html      privacy policy
    style.css         one stylesheet for all of them
    assets/           logo, wordmark and social preview (109 KB)
    robots.txt        allows indexing
    .nojekyll         tells GitHub Pages not to run Jekyll over the files

## Publishing an article

One new file and one new line. Weekly is the intended rhythm; nothing breaks if you skip
a week.

1. Copy `articles/_TEMPLATE.html` to `articles/YYYY-MM-DD-short-slug.html`.
2. Write it. Replace the `<title>`, the description and og:title in the head, the date in
   the `<time>` element, the heading and the lede. Cite the provision for every figure.
3. Add one entry at the **top** of the `articles` array in `articles.json`:

       { "slug":    "YYYY-MM-DD-short-slug",
         "title":   "...",
         "date":    "YYYY-MM-DD",
         "summary": "One or two sentences.",
         "tags":    ["Rates"] }

   The slug must match the file name without `.html`.
4. Commit both files. The index page and the three-card strip on the home page both read
   `articles.json`, so there is nothing else to update.

To **unpublish** without deleting, move the entry from `articles` to `drafts`. The page
stays on the server and drops off every list.

Two things worth knowing:

- The lists are built by `fetch()`, which cannot read a `file://` URL. Opening
  `articles.html` by double-clicking shows an explanatory message instead of the list.
  Serve over HTTP to preview — see below. On GitHub Pages it just works.
- The article pages themselves are plain static HTML with no scripting, so they are
  indexed and readable regardless.

## Preview locally

    python3 -m http.server 8000     # then open http://localhost:8000

## Editing

- **Email** — search for `pragyan.gst@gmail.com` in all three pages.
- **Download link** — `index.html`, the section with `id="download"`. Replace the two
  buttons with a real link when the app is published.
- **Colours** — the `:root` block at the top of `style.css`.
- **Statutory figures** — `compliance.html`. The hero carries a review date; change it
  whenever you check the figures, and change the "Last updated" line in `privacy.html`
  whenever that policy changes.
- **Rates** — section 12 of `compliance.html`. It must agree with
  `gstk/rate_registry.json` in the desktop tool; if you change one, change the other.
- **Limitation dates** — the `YEARS` object in the script at the foot of
  `compliance.html` drives the third calculator. Each year has the annual return due date
  and the s.73 / s.74 notice and order dates. Add a year by copying an entry.

## What to review, and when

The charts are only as good as their last review. Two things change often:

- **Due dates** are extended by notification, sometimes at a few days' notice.
- **Limitation dates for FY 2018-19 and 2019-20** rest on Notification No. 56/2023-CT,
  which is under challenge in several High Courts. If it is struck down those two rows
  change, and the page says so — keep that caveat until the position settles.

## Logo assets

Generated from the supplied artwork with the white background flood-filled away from the
EDGES only, so the white eye and bars inside the mark stay white. Knocking out every white
pixel makes them transparent and the mark falls apart on the navy hero.

    mark.png            300px  the P mark, transparent
    mark-64.png          64px  favicon
    wordmark.png        860px  header, on light backgrounds
    wordmark-light.png  860px  footer, navy letters recoloured white
    lockup.png          700px  stacked mark + wordmark
    og.jpg        1200x630px   social preview

## Hosting: GitHub Pages

1. Create a public repository, e.g. `pragyan-site`.
2. Upload these files to the root of the `main` branch.
3. Settings → Pages → Source: *Deploy from a branch* → `main` / `/ (root)` → Save.
4. Live in a minute or two at `https://<username>.github.io/pragyan-site/`.

Custom domain: Settings → Pages → Custom domain, then at your registrar add a CNAME
record pointing to `<username>.github.io`. Tick *Enforce HTTPS* once the certificate is
issued.
