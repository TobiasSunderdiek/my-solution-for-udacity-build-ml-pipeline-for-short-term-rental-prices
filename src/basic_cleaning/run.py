#!/usr/bin/env python
"""
Download artifact from Weights&Biases, perform some cleaning on the data
and upload cleaned file as artifact to Weights&Biases
"""
import argparse
import logging
import wandb
import pandas as pd
import os
import tempfile

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()

def main(args):
    run = wandb.init(job_type="clean_data")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    logger.info(f"Download {args.input_artifact} from Weights&Biases to temp dir...")
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)

    logger.info(f"Remove outliers from row 'price'. Keep all rows within [{args.min_price}, {args.max_price}]...")
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    logger.info("Convert row 'last_review' from string to datetime...")
    df['last_review'] = pd.to_datetime(df['last_review'])

    logger.info("Remove places which are not within proper location boundaries")
    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()

    logger.info(f"Save cleaned dataframe to file and upload to Weights&Biases as {args.output_artifact}...")
    with tempfile.TemporaryDirectory() as tempdir:
        temppath = os.path.join(tempdir, args.output_artifact)
        df.to_csv(temppath, index=False)
        artifact = wandb.Artifact(args.output_artifact, type=args.output_type, description=args.output_description)
        artifact.add_file(temppath)
        run.log_artifact(artifact)
        # Credits to/Hint from the course: Wait for the artifact to be uploaded before tempDir will be destroyed
        artifact.wait()

if __name__ == "__main__":
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
        help="Tag which describes outputfile-type. default: clean_sample",
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