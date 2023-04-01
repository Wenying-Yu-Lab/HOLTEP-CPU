import argparse

TOXICITY_TYPES = [
    'carcinogenicity',
    'cardiotoxicity',
    'developmental_toxicity',
    'hepatotoxicity',
    'nephrotoxicity',
    'neurotoxicity',
    'reproductive_toxicity',
    'skin_sensitization'
]
MODELS = [
    'Chemprop',
    'Randomforest',
    'SVM',
    'XGboosting',
    'LogisticRegression'
]
ARGS = [
    [
        ['-m', '--model'],
        {
            'type': str,
            'dest': 'model',
            'help': 'Specify the model to be used from the given list (default: Chemprop).',
            'required': False,
            'choices': MODELS,
            'default': 'Chemprop'
        }
    ],
    [
        ['toxicity_type'],
        {
            'type': str,
            'help': 'Specify the toxicity endpoint for prediction from the given list.',
            'choices': TOXICITY_TYPES
        }
    ],
    [
        ['-f', '--fold'],
        {
            'type': str,
            'dest': 'fold_index',
            'help': 'Specify the fold index where the model is used (default: 1, max: 10).',
            'required': False,
            'default': '1'
        }
    ],
    [
        ['data_path'],
        {
            'type': str,
            'help': 'Specify the file containing a series of SMILES data of the structures for prediction.',
        }
    ],
    [
        ['-s', '--save-dir'],
        {
            'type': str,
            'dest': 'save_dir',
            'help': 'Specify a directory to save results (default: ./predictions).',
            'required': False,
            'default': './predictions'
        }
    ],
]

def parse_arguments():
    parser = argparse.ArgumentParser(description='This tool predicts the specific toxicity endpoints of given molecular structures at the human organ level.')
    for i in range(len(ARGS)):
        parser.add_argument(*ARGS[i][0], **ARGS[i][1])
    args = parser.parse_args()
    return args

def arg_check(args):
    if not args.fold_index.isdigit():
        raise RuntimeError('Fold index must be an integer.')
    if not (1 <= int(args.fold_index) < 11):
        raise RuntimeError(f'Fold index out of range: {args.fold_index} (range: [1, 11)).')

def predict(args):
    arg_check(args)
    cur_model = args.model
    if cur_model == 'Chemprop':
        from models import chemprop as cp
        res = cp.predict(args)
    else:
        from models import machine_learning as ml
        res = ml.predict(args)
    return res

def main():
    args = parse_arguments()
    res = predict(args)

if __name__ == '__main__':
    main()
    pass
