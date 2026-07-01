import os
import urllib.request

def download_pdb(pdb_id, output_dir):
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    output_path = os.path.join(output_dir, f"{pdb_id}.pdb")
    
    if os.path.exists(output_path):
        print(f"[{pdb_id}] Já existe. Pulando.")
        return
        
    try:
        print(f"Baixando {pdb_id}...")
        urllib.request.urlretrieve(url, output_path)
        print(f"[{pdb_id}] Download concluído!")
    except Exception as e:
        print(f"Erro ao baixar {pdb_id}: {e}")

def main():
    output_dir = r"G:\Meu Drive\PROJETO-ANTIVIRAIS-NANOTECNOLOGIA-IA\3-SCREENING-OTIMIZACAO\3a-DOCKING_VIRTUAL\3a2_estruturas_proteicas"
    os.makedirs(output_dir, exist_ok=True)
    
    # Lista de alvos do projeto
    targets = {
        "L-Polymerase (Ouro)": ["4ZKX", "6VSR", "3CSY"],
        "VP40 (Controle Off-target)": ["5V6X", "6VSK"],
        "VP35 (Controle Off-target)": ["3IJ4"]
    }
    
    for category, pdbs in targets.items():
        print(f"\n--- Processando {category} ---")
        for pdb_id in pdbs:
            download_pdb(pdb_id, output_dir)
            
    print("\nTodos os cristais foram salvos diretamente no Google Drive (G:\) com sucesso.")

if __name__ == "__main__":
    main()
