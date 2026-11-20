# Project CRH — Literature Review

**Question.** Can two physically distinct "realities" (sets of matter, fields and observers) share one spacetime, be ordinarily unable to interact, and nevertheless undergo a brief, local interaction — and how much of this is already in the literature?

**Short answer.** The *static* half of the hypothesis (two or more mutually invisible sectors on one spacetime) is a mainstream, decades-old idea: it is exactly what "hidden sector", "mirror matter" and "shadow matter" mean. The *transient, localized* half (a coupling that is ordinarily off and switches on in a bounded region) is not a standard model in its own right, but every ingredient needed to build one — environment-dependent couplings, density-triggered scalar condensation, passing lumps of a field that changes local "constants" — also exists. What we did not find is (i) anyone asking what coupling strength a *macroscopic contact force* between two such sectors requires, or (ii) a gate triggered by the *co-presence of matter from both sectors*. Those are the gaps the manuscript works in. Section 11 gives the novelty assessment in detail.

## 0. Method and verification status

- Every arXiv identifier below was checked against the official arXiv metadata API by `verify_arxiv.py`; the log is `arxiv_verification.md` (82 of 82 identifiers match the stated title and author).
- For papers whose *specific numbers* we rely on, the abstract was fetched verbatim (`key_abstracts.md`). These are tagged **[abs]**.
- One paper (Mitra & Foot 2003) was read in full text through a web reader; tagged **[read]**.
- Papers that predate arXiv, and all statements tagged **[mem]**, are cited from the author's memory of the standard literature and were *not* re-checked in this session. They are well-known references, but page numbers and exact figures should be confirmed before any formal use.
- Verification of an identifier establishes that the paper exists and is about what we say. It does not establish that our one-line summary of it is fair. Where the summary matters, we quote the abstract.

Labels used for the status of *ideas*: **Established** (follows from tested theory or is a theorem), **Mainstream-speculative** (a standard, internally consistent proposal without experimental support), **Fringe/contested** (published but not widely accepted), **Constraint** (an experimental or observational bound).

---

## 1. Taxonomy: what "co-located realities" can mean

| Meaning | Where the "other reality" is | Shares our spacetime points? | Status |
|---|---|---|---|
| Hidden / mirror / shadow sector | Same 3+1-dimensional spacetime, different fields | Yes | Mainstream-speculative |
| Many copies of the Standard Model | Same spacetime, *N* copies | Yes | Mainstream-speculative |
| Another brane | Displaced in an extra dimension | Same 4D coordinates, different bulk position | Mainstream-speculative |
| Second metric sector | Same manifold, different metric | Yes, but "same point" becomes dynamical | Mainstream-speculative |
| Everett branches | Same spacetime, different branch of the quantum state | Yes, in a sense | Interpretation of established theory |
| Other "universes" (inflationary, landscape) | Elsewhere or causally disconnected | No | Not relevant here |

Tegmark's hierarchy of "parallel universes" [Tegmark03] is the usual map of the last category; none of his Levels I, II or IV is co-located with us, and Level III (Everett) is discussed in Section 8. The hypothesis under study is the first row, possibly dressed with ideas from the others.

## 2. Hidden sectors and mirror matter

**The idea (Mainstream-speculative).** Lee and Yang's parity paper already raised the possibility of a second set of particles restoring left–right symmetry [LeeYang56, mem]. Kobzarev, Okun and Pomeranchuk [KOP66, mem] showed that such "mirror" particles cannot share our electromagnetic or strong interactions and would communicate with us essentially through gravity; Foot, Lew and Volkas [FLV91, mem] gave the modern gauge-theory formulation. Okun's review [Okun07] is the standard history. Heterotic string theory independently produced "shadow matter" in the hidden E8 factor [KST85, mem]. Reviews of the cosmology and phenomenology: [Berezhiani04], [Foot04], [Foot14], [IgnatievVolkas03].

A mirror world is *precisely* a second reality on our spacetime: it can have its own atoms, chemistry, stars and planets. So the static part of the Co-Located Realities Hypothesis is not new.

**Portals (Established as a classification).** If sector B carries no Standard-Model charges, the lowest-dimension gauge-invariant couplings to our sector are the three renormalizable "portals": photon kinetic mixing ε F·F′ [Holdom86, mem], the Higgs portal |H|²O_B [PattWilczek06], and the neutrino portal. Reviews: [DarkSectors16], [Fabbrichesi20], [Arcadi19]. Additional particle-specific mixings exist, e.g. neutron–mirror-neutron oscillation [BerezhianiBento06], [Berezhiani09], searched for and constrained in [Abel21], [Broussard22].

