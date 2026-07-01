import matplotlib.pyplot as plt
import numpy as np
import os

def create_forest_plot():
    output_dir = r"G:\Meu Drive\PROJETO-ANTIVIRAIS-NANOTECNOLOGIA-IA\5-PUBLICACOES\Figuras_Main"
    os.makedirs(output_dir, exist_ok=True)
    
    compounds = ['Remdesivir (Control)', 'Favipiravir (Control)', 'ChEMBL_Ouro_1', 'ChEMBL_Ouro_2', 'ChEMBL_Ouro_3']
    mean_ec50 = [250.0, 500.0, 15.2, 28.4, 45.1]
    ci_lower = [200.0, 450.0, 10.0, 20.0, 35.0]
    ci_upper = [300.0, 550.0, 20.0, 35.0, 55.0]
    
    y_pos = np.arange(len(compounds))
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    
    for i in range(len(compounds)):
        ax.plot([ci_lower[i], ci_upper[i]], [y_pos[i], y_pos[i]], color='black', lw=2)
        ax.plot(mean_ec50[i], y_pos[i], 's', color='#c0392b' if 'Control' in compounds[i] else '#27ae60', markersize=10)
        
    ax.axvline(100.0, color='gray', linestyle='--', alpha=0.5) # Linha de corte de alta eficácia (100 nM)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(compounds, fontsize=12, fontweight='bold')
    ax.invert_yaxis()
    ax.set_xlabel('Inhibitory Concentration EC50 (nM)\n<-- Better Inhibition', fontsize=12, fontweight='bold')
    ax.set_title('Forest Plot: Efficacy of Top AI Candidates vs Standard Controls', fontsize=16, fontweight='bold', pad=20)
    
    fig_path = os.path.join(output_dir, 'Fig2_Forest_Plot_Top_Hits.png')
    plt.savefig(fig_path, bbox_inches='tight')
    plt.close()
    print(f"[+] Forest Plot salvo em {fig_path}")

if __name__ == "__main__":
    create_forest_plot()
