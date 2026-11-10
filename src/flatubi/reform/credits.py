"""Credits kept against the flat tax (phase 1: EITC and CTC).

Pure numpy, so the solver can recompute the credits at a new rate without a
simulation.
"""

from __future__ import annotations

import numpy as np


def ctc_against_tax(ctc, refundable_max, phase_in, liability):
    """Child tax credit applied to a tax liability, with current-law rules.

    Current law (26 USC 24 and 26(a)): the non-refundable part reduces the
    income tax, up to the tax owed. The refundable part (ACTC) is the lesser
    of the refundable maximum and the amount the credit would grow if the tax
    were higher by the earnings phase-in. Here `liability` is the flat tax of
    the tax unit, not the income tax. The total is never above `ctc`.
    """
    ctc = np.asarray(ctc, float)
    liability = np.maximum(np.asarray(liability, float), 0)
    used = np.minimum(ctc, liability)
    could_use = np.minimum(ctc, liability + np.asarray(phase_in, float))
    refundable = np.minimum(np.minimum(refundable_max, ctc), could_use - used)
    return used + np.maximum(refundable, 0)
