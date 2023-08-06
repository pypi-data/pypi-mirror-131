"""Parse and repair metacyc or biocyc PGDB databases."""
from __future__ import annotations

import logging
import re
from collections import defaultdict
from functools import partial
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Set, Tuple

from ....core.reaction import Monomer
from ..data import ParseCompound, ParseEnzyme, ParseGene, ParseReaction
from .compounds import CompoundParser
from .enzymes import EnzymeParser
from .genes import GeneParser
from .proteins import ProteinParser
from .reactions import ReactionParser
from .sequences import SequenceParser

logger = logging.getLogger(__name__)

__all__ = [
    "Parser",
    "CompoundParser",
    "EnzymeParser",
    "GeneParser",
    "ProteinParser",
    "ReactionParser",
    "SequenceParser",
]


def _remove_top_comments(file: List[str]) -> List[str]:
    """Remove the metainformation from a pgdb file."""
    for i, line in enumerate(file):
        if line.startswith("UNIQUE-ID"):
            return file[i:]
    return file


def _read_file(path: Path) -> List[str]:
    try:
        with open(path, encoding="ISO-8859-14") as f:
            return f.readlines()
    except FileNotFoundError:
        return []


def _read_file_and_remove_comments(path: Path) -> List[str]:
    """Read the file and remove metainformation."""
    return _remove_top_comments(_read_file(path))


def _gather_compound_types(compounds: Dict[str, ParseCompound]) -> Dict[str, List[str]]:
    """Return (type: list(cpds)) dictionary.

    Only uses the highest-level type
    """
    types = defaultdict(list)
    for id_, cpd in compounds.items():
        if bool(cpd.types):
            # Only use highest level
            types[cpd.types[-1] + "_c"].append(id_)
    return dict(types)


def _check_for_monomer(
    enzrxn: str,
    protein: str,
    monomers: Iterable[str],
    complexes: Dict[str, Set[str]],
    enzrxn_to_monomer: Dict[str, Set[str]],
) -> None:
    """Check complex tree until you arrive at monomers."""
    try:
        for subcomplex in complexes[protein]:
            if subcomplex in monomers:
                enzrxn_to_monomer.setdefault(enzrxn, set()).add(subcomplex)
            else:
                _check_for_monomer(enzrxn, subcomplex, monomers, complexes, enzrxn_to_monomer)
    except KeyError:
        pass


def _get_enzrnx_to_monomer_mapping(
    enzrxns: Dict[str, ParseEnzyme],
    monomers: Iterable[str],
    complexes: Dict[str, Set[str]],
) -> Dict[str, Set[str]]:
    """Get mapping of enzyme reactions to monomers."""
    enzrxn_to_monomer: Dict[str, Set[str]] = {}
    for enzrxn, enzrxn_dict in enzrxns.items():
        protein = enzrxn_dict.enzyme
        if protein is not None:
            if protein in monomers:
                enzrxn_to_monomer.setdefault(enzrxn, set()).add(protein)
            else:
                _check_for_monomer(enzrxn, protein, monomers, complexes, enzrxn_to_monomer)
    return enzrxn_to_monomer


def _get_enzrnx_to_sequence_mapping(
    enzrxn_to_monomer: Dict[str, Set[str]], sequences: Dict[str, str]
) -> Dict[str, Dict[str, str]]:
    """Get mapping of enzyme reactions to sequences."""
    enzrxn_to_sequence: Dict[str, Dict[str, str]] = {}
    for enzrxn, monomers in enzrxn_to_monomer.items():
        for monomer in monomers:
            try:
                sequence = sequences[monomer]
                enzrxn_to_sequence.setdefault(enzrxn, dict())[monomer] = sequence
            except KeyError:
                pass
    return enzrxn_to_sequence


def _map_reactions_to_sequences(
    reactions: Dict[str, ParseReaction],
    enzrxn_to_monomer: Dict[str, Set[str]],
    enzrxn_to_seq: Dict[str, Dict[str, str]],
) -> None:
    """Get mapping of enzyme reactions to sequences."""
    for reaction in reactions.values():
        try:
            for enzrxn in reaction.enzymes:
                try:
                    reaction.sequences.update(enzrxn_to_seq[enzrxn])
                except KeyError:
                    pass
                try:
                    reaction.monomers.setdefault(enzrxn, set()).update(enzrxn_to_monomer[enzrxn])
                except KeyError:
                    pass
        except KeyError:
            pass


def _map_reactions_to_kinetic_parameters(
    reactions: Dict[str, ParseReaction],
    enzrxns: Dict[str, ParseEnzyme],
) -> None:
    """Get mapping of enzyme reactions to kinetic parameters."""
    for reaction in reactions.values():
        try:
            for enzrxn in reaction.enzymes:
                try:
                    enzyme = enzrxns[enzrxn]
                except KeyError:
                    pass
                else:
                    if bool(enzyme.kcat):
                        reaction.enzrxns.setdefault(enzyme.id, {}).setdefault("kcat", enzyme.kcat)
                    if bool(enzyme.km):
                        reaction.enzrxns.setdefault(enzyme.id, {}).setdefault("km", enzyme.km)
                    if bool(enzyme.vmax):
                        reaction.enzrxns.setdefault(enzyme.id, {}).setdefault("vmax", enzyme.vmax)
        except KeyError:
            pass


class Parser:
    """Base class for all metacyc/biocyc related databases."""

    def __init__(
        self,
        pgdb_path: Path,
        compartment_map: Dict[str, str],
        type_map: Dict[str, str],
    ) -> None:
        """Parse a *cyc pgdb into a moped.Model.

        Parameters
        ----------
        pgdb_path : Path
            Path to the pgdb
        parse_enzymes : bool
        name : str, optional

        Returns
        -------
        moped.Model
        """
        self.path = Path(pgdb_path)
        self.compartment_map = compartment_map
        self.type_map = type_map

    def parse(
        self,
    ) -> Tuple[Dict[str, ParseCompound], Dict[str, ParseReaction], Dict[str, Monomer], Dict[str, List[str]]]:
        """Parse the database."""
        path = self.path
        parse_compounds = CompoundParser(type_map=self.type_map).parse(
            _read_file_and_remove_comments(path / "compounds.dat")
        )
        compound_types = _gather_compound_types(parse_compounds)
        parse_reactions = ReactionParser(type_map=self.type_map).parse(
            _read_file_and_remove_comments(path / "reactions.dat")
        )
        genes = GeneParser().parse(_read_file_and_remove_comments(path / "genes.dat"))
        enzrxns = EnzymeParser().parse(_read_file_and_remove_comments(path / "enzrxns.dat"))
        monomers, complexes = ProteinParser().parse(_read_file_and_remove_comments(path / "proteins.dat"))
        sequences = SequenceParser().parse(iter(_read_file(path / "protseq.fsa")))
        enzrxn_to_monomer = _get_enzrnx_to_monomer_mapping(enzrxns, monomers, complexes)
        enzrxn_to_seq = _get_enzrnx_to_sequence_mapping(enzrxn_to_monomer, sequences)
        enzrxn_to_monomer = _get_enzrnx_to_monomer_mapping(enzrxns, monomers, complexes)
        enzrxn_to_seq = _get_enzrnx_to_sequence_mapping(enzrxn_to_monomer, sequences)
        _map_reactions_to_sequences(parse_reactions, enzrxn_to_monomer, enzrxn_to_seq)
        _map_reactions_to_kinetic_parameters(parse_reactions, enzrxns)
        return parse_compounds, parse_reactions, genes, compound_types
