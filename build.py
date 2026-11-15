#!/usr/bin/env python3
"""Builds the Nowboy Records pages. Run: python3 build.py"""
import pathlib

HERE = pathlib.Path(__file__).parent
NAV = [("index.html", "Shows"), ("artists.html", "Artists"),
       ("merch.html", "Merch"), ("about.html", "About")]

HEAD = """<title>{title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@300..600&family=Yeseva+One&display=swap">
<link rel="stylesheet" href="site.css">
"""

TOPBAR = """<div class="topbar" id="topbar">
  <div class="wrap">
    <a class="brand" href="index.html">Nowboy Records</a>
    <nav class="nav">{links}</nav>
  </div>
</div>
"""

FOOTER = """<footer>
  <div class="wrap">
    <span>&copy; Nowboy Records &middot; Brighton</span>
    <a href="https://www.instagram.com/nowboyrecords/" target="_blank" rel="noopener">Instagram @nowboyrecords</a>
  </div>
</footer>
"""

SCROLLAWAY = """<script>
/* Top bar slides away as you scroll down and comes back as you scroll up. */
(function () {
  var bar = document.getElementById("topbar"), last = window.scrollY, ticking = false;
  function update() {
    var y = window.scrollY;
    if (y > last + 6 && y > 140) bar.classList.add("is-away");
    else if (y < last - 6) bar.classList.remove("is-away");
    last = y; ticking = false;
  }
  addEventListener("scroll", function () {
    if (!ticking) { ticking = true; requestAnimationFrame(update); }
  }, { passive: true });
})();
</script>
"""


def nav(current):
    return "".join(
        '<a href="%s"%s>%s</a>' % (href, ' aria-current="page"' if href == current else "", label)
        for href, label in NAV)


def page(filename, title, desc, main):
    return HEAD.format(title=title, desc=desc) + TOPBAR.format(links=nav(filename)) + main + FOOTER + SCROLLAWAY


SHOWS_MAIN = """<header class="masthead">
  <div class="wrap">
    <h1 class="sr">Nowboy Records</h1>
    <div class="logo" role="img" aria-label="Nowboy Records, Brighton"></div>
    <p class="standfirst">Country, roots and Americana from the UK's Deep South. Home of Southern Nights, Brighton's country music showcase.</p>
  </div>
</header>

<main class="wrap">
  <div class="head"><h2>Shows</h2><p class="eyebrow" id="count"></p></div>
  <ul class="shows" id="shows"></ul>
</main>

<script>
/* ===== EDIT YOUR SHOWS HERE =====
   One block per show. Put the poster image in the "posters" folder and
   write its file name in poster (leave "" for a plain card).
   Past shows disappear on their own. */
const SHOWS = [
  {
    name: "Southern Nights",
    date: "2026-11-26",
    time: "7:00pm",
    venue: "Alphabet, Brighton",
    poster: "posters/southern-nights-alphabet.jpg",
    tickets: "https://buytickets.at/nowboyrecords/2424887"
  }
];
/* ===== END OF EDITING ===== */

const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const today = new Date(); today.setHours(0, 0, 0, 0);
const fmt = d => d.toLocaleDateString("en-GB", { weekday: "short", day: "numeric", month: "long" });

const upcoming = SHOWS
  .filter(s => new Date(s.date + "T23:59:59") >= today)
  .sort((a, b) => a.date.localeCompare(b.date));

document.getElementById("count").textContent =
  upcoming.length === 1 ? "One date" : upcoming.length ? upcoming.length + " dates" : "";

document.getElementById("shows").innerHTML = upcoming.length ? upcoming.map(s => {
  const when = fmt(new Date(s.date + "T12:00:00"));
  const art = s.poster
    ? `<img src="${esc(s.poster)}" alt="${esc(s.name)} poster" loading="lazy">`
    : `<span class="placeholder"><span class="pname">${esc(s.name)}</span><span class="pwhen">${esc(when)}</span></span>`;
  return `<li class="show"><a href="${esc(s.tickets)}" target="_blank" rel="noopener">
    <span class="poster">${art}</span>
    <h3>${esc(s.name)}</h3>
    <p class="when">${esc(when)} &middot; ${esc(s.time)}<br>${esc(s.venue)}</p>
    <p class="go">Get tickets &rarr;</p>
  </a></li>`;
}).join("") : `<li><p class="standfirst">New dates announced soon.</p></li>`;
</script>
"""

SOON = """<main class="soon">
  <div class="wrap">
    <p class="eyebrow">{eyebrow}</p>
    <h1>{heading}</h1>
    <p>{blurb}</p>
    <a class="btn" href="index.html">See what's on</a>
  </div>
</main>
"""

PAGES = [
    ("index.html", "Nowboy Records",
     "Country, roots and Americana from the UK's Deep South. Home of Southern Nights, Brighton's country music showcase.",
     SHOWS_MAIN),
    ("artists.html", "Artists &middot; Nowboy Records",
     "The Nowboy Records roster. Coming soon.",
     SOON.format(eyebrow="Artists", heading="Coming soon",
                 blurb="The roster is being put together. In the meantime, you can catch our artists live at Southern Nights.")),
    ("merch.html", "Merch &middot; Nowboy Records",
     "Nowboy Records merch. Coming soon.",
     SOON.format(eyebrow="Merch", heading="Coming soon",
                 blurb="Shirts, caps and records are on the way. Follow along on Instagram to hear first.")),
    ("about.html", "About &middot; Nowboy Records",
     "About Nowboy Records, a Brighton label for country, roots and Americana.",
     SOON.format(eyebrow="About", heading="Coming soon",
                 blurb="Nowboy Records is a Brighton label for country, roots and Americana. The full story is on its way.")),
]

SKELETON = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<link rel="icon" href="favicon.png">\n{head}</head>\n<body>\n{body}</body>\n</html>\n')

if __name__ == "__main__":
    for filename, title, desc, main in PAGES:
        full = page(filename, title, desc, main)
        head, body = full.split('<div class="topbar"', 1)
        (HERE / filename).write_text(SKELETON.format(head=head, body='<div class="topbar"' + body))
        print("wrote", filename)
    # the body-only copy used for the preview artifact
    (HERE / "body.html").write_text(page("index.html", *PAGES[0][1:]))
