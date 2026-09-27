# Gage County GOP candidate flyer

## Brief · September 26, 2026

Create a one-page US Letter PDF for Facebook sharing and optional printing. Readers need to locate documented Republican candidates for offices on their own November 2026 ballot. Group names by governmental level and jurisdiction, with clear district labels and voting limits for multi-seat contests. The interpretation is direct, legible, orderly, familiar, portable.

The supplied Cass County flyer is a precedent: dense, emphatic. Preserve its office-to-name hierarchy, but dedicate the page primarily to names instead of a large slogan column. The Gage County GOP website is a branding reference: patriotic, informal. Use its actual GOP logo, red, white, and navy; omit its background imagery to preserve reading space. Candidate information on that website has known errors and MUST NOT be used.

The subject is a structured civic reference, represented literally in type. The audience seeks occasional election reference on phones or paper. People outside these jurisdictions have limited use for this list; do not imply every office appears on every ballot.

## Authority and projection

The generator reads `src/data/elections/2026/election-directory.json` directly. Include only current-general-election candidacies with a documented Republican affiliation and a source. Never copy names into presentation configuration. Primary-history and unresolved-affiliation records are excluded. Preserve names exactly and show ward/district qualifications. The same person may be listed for more than one office.

The user requested only the appeal “Take this with you to vote for Republican Party candidates” and allowed “Provided by” attribution. Use “Provided by Gage County GOP”; no payment, committee-authorization, or endorsement claims. The user's tentative report of Angie Eberspacher's endorsement remains unverified; no mark is printed. The website endorsements page did not name candidates when inspected September 26.

This is a source-dated first edition, not a claim of final ballot certification. Print the county and statewide source cutoffs and tell readers to follow their own ballot's offices and voting limits. Governor is rendered from the candidate record the project actually holds; a running mate is not invented or imported from the branding site. No external candidate records are incorporated.

## Sources outside the candidate model

- Brand and logo: https://www.gagecountygop.org/ (inspected September 26, 2026).
- Logo asset: https://images.squarespace-cdn.com/content/v1/68bdf927f8b06e41342c50ba/dbc31925-8603-478e-b87c-652068af1fa5/Republican-Party-Logo.jpg (downloaded from the displayed website image).
- Election date: https://gagecountyne.gov/election-office/ (November 3, 2026; inspected September 26).

## Reproduction and review

Run `scripts/build-gop-flyer.py` with Python, ReportLab, Pillow and pypdf. It generates the PDF from canonical records and validates the inclusion set, page size, page count, names, and layout bounds. Render with Poppler and inspect before delivery. Platform font files are referenced rather than copied into the repository. This is a specifically requested standalone presentation; it does not change the civic website or its editorial policy.

## Revision: voting reference features

The user requested a small unfilled oval beside every candidate and the five voting-date milestones from the supplied reference image. Preserve the 10-point candidate type and one-page Letter format by shortening the masthead and tightening space between office groups. Ovals are printed reference marks, not interactive ballot fields.

Voting milestones live in `src/data/elections/2026/voting-calendar.json`, separately from candidate data, with the official calendar URL and page provenance. Verified September 26 against the Nebraska Secretary of State's 2026 Election Calendar, pages 9-12. The strip distinguishes registration postmark/online deadlines from receipt of ballot requests and voted early ballots, and specifies Central Time. The PDF links the strip to the calendar. Candidate records still come exclusively from the project.

Closing guidance check: the additions remain derived from structured repository records; no candidate facts were copied from the GOP website and no global guidance change is needed.

## Second design pass: portrait retained

Keep the user's portrait, single-page format, ovals, sentence-case red-band appeal, and five voting milestones. Improve scan continuity by keeping the entire county category together. Pair federal/state with school boards in column one and county with other local districts in column two; retain municipal and township categories in columns three and four. Use a wider candidate face at the existing 10-point size to make candidate emphasis more distinct from office labels. Rebalance category placement and allocate remaining space between office groups; preserve consistent candidate line spacing. Column-specific group padding of 3-10 points brings the four columns to a common lower boundary without splitting categories or shrinking type. Refine voting-date descriptions for short, actionable phrases and increase small supporting text where space permits. A dense one-page reference still requires zooming on a phone; this pass must not claim otherwise.

Second-pass checkpoint: all 80 source-derived listings and 80 ovals retained on one Letter page. Wider candidate type, complete county grouping, and controlled group spacing address the visual review findings. No new global convention is proposed. Phone use still needs zoom; no physical print or device usability test is claimed.

