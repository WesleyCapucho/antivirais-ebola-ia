import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def create_prisma_flowchart(output_path):
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.axis('off')

    def draw_box(ax, text, xy, width, height, facecolor='#ffffff'):
        box = patches.Rectangle(xy, width, height, linewidth=1.5, edgecolor='black', facecolor=facecolor, zorder=2)
        ax.add_patch(box)
        plt.text(xy[0] + width/2, xy[1] + height/2, text, ha='center', va='center', fontsize=11, wrap=True, fontweight='bold')
        return xy[0] + width/2, xy[1]

    def draw_arrow(ax, start, end):
        ax.annotate('', xy=end, xytext=start,
                    arrowprops=dict(facecolor='black', width=2, headwidth=10, shrink=0), zorder=1)

    # Identificação
    p1 = draw_box(ax, "Registros identificados via PubMed\n(n = 9.046)", (3, 10), 4, 1.2, '#e6f2ff')
    
    # Triagem 1
    p2 = draw_box(ax, "Triagem Inicial (Titles/Abstracts)\n(n = 9.046)", (3, 7.5), 4, 1.2, '#e6f2ff')
    draw_arrow(ax, (5, 10), (5, 8.7))
    
    # Exclusão 1
    p2_ex = draw_box(ax, "Registros Excluídos\n- Fora do Escopo\n- Revisões\n- Ausência de IC50/EC50\n(n = 8.113)", (7.5, 7.5), 3, 1.2, '#ffcccc')
    ax.plot([5, 7.5], [8.1, 8.1], color='black', linewidth=2, zorder=1)

    # Elegibilidade
    p3 = draw_box(ax, "Artigos recuperados em texto completo\npara avaliação de elegibilidade\n(n = 933) [TIER 1 OURO]", (3, 5), 4, 1.2, '#e6f2ff')
    draw_arrow(ax, (5, 7.5), (5, 6.2))

    # Exclusão 2
    p3_ex = draw_box(ax, "Excluídos por Risco de Viés (RoB)\n- Sem Controle Positivo\n- Pureza não relatada\n- Toxicity (SI < 10)\n(n = TBD)", (7.5, 5), 3, 1.2, '#ffcccc')
    ax.plot([5, 7.5], [5.6, 5.6], color='black', linewidth=2, zorder=1)

    # Inclusão
    p4 = draw_box(ax, "Estudos incluídos na Meta-Análise\ne Machine Learning (Fase 2)\n(n = TBD)", (3, 2.5), 4, 1.2, '#d9f2d9')
    draw_arrow(ax, (5, 5), (5, 3.7))

    plt.title("Fluxograma PRISMA: Seleção de Estudos (L-Polymerase Inibidores)", fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Fluxograma PRISMA gerado em: {output_path}")

if __name__ == "__main__":
    output_dir = r"G:\Meu Drive\PROJETO-ANTIVIRAIS-NANOTECNOLOGIA-IA\1-META-ANALISE\1c-ANALISES_ESTATISTICAS\1c7_figuras_tabelas_analise"
    os.makedirs(output_dir, exist_ok=True)
    create_prisma_flowchart(os.path.join(output_dir, "PRISMA_Flowchart.png"))