**Prior work on *mechanical* effects of mirror matter (Fringe/contested).** This is the closest existing literature to the "touch" scenario. Foot and collaborators argued that with kinetic mixing, lumps of mirror matter could hit the Earth and produce anomalous impact events [FootYoon02], form ordinary-atom–mirror-atom bound states [FootMitra02], be present as micrometeorites [FootMitra03], and even rest on or inside ordinary matter, held against gravity by a static force [MitraFoot03, read]. In the last paper the authors estimate that "a mirror matter fragment of size R = 1 cm could remain on the Earth's surface if ε is positive and ε ≳ 10⁻¹⁰" (quotation as rendered by the web reader; check against the published text before reuse). None of these proposals has experimental support, and the manuscript (Sec. 5.3 and Experiment 8) argues that the static-force estimate omits a cancelling term. They do establish that the question "can matter from the other sector push on ours?" has been asked before for *always-on* kinetic mixing.

**Constraints.**
- ε < 5.8 × 10⁻⁸ for a massless mirror photon, from orthopositronium [Vigo20, abs].
- Invisible Higgs decays: BR(H → inv) < 0.107 [ATLAS23, abs].
- A long-range force that couples to both dark and ordinary matter is constrained by equivalence-principle tests and galactic dynamics [Carroll09a, abs], [Carroll09b], [KesdenKamionkowski06], [BovyFarrar09].
- Strongly interacting dark matter would overheat the Earth [Mack07].

## 3. Many co-existing copies of the Standard Model

Several serious proposals populate our spacetime with many mutually non-interacting copies of known physics: 10³² dark sectors motivated by a bound on the number of species [Dvali07], [DvaliRedi09]; "N-naturalness" [ArkaniHamed16]; the twin Higgs [Chacko06]; hidden valleys [StrasslerZurek07]. In all of them the copies share gravity and (at most) feeble portals. They show that "more than two realities" is also standard — and that the copies' *cosmological abundance* must be suppressed, because everything gravitates.

## 4. Braneworlds

In braneworld models our fields are confined to a 3-brane in a higher-dimensional bulk [ADD98], [RS99a], [RS99b]. Other branes are other "realities" at the same four-dimensional coordinates. The *Manyfold universe* [ADDK00, abs] is the most on-point: our brane folded many times within sub-millimetre extra dimensions, so that "nearby matter on other folds can be detected gravitationally as dark matter". Cross-fold forces are mediated by bulk fields and fall off exponentially with the bulk separation when the mediator is massive.

Brane *collisions* have been studied as cosmological events (the ekpyrotic scenario [KOST01]) — global, universe-wide, the opposite of requirement 1 of the thought experiment. We did not find a model of *local, transient* brane contact used as a switch for inter-brane forces; the inter-brane distance is, however, a natural example of a "gate field" in the sense of the manuscript (coupling ∝ e^(−m d(x))). We note this as motivation only and do not develop it.

## 5. Gravity: can the sectors avoid sharing it?

**Established results.**
- *Universality.* A massless spin-2 particle must couple with equal strength to all energy-momentum [Weinberg64, mem]. If there is one graviton, sector B gravitates exactly like sector A.
- *No interacting multi-graviton theories.* Boulanger, Damour, Gualtieri and Henneaux proved that several *massless* gravitons cannot be consistently cross-coupled: "the only possible deformations are given by a sum of individual Einstein–Hilbert actions", also "in the presence of scalar matter" [BDGH01, abs]. Two sectors each with its own massless graviton are therefore totally decoupled — and then nothing identifies points of one with points of the other (manuscript, Lemma 1).
- *Massive gravity is delicate.* Generic non-linear completions of a massive graviton contain a ghost [BoulwareDeser72, mem]. The ghost-free completions are dRGT massive gravity [dRGT11] and Hassan–Rosen bimetric theory [HassanRosen12]; multi-metric generalisations exist [HinterbichlerRosen12]. Reviews: [Hinterbichler12], [deRham14], [SchmidtMayVonStrauss16].

**Two matter sectors are natural in bimetric theory (Mainstream-speculative).** In a bimetric theory, coupling the same matter field to both metrics re-introduces the ghost [Yamashita14], [deRhamHeisenbergRibeiro15, abs]; the consistent option is that each matter species couples to one metric only. That yields exactly "two matter sectors that interact only through gravity" (see also [Luben20]). Earlier analyses in the same spirit: "weakly coupled worlds" [DamourKogan02], link fields between sites in "theory space" [AGS03], and bimetric MOND with "twin matter" [Milgrom10].

**Mirror matter with its own metric.** Berezhiani, Nesti, Pilo and Rossi [BNPR09, abs] built a bigravity model for ordinary plus mirror matter in which the cross-sector potential is Yukawa-modified, so that the two sectors gravitate together at large distances but not at short ones. To obtain a clean Yukawa form they use a Lorentz-breaking massive phase. This is the closest thing in the literature to a *gravitational* isolation mechanism, and it is the loophole to the hidden-mass bounds of Section 10.

