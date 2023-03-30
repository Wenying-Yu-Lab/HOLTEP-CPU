# HOLTEP-CPU  
Human Organ Level Toxicity Endpoints Predictor from China Pharmaceutical University (`HOLTEP-CPU`) is a collection of five models that could predict the specific toxicity endpoints of given molecular structures at the human organ level.   

These five models are `Chemprop` (which is a deep learning model), `RandomForest`, `SVM`, `XGboosting` and `LogisticRegression` (which are machine learning models). The supported toxicity endpoints are `carcinogenicity`, `cardiotoxicity`, `developmental_toxicity`, `hepatotoxicity`, `nephrotoxicity`, `neurotoxicity`, `reproductive_toxicity` and `skin_sensitization`.  

In addition, a transfer learning model based on `Chemprop` is also deployed with the help of [pkuwangsw/COVIDVS](https://github.com/pkuwangsw/COVIDVS). It has advantages in predicting `skin_sensitization`.
## Installation  
- Clone repository
```sh
git clone https://github.com/Wenying-Yu-Lab/HOLTEP-CPU.git
```
- Change directory
```sh
cd HOLTEP-CPU
```
- (Optional) Add [pkuwangsw/COVIDVS](https://github.com/pkuwangsw/COVIDVS) as a git submodule to apply the transfer learning model later
```sh
git submodule add https://github.com/pkuwangsw/COVIDVS.git COVIDVS
```
- Create a new conda environment
```sh
conda create -n holtep python=3.8
```
- Activate the environment
```sh
conda activate holtep
```
- Install cuda (11.3) and cudnn
```sh
conda install cudatoolkit 11.3 cudnn
```
- Install PyTorch (1.12.1)
```sh
pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113
```
- Install chemprop and other dependencies
```sh
conda install -c conda-forge rdkit
```
```sh
pip install git+https://github.com/bp-kelley/descriptastorus
```
```sh
pip install chemprop
```  

## Usage
### General usage
```
usage: python -u predict.py [-h] [-m {Chemprop,Randomforest,SVM,XGboosting,LogisticRegression}] [-f FOLD_INDEX] [-s SAVE_DIR] {carcinogenicity,cardiotoxicity,developmental_toxicity,hepatotoxicity,nephrotoxicity,neurotoxicity,reproductive_toxicity,skin_sensitization} data_path

This tool predicts the type-specific toxicity of given molecular structures at the human organ level.

positional arguments:
  {carcinogenicity,cardiotoxicity,developmental_toxicity,hepatotoxicity,nephrotoxicity,neurotoxicity,reproductive_toxicity,skin_sensitization}
                        Specify the toxicity endpoint for prediction from the given list.
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
- Examples:  
  - Do not forget to activate the environment before running predictions.
  ```sh
  conda activate holtep
  ```
  - Example 1. Model: Chemprop from fold 1 of "cardiotoxicity".
  ```sh
  python -u predict.py cardiotoxicity ./model_data/cardiotoxicity/test.csv
  ```
  - Example 2. Model: Randomforest from fold 3 of "developmental_toxicity".
  ```sh
  python -u predict.py -m Randomforest -f 3 developmental_toxicity ./model_data/developmental_toxicity/test.csv
  ```
- Specifications
  - Specification for input data
    - A file containing a list of SMILES data (`*.smi`) is supported
    - A `*.csv` file is supported with additional restrictions:
      - The column that contains the SMILES data should be the first column of the table.
      - If the table contains headers, then the column headers containing the SMILES data should be `smiles` (case insensitive).
  - Specification for toxicity endpoints
    - Available toxicity endpoints:
      - `carcinogenicity`
      - `cardiotoxicity`
      - `developmental_toxicity`
      - `hepatotoxicity`
      - `nephrotoxicity`
      - `neurotoxicity`
      - `reproductive_toxicity`
      - `skin_sensitization`
    - Toxicity endpoints are case sensitive.
  - Specification for models
    - Available models:
      - `Chemprop` (default)
      - `Randomforest`
      - `SVM`
      - `XGboosting`
      - `LogisticRegression`
    - Model names are case sensitive.

### Apply tansfer learning model
- Steps
  - Activate the environment before running predictions
    ```sh
    conda activate holtep
    ```
  - Create a dirctory to save results (skip if it exists)
    ```sh
    mkdir predictions
    ```
  - Change directory
    ```sh
    cd COVIDVS
    ```
  - Generate the descriptors
    ```sh
    python generatorFeatures.py ../model_data/skin_sensitization/test.csv ../model_data/skin_sensitization/test-feat.npy 0
    ```
    - The first argument: data for prediction
    - The second argument: file path to save features (can be specified arbitrarily)
  - Prediction
    ```sh
    python predict.py --gpu 0 --test_path ../model_data/skin_sensitization/test.csv --features_path ../model_data/skin_sensitization/test-feat.npy --preds_path ../predictions/transfer_learning.csv --checkpoint_dir ../model_data/skin_sensitization/transfer_learning/up_AT_mouse_ip_LD50/fold_0/model_0/
    ```
    - `--test_path`: data for prediction
    - `--features_path`: feature file generated in the previous step
    - `--preds_path`: file path to save results (can be specified arbitrarily)
    - `--checkpoint_dir`: directory where the `model.pt` file is located (replace `up_AT_mouse_ip_LD50` with a desired learner)
  - Change directory back
    ```sh
    cd ../
    ```
- Notice
  - Transfer learning model can only be uesd to predict `skin_sensitization`.
  - Refer to [pkuwangsw/COVIDVS](https://github.com/pkuwangsw/COVIDVS#prediction) for more details.
