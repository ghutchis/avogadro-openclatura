#  This source file is part of the Avogadro project
#  This source code is released under the 3-Clause BSD License, (see "LICENSE").
#  https://github.com/ghutchis/avogadro-openclatura/

"""Generate an IUPAC-style name from the current molecule using OpenClatura."""

from openclatura import name_rdkit_mol
from rdkit import Chem


def clatura_name(avo_input: dict) -> dict:
    """Name the current molecule and store the name back on it.

    Avogadro always sends the full molecule as a ``cjson`` object alongside
    the requested ``sdf`` molblock.  We name the RDKit molecule directly
    (OpenClatura 0.1.5+ accepts an RDKit mol), then echo the molecule back
    with a ``name`` property added.  ``readProperties`` merges that property
    in place rather than rebuilding the molecule, so atoms, bonds and the
    undo history are left untouched.

    The echo is also what keeps a message-only response from being treated
    as an empty-molecule replacement by Avogadro.
    """
    output = {}

    # Echo the molecule back untouched; readProperties merges only the data
    # map (i.e. the name) instead of replacing atoms/bonds.
    cjson = avo_input.get("cjson")
    if isinstance(cjson, dict):
        cjson = dict(cjson)
        output["cjson"] = cjson
        output["moleculeFormat"] = "cjson"
        output["readProperties"] = True

    mol = Chem.MolFromMolBlock(avo_input.get("sdf", ""))
    if mol is None:
        output["error"] = "Could not interpret the molecule."
        return output

    smiles = Chem.MolToSmiles(mol)

    try:
        name = name_rdkit_mol(mol)
    except Exception as exc:  # OpenClatura raises for unsupported structures
        output["error"] = f"Could not name {smiles}:\n{exc}"
        return output

    if not name:
        output["message"] = f"No name found for:\n{smiles}"
        return output

    # Store the name on the molecule so Avogadro keeps and displays it.
    if isinstance(cjson, dict):
        cjson["name"] = name

    output["message"] = f"{name}\n\nSMILES: {smiles}"
    return output
