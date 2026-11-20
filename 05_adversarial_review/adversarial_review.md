# Project CRH — Adversarial Review

> These are **simulated** reviews written by the same AI system that produced the manuscript, deliberately arguing against it. They are not independent peer review and should not be cited as such. Their value is that every objection below was taken seriously enough either to change the manuscript or to be recorded as an unresolved problem.

## Summary of objections

Severity: **A** = could invalidate the framework as physics; **B** = undermines a specific result or claim; **C** = presentation or scope.

| # | Objection | Sev. | Outcome |
|---|---|---|---|
| T1 | No ultraviolet completion; every realization needs new sub-GeV physics coupled to nucleons | A | **Stands.** Recorded as the most likely point of failure (ms. §6.8) |
| T2 | The even gate is fine-tuned by ≳ 10¹² | A | **Stands.** Stated as Proposition 6; a geometric alternative is noted but not developed |
| T3 | Attractive touch-strength couplings may bind A nuclei to B nuclei | A | **Stands, newly found in this review.** Added to ms. §6.8 with a square-well estimate |
| E1 | Nothing puts a B hand in the room; residents would feel each other's walls | A | **Stands.** Added to ms. §8 |
| E2 | No event rate is predicted, so non-observation cannot falsify | A | **Stands.** Stated in ms. §8.1 |
| M1 | Lemma 1 is close to a tautology | C | Accepted; described as a restatement |
| M2 | Theorem 1's corollary compares forces across different experiments and geometries | B | Partly addressed; caveats stated here |
| M3 | Lemma 2 as first stated was false for polar molecules and ignored pinning | B | **Fixed.** Statement narrowed; scope paragraph added |
| M4 | "Attraction" in Theorem 3 is loosely defined | C | Accepted; precise statement is "force = gradient of W" |
| M5 | The radiation exponent does not match the scaling argument | B | **Stands.** Reported as a 0.1 discrepancy; claim weakened to a range |
| M6 | Proposition 6 does not cover all protection mechanisms | B | Accepted; restricted to linearly realised internal symmetries; sequestering noted |
| T4 | The seed of the instability is classical noise | B | Stands; affects only a logarithm |
| T5 | A background value of the gate field would open the gate everywhere | B | Stands; listed as an assumption |
| T6 | The bimetric loophole undercuts Corollary 1 | B | Stands; identified, not explored |
| T7 | Is any of this new, or is it a symmetron with a sign flipped? | B | See "Novelty" below |
| E3 | The touch threshold is an assumption uncertain by 10× | B | Stands; all results carry the scaling |
| E4 | Constraints from meson decays and colliders were not evaluated | B | Stands; listed as a limitation |
| E5 | The thermal estimate uses free-particle kinetics | C | Stands; spans a 10³–10⁴ range for that reason |
| E6 | The conflict with Mitra & Foot rests on a second-hand reading | B | Stands; flagged wherever the claim appears |
| E7 | The hidden-mass bound is 25 years old | C | Stands; a newer bound could only strengthen Corollary 1 |

Five severity-A objections stand. That is the main result of this review.

---

## Reviewer 1 — mathematical

**M1. Lemma 1 proves very little.** Its content is that a sum of two generally covariant actions has a product symmetry. The step "every observable of sector A is a functional of sector-A fields" is where the conclusion is assumed: it defines observables so that cross-sector coincidences are excluded. A relational quantity such as "the value of a B field where an A field takes a given value" is perfectly well defined mathematically for a given pair of solutions; the lemma only says nothing in the dynamics correlates it with anything. *Assessment:* correct but nearly definitional. It is useful as a way of saying precisely why "co-located and totally non-interacting" is empty, and should not be advertised as a result. The manuscript now calls it a restatement of known structure.

