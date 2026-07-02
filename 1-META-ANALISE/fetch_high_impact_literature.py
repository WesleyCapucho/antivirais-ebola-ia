from Bio import Entrez
import json
import os
import re

def clean_text(text):
    if not text: return ""
    return re.sub(r'[^a-zA-Z0-9\s.,?!-]', '', str(text))

def generate_bibtex_key(author, year):
    if not author: author = "Unknown"
    last_name = author.split()[-1].replace(",", "").replace(".", "")
    return f"{last_name}{year}"

def fetch_pubmed_literature():
    print("[*] Conectando à API do PubMed (NCBI)...")
    Entrez.email = "wesley.capucho@ai.science"
    
    query = "ebola AND (machine learning OR molecular docking OR virtual screening OR drug discovery)"
    print(f"[*] Buscando: {query}")
    
    try:
        # Busca os IDs
        handle = Entrez.esearch(db="pubmed", term=query, retmax=1000, sort="relevance")
        record = Entrez.read(handle)
        handle.close()
        
        id_list = record["IdList"]
        print(f"[+] Encontrados {len(id_list)} artigos no PubMed.")
        
        if not id_list:
            print("[-] Nenhum artigo encontrado.")
            return
            
        # Puxa os dados dos artigos
        handle = Entrez.efetch(db="pubmed", id=id_list, retmode="xml")
        articles = Entrez.read(handle)
        handle.close()
        
        bibtex_entries = []
        markdown_lines = []
        
        markdown_lines.append("# Literatura Curada: Ebola + Inteligência Artificial / Docking")
        markdown_lines.append(f"Esta lista contém {len(id_list)} artigos extraídos do **PubMed** de alta relevância.\n")
        
        for i, article in enumerate(articles['PubmedArticle']):
            medline = article['MedlineCitation']
            article_data = medline['Article']
            
            title = clean_text(article_data.get('ArticleTitle', 'No Title'))
            
            # Puxando o ano
            year = "2020"
            try:
                year = article_data['Journal']['JournalIssue']['PubDate']['Year']
            except:
                pass
                
            # Puxando o DOI
            doi = ""
            for ids in article['PubmedData']['ArticleIdList']:
                if ids.attributes.get('IdType') == 'doi':
                    doi = str(ids)
                    break
            
            # Puxando o autor
            first_author = "Unknown"
            authors = article_data.get('AuthorList', [])
            if authors:
                try:
                    first_author = authors[0]['LastName']
                except:
                    pass
                    
            bib_key = generate_bibtex_key(first_author, year)
            
            # Cria a entrada BibTeX
            bibtex = f"""@article{{{bib_key},
  title={{{title}}},
  author={{{first_author} and others}},
  year={{{year}}},
  doi={{{doi}}},
  journal={{{article_data['Journal'].get('Title', 'Unknown Journal')}}}
}}"""
            bibtex_entries.append(bibtex)
            
            # Cria a entrada MarkDown
            link = f"https://pubmed.ncbi.nlm.nih.gov/{medline['PMID']}/"
            md_entry = f"{i+1}. **{title}** ({year}). *{first_author} et al.* [PubMed Link]({link})"
            if doi:
                md_entry += f" | [DOI](https://doi.org/{doi})"
            markdown_lines.append(md_entry)
            
        # Salvando BibTeX e Lista
        # Desktop
        desktop_dir = r"C:\Users\Wesley Capucho\Desktop\Artigo_1_Ebola_AI"
        os.makedirs(desktop_dir, exist_ok=True)
        
        bib_path_desktop = os.path.join(desktop_dir, "referencias_massivas_1000.bib")
        md_path_desktop = os.path.join(desktop_dir, "lista_literatura_1000.md")
        
        with open(bib_path_desktop, "w", encoding="utf-8") as f:
            f.write("\n\n".join(bibtex_entries))
            
        with open(md_path_desktop, "w", encoding="utf-8") as f:
            f.write("\n".join(markdown_lines))
            
        print(f"[+] BibTeX gerado em: {bib_path_desktop}")
        print(f"[+] Tabela Resumo gerada em: {md_path_desktop}")
        
    except Exception as e:
        print(f"[-] Erro ao puxar dados do PubMed: {str(e)}")

if __name__ == "__main__":
    fetch_pubmed_literature()
