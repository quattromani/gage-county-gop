# Voter card recheck, October 26, 2026

## Scope and sources

Reviewed the active Gage County GOP card against Local Civic Reference commit `d559ce36c981b4d4df9bcc085fc7871be563f62f`, including its county/state ballot evidence, six judicial retention questions, and four user-approved VIP affiliation updates. Gage County records control local roster and ballot coverage; VIP supplements affiliation evidence. The historical `gage-gop-vote` Sites checkout is retired and was not changed.

The current card snapshot references upstream commit `d16ac31112d285fe415d2d96e56df00c08a93c44`, records reviewed August 12, county filings through August 3, and state filings through July 15. It has 80 listings, 79 distinct candidates, and 47 office records.

## Candidate changes needed

The same documented-Republican/current-general-election inclusion rule applied to current upstream data produces 83 listings, 82 distinct candidates, and 49 office records. No existing listing needs removal. Additions are:

| Candidate | Office | Evidence and ballot treatment |
| --- | --- | --- |
| Gene Radar Reedy | Blue Springs mayor | County voter-roll affiliation; petition filing. County sample ballot prints Radar Reedy, while the filing record uses Gene Radar Reedy. Preserve the source distinction. |
| Eric G. Malina | ESU 6, District 5 | Republican affiliation reported by VIP, newly accepted upstream. Preserve that evidence type and source. |
| Anthony M. Landon | Odell Village Board | County voter-roll affiliation; declared write-in. Explicitly label write-in status rather than suggesting the name is preprinted. |

Jeff Bacon, Dan Osborn, and Mark Cohen remain outside the Republican inclusion set because their newly documented affiliations are Nonpartisan. Mary Benes must remain excluded. Max Manuilov's now-confirmed Nonpartisan affiliation does not add him to this card.

## Architecture and wording findings

The importer currently excludes `filingMethod`, affiliation `evidenceType`, and source review dates from its projection. Before refreshing, preserve the fields needed to explain Landon's write-in status and Malina's reported affiliation. Candidate facts must still be maintained upstream, not independently edited in the card repository.

The importer only reads candidacies, so it cannot import the six separate retention questions. The card has no judicial-retention section. If included, keep judges separate from Republican candidates and show the exact retention question and Yes/No meaning. Retention is not a candidate race, and a GOP-branded card must not imply a Yes recommendation or endorsement from inclusion. VIP's six Republican judge labels do not establish a retention recommendation. Use Ricky A. Schreiner, matching the official ballot.

The website footer and both PDF builders hard-code August/July source dates. Refresh those from the updated source metadata. Regenerate and visually check the letter flyer, mobile PDF, and long PNG alongside the web card; the web build merely copies the existing downloads and cannot establish that their contents match refreshed data.

The existing automated inclusion test compares output with the card's own imported snapshot. It does not detect drift from newer upstream records or stale PDF content. A release needs a source-diff review and cross-format roster checks as well as the existing suite.

## Verification and status

`npm run check` passed all 12 tests for the current publication. The Republican inclusion comparison found exactly the three additions above and no removals. This is a completed recheck, not an updated publication. No imported facts, presentation code, PDFs, or published content were refreshed, and no commit, push, or deployment was performed. Existing unrelated `.gitignore` and leadership-overview work were left untouched.

Shared guidance checkpoint: canonical candidate authority and source distinctions are preserved; the findings identify changes needed before a refreshed release. No new global rule is proposed.
