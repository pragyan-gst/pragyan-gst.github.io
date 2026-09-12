# GST Pragyan, website

A lightweight static website for GST reference, calculators, articles and the GST Pragyan Windows desktop application. No framework or build step is required.

## Site structure

    index.html        task-oriented home page and application glimpse
    compliance.html   GST reference, arranged by topic with sticky navigation
    calculators.html  dedicated GST calculators
    app.html          desktop application, real screenshot, workflow and FAQs
    articles.html     article index, built from articles.json
    articles/         one HTML file per article, plus _TEMPLATE.html
    articles.json     the article manifest
    about.html        About GST Pragyan
    contact.html      Contact Us
    privacy.html      privacy policy
    style.css         single responsive stylesheet
    assets/           logo, social preview and optimised application screenshot
    robots.txt        indexing instructions
    .nojekyll         prevents GitHub Pages Jekyll processing

## Design direction

The site is intentionally practical rather than promotional. The primary navigation is:

- GST Reference
- Calculators
- Desktop Tool
- Articles
- About Us
- Contact Us

The home page is organised around tasks: checking a date, calculating a figure, checking a provision, or analysing returns. The desktop application screenshot is an actual supplied application screen, not a mock-up.

The site does not use the word “free” as marketing language. It also does not link to or name an external government website in the site navigation or footer.

## Publishing an article

1. Copy `articles/_TEMPLATE.html` to `articles/YYYY-MM-DD-short-slug.html`.
2. Replace the title, description, date, heading and article content. Cite the legal basis for each substantive figure.
3. Add the article at the top of the `articles` array in `articles.json`.
4. Commit both files. The home page and article index read the same manifest.

## Preview locally

    python3 -m http.server 8000

Then open `http://localhost:8000`.

## Editing

- Email: search for `pragyan.gst@gmail.com`.
- Navigation/footer: the common blocks are duplicated in each static page.
- Home page application link: `index.html#tool`.
- Application request section: `app.html#download`.
- Colours and responsive layout: the `:root` block and media queries in `style.css`.
- GST reference content: `compliance.html`.
- Calculator logic: the script at the foot of `calculators.html`.
- Article list: `articles.json`.

## Privacy and performance

The website uses system fonts and no third-party font CDN, analytics, advertising or tracking scripts. The application screenshot is stored as a compressed WebP asset (`assets/gst-pragyan-app.webp`) to keep the page lightweight.

## Hosting

The site is suitable for GitHub Pages or any ordinary static host. Upload the contents of this directory to the selected site root.

## House style

- Use commas, full stops or parentheses instead of em-dashes.
- Keep substantive GST figures dated and tied to the relevant legal provision.
- Do not present illustrative graphics as statutory data.
- Keep the distinction between a working aid and an official/legal conclusion clear.

## Professional workflow upgrades

Search, printable/filterable reference tables, calculator working-paper outputs, a dated What's New page, a printable GST quick reference sheet, audience pathways and the actual Desktop Tool screenshot are included.

The site avoids em-dashes in visible copy. Use commas, full stops, parentheses or ordinary hyphens instead.
