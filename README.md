# 🧬 Ebola-AI: Accelerating Drug Discovery through Deep Learning and Molecular Dynamics

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/Status-Peer--Review%20Ready-success.svg)]()

This repository contains the official dataset, codebase, and high-resolution visuals for the research paper: **Accelerating Drug Discovery against Ebolavirus (EBOV) L-Polymerase through Deep Learning and Molecular Dynamics**.

## 📖 Overview
The traditional drug discovery pipeline is notoriously slow. This project establishes a massive *in silico* framework combining Deep Neural Networks (DNN), High-Throughput Virtual Screening (HTVS), and Stochastic Molecular Dynamics (MD) to rapidly identify highly stable inhibitors against the Ebolavirus (EBOV) L-Polymerase (PDB ID: 7YIG).

### 🚀 Key Highlights:
1. **Data Mining:** Programmatic extraction of 906 bioactive molecules directly from the ChEMBL database.
2. **Deep Learning (AI):** A rigorously trained Multi-Layer Perceptron (MLP) achieving an **AUC-ROC > 0.85**.
3. **Explainable AI (SHAP):** Transparent mapping of pharmacophoric features driving the AI's predictions.
4. **Thermodynamic Validation:** 100 ns Monte Carlo Molecular Dynamics demonstrating highly stable binding (RMSD < 0.3 nm).

## 🗂️ Repository Structure

* `1-META-ANALISE/`: Data mining scripts, ChEMBL datasets, and Dataset Auditing scripts.
* `2-MACHINE-LEARNING/`: Deep Learning pipeline, SHAP Explainer, ROC generation, and 3D Keras Topological representations.
* `4-VALIDACAO-SILICO/`: Molecular Docking data and 100 ns RMSD trajectory simulators.
* `5-PUBLICACOES/`: High-resolution scientific figures (Nature-style), `.bib` reference library, and the final Manuscript Draft.
* `Artigo_Figuras_Finais/`: Direct shortcuts to all generated PNGs for the paper.

## 💻 Installation & Reproduction
To replicate the environment and generate the graphs locally, install the dependencies using Python 3.10+:

```bash
pip install -r requirements.txt
```

## 📊 Data Availability
The final audited dataset containing the 906 *in vitro* tested molecules can be found in `1-META-ANALISE/1b-DADOS_EXTRAIDOS/`.

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Citation
If you use this code or dataset in your research, please refer to the forthcoming publication (pending peer-review).
