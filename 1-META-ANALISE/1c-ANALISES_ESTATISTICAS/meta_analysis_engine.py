import numpy as np
import matplotlib.pyplot as plt
import os

def create_forest_plot(output_path):
    # Dados Simulados (Substituiremos pelos dados curados do Tier 1)
    studies = [
        "Wang et al. (2023)", "Chen et al. (2022)", 
        "Smith et al. (2021)", "Johnson et al. (2020)", 
        "Patel et al. (2019)"
    ]
    
    # Efeitos (ex: log(IC50) ou diferença de médias) e Intervalos de Confiança (95% CI)
    effects = np.array([-1.2, -0.8, -1.5, -0.5, -1.1])
    ci_lower = np.array([-1.8, -1.3, -2.1, -1.0, -1.6])
    ci_upper = np.array([-0.6, -0.3, -0.9,  0.0, -0.6])
    
    # Efeito Agrupado (Pooled Effect via Random Effects Model - Simulação)
    pooled_effect = -1.02
    pooled_ci_lower = -1.35
    pooled_ci_upper = -0.69
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Plotar os estudos individuais
    y_pos = np.arange(len(studies), 0, -1)
    ax.errorbar(effects, y_pos, xerr=[effects - ci_lower, ci_upper - effects], 
                fmt='s', color='black', ecolor='gray', capsize=4, markersize=8)
    
    # Plotar o efeito agrupado (Losango / Diamond)
    diamond_x = [pooled_ci_lower, pooled_effect, pooled_ci_upper, pooled_effect]
    diamond_y = [0, 0.2, 0, -0.2]
    ax.add_patch(plt.Polygon(np.column_stack((diamond_x, diamond_y)), color='blue'))
    
    # Linha de nulidade
    ax.axvline(x=0, color='red', linestyle='--', label='No Effect (Linha Nula)')
    ax.axvline(x=pooled_effect, color='blue', linestyle=':', label='Pooled Effect')
    
    # Formatação do eixo Y
    ax.set_yticks(np.append(y_pos, 0))
    ax.set_yticklabels(studies + ['Pooled Effect (I²=32%)'])
    
    # Ajustes estéticos
    ax.set_xlabel('Effect Size (Standardized Mean Difference)')
    ax.set_title('Forest Plot: Eficácia de Inibidores da L-Polymerase vs Controle', pad=15)
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"Forest Plot gerado em: {output_path}")

if __name__ == "__main__":
    output_dir = r"G:\Meu Drive\PROJETO-ANTIVIRAIS-NANOTECNOLOGIA-IA\1-META-ANALISE\1c-ANALISES_ESTATISTICAS\1c7_figuras_tabelas_analise"
    os.makedirs(output_dir, exist_ok=True)
    create_forest_plot(os.path.join(output_dir, "Forest_Plot_Mockup.png"))
