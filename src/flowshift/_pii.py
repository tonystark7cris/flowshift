"""PII scanner — backward-compatibility shim.

The PII detection implementation has moved to the ``flowshift-governance``
sub-package.  This module re-exports everything from there so that all
existing code continues to work unchanged:

    from flowshift._pii import scan_pii, PIIWarning        # still works
    from flowshift import scan_pii                          # still works
    from flowshift_governance import scan_pii, mask_pii    # new canonical home

.. deprecated::
    Import from ``flowshift_governance`` directly for access to the full
    feature set, including :func:`flowshift_governance.pii.mask_pii`.
    The shim re-exports will be removed in flowshift 3.0.
"""

from __future__ import annotations

# Re-export everything the original module exposed, sourced from the
# governance sub-package (single source of truth).
from flowshift_governance.pii import (
    PIIWarning,
    _DEFAULT_PATTERNS,
    scan_pii,
)

__all__ = ["scan_pii", "PIIWarning", "_DEFAULT_PATTERNS"]
