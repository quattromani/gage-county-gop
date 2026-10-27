# Web voter-card style preview

## Brief

Refresh the web card to match the proposed party website while preserving the voter-guide information and behavior. The user requested a local review before publication on October 26, 2026. The user approved committing and publishing the refresh on October 26, 2026, while keeping the custom-domain change pending. The custom-domain connection is a separate pending task awaiting Squarespace email verification.

## Presentation pattern

Use the proposed website's cream paper (#f7f4ed), navy ink (#142d36), Republican red (#ac352c), Georgia display type, Arial body type, G monogram, square buttons, fine rules, and soft neutral panels. Serif headings establish hierarchy; candidate names remain bold sans serif in the shared red, with solid ink ovals. Judicial names use the same red; their retention questions remain informational. Section headings use red rules instead of dark filled bars. Preserve compact phone navigation and the desktop section sidebar. The palette is presentation only; candidate facts, recommendations, vote limits, evidence, and retention wording are unchanged.

CSS is consolidated in src/publications/gage-gop-2026/web/style.css. The build template changes only the masthead and title emphasis. Downloaded PDFs and PNG retain their existing publication designs. JavaScript, calendar generation, download files, and offline behavior remain intact.

## Verification

npm run check passes all 15 release tests, including source roster, recommendation ovals, exact download copies, calendar files and links, offline cache behavior, and sticker sharing. Browser review covers desktop, a 390px phone frame, and a 320px frame; no horizontal content overflow was found at the narrow width. The phone section selector moves focus to the selected heading. Sticker reveal loads the image and enables its share control. Native share-sheet and calendar-app handoffs were not launched during this visual review.

## Local review

Full card: http://localhost:4196/vote-2026/
Phone frame: http://localhost:4192/voter-card-mobile-preview.html

Release uses the existing GitHub Pages address for canonical metadata, social images, and calendar subscriptions. Prepared custom-domain source changes are preserved separately in /Users/maxquattromani/Sites/output/gage-county-gop-domain-change.pending.patch. Domain activation remains pending email verification.

## Download names

Use gage-county-gop-2026-voter-card-mobile.pdf, gage-county-gop-2026-voter-card-letter-size.pdf, and gage-county-gop-2026-voter-card-mobile.png for web delivery. Explicit download attributes match the descriptive PDF filenames. Keep the older candidate-card and print-flyer URLs as aliases for already-shared links and offline copies. Source publication filenames remain stable.

The masthead logo and wordmark link to https://www.gagecountygop.org/ in the same browsing context, providing a return path for visitors arriving from Facebook or a shared link. Keep this a native anchor with the accessible name Gage County Republican Party home and visible keyboard focus.