**M2. Theorem 1 is fine; its corollary is looser than it looks.** The proof is two applications of Cauchy–Schwarz with non-negative weights, and the plane-separation hypothesis is what makes the force weights non-negative. Problems arise in use. (a) The quantity $F_{AA}$ in the theorem is the force between *the same two bodies in the same geometry*; the laboratory bound inserted in Corollary 2 comes from different bodies in different geometries, parametrised by a single-Yukawa $(\alpha,\lambda)$. With several mediators of different ranges, the translation is not one-to-one. (b) Charges are taken proportional to nucleon number; composition-dependent couplings change the numbers. (c) The extension "to any unitary theory" via the spectral representation is asserted as an expectation; contact terms and renormalisation of the composite operators were not treated. (d) The conclusion — a lower bound on a B–B force — concerns something no A observer can measure. *Assessment:* the theorem stands; the corollary is an order-of-magnitude argument; its real role is the qualitative selection rule (factorized portals cannot give contact without side effects), and that survives.

**M3. Lemma 2 was wrong as first drafted.** The first version claimed $\int V\,d^3R=0$ for any neutral distributions. For distributions with a dipole moment, $\tilde V(\mathbf q)$ has a direction-dependent limit as $q\to0$ and the integral is only conditionally convergent — the classic shape-dependence of dipolar sums. Tissue is mostly water, a polar molecule. The lemma is saved by orientational averaging (independent random orientations kill the dipole term at first order), and this hypothesis is now in the statement. Separately, a vanishing *mean* energy does not exclude a first-order energy that *varies* with relative position: two commensurate crystals pin each other at first order in the coupling. The manuscript now says so, and restricts the "no force" conclusion to disordered or incommensurate matter. *Assessment:* fixed; and the fix matters for the comparison with Mitra & Foot, whose scenario involves solid fragments (see E6).

**M4. Theorem 3, item 5.** "Directed toward increasing overlap" is not a mathematical statement unless the family of overlap profiles is ordered. For nested slabs it is; for a general displacement, some points gain overlap and others lose it. The rigorous content is: the force is the gradient of $W$, $W$ is monotone in the overlap function, and $W$ vanishes when the bodies are apart, so separated bodies are never repelled and overlapped bodies are bound. Convexity of $W$ *in the slab width* was observed numerically, not proved (convexity in $s$ does not imply it, since $s_L$ is not affine in $L$).

**M5. The scaling law is not established.** The predicted exponent is $-4/3$; the measured one is $-1.46\pm0.03$. Four standard errors is not agreement. The authors' own estimate of the logarithmic correction explains a quarter of the gap. Possible causes not examined: the smooth-step ramp has curvature during the delay; the slab supports several unstable modes at full strength; the down-ramp and up-ramp contributions may have different prefactors that mix over the fitted range; three seeds is a small sample. Only one spatial dimension was simulated. *Assessment:* the qualitative claim — power law, not exponential — is secure (the radiated fraction falls by a factor of about fifty between $\tau=100$ and $\tau=1600$, where an exponential in $\mu\tau$ would be zero to machine precision). The specific exponent is not. The manuscript now states a range. The extrapolation to $\mu\tau\sim10^{9}$ multiplies whatever error there is by seven decades and should be read as "extremely small", nothing more.

**M6. Proposition 6 overreaches.** "No symmetry forbids $c$" is proved only for internal symmetries acting linearly on the gate. Supersymmetric non-renormalisation, conformal symmetry, or locality in an extra dimension are not covered. The last is not exotic: exponentially small couplings between separated branes are natural without any symmetry. *Assessment:* accepted. The proposition is now stated with its hypothesis, and the braneworld alternative is recorded in the manuscript as an undeveloped direction. Note that it was the *reviewer*, not the original construction, that produced the most promising idea for fixing the model — and that it has not been tested.

**Minor.** In Theorem 2 the non-linear stability statement needs $H\ge c>0$ for coercivity; at exactly marginal $H$ stability is provided only by the quartic term. Time-dependent overlaps permit parametric resonance in principle; the manuscript's "slowly varying" proviso is necessary, not decorative.

