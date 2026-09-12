from __future__ import annotations

import html
import json
import re
from datetime import date, datetime
from pathlib import Path

import mistune
import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "articles"
ARTICLES_DIR = ROOT / "articles"
ARTICLES_JSON = ROOT / "articles.json"
SEARCH_INDEX = ROOT / "search-index.json"
ARTICLES_PAGE = ROOT / "articles.html"

md = mistune.create_markdown(
    escape=False,
    plugins=["table", "strikethrough", "url"]
)


def parse_article(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"Missing front matter: {path}")
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        raise ValueError(f"Invalid front matter: {path}")
    meta = yaml.safe_load(parts[0][4:]) or {}
    body = parts[1].strip() + "\n"
    slug = path.stem
    data = {
        "slug": slug,
        "title": str(meta.get("title", "")).strip(),
        "date": normalize_date(meta.get("date")),
        "reviewed": normalize_date(meta.get("reviewed"), required=False),
        "summary": str(meta.get("summary", "")).strip(),
        "topic": [str(x) for x in meta.get("topic", []) or []],
        "audience": [str(x) for x in meta.get("audience", []) or []],
        "legal_basis": str(meta.get("legal_basis", "")).strip(),
        "common_pitfall": str(meta.get("common_pitfall", "")).strip(),
        "related_reference": str(meta.get("related_reference", "")).strip(),
        "related_calculator": str(meta.get("related_calculator", "")).strip(),
        "body": body,
    }
    required = ["title", "date", "summary", "legal_basis", "body"]
    missing = [k for k in required if not data[k]]
    if missing:
        raise ValueError(f"Missing {', '.join(missing)} in {path}")
    return data


def normalize_date(value, required: bool = True) -> str:
    if value is None:
        if required:
            raise ValueError("Date is required")
        return ""
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    text = str(value).strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        return text
    try:
        return datetime.fromisoformat(text).date().isoformat()
    except ValueError as exc:
        raise ValueError(f"Invalid date: {text}") from exc


