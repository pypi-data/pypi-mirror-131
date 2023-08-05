from __future__ import annotations

from typing import Dict

from ....core.reaction import Monomer
from ..data import ParseReaction


def fix_annotate_monomers(
    rxns: Dict[str, ParseReaction], monomers: Dict[str, Monomer]
) -> Dict[str, ParseReaction]:
    for rxn in rxns.values():
        rxn.monomers_annotated = {
            k: {monomer: monomers[monomer] for monomer in v if monomer in monomers}
            for k, v in rxn.monomers.items()
        }
        del rxn.monomers
    return rxns
