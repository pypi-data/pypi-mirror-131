from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Set, Tuple, Type

from ...core.compound import Compound
from ...core.reaction import KineticData, Monomer, Reaction
from .data import ParseCompound, ParseEnzyme, ParseGene, ParseReaction
from .defaults import COMPARTMENT_MAP, COMPARTMENT_SUFFIXES, MANUAL_ADDITIONS, TYPE_MAP
from .parse import (
    CompoundParser,
    EnzymeParser,
    GeneParser,
    Parser,
    ProteinParser,
    ReactionParser,
    SequenceParser,
)
from .repair import (
    fix_add_important_compounds,
    fix_annotate_monomers,
    fix_create_compartment_variants,
    fix_create_reaction_variants,
    fix_filter_garbage_reactions,
    fix_kinetic_data,
    fix_set_reaction_stoichiometry,
    fix_unify_reaction_direction,
)

__all__ = [
    "RustPipeline",
    "PythonPipeline",
    "Cyc",
    "get_monomers_from_raw_monomers",
    "get_kinetic_data_from_raw",
    "CompoundParser",
    "EnzymeParser",
    "GeneParser",
    "Parser",
    "ProteinParser",
    "ReactionParser",
    "SequenceParser",
    "ParseCompound",
    "ParseEnzyme",
    "ParseGene",
    "ParseReaction",
]

try:
    import cycparser  # type: ignore

    CYCPARSER_FLAG = True
except ImportError:
    CYCPARSER_FLAG = False

if TYPE_CHECKING:

    from cycparser import RawKineticData, RawMonomer  # type: ignore


@dataclass
class BasePipeline:
    pgdb_path: Path
    compartment_map: Dict[str, str]
    type_map: Dict[str, str]
    manual_additions: Dict[str, ParseCompound]
    compartment_suffixes: Dict[str, str]

    def parse_and_repair(self) -> Tuple[Dict[str, ParseCompound], Dict[str, ParseReaction]]:
        raise NotImplementedError


class RustPipeline(BasePipeline):
    @staticmethod
    def get_monomers_from_raw_monomers(
        raw_monomers: Dict[str, Dict[str, RawMonomer]]
    ) -> Dict[str, Dict[str, Monomer]]:
        return {
            k: {k2: Monomer(id=k2, gene=v.gene, database_links=v.database_links)}
            for k, d in raw_monomers.items()
            for k2, v in d.items()
        }

    @staticmethod
    def get_kinetic_data_from_raw(raw_kinetic_data: Dict[str, RawKineticData]) -> Dict[str, KineticData]:
        return {k: KineticData(km=v.km, kcat=v.kcat) for k, v in raw_kinetic_data.items()}

    def parse_and_repair(self) -> Tuple[Dict[str, ParseCompound], Dict[str, ParseReaction]]:
        raw_compounds, raw_reactions = cycparser.parse(
            str(self.pgdb_path),
            self.compartment_map,
            self.type_map,
            self.manual_additions,  # type: ignore
            self.compartment_suffixes,
        )
        parse_compounds = {
            i.id: ParseCompound(
                id=i.id,
                base_id=i.base_id,
                charge=i.charge,
                gibbs0=i.gibbs0,
                smiles=i.smiles,
                name=i.name,
                types=i.types,
                formula=i.formula,
                database_links=i.database_links,
                compartment=c if (c := i.compartment) is not None else "CYTOSOL",
            )
            for i in raw_compounds
        }
        parse_reactions = {
            i.id: ParseReaction(
                id=i.id,
                base_id=i.base_id,
                name=i.name,
                ec=i.ec,
                gibbs0=i.gibbs0,
                types=i.types,
                pathways=i.pathways,
                database_links=i.database_links,
                bounds=i.bounds,
                monomers_annotated=self.get_monomers_from_raw_monomers(i.monomers_annotated),
                sequences=i.sequences,
                kinetic_data=self.get_kinetic_data_from_raw(i.kinetic_data),
                stoichiometries=i.stoichiometries,
                transmembrane=i.transmembrane,
                compartment=i.transmembrane_compartment if i.transmembrane else i.compartment,
                _var=i.var,
            )
            for i in raw_reactions
        }
        return parse_compounds, parse_reactions


