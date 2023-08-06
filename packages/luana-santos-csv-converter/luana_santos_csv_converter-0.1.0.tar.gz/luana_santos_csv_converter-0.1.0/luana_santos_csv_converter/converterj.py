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

def converterj(input: str = "./", output: str = "./", delimiter: str = "./", prefix: str = None):
    input_path = Path(input)
    output_path = Path(output)
    logger.info('Input Path: %s', input_path)
    logger.info('Output Path: %s', output_path)

    for p in [input_path, output_path]:
        if not (p.is_file() or p.is_dir()):
            raise TypeError('Not a valid path or file name.')

    data = read_json_file(source = input_path)
    save_to_csv_files(lists = data, output_path = output_path, prefix = prefix)

def raw_read_json(source: Path):
    """Faz a leitura de um arquivo JSON ou pasta contendo vários arquivos JSON"""
    with open(source) as file:
        data = file.readlines()
    parsed_data = [(obj.rstrip()).lstrip()[:-1] for obj in data[1:-1]]

    return parsed_data

def read_json_file(source: Path):
    """Load a single csv file or all files withing a directory.
    
    Args: 
        source (Path): Path for a single file or directory with files.
        delimiter(str, optional): Separator for columns in the csv's. Defaults to ','.
    
    Returns:
        tuple: All dataframes loades from the given source path.
    """
    if source.is_file():
        logger.info('Reading csv file %s', source)
        raw_read_json(source = source)

    logger.info('Reading all files within the directory: %s', source)
    data = list()
    for i in source.iterdir():
        data.append(raw_read_json(source = i))
    
    return(data)

def parse_json_to_csv(data: list):
    """Converte lista de dados para o formato de matriz"""

    # coloca { onde deveria ter
    data = ['{' if data[i] == '' else data[i] for i in range(len(data))]
    
    # retira aspas duplas 
    data = [string.replace('"', '') for string in data]
    
    # coloca ; no fim pra servir como delimitador depois 
    data = ["{}{}".format(i, '\t') for i in data]
    
    # separa as chaves e valores 
    keys_strings = []
    newer_strings = []

    for i in range(len(data)):
        partitions = data[i].partition(': ')
    
        new_key = partitions[0]
        new_string = partitions[2]
    
        newer_strings.append(new_string)
        keys_strings.append(new_key)
        
    # coloca ; nas chaves tb
    keys_strings = ["{}{}".format(i, '\t') for i in keys_strings]
    
    # Pega o nome das colunas repetidos e deixa em um unico valor
    uniqueList = []

    for letter in keys_strings:
        if letter not in uniqueList:
            uniqueList.append(letter)
        
    # Faz uma lista enorme com o nome das colunas + valores
    final_list = uniqueList + newer_strings
    
    # Forma uma matriz numa estrutura de um banco de dados
    col = len(uniqueList)
    data = [final_list[i:i + col] for i in range(0, len(final_list), col)]
    
    # Retira a primeira coluna
    for x in data:
        del x[0]

    # Retira a última coluna
    for x in data:
        del x[len(data[0])-1]
        
    return data

def write_csv_data(data, output_path: Path):
    """Escreve uma matriz em formato dataframe em disco"""
    with output_path.open(mode = 'w') as testfile:
        for row in data:
            testfile.write(' '.join([str(a) for a in row]) + '\n')
         
def save_to_csv_files(lists: list, output_path: Path, prefix: str = None):
    """Save dataframes to disk.
    
    Args:
        lists (list): list with dataframes that will be converted.
        output_path (Path): Path where to save the json files;
        prefix (str, optional): Name to prepend to files. If nothing is given, it will use file_.
    """
    i = 0
    while i < len(lists):
        file_name = f'{prefix}_{i}.csv'
        output = output_path.joinpath(file_name)
        logger.info('Saving file: %s', output)
        write_csv_data(parse_json_to_csv(lists[i]), output_path = output)
        i += 1


