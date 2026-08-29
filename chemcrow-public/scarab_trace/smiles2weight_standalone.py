#!/usr/bin/env python3
"""
Standalone, GPT-4-free reproduction of ChemCrow's SMILES2Weight tool
(chemcrow/tools/rdkit.py) for Scarab/Pin instruction tracing.

Only dependency is rdkit itself -- no langchain, no BaseTool, no network
calls -- so the traced binary's instruction stream is just Python + RDKit's
C++ extension doing exact-mass calculation on one fixed molecule.

Usage:
    python3 smiles2weight_standalone.py

Fixed input: aspirin (acetylsalicylic acid)
    SMILES = "CC(=O)OC1=CC=CC=C1C(=O)O"
"""

import time

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

# Fixed molecule so runs are directly comparable across trials/machines.
SMILES = "CC(=O)OC1=CC=CC=C1C(=O)O"  # aspirin


def smiles_to_weight(smiles: str):
    """Mirrors SMILES2Weight._run in chemcrow/tools/rdkit.py exactly."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return "Invalid SMILES string"
    return rdMolDescriptors.CalcExactMolWt(mol)


if __name__ == "__main__":
    start = time.perf_counter()
    result = smiles_to_weight(SMILES)
    elapsed = time.perf_counter() - start

    print(f"input_smiles: {SMILES}")
    print(f"exact_mol_wt: {result!r}")
    print(f"runtime_seconds: {elapsed:.6f}")
