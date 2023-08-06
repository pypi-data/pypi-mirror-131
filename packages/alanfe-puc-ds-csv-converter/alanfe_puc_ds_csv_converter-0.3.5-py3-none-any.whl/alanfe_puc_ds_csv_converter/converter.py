import logging
from os import path, write, listdir
from pathlib import Path
import click
from click.termui import prompt
from .readers import *
from .writers import *
from typing import Tuple
from multiprocessing import Pool, cpu_count
from os.path import basename, dirname


logging.basicConfig(
    level='DEBUG',
    format="|%(levelname)s|%(asctime)s|%(name)s| %(message)s"
)

logger = logging.getLogger(__name__)

def convert_file(arg: Tuple):
    i    = arg[0]
    file = str(arg[1])
    input_path= arg[2]
    output_path = arg[3]
    delimiter = arg[4]
    prefix   = arg[5]

    file_name = prefix + f"_{i}"
    
    logger.info("Processing file: %s", file)

    if(".csv" in file):
        logger.info("Reading %s", file)
        matrix = read_csv(input_path / file, delimiter)
        file_name += ".csv"
        logger.info("Saving %s as %s", file, file_name)
        write_json(matrix, output_path, file_name)
    
    elif(".json" in file):
        logger.info("Reading %s", file)
        matrix = read_json(input_path / file)
        file_name += ".csv"
        logger.info("Saving %s as %s", file, file_name)
        write_csv(matrix, output_path, file_name, delimiter)


@click.command()


@click.option(
    "--input", 
    "-i", 
    default="./",
    help="Define the path where is located the input files",
    type=str
)

@click.option(
    "--output", 
    "-o", 
    default="./",
    help="Define the path where files will be saved",
    type=str
)

@click.option(
    "--delimiter", 
    "-d", 
    default=";",
    help="Define the path where files will be saved",
    type=str
)

@click.option(
    "--delimiter", 
    "-d", 
    default=";",
    help="Define the character that is used to separete columns in csv files",
    type=str
)

@click.option(
    "--prefix", 
    prompt=True,
    prompt_required=False,
    default="file",
    help="Define the prefix name that is used to name the output files",
    type=str
)

@click.option(
    "--parallel", 
    "-p",
    default=False,
    help="Define if the program will be runned in parallel",
    type=bool
)


def converter(input: str, output: str, delimiter: str, prefix: str, parallel: bool) -> None:

    input_path = Path(input)
    output_path = Path(output)

    logger.info("Starting processing...")
    logger.info("Input Path: %s", input_path)
    logger.info("Output Path: %s", output_path)


    if(not(input_path.is_file() or input_path.is_dir())):
        logger.error("Input path is invalid (%s)", input_path)
        quit()

    if(not(output_path.is_file() or output_path.is_dir())):
        logger.error("Output path is invalid (%s)", input_path)
        quit()


    if(input_path.is_dir()):
        files = listdir(input_path)
        
        logger.info("The directory that was passed contains these files:\n%s", str(files))
        
        args = []
        
        if(parallel):
            for i, file in enumerate(files):
                args.append((i + 1, file, input_path, output_path, delimiter, prefix))
            p = Pool(cpu_count())
            p.map(convert_file, args)

        else:
            for i, file in enumerate(files):
                convert_file((i + 1, file, input_path, output_path, delimiter, prefix))

    elif(input_path.is_file()):
        convert_file((1, Path(basename(input_path)), Path(dirname(input_path)), output_path, delimiter, prefix))