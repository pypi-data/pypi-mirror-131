from __future__ import annotations

import logging
from dataclasses import dataclass, field
from functools import partial
from typing import Any, Callable, Dict, Iterable

from ..data import ParseCompound
from .shared import (
    MALFORMED_LINE_STARTS,
    _add_database_link,
    _add_type,
    _set_gibbs0,
    _set_name,
)

__all__ = ["CompoundParser"]

logger = logging.getLogger(__name__)


def _set_atom_charges(compounds: Dict[str, ParseCompound], id_: str, content: str) -> None:
    try:
        compounds[id_].charge += int(content[1:-1].split()[-1])
    except ValueError:  # conversion failed
        pass


def _set_chemical_formula(compounds: Dict[str, ParseCompound], id_: str, content: str) -> None:
    atom, count = content[1:-1].split(" ")
    try:
        compounds[id_].formula[atom] = int(count)
    except ValueError:  # conversion failed
        pass


def _set_smiles(compounds: Dict[str, ParseCompound], id_: str, content: str) -> None:
    compounds[id_].smiles = content


@dataclass
class CompoundParser:
    type_map: dict[str, str]
    actions: Dict[str, Callable[[Any, Any, Any], None]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.actions = {
            "TYPES": partial(_add_type, type_map=self.type_map),
            "COMMON-NAME": _set_name,
            "ATOM-CHARGES": _set_atom_charges,
            "CHEMICAL-FORMULA": _set_chemical_formula,
            "DBLINKS": _add_database_link,
            "GIBBS-0": _set_gibbs0,
            "SMILES": _set_smiles,
        }

    def parse(self, file: Iterable[str]) -> Dict[str, ParseCompound]:
        """Parse."""
        compounds: Dict[str, ParseCompound] = {}
        id_ = ""
        for line in file:
            if any(line.startswith(i) for i in MALFORMED_LINE_STARTS):
                continue
            try:
                identifier, content = line.rstrip().split(" - ", maxsplit=1)
            except ValueError:
                logger.info(f"Malformed line in compoudns.dat: {line}")
                continue

            if identifier == "UNIQUE-ID":
                base_id = content
                id_ = content + "_c"
                compounds[id_] = ParseCompound(
                    id=id_,
                    base_id=base_id,
                    compartment="CYTOSOL",
                )
            else:
                if (action := self.actions.get(identifier, None)) is not None:
                    action(compounds, id_, content)
        return compounds
