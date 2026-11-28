#!/usr/bin/env python3
"""Builds the Nowboy Records pages. Run: python3 build.py"""
import pathlib

HERE = pathlib.Path(__file__).parent
NAV = [("index.html", "Shows"), ("artists.html", "Artists"),
       ("merch.html", "Merch"), ("about.html", "About"),
       ("members.html", "Members")]

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
    <a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true"></span>Nowboy Records</a>
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
    <p class="notice">Were you at Southern Nights on 26 November? <a href="https://tally.so/r/8NxpEz" target="_blank" rel="noopener">Tell us how it was &rarr;</a></p>
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

# Signups go straight into the Nowboy Records audience in Mailchimp
# (account nowboyrecords, us1). Nothing goes to Shopify or Grand Hazards.
# The page asks Mailchimp for an answer in the background (JSONP), so
# visitors stay on the page and see Mailchimp's own error messages.
MC_BASE = "https://nowboyrecords.us1.list-manage.com/subscribe"
MC_U = "42f1c02f9e0e5dbaa20bc704c"
MC_ID = "fa8359bae5"

MEMBERS_MAIN = """<main class="members">
  <div class="wrap">
    <div class="members-intro">
      <h1>Nowboy Records Members</h1>
      <p class="standfirst">Free to join. Members hear about shows first, get money off tickets,
        and find out about the best new country, bluegrass and Americana artists before anyone else.</p>
      <ul class="perks">
        <li><strong>Shows first.</strong> New dates and line-ups before we announce them anywhere else.</li>
        <li><strong>New music first.</strong> Find out about upcoming country, bluegrass and Americana artists here first.</li>
        <li><strong>Member discounts.</strong> Money off tickets, plus discounted early-access tickets in a members' presale.</li>
        <li><strong>More on the way.</strong> News, merch and much more coming soon.</li>
      </ul>
    </div>

    <div class="join-card" id="join">
      <div class="join-step">
        <p class="eyebrow">Free membership</p>
        <h2>Join the members list</h2>
        <form class="join-form" id="join-form" method="post" action="@BASE@/post?u=@U@&amp;id=@ID@" target="_self" novalidate>
          <label for="join-name">First name <span class="opt">(optional)</span></label>
          <input id="join-name" type="text" name="FNAME" autocomplete="given-name">
          <label for="join-email">Email</label>
          <input id="join-email" type="email" name="EMAIL" autocomplete="email" required>
          <div aria-hidden="true" style="position:absolute;left:-5000px"><input type="text" name="b_@U@_@ID@" tabindex="-1" value=""></div>
          <p class="join-err" id="join-err" role="alert" hidden></p>
          <button type="submit" class="btn">Become a member</button>
          <p class="small">We'll email you about Nowboy Records shows, artists and member offers.
            No spam, and you can unsubscribe any time.</p>
        </form>
      </div>
      <div class="join-done" hidden tabindex="-1">
        <p class="eyebrow">Welcome in</p>
        <h2 id="join-head">You're a member</h2>
        <p id="join-msg">Thanks for joining. We'll be in touch when there's something worth hearing about.</p>
        <a class="btn" href="index.html">See what's on</a>
      </div>
    </div>
  </div>
</main>

<script>
/* Sends the signup to Mailchimp in the background and shows the answer here.
   If scripts are off, the form posts to Mailchimp's own page in a new tab. */
(function () {
  var form = document.getElementById("join-form"), card = document.getElementById("join"),
      err = document.getElementById("join-err"), btn = form.querySelector("button");
  function fallback() {
    /* Background route didn't answer: send the form to Mailchimp's own page instead. */
    form.target = "_self";
    HTMLFormElement.prototype.submit.call(form);
  }
  function fail(msg) {
    err.textContent = msg; err.hidden = false;
    btn.disabled = false; btn.textContent = "Become a member";
  }
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var email = form.EMAIL.value.trim();
    if (!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(email)) { fail("Please enter a valid email address."); return; }
    err.hidden = true; btn.disabled = true; btn.textContent = "Joining...";
    var cb = "nbJoin" + Date.now(), s = document.createElement("script"), done = false;
    var timer = setTimeout(function () {
      if (done) return; done = true; window[cb] = function () {}; s.remove();
      fallback();
    }, 6000);
    window[cb] = function (r) {
      if (done) return; done = true; clearTimeout(timer); delete window[cb]; s.remove();
      var msg = String(r && r.msg || "").replace(/^\\d+\\s*-\\s*/, "").replace(/<[^>]*>/g, "");
      if (r && r.result === "success") {
        if (/confirm/i.test(msg)) {
          document.getElementById("join-head").textContent = "Check your inbox";
          document.getElementById("join-msg").textContent =
            "Nearly there. We've sent you an email: click the link in it to confirm your membership.";
        }
        card.querySelector(".join-step").hidden = true;
        var d = card.querySelector(".join-done"); d.hidden = false; d.focus();
      } else if (/already subscribed/i.test(msg)) {
        card.querySelector(".join-step").hidden = true;
        document.getElementById("join-msg").textContent = "You're already on the list. Good to have you.";
        var d2 = card.querySelector(".join-done"); d2.hidden = false; d2.focus();
      } else if (/valid|email/i.test(msg)) {
        fail(msg);
      } else {
        fallback();
      }
    };
    var q = "u=@U@&id=@ID@&c=" + cb +
            "&EMAIL=" + encodeURIComponent(email) +
            "&FNAME=" + encodeURIComponent(form.FNAME.value.trim()) +
            "&b_@U@_@ID@=" + encodeURIComponent(form["b_@U@_@ID@"].value);
    s.src = "@BASE@/post-json?" + q;
    s.onerror = function () { if (done) return; done = true; clearTimeout(timer); window[cb] = function () {}; fallback(); };
    document.body.appendChild(s);
  });
})();
</script>
""".replace("@BASE@", MC_BASE).replace("@U@", MC_U).replace("@ID@", MC_ID)

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
    ("members.html", "Members &middot; Nowboy Records",
     "Join Nowboy Records Members for free. Hear about Southern Nights shows first, get member discounts on tickets and discover new country, bluegrass and Americana artists.",
     MEMBERS_MAIN),
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
