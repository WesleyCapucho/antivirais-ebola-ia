import pandas as pd
import numpy as np
import os

def run_audit():
    input_file = r"G:\Meu Drive\PROJETO-ANTIVIRAIS-NANOTECNOLOGIA-IA\1-META-ANALISE\1b-DADOS_EXTRAIDOS\dataset_ebola_massive_chembl_FINAL.csv"
    output_file = r"G:\Meu Drive\PROJETO-ANTIVIRAIS-NANOTECNOLOGIA-IA\1-META-ANALISE\1b-DADOS_EXTRAIDOS\dataset_ebola_massive_AUDITED.csv"
    
    if not os.path.exists(input_file):
        print("[-] Arquivo bruto não encontrado. Verifique o sincronismo do Google Drive.")
        return
        
    print("[*] Iniciando Auditoria Forense do Dataset ChEMBL...")
    df = pd.read_csv(input_file)
    initial_count = len(df)
    
    # 1. Tratamento de Duplicatas (SMILES idênticos)
    # Tira a mediana do Value_nM para laboratórios que testaram a mesma molécula
    print("[*] Consolidando duplicatas moleculares...")
    df = df.groupby('SMILES', as_index=False).mean(numeric_only=True)
    
    # Recalcula Is_Active baseado na média
    df['Is_Active'] = (df['Value_nM'] < 10000).astype(int)
    
    # 2. Remoção de Outliers (Z-score > 3 no Value_nM)
    print("[*] Aplicando Guilhotina Matemática (Remoção de Outliers)...")
    z_scores = np.abs((df['Value_nM'] - df['Value_nM'].mean()) / df['Value_nM'].std())
    df = df[z_scores < 3]
    
    final_count = len(df)
    df.to_csv(output_file, index=False)
    
    print("="*50)
    print(" RELATÓRIO FORENSE DE DADOS")
    print("="*50)
    print(f" Moléculas Iniciais: {initial_count}")
    print(f" Moléculas Duplicadas/Outliers Removidas: {initial_count - final_count}")
    print(f" Moléculas Puras (Auditadas): {final_count}")
    print(f" Arquivo Ouro Salvo: {output_file}")
    print("="*50)

if __name__ == "__main__":
    run_audit()
