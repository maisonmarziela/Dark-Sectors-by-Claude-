# Project CRH — Research Journal

A chronological record of what was tried, what failed, and what was revised. All entries are from a single working session on **2026-11-10**. Entries are numbered in the order the work happened; no clock times were recorded, so none are given.

Conventions: **H** = hypothesis, **→** = what happened to it. "Planning notes" refers to the reasoning done before any file was written.

---

## Entry 1 — Formulating the problem

Read the brief. Turned the thought experiment into explicit requirements (they became R0–R7 in the manuscript). Two requirements are not in the brief but are implied by it: the effect must reach the threshold of human touch (R6), and a B-sector body must actually be at the observer's location (R7). Decided early that these two would probably be the hard ones, because the other five are properties any ordinary local field theory has for free.

Decided on a repository layout and that every numerical claim in the write-ups should be produced by a script.

Environment: Python 3.14 with numpy/scipy/matplotlib present; sympy missing. Created a project-local virtual environment and installed sympy there rather than touching the system installation. No LaTeX toolchain, so documents are Markdown with LaTeX math.

## Entry 2 — Literature pass and citation verification

Wrote the bibliography from memory first, then built `verify_arxiv.py` to check every arXiv identifier against the arXiv API.

- First run: 67 of 70 verified. The three failures were all my title strings ("nonlinear" vs the papers' "non-linear"), not wrong papers.
- I did not trust my memory of nine identifiers and looked those up by title instead. That was the right call: my remembered number for Ignatiev & Volkas was wrong (the correct one is hep-ph/0005125).
- Added 13 references found during the search phase. Final: **82 of 82 verified.**
- Fetched abstracts for the 20 papers whose specific numbers I use.

Discrepancy caught: a web-search summary gave the positronium bound on kinetic mixing as 5.0 × 10⁻⁸; the paper's own arXiv abstract says 5.8 × 10⁻⁸. Used the abstract.

Not verified: papers older than arXiv (cited from memory and tagged as such); the numerical thresholds in the tactile-physiology literature (two searches found the papers but not the numbers). Consequence: the touch threshold in this project is an explicit assumption, not a citation.

Novelty searches: two targeted searches for a scalar coupled to the product of dark-sector and visible-sector densities. Closest hits were single-sector quadratic couplings and dark-matter-induced scalarization of compact objects. Recorded as "not found", which is weaker than "does not exist".

## Entry 3 — First attempts at a mechanism (mostly failures)

**H1. Kinetic mixing between our photon and theirs gives a contact force.** Estimated the force between a neutral mirror atom and a neutral ordinary atom. First-order mean field between neutral objects looked like it should cancel. → Set aside pending a proper argument (became Lemma 2 in Entry 7).

**H2. Put in a switch function g(x,t) by hand.** → Fails immediately: translation invariance is broken explicitly, so momentum is not conserved. Worked out exactly how much is not conserved; this became Proposition 2 rather than a mechanism.

**H3. A bubble of a different vacuum is the gate.** → A bubble of lower energy grows without limit (violates "no universe-wide collision"); one of higher energy collapses in its light-crossing time, 33 ps for 1 cm. Seven orders of magnitude too brief for a nerve. Rejected.

**H4. A passing lump of some light field is the gate.** → Relativistic lumps have the same lifetime problem. A cloud of heavy slow particles can last, but then the "gate" is a third kind of matter that has to be in the right place by chance. Set aside as unmotivated.

**H5. A new long-range force with a light mediator.** This looked promising for a while: because every nucleon in both bodies contributes, the required product of couplings is tiny (around 10⁻³¹), and the coupling to ordinary matter can sit below existing fifth-force bounds. → Then noticed that the cross force is the geometric mean of the two same-sector forces, so a small A–A force forces a gigantic B–B force. Generalised this to several mediators with Cauchy–Schwarz (Theorem 1). Not excluded, but B matter would be bound by the mediator far more strongly than by chemistry, and the force is long-range, not contact. Demoted to a corollary.

**H6. Gate field coupled linearly to the product of densities.** → Integrating it out gives an always-on interaction proportional to the square of the density product. No switch. Kept as "odd gate"; its importance only became clear in Entry 5.

**H7. Gate field coupled quadratically, with the sign that makes it unstable where both sectors are dense.** → χ = 0 is an exact solution, so isolation is exact; instability gives a threshold. This is the overlap-triggered gate. Worked out the slab and ball thresholds, the variational argument for attraction, and the bulk bound.

Side result from H5 and H7 together: the positivity bound explains *why* the gate has to couple to the product O_A·O_B rather than to each sector separately.

## Entry 4 — How strong is a touch?

First guess in planning notes: 1 mN. Revised to a traction of 100 Pa (10 mN on 1 cm²) after working through tissue stiffness and a 10 µm skin displacement. Carried the uncertainty explicitly.

Computed the coherent mean-field traction for a contact coupling: G·n_A·n_B. For weak-interaction strength at water density: 5 mPa. **So touch needs about 2 × 10⁴ G_F.** This was a surprise — I had expected weak-strength to be marginal, not four orders short.

Noted in passing that the ear's threshold corresponds to a coupling 10⁶–10⁷ times smaller than touch. Recorded as a remark; did not pursue.

## Entry 5 — The even gate is unnatural; the odd gate is protected

Put numbers into the even gate (threshold between air-on-flesh and flesh-on-flesh; gate Compton wavelength 1 mm). Got a portal scale of 2 MeV and a quartic coupling of 10⁻¹³. Then checked loops: closing the gate loop regenerates the ungated contact operator at ~10⁸ G_F if the cutoff is the portal scale. **The thing the gate is supposed to switch off comes back ten thousand times stronger.** No symmetry can prevent it, because χ² is neutral under anything that acts on χ.

Looked for a gate whose zero *is* protected. It needs the product O_A·O_B to carry a charge. Ordinary bulk matter is not charge-conjugation symmetric, so a current–current coupling with a gate that is odd under (χ → −χ) combined with sector-B charge conjugation works: protected, and still coherent in matter. But integrating that gate out gives H6's density-quartic term. So: the mechanism that switches is unnatural, and the natural one does not switch. Recorded as Proposition 6.

General lesson noted: requiring a macroscopic force from a contact operator at ordinary densities drives the operator's scale down to keV–GeV whatever its dimension. No ultraviolet completion attempted.

## Entry 6 — Computational experiments

- **exp0 (symbolic).** 18 checks, all passed on the first run.
- **exp1 (conservation, causality).** Passed first time. Second-order convergence of the mismatch between measured non-conservation and Proposition 2. With a dynamical gate, momentum lost by A+B equals momentum gained by the gate. Outside the gate's light cone the coupled and uncoupled runs agree to round-off. One thing I looked at twice: the momentum transfer in the dynamical-gate run changed by 3 % between the two resolutions. Added a third, finer run; the sequence converges (−0.0788, −0.0764, −0.0758).
- **exp2 (thresholds).** Finite-difference eigen-solver reproduces the analytic thresholds to ≤ 3 × 10⁻⁵. Also computed a Gaussian overlap with no closed form to confirm the Sobolev condition is never contradicted.
- **exp3 (static energy).** All parts of Theorem 3 confirmed. The weakly non-linear estimate I had intended only as a cross-check turned out to be a rigorous lower bound (it is a trial-function energy); the numerics approach it from above, as they must.
- **exp4 (contact event).** Force on A = −4.0000 against a predicted −4; displacement −0.10000. **But the script's own acceptance test failed on the first run:** I had required the gate field near the bodies to return to less than 1 % of its open value after retraction, and it was 1.4 %. The field left behind is free radiation of a massive field, which leaves a region only as a power of time. My requirement was wrong, not the code: what vanishes exactly is the *coupling term*, not the gate field. Rewrote the check to test that (force exactly zero) and to measure the remnant's decay (t^−0.56, against t^−1/2 expected in 1D). Extended the run to see the decay.
  Also noticed: the gate opened well after the threshold was crossed, and abruptly, radiating 8 % of its energy in that run.
- **exp5 (radiation vs switching time).** My first working hypothesis (in planning notes) was that a gapped gate driven slowly radiates exponentially little. While designing the test I realised the gap closes at the threshold, so that cannot be right, and derived a Kibble–Zurek-type estimate: radiated fraction ∝ τ^(−4/3), delay ∝ τ^(1/3). Fixed those predictions before running. Result: −1.46 ± 0.03 and +0.31 ± 0.01. The delay exponent agrees; the energy exponent is steeper than predicted by about 0.1. Estimated the logarithmic correction from the seed: explains ~0.03. **Did not resolve the rest.** Reported as a range.
- **exp6 (numbers).** All phenomenological numbers in one script. My first hand estimate of the thermal coupling (0.1 W cm⁻³ K⁻¹) was too low by a factor of 25; the script gives 2.4 as the incoherent floor and ~10⁴ with nuclear coherence.
- **exp7 (positivity bound).** No violation in 2 × 10⁴ random trials. Constructed the mixed-sign counter-example deliberately to show where the hypothesis matters.
- **exp8 (neutral atoms).** First version crashed (an integration routine does not accept break points with an infinite range); split the integral. Cancellation confirmed to ≤ 5 × 10⁻⁹, and the real-space potential agrees with an independent Fourier evaluation.

Full suite run from scratch twice; all nine scripts pass.

## Entry 7 — A conflict with a published estimate

Had a web reader extract the force estimate from Mitra & Foot (2003), the paper closest to the "touch" question. It reports a **non-zero** mean electrostatic energy for a mirror atom in ordinary matter. That contradicts H1's cancellation.

Worked through it. Made a sign error first (took the energy of a small neutral atom inside an electron cloud to be positive; it is negative) and then found the clean argument: the energy is ∫ρ₂φ₁, and averaged over positions it is ⟨ρ₂⟩∫φ₁ = 0 for neutral matter. The published estimate, as I read the summary of its appendix, keeps the nucleus–nucleus repulsion and drops the electrons' compensating term. Wrote exp8 to check the cancellation numerically, independent of the Fourier argument.

Caution recorded at the time and kept: I have not read the paper's appendix directly, only a rendering summarised by an automated reader. The numerical value quoted from it in that summary (10² eV per unit ε) also did not match what I get from the formula as transcribed (a few eV), which is a further reason not to make detailed claims about it. The manuscript says "as we read it" and asks for independent verification.

## Entry 8 — Arguing against the result

Wrote the adversarial review as three hostile referees. Four things came out of it that changed the manuscript:

1. **Lemma 2 was wrong as stated.** Polar molecules have dipole moments; the integral is then only conditionally convergent. Fixed by adding the orientation-averaging hypothesis. Also added that a vanishing mean does not exclude pinning between commensurate crystals.
2. **Cross-sector bound states.** Realised that a coupling of 10⁴ G_F is not weak between nuclei that can interpenetrate, and that the gate's sign is attractive by my own theorem. My first hand estimate of the pair potential was wrong by a factor of ~8 (I mis-multiplied the open-gate coupling); redid it properly as a square-well criterion and added it to exp6. Bound states for ranges below 16 fm (O–O) or 255 fm (Ca–Ca). Did not compute capture rates. This is a new severity-A problem found late.
3. **The floor problem.** A threshold that lets flesh feel flesh is exceeded by rock on flesh. Co-resident worlds would feel each other's solid structures. This cuts against the premise of the thought experiment itself.
4. **A possibly principled fix for naturalness** — couplings between branes are exponentially small by locality, and the brane separation is a field. Noted; not developed. It would have been easy to bolt this on and claim the problem solved. It is not solved.

Declined to add further ingredients to rescue the hypothesis (listed in the review).

## Entry 9 — Writing up

Wrote the manuscript around the negative and structural results, since those are the most defensible. Rewrote the abstract and conclusion after Entry 8 so that they lead with the problems as well as the construction. Chose the classification "interesting but incomplete".

---

## Failed or abandoned hypotheses (summary)

| Hypothesis | Fate |
|---|---|
| Kinetic mixing produces a mean-field contact force | Vanishes at first order (Lemma 2) |
| A switch can be prescribed | Violates conservation (Prop 2) |
| Vacuum bubble as gate | Runs away or lasts 33 ps |
| Passing lump as gate | Needs a coincident third kind of matter |
| Light mediator gives a touch cheaply | Forces enormous B–B self-force (Thm 1) |
| Even gate gives natural exact isolation | Classically yes; radiatively no (Prop 6) |
| Contact events are exponentially silent | Power law (Exp 5) |
| Gate field returns to zero after the event | Only the coupling does; a remnant decays as a power law (Exp 4) |
| Lemma 2 for all neutral matter | False for oriented dipoles; restricted |
| Mean-field analysis is sufficient | No: bound states possible (§6.8) |

## Unresolved questions

1. Does any ultraviolet completion of a touch-strength product portal survive laboratory and astrophysical constraints?
2. Capture rate into cross-sector nuclear bound states for attractive couplings.
3. Why is the measured radiation exponent −1.46 rather than −4/3? Does it change in three dimensions?
4. Is the reading of Mitra & Foot correct? What is the true leading static force (order ε with pinning, or order ε²)?
5. Can the braneworld (sequestered) version be made quantitative?
6. Bimetric gravity with a graviton Compton wavelength of order 1 AU: is a co-located twin world viable there?
7. Quantum treatment of the gate's onset.
8. Is there any mechanism for rotational locking of gravitationally coupled co-located bodies?
9. A proper psychophysical threshold for a volumetric body force on skin.
10. Has the product-of-densities trigger, or the touch bound, been published somewhere we did not look?
