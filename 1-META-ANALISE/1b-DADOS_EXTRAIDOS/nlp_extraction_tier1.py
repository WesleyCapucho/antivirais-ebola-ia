import os
import csv
import time
import re
from Bio import Entrez

Entrez.email = "wesley.pesquisa@antiviral.lab"

def extract_bioactivity(text):
    """Extrai valores de IC50/EC50 de textos não estruturados usando Regex."""
    if not text:
        return ""
    
    # Padrão para encontrar: "IC50 = 1.5 uM", "EC50 of 45 nM", "IC50 12.3 μM"
    pattern = r"(?i)(IC50|EC50|IC_{50}|EC_{50}|Kd|Ki)[ \t:=]*(?:of)?\s*(<|>|~)?\s*([\d\.]+)\s*(uM|nM|microM|nanoM|μM)"
    matches = re.findall(pattern, text)
    
    results = []
    for m in matches:
        metric = m[0].upper().replace("_{50}", "50")
        modifier = m[1]
        value = m[2]
        unit = m[3]
        results.append(f"{metric} {modifier}{value} {unit}".replace("  ", " "))
        
    return " | ".join(results) if results else ""

def fetch_tier1_abstracts(pmid_list):
    results = {}
    batch_size = 150
    total_batches = (len(pmid_list) // batch_size) + 1
    
    for i in range(0, len(pmid_list), batch_size):
        batch = pmid_list[i:i+batch_size]
        print(f"[{i//batch_size + 1}/{total_batches}] Baixando lote do NCBI ({len(batch)} artigos)...")
        try:
            handle = Entrez.efetch(db="pubmed", id=",".join(batch), retmode="xml")
            records = Entrez.read(handle)
            handle.close()
            
            for article in records['PubmedArticle']:
                pmid = str(article['MedlineCitation']['PMID'])
                article_data = article['MedlineCitation']['Article']
                
                year = ""
                try:
                    if 'PubDate' in article_data['Journal']['JournalIssue']:
                        year = article_data['Journal']['JournalIssue']['PubDate'].get('Year', '')
                except:
                    pass
                
                abstract = ""
                if 'Abstract' in article_data and 'AbstractText' in article_data['Abstract']:
                    abstract = " ".join([str(text) for text in article_data['Abstract']['AbstractText']])
                    
                doi = ""
                if 'ELocationID' in article_data:
                    for eloc in article_data['ELocationID']:
                        if eloc.attributes.get('EIdType') == 'doi':
                            doi = str(eloc)
                            break
                            
                # NLP Analysis na mosca
                bioactivity_extracted = extract_bioactivity(abstract)
                
                results[pmid] = {
                    "Year": year,
                    "DOI": doi,
                    "Abstract": abstract,
                    "Bioactivity_Extracted": bioactivity_extracted
                }
        except Exception as e:
            print(f"Erro no lote {i//batch_size + 1}: {e}")
        time.sleep(1.5) # Respeitando limites do NCBI
        
    return results

def main():
    input_csv = r"G:\Meu Drive\PROJETO-ANTIVIRAIS-NANOTECNOLOGIA-IA\1-META-ANALISE\1b-DADOS_EXTRAIDOS\dataset_antivirals_massive_1500plus.csv"
    output_csv = r"G:\Meu Drive\PROJETO-ANTIVIRAIS-NANOTECNOLOGIA-IA\1-META-ANALISE\1b-DADOS_EXTRAIDOS\dataset_tier1_ouro_nlp_curated.csv"
    
    tier1_pmids = []
    base_rows = {}
    
    # Filtrar apenas o Ouro (Tier 1)
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Suggested_Tier"] == "1.0":
                tier1_pmids.append(row["PMID"])
                base_rows[row["PMID"]] = row

    print(f"Total de Artigos Tier 1 (Ouro) separados para o NLP: {len(tier1_pmids)}\n")
    
    details = fetch_tier1_abstracts(tier1_pmids)
    
    # Salvar resultados
    fieldnames = [
        "PMID", "DOI", "Year", "Suggested_Tier", "Reason_Tier", 
        "Bioactivity_Extracted_NLP", "Abstract"
    ]
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for pmid in tier1_pmids:
            if pmid in details:
                writer.writerow({
                    "PMID": pmid,
                    "DOI": details[pmid]["DOI"],
                    "Year": details[pmid]["Year"],
                    "Suggested_Tier": "1.0",
                    "Reason_Tier": base_rows[pmid]["Reason_Tier"],
                    "Bioactivity_Extracted_NLP": details[pmid]["Bioactivity_Extracted"],
                    "Abstract": details[pmid]["Abstract"]
                })
                
    print(f"\nSucesso! Planilha Ouro Otimizada por IA gerada em:\n{output_csv}")

if __name__ == "__main__":
    main()
