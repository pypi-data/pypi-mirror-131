from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, Set, Tuple

from .shared import MALFORMED_LINE_STARTS

logger = logging.getLogger(__name__)

__all__ = ["ProteinParser"]


def _add_component(complexes: Dict[str, Set[str]], complex_id: str, component: str) -> None:
    complexes[complex_id].add(component)


@dataclass
class ProteinParser:
    actions: Dict[str, Callable[[Any, Any, Any], None]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.actions = {
            "COMPONENTS": _add_component,
        }

    def parse(self, file: Iterable[str]) -> Tuple[Set[str], Dict[str, Set[str]]]:
        id_ = ""
        proteins: Dict[str, Set[str]] = {}
        monomers: Set[str] = set()
        complexes: Dict[str, Set[str]] = dict()
        for line in file:
            if any(line.startswith(i) for i in MALFORMED_LINE_STARTS):
                continue
            try:
                identifier, content = line.rstrip().split(" - ", maxsplit=1)
            except ValueError:
                logger.info(f"Malformed line in proteins.dat: {line}")
                continue

            if identifier == "UNIQUE-ID":
                id_ = content
                proteins[id_] = set()
            elif not identifier.startswith("^"):
                if (action := self.actions.get(identifier, None)) is not None:
                    action(proteins, id_, content)

        for k, v in proteins.items():
            if bool(v):
                complexes[k] = v
            else:
                monomers.add(k)
        return monomers, complexes
