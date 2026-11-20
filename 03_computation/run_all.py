"""Run every Project CRH experiment in order and summarise pass/fail.

    python run_all.py            # everything (about 6 minutes on a laptop)
    python run_all.py --quick    # skip the two slow dynamical experiments (4 and 5)

Each experiment writes a JSON table (and usually a PNG) to results/ and exits non-zero if one of
its internal consistency checks fails.  The full console log is saved to results/run_all_log.txt.
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPERIMENTS = [
    ("exp0_symbolic_checks.py", "computer-algebra checks of the analytic identities", False),
    ("exp1_conservation_causality.py", "conservation laws and causality with a gated coupling", False),
    ("exp2_gate_threshold.py", "finite-size threshold for the gate to open", False),
    ("exp3_static_gate_energy.py", "open-gate energy, attraction, bulk bound", False),
    ("exp4_contact_event.py", "full dynamical contact event", True),
    ("exp5_adiabatic_radiation.py", "gate radiation versus switching time", True),
    ("exp6_touch_numbers.py", "physical scales: what touch requires", False),
    ("exp7_positivity_bound.py", "Monte-Carlo test of the cross-force bound", False),
    ("exp8_neutral_matter_meanfield.py", "kinetic mixing: neutral-matter mean field cancels", False),
]


def main() -> int:
    quick = "--quick" in sys.argv
    log = []
    summary = []
    for script, desc, slow in EXPERIMENTS:
        if quick and slow:
            summary.append((script, "SKIPPED (--quick)", 0.0))
            continue
        head = f"\n{'=' * 100}\n{script}  -  {desc}\n{'=' * 100}"
        print(head, flush=True)
        t0 = time.perf_counter()
        p = subprocess.run([sys.executable, str(HERE / script)], cwd=HERE, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        dt = time.perf_counter() - t0
        print(p.stdout, end="")
        if p.stderr.strip():
            print(p.stderr, end="")
        log += [head, p.stdout, p.stderr]
        summary.append((script, "PASS" if p.returncode == 0 else f"FAIL (exit {p.returncode})", dt))
    lines = ["", "=" * 100, "SUMMARY", "=" * 100]
    lines += [f"  {s:<38s} {st:<20s} {dt:7.1f} s" for s, st, dt in summary]
    text = "\n".join(lines)
    print(text)
    (HERE / "results" / "run_all_log.txt").write_text("\n".join(log) + text + "\n", encoding="utf-8")
    return 0 if all(st.startswith(("PASS", "SKIPPED")) for _, st, _ in summary) else 1


if __name__ == "__main__":
    raise SystemExit(main())
