import requests
import json
import os

def fetch_uniprot_data(accession="Q05318"):
    print(f"[*] Fetching UniProt Metadata for Accession: {accession}")
    url = f"https://rest.uniprot.org/uniprotkb/{accession}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"    - Protein: {data.get('proteinDescription', {}).get('recommendedName', {}).get('fullName', {}).get('value')}")
        
        # Extract GO terms
        go_terms = [x for x in data.get('dbReferences', []) if x['type'] == 'GO']
        functions = [go['properties']['term'] for go in go_terms if go['properties']['term'].startswith('F:')]
        print("    - Molecular Functions (GO):")
        for f in functions[:3]:
            print(f"        * {f}")
            
        return data
    else:
        print("[!] Failed to fetch UniProt data.")
        return None

def fetch_pdb_metadata(pdb_id="7YI7"):
    print(f"\n[*] Fetching PDB Crystallography Metadata for: {pdb_id}")
    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        title = data.get('struct', {}).get('title')
        method = data.get('exptl', [{}])[0].get('method')
        resolution = data.get('rcsb_entry_info', {}).get('resolution_combined', [None])[0]
        
        print(f"    - Title: {title}")
        print(f"    - Method: {method}")
        print(f"    - Resolution: {resolution} Angstroms")
        return data
    else:
        print("[!] Failed to fetch PDB data.")
        return None

def fetch_string_network(identifier="Q05318"):
    print(f"\n[*] Fetching STRING Protein-Protein Interaction (PPI) Network for: {identifier}")
    # We use 186538 (Ebola virus taxon id)
    url = f"https://string-db.org/api/json/network?identifiers={identifier}&species=186538"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"    - Found {len(data)} high-confidence interactions.")
        for interaction in data[:5]:
            print(f"        * {interaction['preferredName_A']} <-> {interaction['preferredName_B']} (Score: {interaction['score']})")
        return data
    else:
        print("[!] Failed to fetch STRING data.")
        return None

if __name__ == "__main__":
    print("==================================================")
    print("   Ebola AI - Biological Context Fetcher v1.0")
    print("==================================================")
    
    uniprot = fetch_uniprot_data("Q05318")
    pdb = fetch_pdb_metadata("7YI7")  # 7YI7 is EBOV L-Polymerase complex
    string_net = fetch_string_network("Q05318")
    
    print("\n[+] Systems Biology data extraction complete. Ready for manuscript integration.")
