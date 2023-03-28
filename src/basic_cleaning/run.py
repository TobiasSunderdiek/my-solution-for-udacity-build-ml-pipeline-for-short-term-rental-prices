#!/usr/bin/env python
"""
Download artifact from Weights&Biases, perform some cleaning on the data
and upload cleaned file as artifact to Weights&Biases
"""
import argparse
import logging
import wandb

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()

def main(args):
    run = wandb.init(job_type="clean_data")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    artifact_local_path = run.use_artifact(args.input_artifact).file()

if __name__ == "main":
    parser = argparse.ArgumentParser(description="Download, clean and upload artifact")
    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Inputfile to clean",
        required=True
    )
    parser.add_argument(
        "--output_artifact",
        type=str,
        help="Name of cleaned outputfile",
        required=True
    )
    parser.add_argument(
        "--output_type",
        type=str,
        help="Tag which describes outputfile-type. default: clean_data",
        required=False
    )
    parser.add_argument(
        "--output_description",
        type=str,
        help="Description of the output artifact",
        required=True
    )
    parser.add_argument(
        "--min_price",
        type=float,
        help="Minimum price data must have to consider in resulting artifact",
        required=True
    )
    parser.add_argument(
        "--max_price",
        type=float,
        help="Maximum price data must have to consider in resulting artifact",
        required=True
    )
    args = parser.parse_args()
    main(args)