import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def create_final_prisma():
    output_dir = r"G:\Meu Drive\PROJETO-ANTIVIRAIS-NANOTECNOLOGIA-IA\5-PUBLICACOES\Figuras_Main"
    os.makedirs(output_dir, exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(10, 12), dpi=300)
    ax.axis('off')
    
    # Caixas (x, y, w, h)
    boxes = [
        {"rect": (0.25, 0.85, 0.5, 0.1), "text": "Identification:\nArticles found via NLP\n(n = 9,046)"},
        {"rect": (0.25, 0.65, 0.5, 0.1), "text": "Screening:\nAbstracts curated by AI\n(n = 933)"},
        {"rect": (0.6, 0.5, 0.35, 0.1), "text": "Excluded (No EC50/IC50 data)\n(n = 931)"},
        {"rect": (0.25, 0.45, 0.5, 0.1), "text": "Pivot Strategy:\nChEMBL API Massive Mining\n(Ebolavirus Bioassays)"},
        {"rect": (0.25, 0.25, 0.5, 0.1), "text": "Included:\nFinal Audited Dataset\n(n = 906 molecules)"}
    ]
    
    for b in boxes:
        rect = patches.Rectangle((b["rect"][0], b["rect"][1]), b["rect"][2], b["rect"][3], 
                                 linewidth=2, edgecolor='#2c3e50', facecolor='#ecf0f1')
        ax.add_patch(rect)
        ax.text(b["rect"][0] + b["rect"][2]/2, b["rect"][1] + b["rect"][3]/2, b["text"], 
                horizontalalignment='center', verticalalignment='center', fontsize=12, fontweight='bold', color='#2c3e50')
        
    # Setas
    ax.annotate('', xy=(0.5, 0.75), xytext=(0.5, 0.85), arrowprops=dict(arrowstyle="->", lw=2))
    ax.annotate('', xy=(0.5, 0.55), xytext=(0.5, 0.65), arrowprops=dict(arrowstyle="->", lw=2))
    ax.annotate('', xy=(0.6, 0.55), xytext=(0.5, 0.55), arrowprops=dict(arrowstyle="->", lw=2))
    ax.annotate('', xy=(0.5, 0.35), xytext=(0.5, 0.45), arrowprops=dict(arrowstyle="->", lw=2))
    
    plt.title("PRISMA Flow Diagram (Updated for Massive Data Mining)", fontsize=16, fontweight='bold', pad=20)
    
    fig_path = os.path.join(output_dir, 'Fig1_PRISMA_Flowchart_Final.png')
    plt.savefig(fig_path, bbox_inches='tight')
    plt.close()
    print(f"[+] PRISMA salvo em {fig_path}")

if __name__ == "__main__":
    create_final_prisma()
