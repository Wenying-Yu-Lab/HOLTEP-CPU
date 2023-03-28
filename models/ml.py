from models.base import *
import joblib
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem
import csv


def read_data(path: str, column: int=1) -> list:
    """Reads input files."""
    with open(path, 'r', encoding='utf-8') as f:
        data = list(csv.reader(f))
    smiles_ls = []
    for row in data:
        smiles_ls.append(row[column-1])
    if 'smile' in smiles_ls[0].lower():
        st = 1
    else:
        st = 0
    return smiles_ls[st:]

def gen_MorganFp(smilesList, radius=2, nBits=512):
    smiles_to_morgan = {}
    for smiles in smilesList:
        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            raise ValueError("Could not parse SMILES string:", smiles)
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits)
        a = np.array(fp)
        smiles_to_morgan[smiles] = a

    return smiles_to_morgan

def predict(args):
    save_dir = refine_path(args.save_dir)
    makedirs(save_dir, exist_ok=True)
    save_file_path = f"{save_dir}/{args.model}-{args.toxicity_type}-fold_{args.fold_index}-predictions.csv"

    model_pkl = f"./model_data/{args.toxicity_type}/fold_{args.fold_index}/ml/{args.model}.pkl"
    model = joblib.load(filename=model_pkl)

    data = read_data(args.data_path)
    X_data = list(gen_MorganFp(data).values())

    predictions = list(model.predict(X_data))

    header = ['smiles', 'toxicity']
    res = []
    for i in range(len(data)):
        res.append({
            'smiles': data[i],
            'toxicity': predictions[i]
        })
    with open(save_file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, header)
        writer.writeheader()
        writer.writerows(res)
    return  res
