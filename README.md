## sitemap-scripts

Comparing sitemap intersections and differences with python

This repo contains a script (in `curl-redirects.py` to follow all the routes on a site and check that they resolve proper status codes. With CURL, the python script follows and server side redirects all the way through to their fnial destination to make sure that they don't result in 404s.

### How to Use

1. Clone locally

2. Save an xml sitemap to your machine. (I used [http://gatsbyjs.com/sitemap.xml](http://gatsbyjs.com/sitemap.xml))

3. Update the basepath in `curl-redirects.py` to point at a deployed version of your site on a hosting provider like Netlify or Fastly (where redirects are actually setup). Deploy previews like on Gatsby Cloud won't have redirects created so wouldn't work, this means you may have to deploy to a new site to a netlify subdomain.

4. Run `./curl-redirects.py` in your terminal. It will take awhile to run and write output into a txt file

