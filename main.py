import argparse
import logging
import random
import csv
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_argparse():
    """
    Sets up the argument parser for the command line interface.
    """
    parser = argparse.ArgumentParser(description="Shuffles the order of fields within each data record.")
    parser.add_argument("input_file", help="The input CSV file to shuffle.")
    parser.add_argument("output_file", help="The output CSV file to write the shuffled data to.")
    parser.add_argument("-H", "--header", action="store_true", help="Treat the first row as a header and preserve it.")
    return parser

def shuffle_data(input_file, output_file, header=False):
    """
    Shuffles the fields within each data record of a CSV file.

    Args:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to the output CSV file.
        header (bool): Whether the first row is a header and should be preserved.
    """
    # Refuse in place output before any file is opened. Resolved paths
    # catch the same string, alias spellings, and symlinks alike.
    from pathlib import Path
    if Path(input_file).resolve() == Path(output_file).resolve():
        logging.error("Output file is the same as the input file. Refusing to overwrite the input.")
        sys.exit(1)

    try:
        # Read the whole input before any output path is opened, so a
        # failed run never truncates data or leaves a partial output.
        with open(input_file, 'r', newline='') as infile:
            rows = list(csv.reader(infile))

        if not rows:
            print("Input file is empty.")
            sys.exit(1)

        if header:
            header_row = rows[0]
            data_rows = rows[1:]
        else:
            header_row = None
            data_rows = rows

        with open(output_file, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            if header:
                writer.writerow(header_row)

            for row in data_rows:
                if not row:
                    logging.warning(f"Skipping empty row.")
                    continue

                shuffled_row = row[:]
                random.shuffle(shuffled_row)
                writer.writerow(shuffled_row)

        logging.info(f"Successfully shuffled data from {input_file} to {output_file}.")

    except FileNotFoundError:
        logging.error(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

def main():
    """
    Main function to execute the data field shuffler.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    # Input validation
    if not os.path.exists(args.input_file):
        logging.error(f"Error: Input file '{args.input_file}' does not exist.")
        sys.exit(1)
    if not args.input_file.lower().endswith('.csv'):
        logging.warning(f"Warning: Input file '{args.input_file}' does not have a .csv extension.  Proceeding anyway, but ensure it is a valid CSV file.")
    if os.path.exists(args.output_file):
        logging.warning(f"Warning: Output file '{args.output_file}' already exists. It will be overwritten.")

    shuffle_data(args.input_file, args.output_file, args.header)

# Usage examples
if __name__ == "__main__":
    """
    Example Usage:
    
    # Simple Shuffle:
    # python main.py input.csv output.csv
    
    # Shuffle with Header Preservation:
    # python main.py input.csv output.csv -H 
    """
    main()