**Limits on exotic sign choices.** A bimetric theory in which the second sector feels precisely *opposite* gravitational forces is ruled out by a no-go theorem [HohmannWohlfarth09]; see also [Hossenfelder08] for the kind of construction at issue.

## 6. Couplings that depend on place and time

This is the literature that makes a "gate" physically respectable rather than an arbitrary function.

- **Screening mechanisms (Mainstream-speculative).** In chameleon models a scalar's mass depends on the ambient density [KhouryWeltman04]; in the symmetron model "in regions of sufficiently high matter density, the field is drawn towards φ = 0 where its coupling to matter vanishes ... in regions of low density, however, the symmetry is spontaneously broken, and the field couples to matter" [HinterbichlerKhoury10, abs]. Experimental status: [BurrageSakstein18]. A symmetron is literally a coupling that switches on and off with the environment.
- **Density-triggered condensation (Mainstream-speculative).** The opposite sign — a scalar that condenses *inside* dense matter — is "spontaneous scalarization" [DamourEspositoFarese93, mem], [DamourEspositoFarese96]. Related: an axion "sourced by large dense objects", which thereby "evades fifth force constraints" [HookHuang18, abs]; density-induced vacuum instability [Balkin21, abs]; light scalar dark matter with quadratic couplings, screened or amplified by the Earth [Hees18, abs], [Burrage24, abs].
- **Environment-dependent constants.** [DamourPolyakov94], [OlivePospelov08].
- **Transient, localized changes of couplings.** A passing topological defect of a light field would transiently shift local constants; networks of atomic clocks [DereviankoPospelov14] and magnetometers [GNOME21] search for exactly such bounded, short-lived events.

*Assessment.* A coupling that is zero in ordinary conditions and non-zero in a bounded region for a bounded time is an accepted kind of object, provided the thing that controls it is itself a dynamical field with its own energy. In every example above the trigger is the density of *one* kind of matter, or a free-flying defect. We found no example where the trigger is the *product* of the densities of two otherwise decoupled sectors (two targeted searches, Section 11).

## 7. Vacuum phase transitions

A region in a different vacuum is another way to change couplings locally. The semiclassical theory [Coleman77, mem] implies a dichotomy: a bubble of lower-energy vacuum larger than the critical size expands without limit at nearly the speed of light, and a bubble of higher-energy vacuum collapses in roughly its light-crossing time. The first violates "no universe-wide collision"; the second lasts about 30 picoseconds for a 1 cm region — far too short for a nerve to register. Dense matter can catalyse such bubbles and keep them confined to the dense region [Balkin21], which is again the single-sector analogue of the mechanism studied in the manuscript.

## 8. Quantum mechanics: superselection, decoherence, and branches

- **Superselection (Established).** States that differ in a superselected charge cannot be superposed observably [WWW52, mem]. If A and B were different superselection sectors of one theory in the strict sense, *no* local operator would connect them, and a transient coupling would be impossible by definition. Superselection is thus a model of perfect isolation, not of contact.
- **Decoherence (Established).** Decohered branches of a quantum state are dynamically independent for all practical purposes [Zurek03]. They share spacetime in a loose sense and "do not interact" — but only because quantum mechanics is exactly linear.
- **Cross-branch interaction requires non-linear quantum mechanics (Speculative; constrained).** Weinberg's non-linear extension [Weinberg89, mem] was shown by Polchinski [Polchinski91, mem] to permit either superluminal signalling or communication between branches (the "Everett phone"). Kaplan and Rajendran constructed a causal non-linear framework in which such effects "can be observed in macroscopic systems even in the presence of de-coherence" [KaplanRajendran22, abs]. Dedicated tests have set limits [Polkovnikov23], [Broz23]. A different construction replaces the wavefunction by many interacting classical worlds [HallDeckertWiseman14].

*Relevance.* This is a genuinely different realization of "co-located realities that can touch": the realities are branches, and the gate is a non-linearity of quantum mechanics. It is not the framework developed in the manuscript. It is worth noting that in it the "other reality" is a *copy of ours that diverged*, which trivially solves the problem of why the other observer is standing in the corresponding room — the hardest problem for the field-theory version (manuscript Sec. 2.3).

## 9. Emergent spacetime and the nature of time

- Spacetime connectivity may be built from entanglement [VanRaamsdonk10]. If so, "sharing a spacetime" means sharing an entanglement structure; this is suggestive, but we could extract no usable constraint from it.
- Relational time: in a stationary universe, evolution is correlation with a clock subsystem [PageWootters83, mem]; thermal time ties the flow of time to a state [ConnesRovelli94]. Each sector can serve as the other's clock only if they interact.
- Opposite thermodynamic arrows: Schulman exhibited "a model in which two weakly coupled systems maintain opposite running thermodynamic arrows of time" [Schulman99, abs]. This is the only literature we know that bears directly on co-located systems with different temporal behaviour, and it shows the coexistence is possible only while the coupling stays weak.

