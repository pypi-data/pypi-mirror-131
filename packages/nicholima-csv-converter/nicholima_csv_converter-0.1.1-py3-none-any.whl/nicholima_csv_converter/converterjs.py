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
    help="Path were to find the JSON files to be converted as CSV.", 
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
    "--prefix", 
    "-p",
    prompt = True,
    prompt_required = False, 
    default = "file", 
    help=(
        "Prefix used to prepend to the name of the converted file saved on disk."
        "The suffix will be a number starting from 0. ge: file_0.json"), 
)

def converterjs(input: str = "./", output: str = "./", delimiter: str = "./", prefix: str = None):
    input_path = Path(input)
    output_path = Path(output)
    logger.info('Input Path: %s', input_path)
    logger.info('Output Path: %s', output_path)

    for p in [input_path, output_path]:
        if not (p.is_file() or p.is_dir()):
            raise TypeError('Not a valid path or file name.')

    data = read_json_file(source = input_path)
    save_to_csv_files(lists = data, output_path = output_path, prefix = prefix)

def single_read_json(source: Path):
    """Faz a leitura de um arquivo JSON ou pasta contendo vários arquivos JSON"""
    with open(source) as file:
        data = file.readlines()
    parsed_data = [(obj.rstrip()).lstrip()[:-1] for obj in data[1:-1]]

    return parsed_data

def read_json_file(source: Path):
    """ Carrega um unico arquivo csv ou todos arquivos CSV em um diretório"""
   
    if source.is_file():
        logger.info('Reading csv file %s', source)
        single_read_json(source = source)

    logger.info('Reading all files within the directory: %s', source)
    data = list()
    for i in source.iterdir():
        data.append(single_read_json(source = i))
    
    return(data)

def parse_json_to_csv(data: list):
    """Converte lista de dados para o formato de csv"""

    data = ['{' if data[i] == '' else data[i] for i in range(len(data))]
    data = [string.replace('"', '') for string in data]
    data = ["{}{}".format(i, '\t') for i in data]
    


    keys_string = []
    newer_string = []

    for i in range(len(data)):
        delimiters = data[i].delimiter(': ')
    
        new_key = delimiters[0]
        new_string = delimiters[2]
    
        newer_string.append(new_string)
        keys_string.append(new_key)
        
    keys_strings = ["{}{}".format(i, '\t') for i in keys_string]
    
    
    helpList = []

    for letter in keys_strings:
        if letter not in helpList:
            helpList.append(letter)
        
    lastlist = helpList + newer_string
    
    col = len(helpList)
    data = [lastlist[i:i + col] for i in range(0, len(lastlist), col)]
    
    for x in data:
        del x[0]

    for x in data:
        del x[len(data[0])-1]
        
    return data

def write_csv_data(data, output_path: Path):
    """escreve dataframe no disco."""
    with output_path.open(mode = 'w') as testfile:
        for row in data:
            testfile.write(' '.join([str(a) for a in row]) + '\n')
         
def save_to_csv_files(lists: list, output_path: Path, prefix: str = None):
    """salva o dataframe no disco."""
    i = 0
    while i < len(lists):
        file_name = f'{prefix}_{i}.csv'
        output = output_path.joinpath(file_name)
        logger.info('Saving file: %s', output)
        write_csv_data(parse_json_to_csv(lists[i]), output_path = output)
        i += 1


