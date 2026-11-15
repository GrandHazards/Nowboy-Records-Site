# Nowboy Records website

One page: logo, upcoming gigs as posters, each linking to Ticket Tailor.

## Adding or changing a gig
Open `index.html`, find `EDIT YOUR GIGS HERE`, and copy the block for each new event.
Put the poster image in `posters/` and write its file name in `poster`.
Past gigs hide themselves automatically.

## Hosting (GitHub Pages)
1. New repo on GitHub, e.g. `nowboy-site`, and upload these files.
2. Settings → Pages → Deploy from branch → `main` / root.
3. For a domain like nowboyrecords.com: add it under Settings → Pages → Custom domain,
   then in your DNS add four A records to 185.199.108.153, .109.153, .110.153, .111.153
   and a CNAME `www` → `<your-github-username>.github.io`.