## 10. What observations already constrain

| Constraint | Value | Source |
|---|---|---|
| Hidden (gravitating-only) mass inside the Earth | < 3.8 × 10⁻³ M_Earth | [IgnatievVolkas00, abs] |
| Earth-bound dark matter between satellite and lunar orbits | < 4 × 10⁻⁹ M_Earth | [Adler08, abs] |
| Dark matter density at Earth's orbit | < 1.4 × 10⁻¹⁹ g/cm³ | [PitjevPitjeva13, abs] |
| Fraction of dark matter that can be dissipative (able to form disks, stars, planets) | only a subdominant component; a fraction "comparable to the baryonic fraction" is the scenario shown viable | [FanKatzRandallReece13, abs]; later, tighter limits exist but were not checked here |
| Extra relativistic species / mirror-sector temperature | mirror sector must be colder than ours | [BCV01]; number not re-verified |
| New Yukawa force between ordinary bodies | strength ≲ 10⁻³ of gravity at cm–m ranges; far stronger limits at longer range | [Adelberger03], [MurataTanaka15], [Berge21, abs]; the 10⁻³ figure is quoted in [Berge21] for short ranges |
| Composition-dependent accelerations | 10⁻¹³–10⁻¹⁵ level | [Wagner12], [MICROSCOPE22] |
| Photon–mirror-photon mixing | ε < 5.8 × 10⁻⁸ | [Vigo20, abs] |
| Higgs → invisible | BR < 0.107 | [ATLAS23, abs] |

The first row is decisive for the thought experiment under shared gravity: a second planet occupying the same place as the Earth can have at most 0.4 % of its mass.

## 11. Novelty assessment

**Already in the literature (we claim nothing here):**
1. Two or more sectors on one spacetime, mutually invisible, with their own structure — mirror/shadow/hidden sectors (§2, §3).
2. The necessity of shared gravity with one metric, and the bimetric alternative with one matter sector per metric (§5).
3. Environment-dependent, density-triggered and transient couplings (§6).
4. The idea that mirror matter could exert mechanical forces on ordinary matter through kinetic mixing (§2).
5. The geometric-mean relation between a dark-matter–baryon force and the two self-forces, for a single mediator [Carroll09a].

**Apparently not in the literature (the candidate contributions of the manuscript):**
1. A quantitative *touch bound*: the coupling a coherent contact force needs to reach perception, and the resulting statement that weak-strength, Higgs-portal and kinetic-mixing couplings fall short by factors of roughly 10⁴ and more.
2. The observation that the first-order mean-field energy of neutral matter in neutral matter under kinetic mixing vanishes identically, which appears to conflict with the static-force estimate of [MitraFoot03].
3. A general positivity (Cauchy–Schwarz) form of the cross-force bound for any number of same-sign mediators, and its use as a selection rule: strong cross-sector contact without strong fifth forces requires a *non-factorized* ("product") portal.
4. The *overlap-triggered gate*: a scalar that condenses only where matter of both sectors is co-present, with exact classical isolation below a finite-size threshold, an attractive contact force bounded by a bulk formula, and power-law (Kibble–Zurek-type) rather than exponential suppression of radiation.
5. The naturalness obstruction: an even gate's zero cannot be protected by a symmetry; an odd gate can be protected, and reduces to a density-quartic contact term.

**How strong is the novelty claim?** Weak to moderate. The searches performed were: the 82-entry bibliography; two targeted web searches for a scalar coupled to the product of dark- and visible-sector densities (nearest hits: single-sector quadratic couplings [Burrage24], dark-matter-induced scalarization of black holes and neutron stars); one targeted search on static mirror-matter forces. That is far from a systematic review. Items 1–5 are *elementary* consequences of standard field theory; it is entirely possible that some appear in papers we did not find, or are considered too obvious to publish. They should be described as "to our knowledge not previously stated", never as discoveries.

**Overall.** The Co-Located Realities Hypothesis is **partially novel**: equivalent to hidden-sector physics in its static part; a new *combination* of known mechanisms in its transient part; and new mainly in the question it asks (macroscopic contact), which the existing literature has little reason to pose.

---

## References

Status tags: **[arXiv ✓]** identifier, title and author verified through the arXiv API this session; **[abs]** abstract also read; **[read]** full text read through a web reader; **[mem]** cited from memory, not re-verified.

