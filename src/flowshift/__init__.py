"""flowshift — The fastest path from proprietary visual ETL to open-source Python.

Accelerates migration from legacy visual ETL tools to
open-source Python by providing 1:1 tool palette mappings (Preparation, Join,
Transform, Parse, InOut, Developer). Uses **pandas** (local) or **PySpark** (cluster)
as the underlying data engine. Includes automated ``.yxmd`` workflow conversion tools.

Quick start::

    from flowshift import InOut, Preparation, Join, Transform, Parse, Developer

    df = InOut.input_data("sales.csv")
    high, low = Preparation.filter(df, "Revenue > 1000")
    summary = Transform.summarize(high, group_by="Region",
                                   aggregations={"Revenue": "sum"})
    InOut.output_data(summary, "summary.parquet")
"""

from flowshift._config import backend, get_backend, set_backend
from flowshift._contracts import SchemaViolationError, expect_schema, infer_schema
from flowshift._pii import scan_pii
from flowshift._version import __version__
from flowshift.convert import YxmdConverter
from flowshift.developer import Developer
from flowshift.in_out import InOut
from flowshift.join import Join
from flowshift.parse import Parse
from flowshift.pipeline import Pipeline
from flowshift.preparation import Preparation
from flowshift.transform import Transform

__all__ = [
    "__version__",
    # Converter
    "YxmdConverter",
    # Tool palettes
    "Developer",
    "InOut",
    "Join",
    "Parse",
    "Pipeline",
    "Preparation",
    "Transform",
    "set_backend",
    "get_backend",
    "backend",
    # Data contracts
    "expect_schema",
    "infer_schema",
    "SchemaViolationError",
    # PII scanning
    "scan_pii",
]
