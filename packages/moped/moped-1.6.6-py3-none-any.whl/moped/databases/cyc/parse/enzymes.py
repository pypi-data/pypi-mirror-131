from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable

from ..data import ParseEnzyme
from .shared import MALFORMED_LINE_STARTS

__all__ = ["EnzymeParser"]

logger = logging.getLogger(__name__)


def _set_enzyme(enzrxns: Dict[str, ParseEnzyme], id_: str, enzyme: str) -> None:
    enzrxns[id_].enzyme = enzyme


def _add_kcat(enzrxns: Dict[str, ParseEnzyme], id_: str, substrate: str, kcat: str) -> None:
    try:
        enzrxns[id_].kcat.setdefault(substrate, float(kcat))
    except ValueError:  # conversion failed
        pass


def _add_km(enzrxns: Dict[str, ParseEnzyme], id_: str, substrate: str, km: str) -> None:
    try:
        enzrxns[id_].km.setdefault(substrate, float(km))
    except ValueError:  # conversion failed
        pass


def _add_vmax(enzrxns: Dict[str, ParseEnzyme], id_: str, substrate: str, vmax: str) -> None:
    try:
        enzrxns[id_].vmax.setdefault(substrate, float(vmax))
    except ValueError:  # conversion failed
        pass


@dataclass
class EnzymeParser:
    actions: Dict[str, Callable[[Any, Any, Any], None]] = field(default_factory=dict)
    sub_actions: Dict[str, Dict[str, Callable[[Any, Any, Any, Any], None]]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.actions = {
            "ENZYME": _set_enzyme,
        }
        self.sub_actions = {
            "^SUBSTRATE": {"KM": _add_km, "VMAX": _add_vmax, "KCAT": _add_kcat},
        }

    def parse(self, file: Iterable[str]) -> Dict[str, ParseEnzyme]:
        """Parse."""
        id_ = ""
        enzrxns = {}
        last_identifier = ""
        last_content = ""
        for line in file:
            if any(line.startswith(i) for i in MALFORMED_LINE_STARTS):
                continue
            try:
                identifier, content = line.rstrip().split(" - ", maxsplit=1)
            except ValueError:
                logger.info(f"Malformed line in enzymes.dat {line}")
                continue

            if identifier == "UNIQUE-ID":
                id_ = content
                enzrxns[id_] = ParseEnzyme(id=id_)
            elif identifier.startswith("^"):
                if (subaction := self.sub_actions.get(identifier, {}).get(last_identifier, None)) is not None:
                    subaction(enzrxns, id_, content, last_content)
            else:
                if (action := self.actions.get(identifier, None)) is not None:
                    action(enzrxns, id_, content)
                    last_identifier = identifier
                    last_content = content
        return enzrxns
