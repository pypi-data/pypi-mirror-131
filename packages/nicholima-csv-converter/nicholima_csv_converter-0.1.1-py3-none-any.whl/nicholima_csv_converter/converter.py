import logging
from pathlib import Path
import click

logging.basicConfig(
    level = "DEBUG", format = "'%(asctime)s - %(name)s - %(levelname)s - %(message)s'"
)
logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--input", 
    "-i", 
    default = "./", 
    help="Path were to find the CSV files to be converted as JSON.", 
    type=str,
)
@click.option(
    "--output", 
    "-o", 
    default = "./", 
    help="Path were the converted files will be saved.", 
    type=str,
)
@click.option(
    "--delimiter", 
    "-d", 
    default = ",", 
    help="Separator used to split the files.", 
    type=str,
)
@click.option(
    "--prefix", 
    "-p",
    prompt = True,
    prompt_required = False, 
    default = "file", 
    help=(
        "Prefix used to prepend to the name of the converted file saved on disk."
        "The suffix will be a number starting from 0. ge: file_0.json"), 
)

def converter(input: str = "./", output: str = "./", delimiter: str = "./", prefix: str = None):
    input_path = Path(input)
    output_path = Path(output)
    logger.info('Input Path: %s', input_path)
    logger.info('Output Path: %s', output_path)

    for p in [input_path, output_path]:
        if not (p.is_file() or p.is_dir()):
            raise TypeError('Not a valid path or file name.')

    data = read_csv_file(source = input_path, delimiter = delimiter)
    save_to_json_files(csvs = data, output_path = output_path, prefix = prefix)

def single_read_csv(source: Path, delimiter: str = ","):
    """Load a single csv file withing a directory."""
    
    with source.open(mode = "r") as file:
        dt = file.readlines()

    parsed_data = [line.strip().split(delimiter) for line in dt]
    return parsed_data

def read_csv_file(source: Path, delimiter: str = ','):
    """Load a single csv file or all files withing a directory. """
    if source.is_file():
        logger.info('Reading csv file %s', source)
        single_read_csv(source = source, delimiter = delimiter)

    logger.info('Reading all files within the directory: %s', source)
    data = list()
    for i in source.iterdir():
        data.append(single_read_csv(source = i, delimiter = delimiter))
    
    return(data)

def parse_csv_to_json(data: list[list[str]]):
    """Converte lista de dados para o formato de dicionário"""
    column = data[0]
    lines = data[1:]
    result = [dict(zip(column, line)) for line in lines]
    return result


def write_line(line: tuple, io, append_comma: bool = True):
    """Escreve uma linha do dicionario no disco"""
    key, value = line
    if append_comma:
        io.write(f'\t\t"{key}": "{value}", \n' )
    else:
         io.write(f'\t\t"{key}": "{value}" \n' )

def write_dictionary(data: dict, io, append_comma: bool = True):
    """Escreve dicionario no disco"""
    io.write('\t{\n')
    items = tuple(data.items())
    for line in items[:-1]:
        write_line(line, io, True)
    write_line(items[-1], io, False)
    io.write('\t}')
    if append_comma:
        io.write(',\n')
    else:
        io.write('\n')

def write_json_data(data: list[dict[str, str]], output_path: Path):
    """Escreve uma lista de dicionários em formato json em disco"""
    with output_path.open(mode = 'w') as file:
        file.write('[\n')
        for d in data[:-1]:
            write_dictionary(d, file, append_comma = True)
        write_dictionary(data[-1], file, append_comma = False)
        file.write(']\n')
         
def save_to_json_files(csvs: list, output_path: Path, prefix: str = None):
    """Save dataframes to disk.
    
    Args:
        csvs (list): List with dataframes that will be converted.
        output_path (Path): Path where to save the json files;
        prefix (str, optional): Name to prepend to files. If nothing is given, it will use file_.
    """
    i = 0
    while i < len(csvs):
        file_name = f'{prefix}_{i}.json'
        output = output_path.joinpath(file_name)
        logger.info('Saving file: %s', output)
        write_json_data(parse_csv_to_json(csvs[i]), output_path = output)
        i += 1
