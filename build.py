"""Build publications.claritasz.com from the folders in this repository.

The folders are the single source of truth. Netlify runs this script on every
push; nothing it writes (nl/, en/) is committed. Standard library only.

Weekly reports are found by path and file name:
  reports/de-<architect>/YYYY/<Name>_YY_WW.pdf        Dutch weekly edition
  reports/the-<architect>/eu/YYYY/<Name>_YY_WW.pdf    European weekly edition
  reports/european-architecture-review/YYYY/<Name>_YY_MM.pdf    monthly theme issue
reports/sample/ is kept as published and not listed here.

The central observation and the week's signals are read from the published
PDFs themselves, so the site never says anything the report does not.
"""

import functools
import html
import pathlib
import re

try:  # Reading the reports is optional: without pypdf the tiles show their fixed text.
    import pypdf
except BaseException:  # also a broken crypto backend, which raises outside Exception
    pypdf = None

ROOT = pathlib.Path(__file__).parent
BRAND = "https://claritasz.com"

PERSPECTIVES = ["enterprise", "business", "data", "integration", "security", "infrastructure"]

EDITIONS = {
    "nl": {
        "glob": "reports/de-*/[0-9][0-9][0-9][0-9]/*.pdf",
        "slug": {"enterprise": "de-enterprisearchitect", "business": "de-businessarchitect",
                 "data": "de-dataarchitect", "integration": "de-integratiearchitect",
                 "security": "de-securityarchitect", "infrastructure": "de-infrastructuurarchitect"},
        "name": {"enterprise": "De Enterprisearchitect", "business": "De Businessarchitect",
                 "data": "De Dataarchitect", "integration": "De Integratiearchitect",
                 "security": "De Securityarchitect", "infrastructure": "De Infrastructuurarchitect"},
        "short": {"enterprise": "Enterprise", "business": "Business", "data": "Data",
                  "integration": "Integratie", "security": "Security", "infrastructure": "Infrastructuur"},
    },
    "eu": {
        "glob": "reports/the-*/eu/[0-9][0-9][0-9][0-9]/*.pdf",
        "slug": {"enterprise": "the-enterprise-architect", "business": "the-business-architect",
                 "data": "the-data-architect", "integration": "the-integration-architect",
                 "security": "the-security-architect", "infrastructure": "the-infrastructure-architect"},
        "name": {"enterprise": "The Enterprise Architect", "business": "The Business Architect",
                 "data": "The Data Architect", "integration": "The Integration Architect",
                 "security": "The Security Architect", "infrastructure": "The Infrastructure Architect"},
        "short": {"enterprise": "Enterprise", "business": "Business", "data": "Data",
                  "integration": "Integration", "security": "Security", "infrastructure": "Infrastructure"},
    },
}

REVIEW_GLOB = "reports/european-architecture-review/[0-9][0-9][0-9][0-9]/*.pdf"

MONTHS = {
    "nl": ["januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus",
           "september", "oktober", "november", "december"],
    "en": ["January", "February", "March", "April", "May", "June", "July", "August",
           "September", "October", "November", "December"],
}

