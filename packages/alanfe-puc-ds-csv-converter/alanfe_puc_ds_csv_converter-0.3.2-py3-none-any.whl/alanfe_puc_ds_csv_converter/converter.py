import logging
from os import path, write, listdir
from pathlib import Path
import click
from click.termui import prompt
from .readers import *
from .writers import *


logging.basicConfig(
    level='DEBUG',
    format="'|%(name)s|%(levelname)s|%(asctime)s| %(message)s'"
)

logger = logging.getLogger(__name__)

@click.command()


@click.option(
    "--input", 
    "-i", 
    default="./",
    help="Define path where is located input files",
    type=str
)

@click.option(
    "--output", 
    "-o", 
    default="./",
    help="Define path where files will save",
    type=str
)

@click.option(
    "--delimiter", 
    "-d", 
    default=";",
    help="",
    type=str
)

@click.option(
    "--delimiter", 
    "-d", 
    default=";",
    help="",
    type=str
)

@click.option(
    "--prefix", 
    prompt=True,
    prompt_required=False,
    default="file",
    help="",
    type=str
)

@click.option(
    "--encoding", 
    "-e",
    default="utf8",
    help="",
    type=str
)

@click.option(
    "--parallel", 
    "-p",
    default=True,
    help="",
    type=bool
)


def converter(input: str, output: str, delimiter: str, prefix: str, parallel: bool, encoding: str) -> None:

 
    input_path = Path(input)
    output_path = Path(output)

    logger.info("input Path: %s", input_path)
    logger.info("output Path: %s", output_path)


    if(not(input_path.is_file() or input_path.is_dir())):
        logger.error("Input path is invalid (%s)", input_path)
        quit()

    if(not(output_path.is_file() or output_path.is_dir())):
        logger.error("Output path is invalid (%s)", input_path)
        quit()


    if(input_path.is_dir()):
        files = listdir(input_path)

        for i, file in enumerate(files):
            if(".csv" in file):
                matrix = read_csv(input_path / file, delimiter, encoding)
                write_json(matrix, output_path, prefix + f"_{i}")
            
            elif(".json" in file):
                matrix = read_json(input_path / file, encoding)
                write_csv(matrix, output_path, prefix + f"_{i}")

    elif(input_path.is_file()):
        print(input_path)

        if(".csv" in str(input_path)):
            pass
        elif(".json" in str(input_path)):
            matrix = read_json(input_path, delimiter, encoding)
            write_csv(matrix, output_path,  prefix, encoding)
        
        
        
#matriz = read_csv(input_path, delimiter, enconding)
#write_json(matriz, output_path, prefix + str(1))