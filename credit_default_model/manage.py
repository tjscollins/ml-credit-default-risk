import argparse
import textwrap

from features import engineer_features, prune_features
from load import load_data
from preprocess import clean_data
from training import train_model

parser = argparse.ArgumentParser(
    prog='python manage.py',
    description='Manage the machine learning model.',
    formatter_class=argparse.RawDescriptionHelpFormatter
)

subparsers = parser.add_subparsers(dest='action', description="""\
load        Load the database with raw data from CSV files in data/
preprocess  Preprocess the data to prepare for feature engineering
features    Run the automated feature engineering process
train       Train the model
deploy      Save and deploy the trained model to be used by the web application.
""")

subparsers.add_parser('load').set_defaults(func=load_data)
subparsers.add_parser('preprocess').set_defaults(func=clean_data)
subparsers.add_parser('features').set_defaults(func=engineer_features)

# Training Parser
training_parser = subparsers.add_parser('train')
training_parser.add_argument('model_type', type=str, help="Type of Machine Learning model to be trained on the dataset.  Choose one of: 'DecisionTree', 'RandomForest'")
training_parser.set_defaults(func=lambda args: train_model(model_type=args.model_type))

subparsers.add_parser('deploy').set_defaults(func=lambda x: None)

if __name__ == "__main__":
    args = parser.parse_args()
    args.func(args)
