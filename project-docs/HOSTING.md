# Hosting

This project moved from a temporary Sites deployment to the owner's public GitHub repository. The canonical project checkout is now `/Users/maxquattromani/Sites/gage-county-gop`.

Repository: https://github.com/quattromani/gage-county-gop

Current intended Pages address: https://quattromani.github.io/gage-county-gop/

The Actions workflow builds and validates the card, then publishes public/. Nothing in the build depends on Sites or its generated Worker. Source and media live in this repository. Historical implementation notes are retained in history/ for context, not as current instructions.

## Connect vote.gagecountygop.org later

1. In this repository's Settings → Pages, set the custom domain to `vote.gagecountygop.org`.
2. At the domain's DNS provider, create a CNAME record named `vote` pointing to `quattromani.github.io` (no path). Inspect and replace an existing vote record only when ready to switch.
3. Wait for GitHub's DNS check and certificate provisioning, then enable Enforce HTTPS.
4. Set `src/publications/gage-gop-2026/publication.json` publicBaseUrl to `https://vote.gagecountygop.org/` and push.
5. Verify the card, downloads, calendar response, image share, offline saving and Home Screen installation on the permanent URL.

Do not use the old `custom-domains.chatgpt.site` CNAME or its verification TXT records. They belonged to the retired hosting setup. The main site, www and mail records need no change.

GitHub's instructions: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site

With the Actions publishing workflow, a CNAME file does not itself configure the custom domain; use the Pages setting. No custom domain is enabled in advance because doing so would redirect the working preview before DNS is ready.

Browser selections, offline caches and Home Screen installs are origin-specific. Visitors should save/install again after changing to the permanent address.

## Verified migration · September 26, 2026

The first GitHub Actions build and deployment passed. Live requests returned HTTP 200 for the sticker, calendar and application module; GitHub Pages served ICS as text/calendar and modules as text/javascript. Calendar links do not request forced downloads. The custom server adapter is retired in history/legacy-sites.

The browser confirmed local marks and the new publication path. The Apple subscription link now constructs webcal directly: changing an HTTPS URL object's protocol to a non-special scheme is ignored by browsers, so the old setter did not reliably preserve the intended scheme.

After explicit approval to retire the old link, the temporary Sites publication was changed to owner-only access and its pending vote.gagecountygop.org binding was removed. No DNS records were changed. GitHub Pages is now the public distribution link. The historical deployment checkout remains locally for recovery only.

Editable GOP code and artwork were removed from the neutral civic checkout after the new repository preserved them. A migration pointer remains there. Historical rendered downloads stay in the old output/ folder to preserve earlier chat file links; new work belongs only here.
