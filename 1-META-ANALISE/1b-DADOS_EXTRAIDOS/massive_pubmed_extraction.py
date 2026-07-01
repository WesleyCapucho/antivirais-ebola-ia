import os
import csv
import time
from Bio import Entrez

Entrez.email = "wesley.pesquisa@antiviral.lab"

def fetch_pubmed_ids(query):
    print(f"Executando busca expansiva:\n{query}")
    handle = Entrez.esearch(db="pubmed", term=query, retmax=5000)
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"]

def main():
    # Removendo filtro de data e adicionando filtro para FONTES PRIMÁRIAS (NOT Review, NOT Systematic Review)
    
    # Tier 1 Ouro (Foco em qualquer ensaio bioquímico/polimerase em Filovírus)
    query_tier1 = '((ebolavirus OR "ebola virus" OR filovirus OR marburg OR SUDV)) AND ((polymerase OR "L protein" OR "L-protein" OR RNA-dependent)) AND ((inhibitor OR inhibition OR activity OR antiviral OR screening)) NOT (Review[Publication Type]) NOT (Systematic Review[Publication Type])'
    
    # Tier 2 Prata (Antivirais fenotípicos gerais, high-throughput screening, in vitro)
    query_tier2 = '((ebolavirus OR "ebola virus" OR filovirus OR marburg OR SUDV)) AND ((antiviral OR inhibitor OR compound OR "small molecule" OR screening OR therapeutic OR drug)) AND ((in vitro OR cell culture OR assay OR replication OR EC50 OR IC50)) NOT (Review[Publication Type]) NOT (Systematic Review[Publication Type])'
    
    # Tier 3 Bronze (Exploração Química, análogos, síntese de derivados)
    query_tier3 = '((ebolavirus OR "ebola virus" OR filovirus OR marburg)) AND ((nucleoside OR nucleotide OR analog OR derivative OR synthesis OR structure-activity OR SAR)) NOT (Review[Publication Type]) NOT (Systematic Review[Publication Type])'

    print("Iniciando Busca Massiva de Fontes Primárias no PubMed (>1500 meta)...\n")
    
    ids_t1 = fetch_pubmed_ids(query_tier1)
    print(f"-> TIER 1 (Enzimático/Estrutural Primário): {len(ids_t1)} papers encontrados.\n")
    
    ids_t2 = fetch_pubmed_ids(query_tier2)
    print(f"-> TIER 2 (Fenotípico Celular Primário): {len(ids_t2)} papers encontrados.\n")
    
    ids_t3 = fetch_pubmed_ids(query_tier3)
    print(f"-> TIER 3 (Química Sintética/Análogos Primários): {len(ids_t3)} papers encontrados.\n")

    output_dir = r"G:\Meu Drive\PROJETO-ANTIVIRAIS-NANOTECNOLOGIA-IA\1-META-ANALISE\1b-DADOS_EXTRAIDOS"
    os.makedirs(output_dir, exist_ok=True)
    
    csv_path = os.path.join(output_dir, "dataset_antivirals_massive_1500plus.csv")
    
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
    
    total = len(master_dict)
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        
        for pmid, info in master_dict.items():
            writer.writerow({
                "PMID": info["PMID"],
                "Suggested_Tier": info["Suggested_Tier"],
                "Reason_Tier": info["Reason"]
            })
            
    print(f"\nPLANILHA MASSIVA GERADA! Total de artigos PRIMÁRIOS (sem revisões): {total}")
    if total >= 1500:
        print("MÉTODO DE EXPANSÃO BEM SUCEDIDO: Objetivo de >1.500 papers primários alcançado.")
    print(f"Local: {csv_path}")

if __name__ == "__main__":
    main()