---

## Reviewer 2 — theoretical physicist

**T1. There is no theory here, only operators.** The operators that do the work have dimension 6, 8 and 12 with scales of 2 GeV, 2 MeV and 56 keV. An effective theory with a cutoff of 56 keV cannot describe a nucleus, a star, or a collider — yet it is being applied to nucleons. The claim "isolation is automatic in vacuum" is a claim about energies far above the cutoff, which is exactly where the effective theory says nothing. What would the completion look like? Light mediators with sizeable couplings to nucleons. Those are constrained, tightly, by rare meson decays, beam dumps, neutron scattering, stellar and supernova cooling, and nucleosynthesis. The product structure buys some suppression (several invisible quanta must be emitted together) but nobody has shown it buys enough. *Assessment:* this is the central weakness. Until someone writes down a completion and runs it through the constraints, the framework is a consistent set of low-energy equations whose realisability in nature is unknown, and — on priors — unlikely.

**T2. The even gate is not a mechanism, it is a tuning.** With the benchmark numbers, loops of the gate field regenerate an always-on contact coupling ten thousand times larger than the one being gated, and a gate mass-squared nearly eighteen orders of magnitude above the one assumed. The authors say this themselves. The consequence should be stated more bluntly than the manuscript does: *the even gate's central virtue, exact isolation below threshold, is a property of the classical equations that the quantum theory does not respect.* The odd gate is natural, but it is not a gate: it is a high-dimension contact term. So the one mechanism that genuinely "switches" is unnatural, and the one that is natural does not switch.

**T3. Mean-field theory hides a disaster (new).** A coupling of $10^{4}G_F$ is weak only on atomic scales. Between two nuclei that can interpenetrate — and nuclei of different sectors can, there being no Coulomb barrier — it produces potentials of hundreds of eV to MeV. The gate's sign is attractive by the authors' own Theorem 3. A square-well estimate gives nucleus–nucleus bound states for interaction ranges below about 16 fm (oxygen) or 260 fm (calcium). Nuclei meet about ten thousand times a second. If *any* inelastic process permits capture, the "gentle touch" welds the two bodies together and releases up to nuclear binding energies. The authors computed none of this originally. *Assessment:* potentially fatal for attractive short-range realizations; the manuscript now reports the estimate and marks the problem open. Capture rates were not computed, so it is not yet a no-go theorem. A repulsive realization would avoid it, but Theorem 3 says a self-triggered scalar gate cannot be repulsive.

**T4. The instability's seed.** A classical field sitting exactly at an unstable point stays there for ever. The simulations seed it with noise of arbitrary amplitude. In the real theory the seed is the quantum state of the gate field, and the onset is a quantum-to-classical transition of the kind studied for tachyonic preheating. The dependence is logarithmic, and the benchmark response time (picoseconds) is so short compared with a touch (milliseconds) that the conclusion is safe; but the "opening delay" numbers in gate units are not predictions.

**T5. Initial conditions for the gate field.** Nothing in the model forces the gate field to be zero cosmologically. A light, feebly coupled scalar generically has a misalignment value. Any background value makes the "closed" state partly open everywhere, giving a permanent contact coupling subject to the thermal-isolation bound. The model needs the background to be zero to high precision and offers no reason why.

**T6. Gravity was not dealt with, it was assumed.** Corollary 1 leans on a single metric. The manuscript itself points out that bimetric gravity decouples the sectors at short range. If so, a co-located twin Earth is not excluded and the "visitor, not resident" conclusion fails. The authors decline to explore this on the grounds that the link field is strongly coupled at short distances — for *long* graviton Compton wavelengths. For $1/m\sim1$ AU their own numbers give a strong-coupling length of 0.1 mm, comfortably below room size. That window deserves analysis and did not get it.

