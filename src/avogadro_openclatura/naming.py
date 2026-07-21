#  This source file is part of the Avogadro project
#  This source code is released under the 3-Clause BSD License, (see "LICENSE").
#  https://github.com/ghutchis/avogadro-openclatura/

"""Generate an IUPAC-style name from the current molecule using OpenClatura."""

from openclatura import name_smiles
from rdkit import Chem


def clatura_name(avo_input: dict) -> dict:
    """Derive a canonical SMILES from the molecule and return its name.

    OpenClatura names SMILES strings, so we convert the molblock Avogadro
    sends into a canonical SMILES with RDKit first.  The input molecule is
    echoed back unchanged (a message-only response would otherwise be
    processed as an empty molecule replacement by Avogadro).
    """
    # Echo the molecule back untouched; only add a message/error.
    output = dict(avo_input)

    mol = Chem.MolFromMolBlock(avo_input.get("sdf", ""))
    if mol is None:
        output["error"] = "Could not interpret the molecule."
        return output

    smiles = Chem.MolToSmiles(mol)

    try:
        name = name_smiles(smiles)
    except Exception as exc:  # OpenClatura raises for unsupported structures
        output["error"] = f"Could not name {smiles}:\n{exc}"
        return output

    if not name:
        output["message"] = f"No name found for:\n{smiles}"
    else:
        output["message"] = f"{name}\n\nSMILES: {smiles}"

    return output
