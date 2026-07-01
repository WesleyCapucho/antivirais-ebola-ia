import os
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdForceFieldHelpers

def prepare_ligands():
    """
    Lê a lista de inibidores curados, converte SMILES para objetos 3D,
    adiciona hidrogênios e aplica minimização geométrica (MMFF94).
    """
    output_dir = r"G:\Meu Drive\PROJETO-ANTIVIRAIS-NANOTECNOLOGIA-IA\3-SCREENING-OTIMIZACAO\ligantes_preparados"
    os.makedirs(output_dir, exist_ok=True)
    
    # Mock de compostos "Hits" da Rede Neural
    hits = {
        "Composto_Ouro_1": "CC1=C(C=C(C=C1)O)C=O",
        "Remdesivir_Control": "CCC(C)C"
    }
    
    for name, smiles in hits.items():
        print(f"[*] Processando {name}...")
        mol = Chem.MolFromSmiles(smiles)
        
        if mol is None:
            print(f"[-] Erro ao ler SMILES para {name}")
            continue
            
        # Adiciona Hidrogênios em 3D
        mol = Chem.AddHs(mol)
        
        # Gera a conformação 3D inicial
        AllChem.EmbedMolecule(mol, randomSeed=42)
        
        # Minimiza a energia geométrica usando o campo de força MMFF94
        try:
            rdForceFieldHelpers.MMFFOptimizeMolecule(mol)
            print(f"  [+] Minimização MMFF94 concluída.")
        except Exception as e:
            print(f"  [-] Falha na minimização: {e}")
            
        # Salva o arquivo MDL Molfile (SDF) pronto para o docking
        out_file = os.path.join(output_dir, f"{name}.sdf")
        writer = Chem.SDWriter(out_file)
        writer.write(mol)
        writer.close()
        
        print(f"  [+] Salvo em {out_file}\n")

if __name__ == "__main__":
    prepare_ligands()