TEXT = {
    "nl": {
        "locale": "nl_NL", "lang_label": "Taal",
        "title": "Publicaties", "lead": "Reports, essays, papers en AI prompts. Vrij te lezen en te gebruiken.",
        "reports": "Reports", "essays": "Essays", "papers": "Papers", "prompts": "AI prompts",
        "weekly": "Wekelijks", "edition": "Editie", "latest": "Nieuwste editie",
        "earlier": "Eerdere edities", "none": "De eerste editie volgt.",
        "nl_title": "Nederlandse weekeditie", "nl_when": "Elke dinsdag",
        "nl_lead": "Zes architectuurperspectieven op één gedeelde feitelijke grond, met de blik op Nederland.",
        "eu_title": "Europese weekeditie", "eu_when": "Elke donderdag",
        "eu_lead": "Dezelfde zes perspectieven vanuit een Europese context. Een eigen selectie, geen vertaling.",
        "monthly": "Maandelijks", "issue": "Nummer", "earlier_issues": "Eerdere nummers",
        "review_title": "European Architecture Review", "review_when": "Laatste vrijdag van de maand",
        "review_lead": "Het meest ingrijpende Europese architectuurthema van de maand, vanuit alle zes perspectieven.",
        "review_contents": "Editorial, één pagina per perspectief, synthese over de perspectieven heen en primaire bronnen.",
        "review_none": "Het eerste nummer verschijnt eind oktober 2026.",
        "essay_ambiguity": "Een reflectie of betoog, dat één gedachte uitwerkt.",
        "paper_chain": "Bron, beleid, principe, kader, richtlijn, maatregel. Hoe besluiten door een organisatie stromen.",
        "paper_grounds": "Architectuurpraktijk in complexe, veranderende omgevingen.",
        "prompt_provenance": "Voor Copilot. Maakt architectuurbesluiten herleidbaar: documentatie en databaseschema. Vrij te gebruiken.",
        "source": "Bron op GitHub", "back": "Terug",
    },
    "en": {
        "locale": "en_GB", "lang_label": "Language",
        "title": "Publications", "lead": "Reports, essays, papers and AI prompts. Free to read and to use.",
        "reports": "Reports", "essays": "Essays", "papers": "Papers", "prompts": "AI prompts",
        "weekly": "Weekly", "edition": "Edition", "latest": "Latest edition",
        "earlier": "Earlier editions", "none": "The first edition follows.",
        "nl_title": "Dutch weekly edition", "nl_when": "Every Tuesday",
        "nl_lead": "Six architecture perspectives on one shared factual ground, focused on the Netherlands.",
        "eu_title": "European weekly edition", "eu_when": "Every Thursday",
        "eu_lead": "The same six perspectives from a European context. A separate selection, not a translation.",
        "monthly": "Monthly", "issue": "Issue", "earlier_issues": "Earlier issues",
        "review_title": "European Architecture Review", "review_when": "Last Friday of the month",
        "review_lead": "The most consequential European architecture theme of the month, from all six perspectives.",
        "review_contents": "Editorial, one page per perspective, a cross architecture synthesis and primary sources.",
        "review_none": "The first issue appears at the end of October 2026.",
        "essay_ambiguity": "A reflection or argument, developing a single thought.",
        "paper_chain": "Source, policy, principle, framework, guideline, measure. How decisions flow through an organisation.",
        "paper_grounds": "Architecture practice in complex, changing environments.",
        "prompt_provenance": "For Copilot. Makes architecture decisions traceable: documentation and database schema. Free to use.",
        "source": "Source on GitHub", "back": "Back",
    },
}

WEEK = re.compile(r"_(\d{2})_(\d{2})\.pdf$")


def collect(kind):
    """Return {(yy, ww): {perspective: url}}, newest edition first."""
    spec = EDITIONS[kind]
    by_slug = {slug: p for p, slug in spec["slug"].items()}
    found = {}
    for path in ROOT.glob(spec["glob"]):
        rel = path.relative_to(ROOT)
        perspective = by_slug.get(rel.parts[1])
        match = WEEK.search(path.name)
        if perspective and match:
            found.setdefault(match.groups(), {})[perspective] = "/" + rel.as_posix()
    return dict(sorted(found.items(), reverse=True))


def collect_review():
    """Return {(yy, mm): url}, newest issue first."""
    found = {}
    for path in ROOT.glob(REVIEW_GLOB):
        match = WEEK.search(path.name)
        if match:
            found[match.groups()] = "/" + path.relative_to(ROOT).as_posix()
    return dict(sorted(found.items(), reverse=True))


def month(lang, issue):
    return f"{MONTHS[lang][int(issue[1]) - 1]} 20{issue[0]}"


OBSERVATION = re.compile(r"^(CENTRALE OBSERVATIE|CENTRAL OBSERVATION)$")
SELECTION = re.compile(r"^(WEEKSELECTIE|WEEKLY SELECTION|SELECTION)$")


@functools.lru_cache(maxsize=None)
def read_report(url):
    """Return (observation, [(signal, source), ...]) from a report PDF, or (None, [])."""
    if pypdf is None:
        return None, []
    try:
        lines = [l.strip() for l in pypdf.PdfReader(ROOT / url.lstrip("/")).pages[0].extract_text().splitlines()]
    except Exception:
        return None, []
    observation, signals = [], []
    for i, line in enumerate(lines):
        if OBSERVATION.match(line):
            for nxt in lines[i + 1:]:
                if SELECTION.match(nxt):
                    break
                observation.append(nxt)
        if re.fullmatch(r"[1-9]", line) and i + 2 < len(lines) and " · " in lines[i + 2]:
            signals.append((lines[i + 1], lines[i + 2]))
    return (" ".join(observation) or None), signals