## Mobile card · single-column presentation

Create a separate, continuous portrait card for saving to a phone: a 1080-pixel-wide PNG and a matching custom-height, single-page PDF. Keep the letter-size flyer available. Use a 360-point design width with 24-point margins, 15-point candidate names, clear category transitions, generous office grouping, and empty candidate ovals. Reading order is federal, state, county, schools, cities/villages, township boards, and other local districts, followed by voting dates. All candidates and voting milestones are projected from the same canonical records as the print flyer. Each office label should be complete; unlike the dense print layout, this format has room to spell out village/township boards and school names. No content must be split across pages or columns. This is a separate presentation for phone use, not a change to the canonical facts or the print format.

## Mobile web card

The user approved a phone-width web card with home-screen saving, offline use, selection marks, section shortcuts, calendar files, and existing image/PDF downloads. Build it as a standalone publication under `output/web/gop-card`, sourced from `src/publications/gage-gop-2026/web` and canonical election/calendar records. The neutral civic website and its release workflow remain separate. A public HTTPS host is needed for distribution and phone installation; local preview does not constitute publication. Wallet issuance is a later phase requiring issuer accounts/certificates, so no nonfunctional Wallet controls are shown.

Use semantic, server-rendered HTML for names and provenance, so content and downloads work without JavaScript. Enhance with native checkboxes and local-only selection storage, enforced per-contest voting limits, an optional marked-only view, and service-worker offline saving. Beatrice council wards are separate one-seat contests despite the office-wide seat count. Never transmit selections or put them in share URLs. Explain that browser clearing can remove saved information. Keep a prominent record-review date; display offline confirmation only after assets have been cached successfully. Use a relative manifest, URLs, and worker scope so the package can be deployed below a subpath. Date files use all-day events with exact deadline times in descriptions and an optional day-before reminder. No analytics or external scripts.

## I voted sticker

At the very bottom, let a voter voluntarily reveal an I voted sticker after voting, then save or share the actual PNG. This is a celebratory, occasional phone interaction. Use the existing navy/red/white typography and a familiar circular sticker with stars: recognizable, legible, local, celebratory, restrained. Keep the image square for social posts and readable in a small preview. No vote verification, tracking, candidate selections, automatic posting, or claims of a successfully published social post. Native image sharing depends on the browser and installed apps; retain image saving as a direct fallback. Generate the asset from a reproducible repository script.

## Sticker visual revision

The user rejected the generic ring-and-stars badge and supplied their own Gage County courthouse illustration. Use that artwork as the recognizable local centerpiece, preserving its building geometry, viewpoint, warm stone, slate roof and flag. Pair with expressive, legible I voted lettering and small county/year details. Favor an airy, cohesive illustrated sticker over the former generic seal. Preserve the existing reveal/save/share behavior. Keep the supplied source and generation prompt in the repository; do not regenerate the retired badge over the selected asset.

## Tablet and desktop layouts

Keep the existing single-column phone flow below 740px. Tablet widths use two office columns within each category, grouped dates and a two-part masthead. At 1100px and above, use persistent section navigation beside the reading area, three office columns and three date columns. Preserve federal-to-local category order and row-major reading/keyboard order; never split an office's candidate list across columns. Candidate marks, limits, downloads and sticker actions remain unchanged. Wide screens should shorten scanning and navigation without stretching names across the screen. Check phone, tablet and desktop widths, marked-only filtering and sidebar navigation before publishing.

## Parent project home

Reserve the repository root URL for a small, responsive project index. Link directly to the 2026 voter card in `vote-2026/`, using the existing navy, red and GOP brand. No candidate facts are repeated on the index. Keep calendar subscriptions and previously shared downloads working at their original addresses while new links and offline storage use the project subdirectory.

## Facebook distribution

Use a dedicated 1200 × 630 link-preview image and a separate 1080 × 1080 image for manual photo posts. Both introduce the card instead of compressing the entire candidate list into a thumbnail. Match the existing navy, red, typography and supplied courthouse illustration; keep all essential text inset from image edges. Supply absolute Open Graph image URLs, dimensions and alt text in the card's static HTML so crawlers need no JavaScript. Facebook ultimately controls each placement and its cropping; no image metadata can guarantee every presentation. Preserve the editable social layout and downloadable PNGs in this repository.
