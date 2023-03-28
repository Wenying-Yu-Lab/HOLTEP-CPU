# HOLTEP-CPU  
Human Organ Level Toxicity Endpoints Prediction from China Pharmaceutical University (`HOLTEP-CPU`) is a collection of five models that could predict the type-specific toxicity of given molecular structures at the human organ level.   

These five models are `Chemprop` (which is a deep learning model), `RandomForest`, `SVM`, `XGboosting` and `LogisticRegression` (which are machine learning models). The supported toxicity types are `carcinogenicity`, `cardiotoxicity`, `developmental_toxicity`, `hepatotoxicity`, `nephrotoxicity`, `neurotoxicity`, `reproductive_toxicity` and `skin_sensitization`.
## Installation  
```sh
# Clone repository
git clone https://github.com/Wenying-Yu-Lab/HOLTEP-CPU.git

# Change directory
cd HOLTEP-CPU

# Create a new conda environment
conda create -n holtep python=3.8

# Activate the environment
conda activate holtep

# Install cuda (11.3) and cudnn
conda install cudatoolkit 11.3 cudnn

# Install PyTorch (1.12.1)
pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113

# Install chemprop and other dependencies
conda install -c conda-forge rdkit
pip install git+https://github.com/bp-kelley/descriptastorus
pip install chemprop
```  

## Usage
```
usage: python -u predict.py [-h] [-m {Chemprop,Randomforest,SVM,XGboosting,LogisticRegression}] [-f FOLD_INDEX] [-s SAVE_DIR] {carcinogenicity,cardiotoxicity,developmental_toxicity,hepatotoxicity,nephrotoxicity,neurotoxicity,reproductive_toxicity,skin_sensitization} data_path

This tool predicts the type-specific toxicity of given molecular structures at the human organ level.

positional arguments:
  {carcinogenicity,cardiotoxicity,developmental_toxicity,hepatotoxicity,nephrotoxicity,neurotoxicity,reproductive_toxicity,skin_sensitization}
                        Specify the toxicity type for prediction from the given list.
  data_path             Specify the file containing a series of SMILES data of the structures for prediction.

optional arguments:
  -h, --help            show this help message and exit
  -m {Chemprop,Randomforest,SVM,XGboosting,LogisticRegression}, --model {Chemprop,Randomforest,SVM,XGboosting,LogisticRegression}
                        Specify the model to be used from the given list (default: Chemprop).
  -f FOLD_INDEX, --fold FOLD_INDEX
                        Specify the fold index where the model is used (default: 1, max: 10).
  -s SAVE_DIR, --save-dir SAVE_DIR
                        Specify a directory to save results (default: ./predictions).
```
For example:  
```sh
# Do not forget to activate the environment before running predictions.
conda activate holtep

# Example 1. Model: Chemprop from fold 1 of "cardiotoxicity".
python -u predict.py cardiotoxicity ./model_data/cardiotoxicity/test.csv

# Example 2. Model: Randomforest from fold 3 of "developmental_toxicity".
python -u predict.py -m Randomforest -f 3 developmental_toxicity ./model_data/developmental_toxicity/test.csv
```
- Specification for input data
  - A file containing a list of SMILES data (`*.smi`) is supported
  - A `*.csv` file is supported with additional restrictions:
    - The column that contains the SMILES data should be the first column of the table.
    - If the table contains headers, then the column headers containing the SMILES data should be `smiles` (case insensitive).
- Specification for toxicity types
  - Available toxicity types:
    - `carcinogenicity`
    - `cardiotoxicity`
    - `developmental_toxicity`
    - `hepatotoxicity`
    - `nephrotoxicity`
    - `neurotoxicity`
    - `reproductive_toxicity`
    - `skin_sensitization`
  - Toxicity types are case sensitive.
- Specification for models
  - Available models:
    - `Chemprop` (default)
    - `Randomforest`
    - `SVM`
    - `XGboosting`
    - `LogisticRegression`
  - Model names are case sensitive.
