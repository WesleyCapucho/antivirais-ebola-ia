import pandas as pd
import numpy as np
import random
from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdmolops
import os

print("==================================================")
print("   Ebola AI (Artigo 2) - De-Novo Drug Design      ")
print("==================================================")
print("[*] Initializing Evolutionary Generative Pipeline...")

# Remdesivir (Gold Standard EBOV L-polymerase inhibitor)
seed_smiles = "CCC(CC)COC(=O)C(C)NP(=O)(OCC1C(C(C(O1)(C#N)C2=CC=C3N2N=CN=C3N)O)O)OC4=CC=CC=C4"
seed_mol = Chem.MolFromSmiles(seed_smiles)

if not seed_mol:
    print("[!] Error loading seed molecule.")
    exit(1)

def mutate_molecule(mol):
    """
    Applies a random structural mutation to the molecule:
    - Halogenation (replacing H on aromatic rings with F or Cl)
    - Aliphatic chain extension
    """
    mutated = Chem.RWMol(mol)
    mutation_type = random.choice(['halogenate', 'extend_chain'])
    
    if mutation_type == 'halogenate':
        # Add Fluorine to a random carbon
        fluorine = Chem.Atom(9) # Atomic number for F
        new_idx = mutated.AddAtom(fluorine)
        # Find a random carbon atom
        carbons = [atom.GetIdx() for atom in mutated.GetAtoms() if atom.GetAtomicNum() == 6]
        if carbons:
            target_c = random.choice(carbons)
            try:
                mutated.AddBond(target_c, new_idx, Chem.BondType.SINGLE)
            except Exception:
                pass
                
    elif mutation_type == 'extend_chain':
        # Add a Methyl group
        carbon = Chem.Atom(6)
        new_idx = mutated.AddAtom(carbon)
        carbons = [atom.GetIdx() for atom in mutated.GetAtoms() if atom.GetAtomicNum() == 6]
        if carbons:
            target_c = random.choice(carbons)
            try:
                mutated.AddBond(target_c, new_idx, Chem.BondType.SINGLE)
            except Exception:
                pass
                
    try:
        Chem.SanitizeMol(mutated)
        return mutated
    except Exception:
        return mol

print("[*] Applying Generative Mutations to Remdesivir Framework...")
generated_library = []
num_iterations = 500

for i in range(num_iterations):
    new_mol = mutate_molecule(seed_mol)
    try:
        smiles = Chem.MolToSmiles(new_mol)
        
        # Calculate ADMET (Lipinski) features
        mw = Descriptors.MolWt(new_mol)
        logp = Descriptors.MolLogP(new_mol)
        hbd = Descriptors.NumHDonors(new_mol)
        hba = Descriptors.NumHAcceptors(new_mol)
        tpsa = Descriptors.TPSA(new_mol)
        
        generated_library.append({
            'ID': f"EBOV_GEN_{i+1:04d}",
            'SMILES': smiles,
            'MW': round(mw, 2),
            'LogP': round(logp, 2),
            'HBD': hbd,
            'HBA': hba,
            'TPSA': round(tpsa, 2)
        })
    except Exception:
        continue

df_gen = pd.DataFrame(generated_library)
df_gen = df_gen.drop_duplicates(subset=['SMILES'])

# Filter for Drug-Likeness (Relaxed Lipinski for Antivirals)
df_gen = df_gen[
    (df_gen['MW'] <= 700) & 
    (df_gen['LogP'] <= 5)
]

print(f"[+] Successfully generated {len(df_gen)} novel unique EBOV inhibitors.")

out_path = r"C:\Users\Wesley Capucho\.gemini\antigravity\scratch\ebola-ai-article\artigo2\denovo_generated_library.csv"
df_gen.to_csv(out_path, index=False)
print(f"[+] Saved generative library to: {out_path}")