def label(edition):
    return f"{edition[0]}-{edition[1]}"


def e(text):
    return html.escape(text, quote=True)


def tile(href, title, text="", where="", cls="tile", status="", extra=""):
    parts = [f'        <a class="{cls}" href="{e(href)}">']
    if status:
        parts.append(f'          <span class="status status--live">{e(status)}</span>')
    parts.append(f"          <h3>{e(title)}</h3>")
    if text:
        parts.append(f"          <p>{e(text)}</p>")
    if extra:
        parts.append(extra)
    if where:
        parts.append(f'          <p class="where">{e(where)}</p>')
    parts.append("        </a>")
    return "\n".join(parts)


def section(heading, body, anchor="", note=""):
    ident = f' id="{anchor}"' if anchor else ""
    lines = [f'  <section class="section"{ident}>', '    <div class="wrap">', f"      <h2>{e(heading)}</h2>"]
    if note:
        lines.append(f'      <p class="note">{e(note)}</p>')
    lines += [body, "    </div>", "  </section>"]
    return "\n".join(lines)


def tiles(items):
    return '      <div class="tiles">\n' + "\n".join(items) + "\n      </div>"


def page(lang, path, title, lead, main, back):
    t = TEXT[lang]
    other = "en" if lang == "nl" else "nl"
    here = f'<span aria-current="true" lang="{lang}">{lang.upper()}</span>'
    there = f'<a href="/{other}/{path}" hreflang="{other}" lang="{other}">{other.upper()}</a>'
    nav = f"{here}\n        {there}" if lang == "nl" else f"{there}\n        {here}"
    crumb_html = f'\n    <p class="crumb"><a href="{back}">{e(t["back"])}</a></p>'
    full = f"ClaritasZ · {title}"
    url = f"https://publications.claritasz.com/{lang}/{path}"
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full)}</title>
<meta name="description" content="{e(lead)}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="nl" href="https://publications.claritasz.com/nl/{path}">
<link rel="alternate" hreflang="en" href="https://publications.claritasz.com/en/{path}">
<link rel="icon" href="{BRAND}/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{BRAND}/brand.css">
<link rel="stylesheet" href="{BRAND}/site.css">
<meta property="og:title" content="{e(full)}">
<meta property="og:description" content="{e(lead)}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="{t["locale"]}">
</head>
<body>

<header class="hero">
  <div class="wrap">
    <div class="top">
      <a class="logo" href="{BRAND}/{lang}/"><img src="{BRAND}/claritasz-wordmark.svg" alt="ClaritasZ"></a>
      <nav class="lang" aria-label="{t["lang_label"]}">
        {nav}
      </nav>
    </div>{crumb_html}
    <h1>{e(title)}</h1>
    <p>{e(lead)}</p>
  </div>
</header>

<main>
{main}
</main>

<footer>
  <div class="wrap">
    <p><span class="tagline">ClaritasZ</span> · Consistent in design. Powered by logic.</p>
    <p><a href="https://github.com/ClaritasZ/Publications" target="_blank" rel="noopener">{e(t["source"])}</a></p>
  </div>
</footer>

