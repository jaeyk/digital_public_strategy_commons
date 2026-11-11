"""Run every model and write its report to results/.

    python -m models.run_all            # full runs
    python -m models.run_all --quick    # fewer Monte Carlo trials, for fast checks
"""

from __future__ import annotations

import argparse

from models.capacity_portfolio import run as capacity_portfolio
from models.diffusion import run as diffusion
from models.turnover import run as turnover
from models.vendor_capture import run as vendor_capture


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--quick", action="store_true", help="use 10 trials instead of the defaults")
    args = parser.parse_args(argv)
    trials = ["--trials", "10"] if args.quick else []
    capacity_portfolio.main(trials)
    vendor_capture.main(trials)
    turnover.main([])
    diffusion.main(trials)


if __name__ == "__main__":
    main()
