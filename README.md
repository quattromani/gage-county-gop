# Gage County GOP

A home for Gage County Republican Party projects, publications and reusable artwork. The first project is the 2026 candidate card and its print, mobile and social formats.

- [2026 voter card](https://quattromani.github.io/gage-county-gop/vote-2026/)
- [Letter-size flyer](output/pdf/gage-county-gop-2026-candidate-flyer.pdf)
- [Long phone image](output/pdf/gage-county-gop-2026-mobile-card.png)
- [Continuous phone PDF](output/pdf/gage-county-gop-2026-mobile-card.pdf)
- [Courthouse I voted sticker](src/publications/gage-gop-2026/assets/sticker-courthouse.png)
- [Hosting and future custom domain](project-docs/HOSTING.md)

## Repository structure

- `src/publications/gage-gop-2026/` — editable card code, publication settings, branding, courthouse original and sticker artwork.
- `src/data/elections/2026/` — allowlisted publication snapshot, voting calendar and source provenance.
- `scripts/` — import, build and validation tools.
- `output/pdf/` — approved PDF and long-image deliverables, checked in so publishing needs no design software.
- `public/` — generated website, created by the build and deployed by GitHub Actions.
- `project-docs/` — design briefs, artifact history, provenance and hosting instructions.

Future projects can add their own directories under `src/publications/`, using shared assets when appropriate.

## Build and preview

Node.js 22 or newer is required. There are no npm dependencies.

```sh
npm run check
python3 -m http.server 8767 --directory public
```

The web build uses the committed PDFs and images. It does not need access to another local folder, Sites, or a private service. The default GitHub Pages publication works beneath `/gage-county-gop/vote-2026/`; the same relative paths support a custom domain later.

## Candidate knowledge

The canonical candidate authority remains [Local Civic Reference](https://github.com/quattromani/local-civic-reference). This repository holds a reproducible, dated publication projection: 80 listings, 79 candidates and 47 offices as initially imported. The inclusion policy is documented Republican affiliation and a current general-election candidacy. Inclusion does not imply endorsement or final ballot certification. The GOP branding website is not used as a candidate source.

To refresh from a local checkout of the civic repository:

```sh
node scripts/import-civic-reference.mjs /path/to/local-civic-reference
npm run check
```

Review the snapshot diff and regenerate affected PDFs/images before publishing changed election facts. `provenance.json` records upstream revision and content hashes; the import excludes internal review queues and unrelated candidates. Existing candidate/office identifiers are preserved.

## Print and long-image reproduction

Install Python packages from `requirements-publications.txt`. The print builders currently use macOS system Arial and Arial Narrow fonts; those proprietary font files are not redistributed. Run `python3 scripts/build-gop-flyer.py` and `python3 scripts/build-gop-mobile-card.py`, then render and visually inspect the PDFs. To reproduce the long PNG with Poppler:

```sh
pdftoppm -png -r 216 -singlefile output/pdf/gage-county-gop-2026-mobile-card.pdf output/pdf/gage-county-gop-2026-mobile-card
```

The courthouse sticker is the approved generated artwork; its original reference and exact prompt are retained. Do not run the retired badge generator to replace it.

## Publishing

Push to `main`: GitHub Actions builds, runs checks, and deploys only `public/` to Pages. Pull requests run the same checks without publishing. The custom domain is intentionally not enabled until its DNS can be connected. See `project-docs/HOSTING.md`.

Candidate ovals are visual references only. Native calendar and sharing behavior depends on the visitor's phone/browser; image and PDF downloads remain available.

## Assets and rights

The courthouse reference was supplied by the project owner. The active sticker is an image-generated adaptation, with provenance in `project-docs/sticker-courthouse-prompt.md`. GOP branding assets retain their respective owners' rights. Public repository access is not a blanket license to third-party marks or artwork.
