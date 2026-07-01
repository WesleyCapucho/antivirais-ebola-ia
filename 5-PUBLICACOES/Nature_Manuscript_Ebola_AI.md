# AI-Driven Discovery of Novel L-Polymerase Inhibitors Against Ebola Virus: A High-Confidence Machine Learning and Molecular Docking Approach

**Authors:** [Wesley Capucho et al.]
**Target Journal:** Nature / Nature Methods
**Status:** DRAFT - Skeleton 1.0

## Abstract
(To be written last). Will summarize the extraction of 9,046 articles via NLP, the curation of Tier 1 dataset, the novel Confidence-Weighted MSE Neural Network architecture, and the successful *in-silico* validation (docking) of the top hits against the Ebola L-Polymerase.

## Introduction
* **Paragraph 1:** The urgent need for broad-spectrum antivirals against Filoviridae (Ebola).
* **Paragraph 2:** Challenges in standard drug discovery (high failure rate, biological noise in phenotypic assays).
* **Paragraph 3:** Our novel approach: combining NLP-driven systematic reviews, epistemic uncertainty (MC Dropout), and thermodynamics.

## Results
### Systematic Review and Data Mining (Tier-Based Curations)
* **Main Finding:** The Prisma flowchart results. How we filtered 9,000+ abstracts down to highly rigorous enzymatic Tier 1 datasets.
* **Placeholder:** *Figure 1: PRISMA Flowchart and Dataset Distribution.*

### Deep Learning Architecture with Epistemic Uncertainty
* **Main Finding:** The Neural Network performance. Show how the `Confidence-Weighted MSE` loss function penalized noise and improved prediction accuracy compared to baseline models.
* **Placeholder:** *Figure 2: Model Architecture and Loss Convergence / MC Dropout Variance.*

### Structural Validation of Top Candidates (Molecular Docking)
* **Main Finding:** The binding affinity scores of the top AI predictions compared to standard controls (e.g., Remdesivir).
* **Placeholder:** *Figure 3: 3D Visualization of the Active Site (PyMOL render) and 2D interaction network.*

## Discussion
* Why our pipeline is a paradigm shift: bridging bioinformatics, AI, and physical chemistry.
* Limitations: *in-silico* findings require *in-vitro* validation (which defines the boundary of the paper).
* Future directions.

## Methods
### NLP and Data Extraction
* Description of the regular expressions and RoB heuristics used to build the Tier 1 dataset.
### Machine Learning Model
* Detailed mathematics of the `Confidence-Weighted MSE`.
* Architecture of the `MCDropout` networks and RDKit Morgan Fingerprint processing.
### Molecular Docking
* Protocol for `Smina` (AutoDock Vina fork).
* PDB acquisition (`7YIG`), ligand preparation (`MMFF94`), and grid box definition.

## References
* [See references_library.bib]

## Acknowledgements
* Acknowledge the computational resources (Google Colab) and funding/support.
