"""Phase 1 transition rules (spec Section 2.5, `phase1`)."""

from __future__ import annotations

from policyengine_us.model_api import max_, where


def offset_ubi(person, period, amount, offset_applies):
    """Social Security offset, not cut.

    Spec 2.5 phase1: each beneficiary gets max(social_security, ubi_adult).
    Social Security stays at current law. The UBI for a person who gets it
    as an adult is cut by that person's Social Security, down to zero. So
    Social Security + UBI = max(social_security, ubi_adult).

    Working-age beneficiaries (SSDI, survivors) get no UBI in phase1, so
    the offset does not touch them: they keep their Social Security.
    """
    social_security = person("social_security", period)
    return where(offset_applies, max_(amount - social_security, 0), amount)