</body>
</html>
"""


def edition_page(lang, kind, editions):
    t = TEXT[lang]
    names = EDITIONS[kind]["name"]
    if not editions:
        main = section(t["latest"], f'      <p class="note">{e(t["none"])}</p>')
    else:
        (latest, files), *earlier = editions.items()
        items = [tile(files[p], names[p], read_report(files[p])[0] or "", f"PDF · {label(latest)}", cls="tile tile--domain")
                 for p in PERSPECTIVES if p in files]
        main = section(f'{t["edition"]} {label(latest)}', tiles(items))
        if earlier:
            rows = []
            for edition, files in earlier:
                short = EDITIONS[kind]["short"]
                links = " · ".join(f'<a href="{e(files[p])}" title="{e(names[p])}">{e(short[p])}</a>'
                                   for p in PERSPECTIVES if p in files)
                rows.append(f'        <li><span class="edition">{label(edition)}</span> {links}</li>')
            main += "\n" + section(t["earlier"], '      <ul class="editions">\n' + "\n".join(rows) + "\n      </ul>")
    return page(lang, f"reports/{kind}/", t[f"{kind}_title"], t[f"{kind}_lead"], main, back=f"/{lang}/")


def review_page(lang, issues):
    t = TEXT[lang]
    if not issues:
        main = section(t["latest"], f'      <p class="note">{e(t["review_none"])}</p>')
    else:
        (latest, url), *earlier = issues.items()
        main = section(f'{t["issue"]} {month(lang, latest)}',
                       tiles([tile(url, f'{t["review_title"]} · {month(lang, latest)}', t["review_contents"],
                                   f"PDF · {label(latest)}", cls="tile tile--domain")]))
        if earlier:
            rows = [f'        <li><span class="edition">{label(issue)}</span> <a href="{e(url)}">{e(month(lang, issue))}</a></li>'
                    for issue, url in earlier]
            main += "\n" + section(t["earlier_issues"], '      <ul class="editions">\n' + "\n".join(rows) + "\n      </ul>")
    return page(lang, "reports/review/", t["review_title"], t["review_lead"], main, back=f"/{lang}/")


def signal_list(editions):
    """The latest edition's signals, read from its first readable report."""
    if not editions:
        return ""
    files = next(iter(editions.values()))
    for p in PERSPECTIVES:
        if p in files:
            signals = read_report(files[p])[1]
            if signals:
                items = "\n".join(f"            <li>{e(title)}</li>" for title, _ in signals)
                return f'          <ul class="signals">\n{items}\n          </ul>'
    return ""


def index_page(lang, all_editions, issues):
    t = TEXT[lang]
    reports = []
    for kind in ("nl", "eu"):
        editions = all_editions[kind]
        where = f'{t[f"{kind}_when"]} · {t["edition"]} {label(next(iter(editions)))}' if editions else t["none"]
        reports.append(tile(f"/{lang}/reports/{kind}/", t[f"{kind}_title"], t[f"{kind}_lead"], where,
                            cls="tile tile--domain", status=t["weekly"], extra=signal_list(editions)))
    where = f'{t["review_when"]} · {month(lang, next(iter(issues)))}' if issues else t["review_none"]
    reports.append(tile(f"/{lang}/reports/review/", t["review_title"], t["review_lead"], where,
                        cls="tile tile--domain", status=t["monthly"]))
    main = "\n".join([
        section(t["reports"], tiles(reports), "reports"),
        section(t["essays"], tiles([tile("/essays/ClaritasZ_Ambiguity_Is_the_Attack_Surface_v1_0.pdf",
                                         "Ambiguity Is the Attack Surface", t["essay_ambiguity"], "PDF · 1.0")]), "essays"),
        section(t["papers"], tiles([tile("/papers/the-governance-chain.pdf", "The Governance Chain", t["paper_chain"], "PDF"),
                                    tile("/papers/explicit-grounds.pdf", "Explicit Grounds", t["paper_grounds"], "PDF")]), "papers"),
        section(t["prompts"], tiles([tile("/prompts/provenance-framework-v1.0.zip", "Provenance Framework",
                                          t["prompt_provenance"], "ZIP · 1.0")]), "prompts"),
    ])
    return page(lang, "", t["title"], t["lead"], main, back=f"{BRAND}/{lang}/")


def write(rel, content):
    target = ROOT / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def main():
    all_editions = {kind: collect(kind) for kind in EDITIONS}
    issues = collect_review()
    for lang in TEXT:
        write(f"{lang}/index.html", index_page(lang, all_editions, issues))
        write(f"{lang}/reports/review/index.html", review_page(lang, issues))
        for kind, editions in all_editions.items():
            write(f"{lang}/reports/{kind}/index.html", edition_page(lang, kind, editions))
    for kind, editions in all_editions.items():
        print(f"{kind}: {len(editions)} edition(s)" + (f", latest {label(next(iter(editions)))}" if editions else ""))
    print(f"review: {len(issues)} issue(s)" + (f", latest {label(next(iter(issues)))}" if issues else ""))


if __name__ == "__main__":
    main()
