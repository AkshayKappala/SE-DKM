# SE-DKM: Dynamic Key Management for Selective Encryption 🔑🖼️

[![Last Commit](https://img.shields.io/github/last-commit/AkshayKappala/SE-DKM?style=flat-square)](https://github.com/AkshayKappala/SE-DKM/commits/main)
[![Repo Size](https://img.shields.io/github/repo-size/AkshayKappala/SE-DKM?style=flat-square)](https://github.com/AkshayKappala/SE-DKM)
[![License](https://img.shields.io/github/license/AkshayKappala/SE-DKM?style=flat-square)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&style=flat-square)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter&style=flat-square)](https://jupyter.org/)

## 🚀 Overview

**SE-DKM** is an extension of ProjectSE, implementing **dynamic key management based on image variance** for selective encryption. The project aims to elevate cryptographic security by adjusting encryption schemes in real time, leveraging image content variability for robust protection—especially relevant in high-performance applications and quantum-aware environments.

---

## ✨ Features

- **Dynamic Key Generation**: Generates encryption keys based on image variance for adaptive security.
- **Selective Encryption Modules**: Efficiently encrypts only sensitive parts of data to balance speed and security.
- **Buffer Size Optimization**: Analyzes and optimizes buffer sizes for throughput.
- **Comprehensive Analysis**: Includes modules for similarity testing, entropy calculation, and security analysis with real and post-quantum crypto.
- **Python & Jupyter Native**: Easily extensible and ideal for research or prototype tasks.

---

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **Major Tools**: Jupyter Notebook, NumPy, OpenCV, PyWavelets
- **Cryptography**: pycryptodome, post-quantum algorithms

> All dependencies are listed in [`requirements.txt`](https://github.com/AkshayKappala/SE-DKM/blob/main/requirements.txt)

---

## ⚡ Quick Start

**1. Clone the repository**
```bash
git clone https://github.com/AkshayKappala/SE-DKM.git
cd SE-DKM
```

**2. Set up environment**
```bash
pip install -r requirements.txt
```

**3. Run Buffer Size Optimization (Jupyter Notebook):**
```bash
jupyter notebook BufferSizeOptimization.ipynb
```

**4. Example: Run Dynamic Key Generation**
```bash
python se_dynamic_keygen.py --input data/sample.png --output keys/dynamic_key.json
```

**5. Encrypt data selectively**
```bash
python selective_encryption.py --input data/image.png --key keys/dynamic_key.json --output encrypted.dat
```

---

## 📚 Project Structure

```
SE-DKM/
│
├── BufferSizeOptimization.ipynb     # Buffer size optimization notebook
├── CWT_SSIM.py                     # Continuous Wavelet Transform (CWSSIM) implementation
├── DWT_SSIM.py                     # Discrete Wavelet Transform (DWSSIM) module
├── ED_IOU.py                       # Endpoint Detection with Intersection over Union
├── ID_MSE.py                       # Identification using Mean Squared Error
├── LogParser.ipynb                 # Parsing and analysis of log files
├── PostQuantumSelectiveEncryption.ipynb # PQC-aware selective encryption analysis
├── SecurityAnalysis.ipynb          # Security evaluation notebooks
├── Similarity_Test*.py             # Suite for similarity metric testing
├── csv/, data/                     # Data directories
├── dwt*.py, selective_encryption*.py # DWT and encryption scripts
├── keys/, others/, plots/, split_logs/ # Supporting directories
├── requirements.txt                # Python dependencies
├── utils*.py                       # Utility modules
└── ... (see [all files](https://github.com/AkshayKappala/SE-DKM/tree/main))
```
> **Note:** Only the most relevant files are shown above. [View all files](https://github.com/AkshayKappala/SE-DKM/tree/main)

---

## 📝 Example Usage

Below is an actual snippet for running the dynamic key generator and then using the key for selective encryption:

```python
# se_dynamic_keygen.py
from se_dynamic_keygen import generate_dynamic_key

dynamic_key = generate_dynamic_key('data/image.png')
print(dynamic_key)
```

```python
# selective_encryption.py
from selective_encryption import encrypt_image

encrypt_image('data/image.png', key_path='keys/dynamic_key.json', output_path='encrypted.dat')
```

---

## 🔧 Customization Guide

- **Adjust Encryption Scope**: Edit `selective_encryption.py` to change the area or coefficients being encrypted.
- **Configure Key Generation**: Modify parameters in `se_dynamic_keygen.py` for different variance models or security levels.
- **Add Post-Quantum Algorithms**: Extend `pq_sign_util.py` or `PostQuantumSelectiveEncryption.ipynb` with new PQ algorithms as needed.

---

## 🚀 Deployment Instructions

This project is typically run in research, prototyping, or local batch mode. For persistent deployment:
1. **Environment**: Use a Python 3.8+ virtual environment.
2. **Script Execution**: Batch run scripts with prepared datasets—see the `/data` directory.
3. **Notebook Automation (Optional)**: Convert notebooks to scripts for batch workflow:
   ```bash
   jupyter nbconvert --to script BufferSizeOptimization.ipynb
   python BufferSizeOptimization.py
   ```

---

## 🩺 Troubleshooting

- ❗ **Missing Dependencies**:  
  ```bash
  pip install -r requirements.txt
  ```
- ❗ **Jupyter Notebooks Not Running**:  
  Ensure Jupyter is installed and the correct kernel/environment is selected.

- ❗ **File Not Found Errors**:  
  Make sure your input paths (e.g., images or keys) exist and are correct.

- ❗ **Permission Issues**:  
  Use `chmod +x script.py` if you encounter permission errors on scripts.

---

## 👤 Contact

- **Author:** Akshay Kappala  
- **GitHub:** [@AkshayKappala](https://github.com/AkshayKappala)

---

*Building adaptive, real-time cryptographic security—one pixel at a time!* 🚀🛡️