**T7. Novelty.** Strip the vocabulary and the even gate is spontaneous scalarization with the trigger $\rho\to\rho_A\rho_B$; the odd gate is an eight-fermion operator; the positivity bound is Cauchy–Schwarz applied to a relation the dark-matter fifth-force community has used for fifteen years; the co-location lemma is the Stückelberg construction read backwards. Is there a new *idea*? *Assessment:* the honest answer is that the new thing is the question — what would it take for hidden-sector matter to be *felt* — and the bookkeeping that follows. The touch bound, the thermal corollary and the cancellation lemma are small, concrete, checkable statements that do not seem to be in the literature. None is deep. "Partially novel; substantially an assembly of existing mechanisms" is the fair description, and it is the one the final assessment adopts.

**T8. A resident B observer needs a world.** Under shared gravity the co-located twin is a body of 2 % of the density of water held up against a gigapascal. It needs an energy source; the solar system has no room for a hidden star. It must co-rotate with the Earth to within walking speed with nothing to enforce that. Each of these can be evaded by assumption, and the number of assumptions is the objection.

---

## Reviewer 3 — experimental physicist

**E1. Where is the hand?** The model says what happens *if* a dense B body overlaps a person. It gives no reason why one ever would. Worse, it undermines its own premise: a gate tuned so that flesh feels flesh is triggered even more strongly by rock on flesh. If B people lived at "corresponding locations" they would feel our floors and walls, and we would feel theirs, continuously. No such thing is observed. The only consistent reading is that dense B matter is essentially never where dense A matter is — in which case the thought experiment's premise (another observer, at the corresponding place) is what the model excludes.

**E2. What would count against it?** The framework predicts no rate, no location, no preferred time. Every null result is compatible with "no B body was there". The conditional predictions (a pull, with heat, above a size threshold) are sharp, but they are predictions about an event the theory does not predict will happen. As it stands this is not an experimentally falsifiable proposal. The pieces that *are* checkable are checkable on paper: Lemma 2, Theorem 1, and whether an ultraviolet completion exists.

**E3. The touch threshold.** 100 Pa over a square centimetre is plausible but assumed. Receptors respond to strain and strain rate, not to pressure; a body force acting through the tissue is not a filament pressing on the skin, and the mapping between the two was a one-line estimate ($Pa/E$). The literature value actually verified is a clinical filament force, for a very different stimulus. The conclusion "weak-strength is not enough" survives a factor of 100 either way for touch, but note the authors' own remark that the *ear* is five to six orders of magnitude more sensitive: a weak-strength coupling is within two orders of magnitude of being *audible* if a B body straddled the inner ear. The headline no-go is specific to touch.

**E4. Existing laboratory constraints were not used.** A contact coupling of $10^{4}G_F$ between nucleons and light invisible particles would show up in pion, kaon and B-meson decays to invisible final states and in missing-energy searches unless the B particles are heavy or the coupling really is absent in vacuum. The manuscript says "depends on the ultraviolet completion". That is true, and it is also the place where the model would most likely die if anyone looked.

**E5. The thermal estimate.** Free-particle kinetic theory for atoms bound in a liquid; cross-sections in Born approximation in a regime the authors show is non-perturbative for nuclei; an answer that ranges from half a millisecond to two seconds. Order-of-magnitude at best. The qualitative point — force and heat exchange go together, and heat scales as the square — is sound and is a useful discriminator.

**E6. The claim against Mitra & Foot.** The authors assert that a published estimate omits a cancelling term. Their evidence is (i) a general lemma, which is correct, and (ii) their reading of an appendix they accessed through a web rendering summarised by an automated reader. Point (ii) is weak. The published scenario concerns a *solid* fragment at a *boundary between two media*; pinning and surface terms, which the authors concede exist at first order, may be what the original estimate is implicitly about. Until someone reads the paper properly and redoes the calculation, the correct statement is: "the mean-field energy vanishes; whether this contradicts the published estimate is unverified." The manuscript's wording is close to this and should not be strengthened.

