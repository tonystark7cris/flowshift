"""Declarative pipeline engine for flowshift.

Allows executing a series of flowshift tools defined in a YAML configuration file.
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path
from typing import Any

import yaml


class Pipeline:
    """Engine to execute a flowshift pipeline from a YAML configuration."""

    def __init__(self, config_path: str | Path):
        """Initialize the pipeline with a path to a YAML configuration file."""
        self.config_path = Path(config_path)
        with self.config_path.open("r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        self.name = self.config.get("name", "Unnamed Pipeline")
        self.backend_name = self.config.get("backend", None)
        self.steps = self.config.get("steps", [])
        self.state: dict[str, Any] = {}

    def _resolve_input(self, ref: str) -> Any:
        """Resolve an input reference string to a DataFrame from state.

        Supports resolving tuple items (e.g., 'filter_step.0').
        """
        if not isinstance(ref, str):
            return ref

        parts = ref.split(".")
        step_id = parts[0]
        if step_id not in self.state:
            raise ValueError(f"Input reference '{step_id}' not found in pipeline state.")

        value = self.state[step_id]

        # Handle tuple indexing (e.g., filter_high_value.0)
        if len(parts) > 1:
            try:
                idx = int(parts[1])
                return value[idx]
            except (ValueError, TypeError, IndexError) as e:
                raise ValueError(
                    f"Could not resolve index '{parts[1]}' on output of step '{step_id}'. "
                    f"Output is of type {type(value)}."
                ) from e

        return value

    def _get_tool_callable(self, tool_path: str) -> Any:
        """Dynamically load a flowshift method (e.g., 'Preparation.filter')."""
        try:
            class_name, method_name = tool_path.split(".")
        except ValueError as e:
            raise ValueError(f"Invalid tool format '{tool_path}'. Expected 'Class.method'") from e

        # All flowshift tools are exported at the root module level
        try:
            module = importlib.import_module("flowshift")
            tool_class = getattr(module, class_name)
            tool_func = getattr(tool_class, method_name)
            return tool_func
        except AttributeError as e:
            raise ValueError(f"Could not find tool '{tool_path}' in flowshift.") from e

    def execute(self) -> None:
        """Run all steps in the pipeline sequentially."""
        print(f"Starting Pipeline: {self.name}")

        if self.backend_name:
            from flowshift._config import set_backend
            set_backend(self.backend_name, **self.config.get("spark_config", {}))

        for step in self.steps:
            step_id = step.get("id")
            tool_name = step.get("tool")
            inputs = step.get("inputs", {})
            args = step.get("args", {})

            if not step_id or not tool_name:
                raise ValueError("Each step must have an 'id' and a 'tool'.")

            print(f"  -> Executing step: {step_id} ({tool_name})")

            # 1. Resolve inputs
            resolved_inputs = {}
            for param_name, ref in inputs.items():
                resolved_inputs[param_name] = self._resolve_input(ref)

            # 2. Merge inputs with other kwargs
            kwargs = {**resolved_inputs, **args}

            # 3. Get callable
            tool_func = self._get_tool_callable(tool_name)

            # 4. Execute
            result = tool_func(**kwargs)

            # 5. Store in state
            self.state[step_id] = result

        print("Pipeline completed successfully.")

    @classmethod
    def run(cls, config_path: str | Path) -> None:
        """Convenience method to load and execute a pipeline."""
        pipeline = cls(config_path)
        pipeline.execute()


def cli_main() -> None:
    """CLI entry point for running pipelines."""
    parser = argparse.ArgumentParser(description="Run a flowshift YAML pipeline.")
    parser.add_argument(
        "command",
        choices=["run"],
        help="Command to execute (e.g., 'run')."
    )
    parser.add_argument(
        "config_path",
        type=str,
        help="Path to the YAML pipeline configuration file."
    )

    args = parser.parse_args()

    if args.command == "run":
        try:
            Pipeline.run(args.config_path)
        except Exception as e:
            print(f"Pipeline failed: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    cli_main()
