import logging # import para exibição de datas no terminal
from pathlib import Path
from typing import List
import click


logging.basicConfig(
    level='DEBUG', format="'%(asctime)s - %(name)s - %(levelname)s  - %(message)s'"
)

logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--input",
    "-i",
    default="./",
    help="Path where the files will be loaded for conversion.",
    type=str,
)
@click.option(
    "--output",
    "-o",
    default="./",
    help="Path where the converted files will be saved.",
    type=str,
)
@click.option(
    "--delimiter",
    "-d",
    default=",",
    help="Separator used to split the files.",
    type=str,
)
@click.option(
    "--prefix",
    "-p",
    prompt=True,
    prompt_required=False,
    default="file",
    help=(
        "Prefix used to prepend to the name of the converted file saved on disk."
        " The suffix will be a number starting from 0. ge: file_0.json."
    ),
)

def converter(
    input: str ="./", output: str = "./", delimiter: str =',', prefix = None
):
    """ Convert single file or list of CSV"""
    """ Converte um unico arquivou ou lista de arquivos CSV"""
    input_path = Path(input)
    output_path = Path(output)

    logger.info("Input Path: %s", input_path)
    logger.info("Outputh Path: %s", output_path)

    for p in [input_path, output_path]:
        if not(p.is_file()or p.is_dir()):
            raise TypeError("Not a valid path of file name")

data = read_csv_file(source=input_path, delimiter=delimiter)
save_to_json_file(csvs=data, output_path=output_path, prefix=prefix)


def read_csv_file(input_path: Path, delimiter: str = ",") -> list[list[str]]:
    """Faz a leitura de um arquivo CSV ou Pasta contendo arquivos CSV."""
    with input_path.open(mode='r') as file:
        data = file.readlines()
    parsed_data = [line.strip().split(delimiter) for line in data]
    return parsed_data

