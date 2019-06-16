import argparse
import textwrap

from db import load_data

parser = argparse.ArgumentParser(
    prog='python manage.py',
    description='Manage the machine learning model.',
    formatter_class=argparse.RawDescriptionHelpFormatter
)

subparsers = parser.add_subparsers(dest='action', description="""\
load        Load the database with raw data from CSV files in data/
preprocess  Preprocess the data to prepare for feature engineering
feature     Run the automated feature engineering process
train       Train the model
deploy      Save and deploy the trained model to be used by the web application.
""")

subparsers.add_parser('load').set_defaults(func=load_data)
subparsers.add_parser('preprocess').set_defaults(func=lambda x: None)
subparsers.add_parser('feature').set_defaults(func=lambda x: None)
subparsers.add_parser('train').set_defaults(func=lambda x: None)
subparsers.add_parser('deploy').set_defaults(func=lambda x: None)

if __name__ == "__main__":
    args = parser.parse_args()
    args.func(args)