**E7. Reproducibility.** The code runs, the checks pass, the figures match the text. But all the simulations test the model against itself. The experiments most worth doing — a 3+1-dimensional evolution, a quantum treatment of the onset, deformable rather than rigid bodies — were not done.

---

## Attempts to falsify that were actually carried out

Tests that could have failed and what happened:

| Test | Could have shown | Result |
|---|---|---|
| Conservation with a prescribed gate (Exp 1a) | Proposition 2's formulas wrong | Passed; second-order convergence |
| Causality (Exp 1c) | Disturbance outside the light cone | Passed to round-off |
| Thresholds by eigen-solver (Exp 2) | Formulas (6.3) wrong | Passed, ≤ 3×10⁻⁵ |
| Sobolev condition vs exact threshold | Sufficient condition inconsistent | Passed |
| Bulk bound, monotonicity (Exp 3) | Theorem 3 wrong | Passed |
| Dynamic force equals static prediction (Exp 4) | Adiabatic force formula wrong | Passed to 5 digits |
| Random search for violations of Theorem 1 (Exp 7) | Counter-example | None in 2×10⁴ trials (one constructed for mixed-sign channels, as expected) |
| Real-space integral for Lemma 2 (Exp 8) | Non-zero mean field | Cancels to ≤ 5×10⁻⁹ |
| **"The event is exponentially silent" (Exp 5)** | — | **Failed.** The first working hypothesis was exponential suppression by the gate's mass gap. A scaling argument made while designing the test predicted a power law instead (exponent −4/3, fixed before the run); the simulation confirmed a power law, with exponent −1.46. The manuscript reports the corrected statement and the residual discrepancy |
| **"After the event the gate field returns to zero" (Exp 4, first version)** | — | **Failed as first formulated.** A remnant of free gate field lingers and decays only as a power of time. The claim was corrected to "the coupling term vanishes identically; a decaying remnant remains" |
| **Lemma 2, first statement** | — | **Failed** for polar molecules; narrowed (M3) |

## What changed in the manuscript because of this review

1. Lemma 2 restated with the orientation-averaging hypothesis; scope paragraph on pinning and surface terms added.
2. New paragraph in §6.8 on cross-sector bound states, with a quantitative criterion (and a new block in Experiment 6).
3. New paragraph in §8 on the tension between isolation and perceptibility for co-resident worlds; energy-source remark.
4. §6.5 now reports the exponent discrepancy explicitly and claims only a range.
5. Proposition 6 restricted to internal symmetries; geometric sequestering recorded as an open direction.
6. Limitations 10–13 added.
7. Abstract and conclusion rewritten to carry the negative findings.

## What was deliberately *not* changed

The instructions for this project warn against modifying a theory endlessly to keep a hypothesis alive. The following repairs were available and were declined because each would be an ad hoc addition without independent motivation:

- adding a second field or symmetry to protect the even gate's zero;
- adding a repulsive short-range core to prevent cross-sector bound states;
- choosing the gate threshold in a narrow window so that hands feel hands but not floors;
- postulating that B bodies are rare, slow and nearby so that R7 holds;
- switching to bimetric gravity solely to rescue a twin Earth.

Each is recorded as an open problem instead.

## Verdict of the simulated panel

- *Mathematics:* the elementary results are correct as now stated. One lemma needed repair; one scaling law is only qualitatively supported.
- *Theory:* a consistent classical effective description exists. As a quantum theory of nature it has three unresolved severity-A problems (completion, tuning, bound states).
- *Experiment:* no observation supports it, none is predicted with a rate, and its own logic makes the motivating scenario (a resident observer at the corresponding place) inconsistent with ordinary isolation.

**Recommendation:** classify as *interesting but incomplete*; do not describe any part as a discovery; the useful residue is the set of negative and structural results.
