> Historical record of the temporary host. Superseded by ../HOSTING.md; do not use its deployment or DNS instructions.

# Gage GOP phone card

This standalone publication renders the canonical election directory and voting calendar. Candidate inclusion matches the existing print/mobile publications: documented Republican affiliations and current general-election candidacies. It does not change the neutral civic website.

## Build and preview

Run `npm run build:gop-card`, then `npm run test:gop-card`. The builder expects the three existing print/mobile artifacts in `output/pdf`; their builders are `scripts/build-gop-flyer.py` and `scripts/build-gop-mobile-card.py`. Source assets and browser code live under `src/publications/gage-gop-2026`.

Serve `output/web/gop-card` with a local HTTP server. The current preview uses http://127.0.0.1:8766/. A localhost address works only on the computer running it and is not a public phone link.

## Publish

Upload the contents of `output/web/gop-card` together to a static HTTPS host, at its root or one stable subdirectory. Relative manifest, download and worker URLs support either placement. Keep the full directory structure. Serve JavaScript and `.mjs` as JavaScript, `.webmanifest` as a web manifest, `.ics` as `text/calendar`, and PDFs/PNGs with their proper media types. Use revalidation for HTML and `sw.js` rather than long immutable caching. Do not rewrite missing asset URLs to HTML.

A normal website page or embedded image alone cannot provide this package's offline installation behavior. A branded subdomain on a static host is suitable if the main site's platform cannot serve the worker and accompanying files. The user selected a separate public site, eventually at vote.gagecountygop.org. Sites project appgprj_6ab84f7354588191b80a0d1ec3d28bf3 is the hosting destination. Its deployment checkout is /Users/maxquattromani/Sites/gage-gop-vote; dist/ is a generated transport copy, never an independent candidate authority. DNS connection remains pending.

On the final HTTPS address, test Safari on an iPhone and Chrome on Android: mark a name, reload, save offline, enable airplane mode, reopen the card and downloads, restore connectivity, and save to the Home Screen. Installed web apps may have separate storage from their originating browser. Browser eviction or clearing storage can remove offline files and marks.

## Behavior and privacy

The card opens at device width, offers section shortcuts, local marks, a marked-only filter, selection limits, explicit offline saving, image/PDF downloads and five calendar files. All selections stay in browser storage; no accounts, tracking or selection transmission are implemented. The host may keep ordinary access logs. Shared links and downloads never contain selected names.

Calendar events are all-day entries; exact deadline times are in descriptions. Imported reminders depend on the receiving calendar application's settings. Users should review imported dates and alerts.

Wallet files are not part of this build. Apple requires signed passes and Google requires an issuer integration. Do not add nonfunctional Wallet buttons.

## Verification · September 26, 2026

Seven automated tests passed (including cross-location offline-cache isolation): canonical inclusion, contest limits, saved-selection restoration, download/manifest/calendar integrity, offline cache success/subpath fallback, and failure reporting. Browser checks confirmed persisted marks, a four-choice attempt limited to three for Freeman, marked-only filtering, clear marks and successful offline cache saving. DOM layout measurements fit 320px and 390px with no horizontal overflow. The in-app browser's pointer automation was unreliable after viewport changes; keyboard interactions verified the controls. Physical iPhone/Android installation and airplane-mode testing remain to be performed after hosting.

Guidance checkpoint: this presentation reuses repository knowledge and preserves source dates, scope and uncertainty. The existing brief records the new phone-use context. No material guidance divergence or new global convention is proposed.

## Hosting handoff

After source changes, rebuild and test here, copy output/web/gop-card into the separate checkout’s dist/ directory, and follow the Sites hosting workflow using its existing .openai/hosting.json project ID. Do not create another Site. Rebuild the image/PDF presentations too when their inputs change. Candidate review and calendar review dates now render directly from canonical records. Offline caches are scoped to the publication URL so saving one hosted copy cannot remove another copy’s cache.

Public deployment succeeded: https://gage-gop-vote.max492493.chatgpt.site. See gage-gop-domain-setup.md for the pending custom-domain DNS records.

## Calendar handoff correction

The phone test exposed that download-only ICS links did not open a native calendar. Replaced the primary all-dates action with an explicitly labeled Apple Calendar subscription using webcal, and individual actions with Google Calendar event templates. ICS downloads remain labeled downloads. Apple subscriptions are read-only calendars; Google opens an event editor and requires confirmation. The HTTPS page updates subscription links to its current origin so the custom domain works after connection. Local previews use the published origin. In-app browser restrictions and device app routing remain platform-dependent; physical phone confirmation is still required. Eight automated checks pass, including event dates, Central timezone, and link semantics. This corrects an interaction promise; no new global design convention is proposed.

## iPhone event preview response fix

Individual dates now offer Apple Calendar links without the download attribute. Live inspection identified application/octet-stream for ICS. Static _headers configuration was ignored by this host, so production now uses a generated Worker response adapter (scripts/build-gop-hosted-worker.mjs), serving the same publication bytes with explicit media types and inline calendar disposition. This is a hosting-specific compatibility decision, not a second data authority. Build it into /Users/maxquattromani/Sites/gage-gop-vote/dist/server after rebuilding the card; retain the hosting manifest without a static field. The adapter embeds the small publication asset set and supports GET/HEAD plus proper 404/405 responses.

Live verification September 26: /calendar/2026-11-03.ics returned HTTP 200, Content-Type text/calendar; charset=utf-8, and Content-Disposition inline; filename="2026-11-03.ics". All six calendar responses were tested locally. Nine publication tests pass. iPhone native preview behavior remains to be confirmed on the user's device; do not claim a verified device handoff from headers alone. Current deployed source b50e0169e852c48e00e78f2a5583c2d19caf32f2, Sites version 4.

## I voted sticker · September 26

The final section reveals an original 1080px square PNG after a voluntary I voted button. A second user tap opens native file sharing; the image is prepared before that tap to retain iPhone user activation. Only the PNG is shared, never reference selections. Cancellation is distinguished from failure and no social-post success is claimed. Saving and opening the image remain available without native file-sharing support. The actual asset and share module join the offline bundle. Source image generator: scripts/build-gop-sticker.py. Browser verification confirmed reveal, 1080px image loading and a ready Share control. Eleven automated checks pass, including file-only share payload, cancellation and unsupported-browser fallback. Actual social-app handoff still depends on device support. No global guidance change is proposed.