def pretty_date(iso: str) -> str:
    return datetime.strptime(iso, "%Y-%m-%d").strftime("%-d %B %Y")


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def render_article(article: dict) -> str:
    tags = "".join(f'<span class="chip">{esc(t)}</span>' for t in article["topic"])
    reviewed = (
        f'<div class="article-review"><strong>Last reviewed:</strong> {pretty_date(article["reviewed"])}'
        if article["reviewed"] else ""
    )
    if reviewed:
        reviewed += "</div>"
    legal = f'<p><strong>Legal basis.</strong> {esc(article["legal_basis"])}</p>'
    pitfall = (
        f'<p class="note warn"><strong>Common pitfall.</strong> {esc(article["common_pitfall"])}</p>'
        if article["common_pitfall"] else ""
    )
    related = []
    if article["related_reference"]:
        related.append(f'<a href="../{esc(article["related_reference"])}">Related GST reference</a>')
    if article["related_calculator"]:
        related.append(f'<a href="../{esc(article["related_calculator"])}">Related calculator</a>')
    related_html = (
        '<div class="article-related"><strong>Continue the work</strong><div class="chips">' +
        " ".join(f'<span class="chip-link">{x}</span>' for x in related) +
        '</div></div>'
        if related else ""
    )
    body_html = md(article["body"])
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(article["title"])} | GST Pragyan</title>
<meta name="description" content="{esc(article["summary"])}">
<meta property="og:title" content="{esc(article["title"])}">
<meta property="og:description" content="{esc(article["summary"])}">
<meta property="og:image" content="../assets/og.jpg">
<meta name="theme-color" content="#0B2440">
<link rel="stylesheet" href="../style.css">
<link rel="icon" type="image/png" href="../assets/mark-64.png">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap nav"><a class="brand" href="../index.html" aria-label="GST Pragyan home"><img src="../assets/wordmark.png" alt="GST Pragyan" width="215" height="27" class="wm"></a><div class="nav-tools"><button class="search-trigger" type="button" data-search-open aria-label="Search GST Pragyan" title="Search GST Pragyan (Ctrl K)"><span class="search-icon">⌕</span><span class="search-trigger-label">Search</span><kbd>Ctrl K</kbd></button><nav class="desktop-nav" aria-label="Primary navigation"><a href="../compliance.html">GST Reference</a><a href="../calculators.html">Calculators</a><a href="../app.html">Desktop Tool</a><a href="../articles.html" aria-current="page">Articles</a><a href="../about.html">About Us</a><a href="../contact.html">Contact Us</a></nav><details class="mobile-nav"><summary aria-label="Open navigation">Menu</summary><nav aria-label="Mobile navigation"><a href="../search.html">Search</a><a href="../compliance.html">GST Reference</a><a href="../calculators.html">Calculators</a><a href="../app.html">Desktop Tool</a><a href="../articles.html" aria-current="page">Articles</a><a href="../about.html">About Us</a><a href="../contact.html">Contact Us</a></nav></details></div></div></header>
<main id="main">
<section class="hero slim"><div class="wrap narrow"><span class="eyebrow"><a href="../articles.html" style="color:inherit">Articles</a> · <time datetime="{esc(article["date"])}">{pretty_date(article["date"])}</time></span><h1>{esc(article["title"])}</h1><p class="lede">{esc(article["summary"])}</p><div class="article-topic-row">{tags}</div></div></section>
<section class="wrap prose article-prose">{reviewed}{body_html}<div class="article-source"><h2>Legal basis and links</h2>{legal}{pitfall}{related_html}</div></section>
</main>
<footer class="site"><div class="wrap"><div class="footer-top"><div class="footer-brand"><a class="brand footer-mark" href="../index.html" aria-label="GST Pragyan home"><img src="../assets/mark.png" alt="" width="58" height="58"><span><strong>GST Pragyan</strong><small>Practical GST reference and working tools</small></span></a><p>A practical GST reference, calculators, articles and a Windows desktop application for working with downloaded GST data.</p><p class="footer-email"><a href="mailto:pragyan.gst@gmail.com">pragyan.gst@gmail.com</a> · <a href="../contact.html">Report an error</a></p></div><div><h4>Reference</h4><ul><li><a href="../compliance.html#duedates">Due dates</a></li><li><a href="../compliance.html#history">Late fee &amp; interest</a></li><li><a href="../compliance.html#limitation">Limitation</a></li><li><a href="../compliance.html#itc">Input tax credit</a></li><li><a href="../compliance.html#rates">GST rates</a></li></ul></div><div><h4>Tools</h4><ul><li><a href="../calculators.html">GST calculators</a></li><li><a href="../app.html">Desktop tool</a></li><li><a href="../articles.html">Articles</a></li><li><a href="../whats-new.html">What's New</a></li></ul></div><div><h4>GST Pragyan</h4><ul><li><a href="../about.html">About Us</a></li><li><a href="../contact.html">Contact Us</a></li><li><a href="../privacy.html">Privacy</a></li></ul></div></div><div class="footer-bottom"><p>GST Pragyan is an independent GST working and reference tool. It is not an official government website or government-affiliated service.</p><p>For reference and working purposes only. Verify the applicable Act, rule, notification, circular and record before relying on a figure or conclusion.</p><p>© 2026 GST Pragyan.</p></div></div></footer>
<script src="../site.js" defer></script>
</body></html>
'''


def article_card(article: dict) -> str:
    tags = "".join(f'<span class="chip">{esc(t)}</span>' for t in article["topic"])
    return f'<article class="card art article-static" data-tags="{esc(" ".join(article["topic"]).lower())}"><div class="art-meta"><time datetime="{esc(article["date"])}">{pretty_date(article["date"])}</time> {tags}</div><h3><a href="articles/{esc(article["slug"])}.html">{esc(article["title"])}</a></h3><p>{esc(article["summary"])}</p><p><a class="more" href="articles/{esc(article["slug"])}.html">Read article →</a></p></article>'


def build_articles_json(articles):
    payload = {
        "articles": [
            {
                "slug": a["slug"],
                "title": a["title"],
                "date": a["date"],
                "reviewed": a["reviewed"],
                "summary": a["summary"],
                "tags": a["topic"],
                "audience": a["audience"],
                "legal_basis": a["legal_basis"],
                "common_pitfall": a["common_pitfall"],
                "related_reference": a["related_reference"],
                "related_calculator": a["related_calculator"],
            }
            for a in articles
        ],
        "drafts": [],
    }
    ARTICLES_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_search_index(articles):
    existing = json.loads(SEARCH_INDEX.read_text(encoding="utf-8")) if SEARCH_INDEX.exists() else []
    article_urls = {f'articles/{a["slug"]}.html' for a in articles}
    filtered = [x for x in existing if x.get("url") not in article_urls and x.get("kind") != "Article"]
    for a in articles:
        clean = re.sub(r"<[^>]+>", " ", a["body"])
        clean = re.sub(r"[#*`_]+", " ", clean)
        clean = re.sub(r"\s+", " ", clean).strip()
        filtered.append({
            "title": a["title"],
            "description": a["summary"],
            "url": f'articles/{a["slug"]}.html',
            "kind": "Article",
            "tags": ["Article"] + a["topic"],
            "text": f'{a["title"]} {clean}',
        })
    SEARCH_INDEX.write_text(json.dumps(filtered, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def update_articles_page(articles):
    text = ARTICLES_PAGE.read_text(encoding="utf-8")
    start = "<!-- ARTICLE_STATIC_START -->"
    end = "<!-- ARTICLE_STATIC_END -->"
    block = "\n".join(article_card(a) for a in articles)
    pattern = re.compile(re.escape(start) + ".*?" + re.escape(end), re.S)
    replacement = f"{start}\n{block}\n{end}"
    if pattern.search(text):
        text = pattern.sub(replacement, text)
    else:
        marker = '<div id="article-list">'
        if marker in text:
            before, rest = text.split(marker, 1)
            _, after = rest.split('</div>', 1)
            text = before + marker + replacement + '</div>' + after
        else:
            raise ValueError("Could not find article list in articles.html")
    ARTICLES_PAGE.write_text(text, encoding="utf-8")



def update_whats_new(articles):
    page = ROOT / "whats-new.html"
    text = page.read_text(encoding="utf-8")
    start = "<!-- ARTICLE_UPDATES_START -->"
    end = "<!-- ARTICLE_UPDATES_END -->"
    rows = []
    for a in articles[:5]:
        chips = " ".join(f'<span class="chip">{esc(t)}</span>' for t in a["topic"])
        rows.append(
            f'<div class="update-item"><div class="updated">{pretty_date(a["date"])}</div>'
            f'<h2><a href="articles/{esc(a["slug"])}.html">{esc(a["title"])}</a></h2>'
            f'<p>{esc(a["summary"])}</p><div class="chips">{chips} <span class="chip">Article</span></div></div>'
        )
    block = "\n".join(rows)
    pattern = re.compile(re.escape(start) + ".*?" + re.escape(end), re.S)
    if not pattern.search(text):
        raise ValueError("Could not find article update markers in whats-new.html")
    text = pattern.sub(f"{start}\n{block}\n{end}", text)
    page.write_text(text, encoding="utf-8")

def main():
    articles = [parse_article(p) for p in CONTENT.glob("*.md")]
    articles.sort(key=lambda x: x["date"], reverse=True)
    if not articles:
        raise SystemExit("No articles found in content/articles")
    for a in articles:
        (ARTICLES_DIR / f'{a["slug"]}.html').write_text(render_article(a), encoding="utf-8")
    build_articles_json(articles)
    build_search_index(articles)
    update_articles_page(articles)
    update_whats_new(articles)
    print(f"Built {len(articles)} article(s)")


if __name__ == "__main__":
    main()
