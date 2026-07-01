import os
import csv
import re

def parse_bioactivity(nlp_string):
    """Converte strings como 'IC50 <1.5 uM | EC50 45 nM' para um valor numérico em micromolar."""
    if not nlp_string:
        return None
        
    # Pega o primeiro valor encontrado por simplicidade (ou o mais razoável)
    # A string já tem o formato "METRICA MODIFICADORVALOR UNIDADE"
    parts = nlp_string.split('|')
    for part in parts:
        match = re.search(r'([\d\.]+)\s*(uM|nM|microM|nanoM|μM)', part, re.IGNORECASE)
        if match:
            val = float(match.group(1))
            unit = match.group(2).lower()
            if unit in ['nm', 'nanom']:
                return val / 1000.0 # converte para uM
            return val
    return None

def assess_rob_from_abstract(abstract):
    """Avaliação de Risco de Viés Automática usando heurísticas no texto."""
    if not abstract:
        return 0, "No"
    
    score = 1 # Base score
    abstract_lower = abstract.lower()
    
    # Critério 1: Toxicidade avaliada?
    has_tox = "No"
    if any(k in abstract_lower for k in ['cc50', 'cytotoxicity', 'selectivity index', 'si ']):
        score += 2
        has_tox = "Yes"
        
    # Critério 2: Enzima purificada ou mecanismo validado?
    if any(k in abstract_lower for k in ['purified', 'recombinant', 'polymerase assay', 'rdrp assay']):
        score += 2
        
    return score, has_tox

def main():
    input_csv = r"G:\Meu Drive\PROJETO-ANTIVIRAIS-NANOTECNOLOGIA-IA\1-META-ANALISE\1b-DADOS_EXTRAIDOS\dataset_tier1_ouro_nlp_curated.csv"
    output_csv = r"G:\Meu Drive\PROJETO-ANTIVIRAIS-NANOTECNOLOGIA-IA\1-META-ANALISE\1b-DADOS_EXTRAIDOS\dataset_tier1_FINAL_curado.csv"
    
    if not os.path.exists(input_csv):
        print(f"Erro: Arquivo base não encontrado: {input_csv}")
        return

    curated_data = []
    total_valid = 0
    
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ec50_clean = parse_bioactivity(row.get('Bioactivity_Extracted_NLP', ''))
            rob, tox = assess_rob_from_abstract(row.get('Abstract', ''))
            
            # Só aceitar se acharmos um EC50 numérico limpo
            if ec50_clean is not None:
                new_row = {
                    "PMID": row["PMID"],
                    "DOI": row["DOI"],
                    "Year": row["Year"],
                    "EC50_uM_Clean": round(ec50_clean, 4),
                    "Toxicity_Reported_Yes_No": tox,
                    "RoB_Score_AI": rob,
                    "Quality_Label": "High Quality" if rob >= 3 else "Low Quality (Review Needed)",
                    "Raw_NLP_Extracted": row.get("Bioactivity_Extracted_NLP", "")
                }
                curated_data.append(new_row)
                total_valid += 1
                
    if not curated_data:
        print("Nenhum dado numérico pôde ser curado. O dataset não possuía extrações válidas.")
        return
        
    fieldnames = ["PMID", "DOI", "Year", "EC50_uM_Clean", "Toxicity_Reported_Yes_No", "RoB_Score_AI", "Quality_Label", "Raw_NLP_Extracted"]
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(curated_data)
        
    print(f"Curadoria finalizada! {total_valid} artigos superaram o funil estrito e possuem EC50 limpos.")
    print(f"Planilha salva em: {output_csv}")

if __name__ == "__main__":
    main()
