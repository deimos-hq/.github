## Deimos AI LLC

Deimos AI LLC builds software for the people who run AI agents, so that what an agent does is seen, approved, stoppable and provable ([deimoscore.com](https://www.deimoscore.com/), [press kit](https://www.deimoscore.com/brand/)).
Our site keeps a Record of our claims, each with its status, its source and the date we last checked it ([the Record](https://www.deimoscore.com/record/)).

**Don't trust us, check us** ([security page](https://www.deimoscore.com/security/)): every sentence on this page links to where you can check it.

**UNKNOWN is never rounded up to SAFE** ([assurance case, R1](https://github.com/deimos-hq/wardlatch/blob/main/ASSURANCE_CASE.md)): Wardlatch's first requirement is that a line says SAFE only after a control has shown the check could have seen exposure, and that when it cannot tell, the line says UNKNOWN (could not be tested) and the run does not end with exit code 0 ([exit codes](https://github.com/deimos-hq/wardlatch#reference)).
Several of Wardlatch's published advisories are about falling short of that, and say so in their titles ([Wardlatch's advisories](https://github.com/deimos-hq/wardlatch/security/advisories)).

### Wardlatch: free, on your own computer

[Wardlatch](https://github.com/deimos-hq/wardlatch) is a free, open-source check you run on your own computer, under the [Apache-2.0 licence](https://github.com/deimos-hq/wardlatch/blob/main/LICENSE).
It checks your machine against current incidents, starting with the compromised eMudhra certificate keys: curl, Node.js, Python and each project's own certificate bundle keep their own list of who to trust, and Wardlatch tells you which ones still trust the compromised keys ([README](https://github.com/deimos-hq/wardlatch), [incident list](https://github.com/deimos-hq/wardlatch#incidents)).

```
npx wardlatch@latest
```

Run it from your home folder (`cd ~` first), not from inside a project, and keep the `@latest` ([why, in the README](https://github.com/deimos-hq/wardlatch)).
It needs Node.js 18.17 or later ([package.json](https://github.com/deimos-hq/wardlatch/blob/main/package.json)).
It runs on macOS and Linux, and Windows is not supported yet ([README](https://github.com/deimos-hq/wardlatch)).

Each line it prints starts with one of four answers ([README, Reference](https://github.com/deimos-hq/wardlatch#reference)):

- `SAFE`: a control showed the check could have seen exposure, and it found none ([assurance case, R1](https://github.com/deimos-hq/wardlatch/blob/main/ASSURANCE_CASE.md)).
- `EXPOSED`: it found exposure, and the fix is printed under the line ([README, Reference](https://github.com/deimos-hq/wardlatch#reference)).
- `UNKNOWN`: it could not be tested, and the line says why ([README, Reference](https://github.com/deimos-hq/wardlatch#reference)).
- `REVIEW`: something for you to look at, such as a new workflow file ([README, Reference](https://github.com/deimos-hq/wardlatch#reference)).

It sends no telemetry, results or machine details; its only network traffic is TLS connections to the incident's public test hosts and two control sites (the advisory's own page, and a self-signed test site for containers), and your own container engine ([README, Privacy](https://github.com/deimos-hq/wardlatch#privacy)).
The command changes nothing on your system, and each result comes with the fix for you to apply ([README, Privacy](https://github.com/deimos-hq/wardlatch#privacy)).
A flaw in Wardlatch itself is fixed, released, and then disclosed in a published security advisory ([SECURITY.md](https://github.com/deimos-hq/wardlatch/blob/main/SECURITY.md), [advisories so far](https://github.com/deimos-hq/wardlatch/security/advisories)).

[How it works](https://www.deimoscore.com/wardlatch/) · [Source](https://github.com/deimos-hq/wardlatch) · [npm](https://www.npmjs.com/package/wardlatch) · [Latest release](https://github.com/deimos-hq/wardlatch/releases/latest) · [Changelog](https://github.com/deimos-hq/wardlatch/blob/main/CHANGELOG.md)

### Our other work

**Ratchet** is live: the effect gate for AI agents, so that a retried charge, deploy or email is started at most once ([ratchetgate.com](https://ratchetgate.com/)).
If an agent dies before reporting, the effect is marked indeterminate instead of guessed, and your policy decides what happens next ([ratchetgate.com](https://ratchetgate.com/)).
In a published run on the live service, a script standing in for a runaway agent made 100 concurrent charge attempts against a ceiling of 20 an hour, and the gate let 20 through and denied 80 ([the run](https://ratchetgate.com/notes/what-happens-when-step-five-fails)).
The free plan is 1,000 gated effects a month, on a workspace whose email has been confirmed ([pricing](https://ratchetgate.com/pricing)).
Its source is open under Apache-2.0 ([source](https://github.com/thearchitect0x-glitch/ratchet)).

**Crimp** is an open-source decision gate for AI agents: the agent brings the rule and the facts, never a conclusion ([Crimp](https://www.deimoscore.com/crimp/)).
The rule is sealed before anyone knows the outcome, and when a fact it stood on breaks, the decision withdraws itself ([Crimp](https://www.deimoscore.com/crimp/)).
Its v0.1.0 release is signed, with a Sigstore attestation and a SHA-256 checksum you can check yourself ([release](https://github.com/thearchitect0x-glitch/crimp/releases/tag/v0.1.0), [how to verify](https://www.deimoscore.com/security/)).
Its source is open under Apache-2.0 ([source](https://github.com/thearchitect0x-glitch/crimp)).

**Clockford™** is not released yet ([Clockford](https://www.deimoscore.com/clockford/), [our site's summary](https://www.deimoscore.com/llms.txt)).
Its published outcomes are these: you see every agent you run, live, in one place; nothing that matters happens without your yes; you can stop an agent from your phone; and you keep a record of what happened that you can check for yourself ([outcomes](https://www.deimoscore.com/clockford/)).
It is built for the agents your team already uses, whichever company made them ([Clockford](https://www.deimoscore.com/clockford/), [clockford.com](https://clockford.com/)).
We publish outcomes only, and how it works is withheld until launch ([Clockford](https://www.deimoscore.com/clockford/)).

**Marklode** is live: startup due diligence before the pitch, covering the competitors and who funded them, prior art, the strongest attacks on the idea, and a verdict, in 24 to 72 hours ([marklode.com](https://marklode.com/), [Marklode](https://www.deimoscore.com/marklode/)).
Every source is linked, every finding is checked by a person, and it is not legal, patent or investment advice ([Marklode](https://www.deimoscore.com/marklode/)).
Its census of the public MCP registry counted 156,111 registry entries and 45,156 distinct servers behind them, as of 2026-10-17, from metadata only, with no server contacted ([census](https://www.deimoscore.com/marklode/census/)).

### OpenSSF Best Practices

Three of our projects hold a self-certified OpenSSF Best Practices badge, and on 2026-10-31 each project's page showed the level below ([what the badge is](https://www.bestpractices.dev/en)).

- Ratchet, project 14440: Silver ([bestpractices.dev/projects/14440](https://www.bestpractices.dev/projects/14440)).
- Crimp, project 14613: Silver ([bestpractices.dev/projects/14613](https://www.bestpractices.dev/projects/14613)).
- Wardlatch, project 15757: Silver ([bestpractices.dev/projects/15757](https://www.bestpractices.dev/projects/15757)).

### Report a security issue

For Wardlatch, Ratchet or Crimp, report it privately on the project's repository, where only the maintainers can see it ([Wardlatch](https://github.com/deimos-hq/wardlatch/security/advisories/new), [Ratchet](https://github.com/thearchitect0x-glitch/ratchet/security/advisories/new), [Crimp](https://github.com/thearchitect0x-glitch/crimp/security/advisories/new)).
For Wardlatch you hear back within 72 hours and get a first assessment within 7 days ([SECURITY.md](https://github.com/deimos-hq/wardlatch/blob/main/SECURITY.md)).
For anything else, use the contacts in our [security.txt](https://www.deimoscore.com/.well-known/security.txt), or message Deimos AI LLC on [LinkedIn](https://www.linkedin.com/company/deimoshq/) and we will open a private channel ([policy](https://www.deimoscore.com/security/#report)).
Please do not report a vulnerability in a public issue ([policy](https://www.deimoscore.com/security/#report)).

### Sponsorship (paid support, labelled as such)

You can sponsor Deimos AI LLC through [GitHub Sponsors](https://github.com/sponsors/deimos-hq).
Sponsorship never buys a result: no one can pay for a check to read SAFE or for a product to be left out of one, and no sponsor's name appears next to a result ([the listing](https://github.com/sponsors/deimos-hq)).
Deimos AI LLC is a company, so sponsorship is not a tax-deductible donation ([the listing](https://github.com/sponsors/deimos-hq)).

---

Deimos AI LLC is a Delaware limited liability company in the United States ([legal](https://www.deimoscore.com/legal/)).

[deimoscore.com](https://www.deimoscore.com/) · [X](https://x.com/DeimosAiLLC) · [LinkedIn](https://www.linkedin.com/company/deimoshq/) · [Facebook](https://www.facebook.com/deimosaillc) · [Instagram](https://www.instagram.com/deimosaillc/)
