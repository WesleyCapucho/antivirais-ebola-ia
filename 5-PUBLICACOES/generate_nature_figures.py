import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

def generate_figures():
    """
    Gera gráficos com qualidade de publicação (Nature/Science) baseados no dataset auditado.
    """
    input_file = r"G:\Meu Drive\PROJETO-ANTIVIRAIS-NANOTECNOLOGIA-IA\1-META-ANALISE\1b-DADOS_EXTRAIDOS\dataset_ebola_massive_AUDITED.csv"
    output_dir = r"G:\Meu Drive\PROJETO-ANTIVIRAIS-NANOTECNOLOGIA-IA\5-PUBLICACOES\Figuras_Main"
    os.makedirs(output_dir, exist_ok=True)
    
    # Mock de dados se o arquivo não existir localmente para simular o layout
    if os.path.exists(input_file):
        df = pd.read_csv(input_file)
    else:
        print("[!] Arquivo real não encontrado. Gerando gráficos de demonstração estrutural...")
        import numpy as np
        df = pd.DataFrame({
            'Value_nM': np.concatenate([np.random.normal(5000, 1500, 400), np.random.normal(15000, 3000, 480)]),
            'Is_Active': np.concatenate([np.ones(400), np.zeros(480)])
        })

    # Estética Acadêmica Sênior (Nature Style)
    sns.set_theme(style="ticks", palette="pastel")
    plt.rcParams.update({'font.size': 12, 'font.family': 'sans-serif'})
    
    # ==========================================
    # Figura 1A: Distribuição de Atividade
    # ==========================================
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
    sns.histplot(data=df, x='Value_nM', hue='Is_Active', multiple="stack", 
                 palette=['#e74c3c', '#2ecc71'], bins=40, kde=True, ax=ax)
    
    ax.set_title('Ebolavirus Inhibitor Bioactivity Distribution (ChEMBL)', fontweight='bold', pad=15)
    ax.set_xlabel('Inhibitory Concentration (EC50/IC50 in nM)')
    ax.set_ylabel('Molecular Count')
    ax.legend(title='Compound Status', labels=['Active (< 10 µM)', 'Inactive'])
    sns.despine()
    
    fig1_path = os.path.join(output_dir, 'Fig1A_Bioactivity_Distribution.png')
    plt.savefig(fig1_path, bbox_inches='tight')
    plt.close()
    
    print(f"[+] Gráfico de Distribuição gerado: {fig1_path}")
    
if __name__ == "__main__":
    generate_figures()
