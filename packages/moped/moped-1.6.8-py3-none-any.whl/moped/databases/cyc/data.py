from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple

from ...core.reaction import KineticData, Monomer

__all__ = [
    "ParseGene",
    "ParseCompound",
    "ParseReaction",
    "ParseEnzyme",
]


@dataclass
class ParseGene:
    id: str
    product: str | None = None
    database_links: Dict[str, Set[str]] = field(default_factory=dict)


@dataclass
class ParseCompound:
    id: str
    base_id: str
    charge: int = 0
    compartment: str = "CYTOSOL"
    smiles: str | None = None
    name: str | None = None
    gibbs0: float | None = None
    types: List[str] = field(default_factory=list)
    formula: Dict[str, float] = field(default_factory=dict)
    database_links: Dict[str, Set[str]] = field(default_factory=dict)


@dataclass
class ParseReaction:
    id: str
    base_id: str
    bounds: Tuple[float, float] = (0, 0)
    name: str | None = None
    ec: str | None = None
    gibbs0: float | None = None
    direction: str = "LEFT-TO-RIGHT"
    reversible: bool = False
    transmembrane: bool = False
    substrates: Dict[str, float] = field(default_factory=dict)
    substrate_compartments: Dict[str, str] = field(default_factory=dict)
    products: Dict[str, float] = field(default_factory=dict)
    product_compartments: Dict[str, str] = field(default_factory=dict)
    types: List[str] = field(default_factory=list)
    locations: List[str] = field(default_factory=list)
    pathways: Set[str] = field(default_factory=set)
    enzymes: Set[str] = field(default_factory=set)
    database_links: Dict[str, Set[str]] = field(default_factory=dict)
    _var: int | None = None
    # Later additions
    monomers: Dict[str, Set[str]] = field(default_factory=dict)
    monomers_annotated: Dict[str, Dict[str, Monomer]] = field(default_factory=dict)
    sequences: Dict[str, str] = field(default_factory=dict)
    enzrxns: Dict[str, Dict[str, Dict[str, float]]] = field(default_factory=dict)
    kinetic_data: Dict[str, KineticData] = field(default_factory=dict)
    compartment: str | Tuple[str, str] | None = None
    stoichiometries: Dict[str, float] = field(default_factory=dict)


@dataclass
class ParseEnzyme:
    id: str
    enzyme: str | None = None
    kcat: Dict[str, float] = field(default_factory=dict)
    km: Dict[str, float] = field(default_factory=dict)
    vmax: Dict[str, float] = field(default_factory=dict)
