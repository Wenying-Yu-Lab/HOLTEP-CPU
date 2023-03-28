import chemprop
from models.base import *

def predict(args):
    save_dir = refine_path(args.save_dir)
    makedirs(save_dir, exist_ok=True)
    save_file_path = f"{save_dir}/{args.model}-{args.toxicity_type}-fold_{args.fold_index}-predictions.csv"
    arguments = [
        '--test_path', args.data_path,
        '--preds_path', save_file_path,
        '--checkpoint_dir', f"./model_data/{args.toxicity_type}/fold_{args.fold_index}/chemprop/fold_0/model_0"
    ]
    chemprop_args = chemprop.args.PredictArgs().parse_args(arguments)
    preds = chemprop.train.make_predictions(args=chemprop_args)
    with open(save_file_path, 'r', encoding='utf-8') as f:
        txt = f.read()
    new_txt = txt.replace('\n\n', '\n')
    with open(save_file_path, 'w', encoding='utf-8') as f:
        f.write(new_txt)
    return preds
