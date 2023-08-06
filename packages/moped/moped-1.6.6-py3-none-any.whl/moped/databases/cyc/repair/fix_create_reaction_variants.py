from __future__ import annotations

import itertools as it
from copy import deepcopy
from typing import Dict, Iterable, List

from ..data import ParseCompound, ParseReaction
from ..utils import _reaction_is_bad


def _get_compound_variants(
    cpds: Dict[str, float],
    cpd_types: Dict[str, List[str]],
) -> Dict[str, List[str]]:
    return {cpd: cpd_types[cpd] for cpd in cpds if cpd in cpd_types}


def _get_reaction_variant(
    rxn: ParseReaction,
    old_cpds: Iterable[str],
    new_cpds: Iterable[str],
    substrate_variants: Dict[str, List[str]],
    product_variants: Dict[str, List[str]],
    count: int,
) -> ParseReaction:
    local = deepcopy(rxn)
    local_cpds = dict(zip(old_cpds, new_cpds))
    for old_sub in substrate_variants:
        new_sub = local_cpds[old_sub]
        local.substrates[new_sub] = local.substrates.pop(old_sub)
        local.substrate_compartments[new_sub] = local.substrate_compartments.pop(old_sub)
    for old_prod in product_variants:
        new_prod = local_cpds[old_prod]
        local.products[new_prod] = local.products.pop(old_prod)
        local.product_compartments[new_prod] = local.product_compartments.pop(old_prod)
    local.id = f"{local.id}__var__{count}"
    local._var = count
    return local


def fix_create_reaction_variants(
    rxns: Dict[str, ParseReaction],
    cpds: Dict[str, ParseCompound],
    compound_types: Dict[str, List[str]],
) -> Dict[str, ParseReaction]:
    """Create all mass and charge balanced reaction variants of reactions containing compound classes."""
    new_rxns = {}
    for rxn_id, rxn in rxns.items():
        count = 0
        substrate_variants = _get_compound_variants(rxn.substrates, compound_types)
        product_variants = _get_compound_variants(rxn.products, compound_types)

        variants = {**substrate_variants, **product_variants}
        if len(variants) == 0:
            new_rxns[rxn_id] = rxn
        else:
            for new_cpds, old_cpds in zip(
                it.product(*variants.values()),
                it.repeat(variants.keys()),
            ):
                new_rxn = _get_reaction_variant(
                    rxn,
                    old_cpds,
                    new_cpds,
                    substrate_variants,
                    product_variants,
                    count,
                )
                # Performance improvement: filter garbage reactions already here
                if _reaction_is_bad(new_rxn, cpds):
                    continue
                new_rxns[new_rxn.id] = new_rxn
                count += 1
    return new_rxns