- [Abel21] C. Abel et al. (nEDM collaboration), "A search for neutron to mirror-neutron oscillations", arXiv:2009.11046. [arXiv ✓]
- [ADD98] N. Arkani-Hamed, S. Dimopoulos, G. Dvali, "The hierarchy problem and new dimensions at a millimeter", arXiv:hep-ph/9803315. [arXiv ✓]
- [ADDK00] N. Arkani-Hamed, S. Dimopoulos, G. Dvali, N. Kaloper, "Manyfold universe", arXiv:hep-ph/9911386. [arXiv ✓, abs]
- [Adelberger03] E. G. Adelberger, B. R. Heckel, A. E. Nelson, "Tests of the gravitational inverse-square law", arXiv:hep-ph/0307284. [arXiv ✓]
- [Adler08] S. L. Adler, "Placing direct limits on the mass of earth-bound dark matter", J. Phys. A 41 (2008) 412002, arXiv:0808.0899. [arXiv ✓, abs]
- [AGS03] N. Arkani-Hamed, H. Georgi, M. D. Schwartz, "Effective field theory for massive gravitons and gravity in theory space", arXiv:hep-th/0210184. [arXiv ✓]
- [Arcadi19] G. Arcadi, A. Djouadi, M. Raidal, "Dark matter through the Higgs portal", arXiv:1903.03616. [arXiv ✓]
- [ArkaniHamed16] N. Arkani-Hamed et al., "Nnaturalness", arXiv:1607.06821. [arXiv ✓]
- [ATLAS23] ATLAS Collaboration, "Combination of searches for invisible decays of the Higgs boson using 139 fb⁻¹ ...", Phys. Lett. B 842 (2023) 137963, arXiv:2301.10731. [arXiv ✓, abs]
- [Balkin21] R. Balkin, J. Serra, K. Springmann, S. Stelzl, A. Weiler, "Density induced vacuum instability", arXiv:2105.13354. [arXiv ✓, abs]
- [BCV01] Z. Berezhiani, D. Comelli, F. L. Villante, "The early mirror universe: inflation, baryogenesis, nucleosynthesis and dark matter", arXiv:hep-ph/0008105. [arXiv ✓]
- [BDGH01] N. Boulanger, T. Damour, L. Gualtieri, M. Henneaux, "Inconsistency of interacting, multi-graviton theories", arXiv:hep-th/0007220. [arXiv ✓, abs]
- [Berezhiani04] Z. Berezhiani, "Mirror world and its cosmological consequences", arXiv:hep-ph/0312335. [arXiv ✓]
- [Berezhiani09] Z. Berezhiani, "More about neutron–mirror neutron oscillation", arXiv:0804.2088. [arXiv ✓]
- [BerezhianiBento06] Z. Berezhiani, L. Bento, "Neutron–mirror neutron oscillations: how fast might they be?", arXiv:hep-ph/0507031. [arXiv ✓]
- [Berge21] J. Bergé, M. Pernot-Borràs, J.-P. Uzan, P. Brax et al., "MICROSCOPE's constraint on a short-range fifth force", arXiv:2102.00022. [arXiv ✓, abs]
- [BNPR09] Z. Berezhiani, F. Nesti, L. Pilo, N. Rossi, "Gravity modification with Yukawa-type potential: dark matter and mirror gravity", JHEP 0907:083 (2009), arXiv:0902.0144. [arXiv ✓, abs]
- [BoulwareDeser72] D. G. Boulware, S. Deser, "Can gravitation have a finite range?", Phys. Rev. D 6 (1972) 3368. [mem]
- [BovyFarrar09] J. Bovy, G. R. Farrar, "Connection between a possible fifth force and the direct detection of dark matter", arXiv:0807.3060. [arXiv ✓]
- [Broussard22] L. J. Broussard et al., "Experimental search for neutron to mirror neutron oscillations as an explanation of the neutron lifetime anomaly", arXiv:2111.05543. [arXiv ✓]
- [Broz23] J. Broz, B. You, S. Khan, H. Häffner, D. E. Kaplan, S. Rajendran, "Test of causal non-linear quantum mechanics by Ramsey interferometry on the vibrational mode of a trapped ion", Phys. Rev. Lett. 130 (2023) 200201, arXiv:2206.12976. [arXiv ✓]
- [Burrage24] C. Burrage, B. Elder, Y. Garcia del Castillo, J. Jaeckel, "On the time-dependent density of quadratically coupled dark matter around ordinary matter objects", arXiv:2410.23350. [arXiv ✓, abs]
- [BurrageSakstein18] C. Burrage, J. Sakstein, "Tests of chameleon gravity", arXiv:1709.09071. [arXiv ✓]
- [Carroll09a] S. M. Carroll, S. Mantry, M. J. Ramsey-Musolf, C. W. Stubbs, "Dark-matter-induced weak equivalence principle violation", arXiv:0807.4363. [arXiv ✓, abs]
- [Carroll09b] S. M. Carroll, S. Mantry, M. J. Ramsey-Musolf, "Implications of a scalar dark force for terrestrial experiments", arXiv:0902.4461. [arXiv ✓]
- [Chacko06] Z. Chacko, H.-S. Goh, R. Harnik, "The twin Higgs: natural electroweak breaking from mirror symmetry", arXiv:hep-ph/0506256. [arXiv ✓]
- [Coleman77] S. Coleman, "Fate of the false vacuum: semiclassical theory", Phys. Rev. D 15 (1977) 2929. [mem]
- [ConnesRovelli94] A. Connes, C. Rovelli, "Von Neumann algebra automorphisms and time-thermodynamics relation in general covariant quantum theories", arXiv:gr-qc/9406019. [arXiv ✓]
- [DamourEspositoFarese93] T. Damour, G. Esposito-Farèse, "Nonperturbative strong-field effects in tensor-scalar theories of gravitation", Phys. Rev. Lett. 70 (1993) 2220. [mem]
- [DamourEspositoFarese96] T. Damour, G. Esposito-Farèse, "Tensor-scalar gravity and binary-pulsar experiments", arXiv:gr-qc/9602056. [arXiv ✓]
- [DamourKogan02] T. Damour, I. I. Kogan, "Effective Lagrangians and universality classes of nonlinear bigravity", arXiv:hep-th/0206042. [arXiv ✓]
- [DamourPolyakov94] T. Damour, A. M. Polyakov, "The string dilaton and a least coupling principle", arXiv:hep-th/9401069. [arXiv ✓]
- [DarkSectors16] J. Alexander et al., "Dark Sectors 2016 Workshop: Community Report", arXiv:1608.08632. [arXiv ✓]
- [deRham14] C. de Rham, "Massive gravity", arXiv:1401.4173. [arXiv ✓]
- [deRhamHeisenbergRibeiro15] C. de Rham, L. Heisenberg, R. H. Ribeiro, "On couplings to matter in massive (bi-)gravity", arXiv:1408.1678. [arXiv ✓, abs]
- [DereviankoPospelov14] A. Derevianko, M. Pospelov, "Hunting for topological dark matter with atomic clocks", arXiv:1311.1244. [arXiv ✓]
- [dRGT11] C. de Rham, G. Gabadadze, A. J. Tolley, "Resummation of massive gravity", arXiv:1011.1232. [arXiv ✓]
- [Dvali07] G. Dvali, "Black holes and large N species solution to the hierarchy problem", arXiv:0706.2050. [arXiv ✓]
- [DvaliRedi09] G. Dvali, M. Redi, "Phenomenology of 10³² dark sectors", arXiv:0905.1709. [arXiv ✓]
- [Fabbrichesi20] M. Fabbrichesi, E. Gabrielli, G. Lanfranchi, "The dark photon", arXiv:2005.01515. [arXiv ✓]
- [FanKatzRandallReece13] J. Fan, A. Katz, L. Randall, M. Reece, "Double-disk dark matter", arXiv:1303.1521. [arXiv ✓, abs]
- [FLV91] R. Foot, H. Lew, R. R. Volkas, "A model with fundamental improper spacetime symmetries", Phys. Lett. B 272 (1991) 67. [mem]
- [Foot04] R. Foot, "Mirror matter-type dark matter", Int. J. Mod. Phys. D 13 (2004) 2161, arXiv:astro-ph/0407623. [arXiv ✓]
- [Foot14] R. Foot, "Mirror dark matter: cosmology, galaxy structure and direct detection", arXiv:1401.3965. [arXiv ✓]
- [FootMitra02] R. Foot, S. Mitra, "Ordinary atom–mirror atom bound states: a new window on the mirror world", Phys. Rev. D 66 (2002) 061301, arXiv:hep-ph/0204256. [arXiv ✓]
- [FootMitra03] R. Foot, S. Mitra, "Have mirror micrometeorites been detected?", Phys. Rev. D 68 (2003) 071901, arXiv:hep-ph/0306228. [arXiv ✓]
- [FootYoon02] R. Foot, T. L. Yoon, "Exotic meteoritic phenomena: the Tunguska event and anomalous low altitude fireballs — manifestations of the mirror world?", arXiv:astro-ph/0203152. [arXiv ✓]
- [GNOME21] S. Afach et al., "Search for topological defect dark matter with a global network of optical magnetometers", arXiv:2102.13379. [arXiv ✓]
- [HallDeckertWiseman14] M. J. W. Hall, D.-A. Deckert, H. M. Wiseman, "Quantum phenomena modelled by interactions between many classical worlds", Phys. Rev. X 4 (2014) 041013, arXiv:1402.6144. [arXiv ✓]
- [HassanRosen12] S. F. Hassan, R. A. Rosen, "Bimetric gravity from ghost-free massive gravity", arXiv:1109.3515. [arXiv ✓]
- [Hees18] A. Hees, O. Minazzoli, E. Savalle, Y. V. Stadnik, P. Wolf, "Violation of the equivalence principle from light scalar dark matter", Phys. Rev. D 98 (2018) 064051, arXiv:1807.04512. [arXiv ✓, abs]
- [Hinterbichler12] K. Hinterbichler, "Theoretical aspects of massive gravity", arXiv:1105.3735. [arXiv ✓]
- [HinterbichlerKhoury10] K. Hinterbichler, J. Khoury, "Symmetron fields: screening long-range forces through local symmetry restoration", arXiv:1001.4525. [arXiv ✓, abs]
- [HinterbichlerRosen12] K. Hinterbichler, R. A. Rosen, "Interacting spin-2 fields", arXiv:1203.5783. [arXiv ✓]
- [HohmannWohlfarth09] M. Hohmann, M. N. R. Wohlfarth, "No-go theorem for bimetric gravity with positive and negative mass", Phys. Rev. D 80 (2009) 104011, arXiv:0908.3384. [arXiv ✓]
- [Holdom86] B. Holdom, "Two U(1)'s and ε charge shifts", Phys. Lett. B 166 (1986) 196. [mem]
- [HookHuang18] A. Hook, J. Huang, "Probing axions with neutron star inspirals and other stellar processes", arXiv:1708.08464. [arXiv ✓, abs]
- [Hossenfelder08] S. Hossenfelder, "A bi-metric theory with exchange symmetry", arXiv:0807.2838. [arXiv ✓]
- [IgnatievVolkas00] A. Yu. Ignatiev, R. R. Volkas, "Geophysical constraints on mirror matter within the Earth", Phys. Rev. D 62 (2000) 023508, arXiv:hep-ph/0005125. [arXiv ✓, abs]
- [IgnatievVolkas03] A. Yu. Ignatiev, R. R. Volkas, "Mirror matter", arXiv:hep-ph/0306120. [arXiv ✓]
- [KaplanRajendran22] D. E. Kaplan, S. Rajendran, "A causal framework for non-linear quantum mechanics", arXiv:2106.10576. [arXiv ✓, abs]
- [KesdenKamionkowski06] M. Kesden, M. Kamionkowski, "Galilean equivalence for galactic dark matter", Phys. Rev. Lett. 97 (2006) 131303, arXiv:astro-ph/0606566. [arXiv ✓]
- [KhouryWeltman04] J. Khoury, A. Weltman, "Chameleon fields: awaiting surprises for tests of gravity in space", arXiv:astro-ph/0309300. [arXiv ✓]
- [KOP66] I. Yu. Kobzarev, L. B. Okun, I. Ya. Pomeranchuk, "On the possibility of observing mirror particles", Sov. J. Nucl. Phys. 3 (1966) 837. [mem]
- [KOST01] J. Khoury, B. A. Ovrut, P. J. Steinhardt, N. Turok, "The ekpyrotic universe: colliding branes and the origin of the hot big bang", arXiv:hep-th/0103239. [arXiv ✓]
- [KST85] E. W. Kolb, D. Seckel, M. S. Turner, "The shadow world of superstring theories", Nature 314 (1985) 415. [mem]
- [LeeYang56] T. D. Lee, C. N. Yang, "Question of parity conservation in weak interactions", Phys. Rev. 104 (1956) 254. [mem]
- [Luben20] M. Lüben, A. Schmidt-May, J. Weller, "Physical parameter space of bimetric theory and SN1a constraints", arXiv:2003.03382. [arXiv ✓]
- [Mack07] G. D. Mack, J. F. Beacom, G. Bertone, "Towards closing the window on strongly interacting dark matter: far-reaching constraints from Earth's heat flow", arXiv:0705.4298. [arXiv ✓]
- [MICROSCOPE22] P. Touboul et al., "MICROSCOPE mission: final results of the test of the equivalence principle", Phys. Rev. Lett. 129 (2022) 121102, arXiv:2209.15487. [arXiv ✓]
- [Milgrom10] M. Milgrom, "Matter and twin matter in bimetric MOND", MNRAS 405 (2010) 1129, arXiv:1001.4444. [arXiv ✓]
- [MitraFoot03] S. Mitra, R. Foot, "Detecting dark matter using centrifuging techniques", Phys. Lett. B 558 (2003) 9, arXiv:astro-ph/0301229. [arXiv ✓, read]
- [MurataTanaka15] J. Murata, S. Tanaka, "A review of short-range gravity experiments in the LHC era", arXiv:1408.3588. [arXiv ✓]
- [Okun07] L. B. Okun, "Mirror particles and mirror matter: 50 years of speculation and search", arXiv:hep-ph/0606202. [arXiv ✓]
- [OlivePospelov08] K. A. Olive, M. Pospelov, "Environmental dependence of masses and coupling constants", Phys. Rev. D 77 (2008) 043524, arXiv:0709.3825. [arXiv ✓]
- [PageWootters83] D. N. Page, W. K. Wootters, "Evolution without evolution: dynamics described by stationary observables", Phys. Rev. D 27 (1983) 2885. [mem]
- [PattWilczek06] B. Patt, F. Wilczek, "Higgs-field portal into hidden sectors", arXiv:hep-ph/0605188. [arXiv ✓]
- [PitjevPitjeva13] N. P. Pitjev, E. V. Pitjeva, "Constraints on dark matter in the solar system", arXiv:1306.5534. [arXiv ✓, abs]
- [Polchinski91] J. Polchinski, "Weinberg's nonlinear quantum mechanics and the Einstein–Podolsky–Rosen paradox", Phys. Rev. Lett. 66 (1991) 397. [mem]
- [Polkovnikov23] M. Polkovnikov, A. V. Gramolin, D. E. Kaplan, S. Rajendran, A. O. Sushkov, "Experimental limit on non-linear state-dependent terms in quantum theory", Phys. Rev. Lett. 130 (2023) 040202, arXiv:2204.11875. [arXiv ✓]
- [RS99a] L. Randall, R. Sundrum, "A large mass hierarchy from a small extra dimension", arXiv:hep-ph/9905221. [arXiv ✓]
- [RS99b] L. Randall, R. Sundrum, "An alternative to compactification", arXiv:hep-th/9906064. [arXiv ✓]
- [SchmidtMayVonStrauss16] A. Schmidt-May, M. von Strauss, "Recent developments in bimetric theory", arXiv:1512.00021. [arXiv ✓]
- [Schulman99] L. S. Schulman, "Opposite thermodynamic arrows of time", Phys. Rev. Lett. 83 (1999) 5419, arXiv:cond-mat/9911101. [arXiv ✓, abs]
- [StrasslerZurek07] M. J. Strassler, K. M. Zurek, "Echoes of a hidden valley at hadron colliders", arXiv:hep-ph/0604261. [arXiv ✓]
- [Tegmark03] M. Tegmark, "Parallel universes", arXiv:astro-ph/0302131. [arXiv ✓]
- [VanRaamsdonk10] M. Van Raamsdonk, "Building up spacetime with quantum entanglement", arXiv:1005.3035. [arXiv ✓]
- [Vigo20] C. Vigo, L. Gerchow, B. Radics, M. Raaijmakers, A. Rubbia, P. Crivelli, "New bounds from positronium decays on massless mirror dark photons", Phys. Rev. Lett. 124 (2020) 101803, arXiv:1905.09128. [arXiv ✓, abs]
- [Wagner12] T. A. Wagner, S. Schlamminger, J. H. Gundlach, E. G. Adelberger, "Torsion-balance tests of the weak equivalence principle", arXiv:1207.2442. [arXiv ✓]
- [Weinberg64] S. Weinberg, "Photons and gravitons in S-matrix theory: derivation of charge conservation and equality of gravitational and inertial mass", Phys. Rev. 135 (1964) B1049. [mem]
- [Weinberg89] S. Weinberg, "Testing quantum mechanics", Ann. Phys. 194 (1989) 336. [mem]
- [WWW52] G. C. Wick, A. S. Wightman, E. P. Wigner, "The intrinsic parity of elementary particles", Phys. Rev. 88 (1952) 101. [mem]
- [Yamashita14] Y. Yamashita, A. De Felice, T. Tanaka, "Appearance of Boulware–Deser ghost in bigravity with doubly coupled matter", arXiv:1408.0487. [arXiv ✓]
- [Zurek03] W. H. Zurek, "Decoherence, einselection, and the quantum origins of the classical", arXiv:quant-ph/0105127. [arXiv ✓]

**Tactile-physiology sources** (used only to set the scale of a "touch"; none is an arXiv paper):
- R. S. Johansson, Å. B. Vallbo, "Detection of tactile stimuli. Thresholds of afferent units related to psychophysical thresholds in the human hand", J. Physiol. 297 (1979) 405–422. Existence, title and journal confirmed by web search this session; the numerical thresholds were **not** retrieved, so no number in this project is attributed to it.
- Semmes–Weinstein monofilament convention: the 2.83 filament (≈ 0.07 gram-force ≈ 0.69 mN) is the clinical marker of normal light-touch sensation on the hand (confirmed against several clinical sources by web search; these are clinical conventions, not precision psychophysics).
