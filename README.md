# Project CRH — Co-Located Realities Hypothesis

An independent theoretical study of one question: **could two physically distinct "realities" share one spacetime, be ordinarily unable to interact, and still exchange a brief, local touch — without breaking established physics?**

**Outcome: interesting but incomplete.** A classical effective field theory that does everything the thought experiment asks can be written down and behaves as claimed under numerical test. As a candidate description of nature it has three unresolved, potentially fatal problems, and no observation supports it. The most durable results are constraints. See [`07_final_assessment/final_assessment.md`](07_final_assessment/final_assessment.md).

> This work was carried out by an AI system in a single session. It has not been reviewed by a physicist. Nothing here is evidence that other realities exist.

## Where to start

| If you want… | Read |
|---|---|
| The story without the mathematics | [`06_plain_english/companion_report.md`](06_plain_english/companion_report.md) |
| The verdict and how confident it is | [`07_final_assessment/final_assessment.md`](07_final_assessment/final_assessment.md) |
| The mathematics | [`02_manuscript/manuscript.md`](02_manuscript/manuscript.md) |
| The strongest objections | [`05_adversarial_review/adversarial_review.md`](05_adversarial_review/adversarial_review.md) |
| What already exists in the literature | [`01_literature_review/literature_review.md`](01_literature_review/literature_review.md) |
| What was tried and what failed | [`04_research_journal/journal.md`](04_research_journal/journal.md) |
| To rerun the numerics | [`03_computation/README.md`](03_computation/README.md) |
| To continue the work | [`RESEARCH_STATE.md`](RESEARCH_STATE.md) |

## Main findings

1. **"Same place" requires a shared field.** Two sectors with nothing in common — not even gravity — are not meaningfully co-located (Lemma 1).
2. **With ordinary gravity, the other world weighs.** A world sharing the Earth's location can hold at most 0.4 % of the Earth's mass: no twin Earth (Corollary 1, using a published geophysical bound).
3. **A switch cannot be imposed.** A coupling turned on by hand violates energy–momentum conservation by a computable amount; the switch must be a dynamical "gate" field (Proposition 2, confirmed numerically).
4. **A positivity bound.** For forces carried by mediators that couple to each sector separately, F_AB² ≤ F_AA·F_BB. Contact-like cross-sector forces without side effects need a *product portal* (Theorem 1).
5. **The touch bound.** Feeling a hidden-sector object requires an effective coupling about 2 × 10⁴ times the Fermi constant. Weak-scale exchange, the Higgs portal and photon kinetic mixing fall short by four or more orders of magnitude (Proposition 4, Lemma 2).
6. **Force comes with heat.** A coupling of touch strength would bring the overlapping bodies to a common temperature within seconds or less (Proposition 5).
7. **An overlap-triggered gate works on paper.** Exactly isolated below a finite-size threshold, a bounded attractive force above it, nothing left afterwards, power-law-small radiation (Theorems 2–3, Experiments 2–5).
8. **Why it probably is not real.** The gate is fine-tuned by ≳ 10¹²; every version needs new sub-GeV physics that has not been exhibited; the attraction may bind nuclei of the two sectors together; and a gate that lets a hand feel a hand would let it feel the floor.

## Repository layout

```
project-crh/
├── README.md                      this file
├── RESEARCH_STATE.md              checkpoint: done / verified / failed / open / next steps
├── 01_literature_review/
│   ├── literature_review.md       referenced assessment and novelty analysis
│   ├── verify_arxiv.py            checks every arXiv id against the arXiv API
│   ├── arxiv_verification.md      the verification log (82 / 82)
│   ├── arxiv_verification.json
│   ├── fetch_abstracts.py         fetches abstracts of the papers whose numbers are used
│   └── key_abstracts.md           those abstracts, verbatim
├── 02_manuscript/
│   └── manuscript.md              the research paper (Markdown with LaTeX math)
├── 03_computation/
│   ├── README.md                  how to run; what each experiment tests
│   ├── requirements.txt
│   ├── run_all.py                 runs everything (≈ 6 min)
│   ├── crh_common.py
│   ├── exp0 … exp8 *.py           nine experiments
│   └── results/                   JSON tables, figures, full run log
├── 04_research_journal/journal.md
├── 05_adversarial_review/adversarial_review.md
├── 06_plain_english/companion_report.md
└── 07_final_assessment/final_assessment.md
```

## Reproducing

```
cd project-crh
python -m venv .venv
.venv\Scripts\python -m pip install -r 03_computation\requirements.txt
cd 03_computation
..\.venv\Scripts\python run_all.py
```

To re-check the bibliography (needs internet access to arxiv.org):

```
.venv\Scripts\python 01_literature_review\verify_arxiv.py
```

## What "verified" means here

- **Citations:** each arXiv identifier exists and matches the stated title and author (automatic). Specific numbers were checked against abstracts. Pre-arXiv references are from memory and flagged.
- **Mathematics:** hand derivation, plus computer algebra (18 checks), plus numerical experiments with convergence tests. All pass. This shows the derivations are free of the errors those tests can catch.
- **Physics:** not verified by anyone. In particular the novelty claims rest on a limited search, and one claimed disagreement with a published paper rests on our own reading of it.

Markdown files use `$…$` LaTeX math; view them in an editor or site that renders it (VS Code, GitHub, Obsidian).
