# Voter card update, October 26, 2026

## Brief and scope

Refresh the existing GOP publication for voters saving or printing a ballot reference. Preserve the established navy/red candidate design, clear voting limits, noninteractive ovals, offline assets, and source boundaries. Add three documented Republican listings and six separately presented judicial retention questions. Retention uses neutral typography and explanatory Yes/No wording, with no recommended outcome. Preserve the candidate/retention distinction in all formats.

## Changes

- Imported 83 listings for 82 distinct candidates and 49 offices from Local Civic Reference. Additions: Gene Radar Reedy, Eric G. Malina, Anthony M. Landon. No existing candidate removed; Mary Benes excluded.
- Preserved filing methods, affiliation evidence type, and source review dates. Landon is labeled write-in with instructions. Malina's affiliation is identified as reported by VIP.
- Imported the upstream publication-safe retention projection and copy into a separate judicial file, with source hash and upstream revision. Six exact questions, court groupings, Yes/No choices, and official links appear in the web card and both PDFs. Judges are not part of candidate counts or simulated ballot marks.
- Added retention navigation for desktop and phone. Candidate notes occupy a separate row under the name. Existing sticker and calendar behavior remains in place.
- Letter flyer: candidate reference on page 1 and retention questions on page 2, with page counts. The continuous phone PDF and PNG contain both subjects. PDF links include source references.
- Retired hard-coded August/July candidate-source copy in favor of imported review metadata. Binary publication formats are marked binary in `.gitattributes`.

## Upstream correction found during visual review

Blue Springs mayor was incorrectly recorded as two seats/two votes upstream. The archived official general-election sample ballot says vote for one. Corrected the source transcription and canonical output in Local Civic Reference, added a focused assertion, and ran its full release suite successfully. This correction remains uncommitted there. The GOP import records the dirty upstream state honestly. Before publication, commit the correction upstream and refresh GOP import provenance; do not publish a claim that all source changes are in the recorded upstream commit.

The previously identified Rhine/Rinne spelling difference remains unresolved and was not changed by this task.

## Verification

- `npm run check`: 14 passing tests, including exact Republican inclusion set, the three additions, one-vote Blue Springs mayor, Landon write-in status, six separate retention questions, no Mary Benes, no selection controls, navigation/assets, matching downloadable copies, and offline behavior.
- Publication Python builders: validated every included name; 83 candidate ovals; exact six retention questions; letter flyer two pages and continuous mobile PDF one page.
- `scripts/test-gop-artifacts.py`: all candidate names and retention questions agree across PDFs, write-in label present, Mary excluded, retention recommendation disclaimer present, and PNG dimensions match the mobile PDF at 216 dpi. PNG is 1080 x 21315 pixels.
- Visual QA: rendered and inspected both letter pages and the mobile write-in/retention regions. Browser checked at 390px width; no horizontal overflow; retention navigation focuses its heading.
- Local Civic Reference full release suite passed after the one-vote correction.
- `git diff --check` passed with binary artifacts correctly classified.

## Review state

Ready for local user review at port 4174, `/vote-2026/`. No commit, push, or deployment authorized or performed. The user's pre-existing `.gitignore`, leadership-overview script, and leadership PDF were not edited. Shared guidance checkpoint: source authority, separate retention meaning, accessible text, consistent design, and publication/source separation preserved. No material divergence or global guidance proposal.

## Release authorization

The user approved the ordered release on October 26, 2026. The Blue Springs correction was committed and pushed upstream as `c842847`; the GOP import was refreshed afterward to that exact revision with `candidateSourceHasUncommittedChanges: false`. The earlier uncommitted-source warning above describes the review stage and is now resolved. Web and cross-format checks were repeated before the GOP commit. Unrelated leadership-overview work and `.gitignore` remain outside this release.
