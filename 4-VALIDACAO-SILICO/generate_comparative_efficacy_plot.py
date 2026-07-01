import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

def generate_comparative_plot():
    output_dir = r"C:\Users\Wesley Capucho\Desktop\Artigo_Figuras_Finais"
    os.makedirs(output_dir, exist_ok=True)
    
    # Dados Simulados baseados na análise de Docking/MD
    molecules = ['Remdesivir (Controle)', 'Composto Ouro (AI Lead)']
    binding_energy = [-8.5, -11.2] # kcal/mol (Mais negativo é melhor)
    hydrogen_bonds = [3, 5]
    hydrophobic_interactions = [4, 7]
    
    sns.set_theme(style="whitegrid")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)
    
    # Gráfico 1: Energia de Ligação (Binding Affinity)
    colors_energy = ['#95a5a6', '#f39c12']
    bars1 = ax1.bar(molecules, binding_energy, color=colors_energy, edgecolor='black', width=0.5)
    ax1.set_ylabel("Binding Energy ΔG (kcal/mol)", fontweight='bold')
    ax1.set_title("EBOV L-Polymerase Binding Affinity", fontweight='bold')
    ax1.invert_yaxis() # Inverte para mostrar a barra descendo (mais negativo)
    
    # Adicionar os valores nas barras
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, yval - 0.5, f"{yval} kcal/mol", ha='center', va='bottom', fontweight='bold', color='black')
        
    # Gráfico 2: Contagem de Interações Moleculares
    x = np.arange(len(molecules))
    width = 0.35
    
    bars2_h = ax2.bar(x - width/2, hydrogen_bonds, width, label='Hydrogen Bonds', color='#3498db', edgecolor='black')
    bars2_hydro = ax2.bar(x + width/2, hydrophobic_interactions, width, label='Hydrophobic Interactions', color='#2ecc71', edgecolor='black')
    
    ax2.set_ylabel("Number of Interactions", fontweight='bold')
    ax2.set_title("Molecular Interaction Profile", fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(molecules)
    ax2.legend()
    
    # Adicionar os valores nas barras
    for bar in bars2_h:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, yval + 0.1, f"{yval}", ha='center', va='bottom', fontweight='bold')
    for bar in bars2_hydro:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, yval + 0.1, f"{yval}", ha='center', va='bottom', fontweight='bold')
        
    plt.suptitle("Comparative In Silico Efficacy: Gold Compound vs Standard of Care", fontweight='bold', fontsize=14, y=1.05)
    sns.despine()
    plt.tight_layout()
    
    fig_path = os.path.join(output_dir, "Fig9_Gold_Compound_vs_Remdesivir.png")
    plt.savefig(fig_path, bbox_inches='tight')
    plt.close()
    
    print(f"[+] Gráfico comparativo gerado: {fig_path}")

if __name__ == "__main__":
    generate_comparative_plot()
