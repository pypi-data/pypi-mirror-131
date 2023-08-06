from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable

from ....core.reaction import Monomer
from ..data import ParseGene
from .shared import MALFORMED_LINE_STARTS, _add_database_link

__all__ = ["GeneParser"]


def _set_gene_product(genes: Dict[str, ParseGene], id_: str, product: str) -> None:
    genes[id_].product = product


logger = logging.getLogger(__name__)


@dataclass
class GeneParser:
    actions: Dict[str, Callable[[Any, Any, Any], None]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.actions = {
            "DBLINKS": _add_database_link,
            "PRODUCT": _set_gene_product,
        }

    def parse(self, file: Iterable[str]) -> Dict[str, Monomer]:
        genes: Dict[str, ParseGene] = {}
        id_ = ""
        for line in file:
            if any(line.startswith(i) for i in MALFORMED_LINE_STARTS):
                continue
            try:
                identifier, content = line.rstrip().split(" - ", maxsplit=1)
            except ValueError:
                logger.info(f"Malformed line in genes.dat: {line}")
                continue

            if identifier == "UNIQUE-ID":
                id_ = content
                genes[content] = ParseGene(id=content)
            else:
                if (action := self.actions.get(identifier, None)) is not None:
                    action(genes, id_, content)
        return {
            product: Monomer(id=product, gene=i.id, database_links=i.database_links)
            for i in genes.values()
            if (product := i.product) is not None
        }
