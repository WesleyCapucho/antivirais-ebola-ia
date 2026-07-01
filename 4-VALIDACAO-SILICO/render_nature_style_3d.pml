# PyMOL Script Automático: Renderização de Docking (Padrão Nature/Science)
# Uso: pymol -cq render_nature_style_3d.pml

# 1. Carregamento das Estruturas
load "G:/Meu Drive/PROJETO-ANTIVIRAIS-NANOTECNOLOGIA-IA/0-ESTRUTURAS_PDB/7YIG_clean.pdb", receptor
load "G:/Meu Drive/PROJETO-ANTIVIRAIS-NANOTECNOLOGIA-IA/3-SCREENING-OTIMIZACAO/resultados_docking/Composto_Ouro_1_docked.sdf", ligante

# 2. Configurações de Fundo e Luz (Estética Limpa)
bg_color white
set ray_trace_mode, 1
set ray_shadow, 0
set ambient, 0.4
set specular, 0.5
set depth_cue, 1

# 3. Estilização do Receptor (Vírus)
hide all
show surface, receptor
color gray80, receptor
set transparency, 0.3

# 4. Estilização do Ligante (Inibidor)
show sticks, ligante
color orange, ligante
util.cnc ligante   # Carbonos laranjas, Nitrogênios azuis, Oxigênios vermelhos
set stick_radius, 0.15

# 5. Destaque do Sítio Ativo (Ciano Metálico)
# Seleciona todos os aminoácidos da proteína a menos de 5 Angstroms do ligante
select sitio_ativo, byres receptor within 5.0 of ligante
show sticks, sitio_ativo
color cyan, sitio_ativo
util.cnc sitio_ativo

# 6. Mapeamento de Pontes de Hidrogênio (H-Bonds)
distance hbonds, receptor, ligante, 3.2, mode=2
hide labels, hbonds
set dash_color, yellow
set dash_radius, 0.05
set dash_gap, 0.15

# 7. Posicionamento de Câmera e Renderização
zoom sitio_ativo, 2
center ligante
ray 2400, 1800
png "G:/Meu Drive/PROJETO-ANTIVIRAIS-NANOTECNOLOGIA-IA/4-VALIDACAO-SILICO/figura_docking_nature_style.png", dpi=300
quit
