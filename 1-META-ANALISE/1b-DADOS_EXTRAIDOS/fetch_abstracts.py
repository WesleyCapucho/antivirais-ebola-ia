import os
import csv
import time
from Bio import Entrez

Entrez.email = "wesley.pesquisa@antiviral.lab"

def fetch_details(pmid_list):
    """Busca detalhes (DOI, Título, Resumo, Ano) em lote via PubMed API."""
    results = {}
    
    # Processar em lotes de 100 para respeitar limites da API
    batch_size = 100
    for i in range(0, len(pmid_list), batch_size):
        batch = pmid_list[i:i+batch_size]
        print(f"Buscando metadados lote {i//batch_size + 1}...")
        try:
            handle = Entrez.efetch(db="pubmed", id=",".join(batch), retmode="xml")
            records = Entrez.read(handle)
            handle.close()
            
            for article in records['PubmedArticle']:
                pmid = str(article['MedlineCitation']['PMID'])
                article_data = article['MedlineCitation']['Article']
                
                # Extrair Ano
                year = ""
                try:
                    if 'PubDate' in article_data['Journal']['JournalIssue']:
                        year = article_data['Journal']['JournalIssue']['PubDate'].get('Year', '')
                except:
                    pass
                
                # Extrair Abstract
                abstract = ""
                if 'Abstract' in article_data and 'AbstractText' in article_data['Abstract']:
                    abstract = " ".join([str(text) for text in article_data['Abstract']['AbstractText']])
                    
                # Extrair DOI
                doi = ""
                if 'ELocationID' in article_data:
                    for eloc in article_data['ELocationID']:
                        if eloc.attributes.get('EIdType') == 'doi':
                            doi = str(eloc)
                            break
                            
                # Se não achou DOI, procura em PubmedData
                if not doi and 'PubmedData' in article and 'ArticleIdList' in article['PubmedData']:
                    for aid in article['PubmedData']['ArticleIdList']:
                        if aid.attributes.get('IdType') == 'doi':
                            doi = str(aid)
                            break
                            
                results[pmid] = {
                    "Year": year,
                    "Abstract": abstract,
                    "DOI": doi
                }
        except Exception as e:
            print(f"Erro no lote: {e}")
        time.sleep(1) # Rate limit gentil
        
    return results

def main():
    csv_path = r"G:\Meu Drive\PROJETO-ANTIVIRAIS-NANOTECNOLOGIA-IA\1-META-ANALISE\1b-DADOS_EXTRAIDOS\dataset_antivirals_tiered_v1.csv"
    output_path = r"G:\Meu Drive\PROJETO-ANTIVIRAIS-NANOTECNOLOGIA-IA\1-META-ANALISE\1b-DADOS_EXTRAIDOS\dataset_antivirals_tiered_v1_enriched.csv"
    
    # 1. Ler o CSV base
    rows = []
    pmids = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        if "Abstract" not in fieldnames:
            fieldnames.append("Abstract") # Adicionando coluna
        for row in reader:
            rows.append(row)
            pmids.append(row["PMID"])
            
    print(f"Total de PMIDs para extrair dados: {len(pmids)}")
    
    # 2. Buscar detalhes no PubMed
    details = fetch_details(pmids)
    
    # 3. Atualizar linhas
    for row in rows:
        pmid = row["PMID"]
        if pmid in details:
            row["DOI"] = details[pmid]["DOI"]
            row["Year"] = details[pmid]["Year"]
            row["Abstract"] = details[pmid]["Abstract"]
            
    # 4. Salvar novo CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"\nExtração concluída! Planilha enriquecida salva em: {output_path}")

if __name__ == "__main__":
    main()