@dataclass
class PythonPipeline(BasePipeline):
    def parse(
        self,
    ) -> Tuple[Dict[str, ParseCompound], Dict[str, ParseReaction], Dict[str, Monomer], Dict[str, List[str]]]:
        return Parser(
            pgdb_path=self.pgdb_path,
            compartment_map=self.compartment_map,
            type_map=self.type_map,
        ).parse()

    def repair(
        self,
        parse_compounds: Dict[str, ParseCompound],
        parse_reactions: Dict[str, ParseReaction],
        monomers: Dict[str, Monomer],
        compound_types: Dict[str, List[str]],
    ) -> Tuple[Dict[str, ParseCompound], Dict[str, ParseReaction]]:

        parse_compounds = fix_add_important_compounds(parse_compounds, self.manual_additions)
        parse_reactions = fix_unify_reaction_direction(parse_reactions)
        parse_reactions = fix_kinetic_data(parse_reactions)
        parse_reactions = fix_annotate_monomers(parse_reactions, monomers)

        # Larger changes
        parse_reactions = fix_create_reaction_variants(parse_reactions, parse_compounds, compound_types)
        parse_reactions = fix_filter_garbage_reactions(parse_reactions, parse_compounds)
        parse_reactions = fix_create_compartment_variants(
            parse_reactions,
            parse_compounds,
            self.compartment_map,
            self.compartment_suffixes,
        )
        parse_reactions = fix_set_reaction_stoichiometry(parse_reactions)
        return parse_compounds, parse_reactions

    def parse_and_repair(self) -> Tuple[Dict[str, ParseCompound], Dict[str, ParseReaction]]:
        return self.repair(*self.parse())


@dataclass(init=False)
class Cyc:
    compartment_suffixes: Dict[str, str]
    pipeline: BasePipeline

    def __init__(
        self,
        pgdb_path: Path,
        compartment_map: Dict[str, str] | None,
        type_map: Dict[str, str] | None,
        manual_additions: Dict[str, ParseCompound] | None,
        compartment_suffixes: Dict[str, str] | None,
        Pipeline: Type[BasePipeline] | None = None,
    ) -> None:
        if compartment_map is None:
            compartment_map = COMPARTMENT_MAP
        if type_map is None:
            type_map = TYPE_MAP
        if manual_additions is None:
            manual_additions = MANUAL_ADDITIONS
        if compartment_suffixes is None:
            compartment_suffixes = COMPARTMENT_SUFFIXES
        self.compartment_suffixes = compartment_suffixes

        if Pipeline is None:
            if CYCPARSER_FLAG:
                self.pipeline = RustPipeline(
                    pgdb_path=Path(pgdb_path),
                    compartment_map=compartment_map,
                    type_map=type_map,
                    manual_additions=manual_additions,
                    compartment_suffixes=compartment_suffixes,
                )
            else:
                self.pipeline = PythonPipeline(
                    pgdb_path=Path(pgdb_path),
                    compartment_map=compartment_map,
                    type_map=type_map,
                    manual_additions=manual_additions,
                    compartment_suffixes=compartment_suffixes,
                )
        else:
            self.pipeline = Pipeline(
                pgdb_path=Path(pgdb_path),
                compartment_map=compartment_map,
                type_map=type_map,
                manual_additions=manual_additions,
                compartment_suffixes=compartment_suffixes,
            )

    def _to_moped(
        self,
        parse_compounds: Dict[str, ParseCompound],
        parse_reactions: Dict[str, ParseReaction],
    ) -> Tuple[list[Compound], list[Reaction], Dict[str, str]]:
        compounds = [
            Compound(
                base_id=v.base_id,
                compartment=v.compartment,
                formula=v.formula,
                charge=v.charge,
                name=v.name,
                gibbs0=v.gibbs0,
                smiles=v.smiles,
                database_links=v.database_links,
                types=v.types,
                id=v.id,
            )
            for v in parse_compounds.values()
        ]
        reactions = [
            Reaction(
                base_id=v.base_id,
                id=v.id,
                stoichiometries=v.stoichiometries,
                compartment=v.compartment,
                name=v.name,
                bounds=v.bounds,
                gibbs0=v.gibbs0,
                ec=v.ec,
                types=v.types,
                pathways=v.pathways,
                sequences=v.sequences,
                monomers=v.monomers_annotated,
                kinetic_data=v.kinetic_data,
                database_links=v.database_links,
                transmembrane=v.transmembrane,
                _var=v._var,
            )
            for v in parse_reactions.values()
        ]
        used_compartments: Set[str] = {i.compartment for i in compounds if i.compartment is not None}
        compartments: Dict[str, str] = {i: self.compartment_suffixes[i] for i in used_compartments}
        return compounds, reactions, compartments

    def parse(self) -> Tuple[list[Compound], list[Reaction], Dict[str, str]]:
        parse_compounds, parse_reactions = self.pipeline.parse_and_repair()
        return self._to_moped(parse_compounds, parse_reactions)


def get_monomers_from_raw_monomers(
    raw_monomers: Dict[str, Dict[str, RawMonomer]]
) -> Dict[str, Dict[str, Monomer]]:
    return {
        k: {k2: Monomer(id=k2, gene=v.gene, database_links=v.database_links)}
        for k, d in raw_monomers.items()
        for k2, v in d.items()
    }


def get_kinetic_data_from_raw(raw_kinetic_data: Dict[str, RawKineticData]) -> Dict[str, KineticData]:
    return {k: KineticData(km=v.km, kcat=v.kcat) for k, v in raw_kinetic_data.items()}
