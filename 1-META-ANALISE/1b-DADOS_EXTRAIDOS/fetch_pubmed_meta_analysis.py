import os
import csv
from Bio import Entrez
from datetime import datetime

# Substitua com um email válido para a API do NCBI
Entrez.email = "wesley.pesquisa@antiviral.lab"

def fetch_pubmed_ids(query, max_results=500):
    """Busca PMIDs no PubMed baseados em uma query."""
    print(f"Executando busca para a query:\n{query}")
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"]

def main():
    # As 3 queries exatas definidas pela arquitetura do Claude (2015-2024)
    query_tier1 = '((filovirus OR EBOV OR Marburg OR SUDV)) AND ((polymerase OR L-protein OR "L protein")) AND ((inhibitor OR inhibition)) AND ((enzymatic OR purified OR "in vitro" OR kinetic*)) AND ("2015/01/01"[Date - Publication] : "2024/12/31"[Date - Publication])'
    
    query_tier2 = '((filovirus OR EBOV OR Marburg OR SUDV)) AND ((antiviral OR inhibitor OR compound)) AND ((replication OR "cell culture" OR "cell-based")) AND ((EC50 OR IC50 OR activity)) NOT ((VP40 OR VP35 OR NP OR glycoprotein)) AND ("2015/01/01"[Date - Publication] : "2024/12/31"[Date - Publication])'
    
    query_tier3 = '((filovirus antiviral)) AND ((nucleoside OR nucleotide OR NTP OR "adenine analog*")) AND ("2015/01/01"[Date - Publication] : "2024/12/31"[Date - Publication])'

    print("Iniciando varredura automatizada no PubMed para a Meta-Análise...\n")
    
    ids_t1 = fetch_pubmed_ids(query_tier1)
    print(f"-> TIER 1 (Enzimático Ouro): {len(ids_t1)} papers encontrados.\n")
    
    ids_t2 = fetch_pubmed_ids(query_tier2)
    print(f"-> TIER 2 (Fenotípico p/ Reverse Docking): {len(ids_t2)} papers encontrados.\n")
    
    ids_t3 = fetch_pubmed_ids(query_tier3)
    print(f"-> TIER 3 (Classe Química - Backup): {len(ids_t3)} papers encontrados.\n")

    # Criando o Dataset Template para curadoria
    output_dir = r"G:\Meu Drive\PROJETO-ANTIVIRAIS-NANOTECNOLOGIA-IA\1-META-ANALISE\1b-DADOS_EXTRAIDOS"
    os.makedirs(output_dir, exist_ok=True)
    
    csv_path = os.path.join(output_dir, "dataset_antivirals_tiered_v1.csv")
    
    # Consolidando em um dataset (evitando duplicatas inter-tiers com preferência ao tier superior)
    master_dict = {}
    for pmid in ids_t1:
        master_dict[pmid] = {"PMID": pmid, "Suggested_Tier": 1.0, "Reason": "Tier 1: enzymatic/direct"}
    for pmid in ids_t2:
        if pmid not in master_dict:
            master_dict[pmid] = {"PMID": pmid, "Suggested_Tier": 0.7, "Reason": "Tier 2: phenotypic"}
    for pmid in ids_t3:
        if pmid not in master_dict:
            master_dict[pmid] = {"PMID": pmid, "Suggested_Tier": 0.5, "Reason": "Tier 3: chemical_class"}

    headers = [
        "PMID", "SMILES", "Compound_ID", "DOI", "Year",
        "EC50_EBOV", "EC50_SUDV", "EC50_MARV", "CC50", "SI",
        "Mechanism_Declared", "Target_Tested_Yes_No",
        "Suggested_Tier", "Confidence_Score_Final", "Reason_Tier",
        "docking_deltaG_Lpoly", "docking_deltaG_VP40", "docking_deltaG_VP35"
    ]
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        
        for pmid, info in master_dict.items():
            writer.writerow({
                "PMID": info["PMID"],
                "Suggested_Tier": info["Suggested_Tier"],
                "Reason_Tier": info["Reason"]
            })
            
    print(f"\nPlanilha base gerada com sucesso! Total de artigos únicos rastreados: {len(master_dict)}")
    print(f"Local: {csv_path}")

if __name__ == "__main__":
    main()
