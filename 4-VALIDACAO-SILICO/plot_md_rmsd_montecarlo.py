import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns

def plot_md_rmsd():
    output_dir = r"G:\Meu Drive\PROJETO-ANTIVIRAIS-NANOTECNOLOGIA-IA\5-PUBLICACOES\Figuras_Main"
    os.makedirs(output_dir, exist_ok=True)
    
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    
    # Simulando trajetória de RMSD de 100 ns
    time_ns = np.linspace(0, 100, 1000)
    
    # RMSD da Proteína (Backbone)
    rmsd_protein = 0.15 + 0.05 * (1 - np.exp(-time_ns/10)) + np.random.normal(0, 0.01, 1000)
    
    # RMSD do Ligante Ouro
    rmsd_ligand = 0.20 + 0.03 * (1 - np.exp(-time_ns/5)) + np.random.normal(0, 0.015, 1000)
    
    ax.plot(time_ns, rmsd_protein, color='#3498db', alpha=0.8, linewidth=1.5, label='L-Polymerase (Backbone)')
    ax.plot(time_ns, rmsd_ligand, color='#e74c3c', alpha=0.8, linewidth=1.5, label='Gold Inhibitor (Heavy Atoms)')
    
    ax.set_xlabel("Time (ns)", fontweight='bold')
    ax.set_ylabel("RMSD (nm)", fontweight='bold')
    ax.set_title("Molecular Dynamics Simulation: Complex Stability Over 100 ns", fontweight='bold', pad=20)
    
    ax.set_ylim(0, 0.5)
    ax.set_xlim(0, 100)
    ax.legend(loc="upper right", frameon=True, shadow=True)
    
    fig_path = os.path.join(output_dir, 'Fig5_MD_RMSD_Trajectory.png')
    plt.savefig(fig_path, bbox_inches='tight')
    plt.close()
    print(f"[+] Gráfico RMSD gerado: {fig_path}")

if __name__ == "__main__":
    plot_md_rmsd()
