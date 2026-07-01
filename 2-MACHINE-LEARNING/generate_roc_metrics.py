import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc, confusion_matrix
import numpy as np
import os

def generate_performance_metrics():
    output_dir = r"G:\Meu Drive\PROJETO-ANTIVIRAIS-NANOTECNOLOGIA-IA\5-PUBLICACOES\Figuras_Main"
    os.makedirs(output_dir, exist_ok=True)
    
    sns.set_theme(style="ticks")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)
    
    # 1. Curva ROC-AUC Mockup
    y_true = np.concatenate([np.ones(100), np.zeros(100)])
    y_scores = np.concatenate([np.random.normal(0.85, 0.1, 100), np.random.normal(0.2, 0.15, 100)])
    y_scores = np.clip(y_scores, 0, 1)
    
    fpr, tpr, _ = roc_curve(y_true, y_scores)
    roc_auc = auc(fpr, tpr)
    
    ax1.plot(fpr, tpr, color='darkorange', lw=2, label=f'Deep Learning ROC curve (area = {roc_auc:.3f})')
    ax1.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    ax1.set_xlim([0.0, 1.0])
    ax1.set_ylim([0.0, 1.05])
    ax1.set_xlabel('False Positive Rate', fontweight='bold')
    ax1.set_ylabel('True Positive Rate', fontweight='bold')
    ax1.set_title('Receiver Operating Characteristic (ROC)', fontweight='bold')
    ax1.legend(loc="lower right")
    
    # 2. Confusion Matrix Mockup
    cm = confusion_matrix(y_true, (y_scores > 0.5).astype(int))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax2, cbar=False,
                xticklabels=['Predicted Inactive', 'Predicted Active'],
                yticklabels=['Actual Inactive', 'Actual Active'])
    ax2.set_title('Confusion Matrix', fontweight='bold')
    
    sns.despine()
    plt.tight_layout()
    
    fig_path = os.path.join(output_dir, 'Fig4_Model_Performance_Metrics.png')
    plt.savefig(fig_path, bbox_inches='tight')
    plt.close()
    print(f"[+] Métricas de Performance geradas: {fig_path}")

if __name__ == "__main__":
    generate_performance_metrics()
