# Nowboy Records website

Four pages: Shows (the home page), Artists, Merch and About.
Artists, Merch and About are "coming soon" holding pages for now.

## Adding or changing a show
Open `index.html`, find `EDIT YOUR SHOWS HERE`, and copy the block for each new show.
Put the poster image in `posters/` and write its file name in `poster`.
Past shows disappear on their own.

## Changing the look
All the styling is in `site.css`, shared by every page.

## Rebuilding the pages
`build.py` generates the four pages so they share one header and footer.
If you edit a page by hand, edit the HTML directly and don't re-run it, or
edit `build.py` and run `python3 build.py`.

## Hosting (GitHub Pages)
Settings → Pages → Deploy from branch → `main` / root.
For a domain like nowboyrecords.com: add it under Settings → Pages → Custom domain,
then in your DNS add four A records to 185.199.108.153, .109.153, .110.153, .111.153
and a CNAME `www` → `grandhazards.github.io`.
