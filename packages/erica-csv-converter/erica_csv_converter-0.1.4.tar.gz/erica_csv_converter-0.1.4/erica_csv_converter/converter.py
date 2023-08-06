import csv
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Tuple

import click

logging.basicConfig(level="DEBUG", format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'")
logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--input",
    "-i",
    default="./",
    help="Path where to read the files for conversion",
    type=str,
)
@click.option(
    "--output",
    "-o",
    default="./",
    help="Path where the converted files will be saved",
    type=str,
)
@click.option(
    "--delimiter",
    "-d",
    default=",",
    help="Separator used to slit the files",
    type=str,
)
@click.option(
    "--prefix",
    "-prefix",
    prompt=True,
    prompt_required=False,
    default="file",
    help=(
        "Prefix used to prepend to the name of the converted file saved on disk"
        "The suffix will be a number starting from 0. ge/; file_0.jason."
    ),
)
def converter(
    type_module: str,
    input: str = "./",
    output: str = "./",
    delimiter: str = ",",
    prefix: str = "file",
) -> None:
    """Convert sigle file or list of cvs to jason"""
    input_path = Path(input)
    output_path = Path(output)
    logger.info("Input Path: %s", input_path)
    logger.info("Output Path: %s", output_path)

    for p in [input_path, output_path]:
        if not (p.is_file() or p.is_dir()):
            raise (TypeError("Arquivo invalido"))

    if type_module == "csv":
        data = read_csv_file(source=input_path, delimiter=delimiter)
        save_to_json_files(data, output_path, prefix)
    elif type_module == "json":
        data = read_json_file(source=input_path)
        save_to_csv_files(data, output_path, prefix, delimiter)


def load_csv_file(file_path: Path, delimiter: str) -> List[Dict[str, Any]]:
    with open(file_path, newline="") as file_csv:
        load_ = csv.DictReader(file_csv, delimiter=delimiter)
        return list(load_)


def read_csv_file(source: Path, delimiter: str) -> Tuple[List[Dict[str, Any]], ...]:
    """Load csv files from disk
    Arqs:
        source (Pàth): Path of a sigle csv file or directoru containing csvs to be parsed
        delimiter(str): Separator for columns in csv

    Returns:
        tuple: Tuple of DataFrames
    """
    if source.is_file():
        logger.info("Reading Sigle File %s", source)
        return (load_csv_file(file_path=source, delimiter=delimiter),)

    logger.info("Reading all files for given path %s", source)
    data = tuple([load_csv_file(file_path=name, delimiter=delimiter) for name in source.iterdir()])
    return data


def save_to_json_files(
    csvs: Tuple[List[Dict[str, Any]], ...],
    output_path: Path,
    prefix: str = "file",
) -> None:

    i = 0
    while i < len(csvs):
        file_name = f"{prefix}_{i}.json"
        logger.info("Saving file %s in folder %s", file_name, output_path)

        data: List[Dict[str, Any]] = csvs[i]
        json.dump(data, open(output_path.joinpath(file_name), "w"), indent=4)
        i += 1


def read_json_file(source: Path) -> Tuple[List[Dict[str, Any]], ...]:
    """Load json files from disk."""
    if source.is_file():
        logger.info("Reading single file %s", source)
        return (json.load(open(source)),)

    logger.info("Reading all files for given path %s", source)
    data = tuple([json.load(open(name)) for name in source.iterdir()])
    return data


def save_to_csv_files(
    jsons: Tuple[List[Dict[str, Any]], ...],
    output_path: Path,
    prefix: str = "file",
    delimiter: str = ",",
) -> None:
    """Save in CSV to Disk."""
    i = 0
    while i < len(jsons):
        file_name = f"{prefix}_{i}.csv"
        logger.info("Saving file %s in folder %s", file_name, output_path)

        data: List[Dict[str, Any]] = jsons[i]
        with open(output_path.joinpath(file_name), "w") as file_csv:
            fieldnames = data[0].keys()
            writer: csv.DictWriter = csv.DictWriter(file_csv, fieldnames=fieldnames, delimiter=delimiter)  # type: ignore
            writer.writeheader()
            for item in data:
                writer.writerow(item)

        i += 1
