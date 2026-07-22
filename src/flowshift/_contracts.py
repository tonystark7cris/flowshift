"""Data contract validation — backward-compatibility shim.

The schema contract implementation has moved to the ``flowshift-governance``
sub-package.  This module re-exports everything from there so that all
existing code continues to work unchanged:

    from flowshift._contracts import expect_schema, SchemaViolationError  # still works
    from flowshift import expect_schema, infer_schema                      # still works
    from flowshift_governance import expect_schema, profile, ContractSuite # new canonical home

.. deprecated::
    Import from ``flowshift_governance`` directly for access to the full
    feature set, including :func:`flowshift_governance.contracts.profile`
    and :class:`flowshift_governance.contracts.ContractSuite`.
    The shim re-exports will be removed in flowshift 3.0.
"""

from __future__ import annotations

# Re-export everything the original module exposed, sourced from the
# governance sub-package (single source of truth).
from flowshift_governance.contracts import (
    SchemaViolationError,
    _dtype_matches,
    expect_schema,
    infer_schema,
)

__all__ = ["SchemaViolationError", "expect_schema", "infer_schema", "_dtype_matches"]
