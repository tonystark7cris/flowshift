"""flowshift — Python ETL toolkit — Flowshift..

Replicate every major visual ETL tool as an independent Python
function, organised under classes that mirror Flowshift's tool palette
categories. Uses **pandas** (local) or **PySpark** (cluster) as the data engine.

Quick start::

    from flowshift import InOut, Preparation, Join, Transform, Parse, Developer

    df = InOut.input_data("sales.csv")
    high, low = Preparation.filter(df, "Revenue > 1000")
    summary = Transform.summarize(high, group_by="Region",
                                   aggregations={"Revenue": "sum"})
    InOut.output_data(summary, "summary.parquet")
"""

from flowshift._config import backend, get_backend, set_backend
from flowshift._version import __version__
from flowshift.developer import Developer
from flowshift.in_out import InOut
from flowshift.join import Join
from flowshift.parse import Parse
from flowshift.pipeline import Pipeline
from flowshift.preparation import Preparation
from flowshift.transform import Transform

__all__ = [
    "__version__",
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
]
