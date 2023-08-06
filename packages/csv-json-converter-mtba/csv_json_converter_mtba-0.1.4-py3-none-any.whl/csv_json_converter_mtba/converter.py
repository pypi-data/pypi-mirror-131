import click
import logging
from pathlib import Path

logging.basicConfig(level='DEBUG', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging .getLogger(__name__)

@click.command()
@click.option('--input', '-i', default='./', help='Caminho do(s) arquivo(s) de entrada', type=str)
@click.option('--output', '-o', default='./', help='Caminho do(s) arquivo(s) de saída', type=str)
@click.option('--delimiter', '-d', default=',', help='Delimitador dos dados ([,] ou [;])', type=str)
@click.option('--prefix', '-p', prompt=True, prompt_required=False, default='file', help='Prefixo do(s) arquivo(s) de saída', type=str)
def converter(
    input: str = './',
    output: str = './',
    delimiter: str = ',',
    prefix: str = None
):
    """
    ======================================================================
    Conversão entre arquivo(s) CSV e JSON
    ======================================================================
    """

    input_path = Path(input)
    output_path = Path(output)

    logger.info('==================================================')
    logger.info('RESUMO')
    logger.info('==================================================')
    logger.info('Caminho de entrada: %s', input_path)
    logger.info('Caminho de saída: %s', output_path)
    logger.info('Delimitador: %s', delimiter)
    logger.info('Prefixo do arquivo de saída: %s', prefix)

    if not (input_path.is_file() or input_path.is_dir()):
        logger.error('--------------------------------------------------')
        logger.error('Caminho de entrada inválido.')
        logger.error('--------------------------------------------------')
        
        raise TypeError('Caminho de entrada inválido.')

    if not (output_path.is_dir()):
        logger.error('--------------------------------------------------')
        logger.error('Caminho de saída inválido.')
        logger.error('--------------------------------------------------')

        raise TypeError('Caminho de saída inválido.')

    if delimiter not in [',', ';']:
        logger.error('--------------------------------------------------')
        logger.error('Delimitador inválido.')
        logger.error('--------------------------------------------------')

        raise TypeError('Delimitador inválido.')

    logger.info('==================================================')
    logger.info('PROCESSO INICIADO')
    logger.info('==================================================')

    if input_path.is_file():
        output_path = f'{output}/{prefix}'

        convert(input_path = input_path, output_path = output_path, delimiter = delimiter)
    else:
        for i, file in enumerate(input_path.iterdir()):
            output_path = f'{output}/{prefix}_{i+1}'

            convert(input_path = file, output_path = output_path, delimiter = delimiter)

    logger.info('==================================================')
    logger.info('PROCESSO FINALIZADO')
    logger.info('==================================================')


def convert(input_path: Path, output_path: str, delimiter: str):
    """
    Converte arquivo CSV para JSON e JSON para CSV

    Args:
        input_path (Path):      Caminho de entrada
        output_path (str):      Caminho de saída
        delimiter (str):        Delimitador
    """

    if input_path.suffix.lower() == '.csv':
        convert_csv(input_path = input_path, output_path = output_path, delimiter = delimiter)

    if input_path.suffix.lower() == '.json':
        convert_json(input_path = input_path, output_path = output_path, delimiter = delimiter)


def convert_csv(input_path: Path, output_path: str, delimiter: str):
    """
    Converte arquivo CSV para JSON

    Args:
        input_path (Path):      Caminho de entrada
        output_path (str):      Caminho de saída
        delimiter (str):        Delimitador
    """

    logger.info('--------------------------------------------------')
    logger.info('Conversão de CSV para JSON - Arquivo %s', input_path.name)
    logger.info('--------------------------------------------------')

    data = read_csv(input_path = input_path, delimiter = delimiter)
    converted_data = parse_csv_to_json(data = data)
    write_json(data = converted_data, output_path = output_path)


def convert_json(input_path: Path, output_path: str, delimiter: str):
    """
    Converte arquivo JSON para CSV

    Args:
        input_path (Path):      Caminho de entrada
        output_path (str):      Caminho de saída
        delimiter (str):        Delimitador
    """

    logger.info('--------------------------------------------------')
    logger.info('Conversão de JSON para CSV - Arquivo %s', input_path.name)
    logger.info('--------------------------------------------------')
    
    data = read_json(input_path = input_path)
    converted_data = parse_json_to_csv(data = data)
    write_csv(data = converted_data, output_path = output_path, delimiter = delimiter)

def read_csv(input_path: Path, delimiter: str) -> list[list[str]]:
    """
    Lê arquivo CSV

    Args:
        input_path (Path):      Caminho de entrada
        delimiter (str):        Delimitador

    Returns:
        list[list[str]]:        Arquivo CSV em formato de matriz
    """

    logger.info('Leitura do arquivo CSV')

    with input_path.open(mode='r') as file:
        data = file.readlines()

    data = [line.strip().split(delimiter) for line in data]
    data = [([item.strip() for item in line]) for line in data]
    
    return data


def read_json(input_path: Path) -> list[list[str]]:
    """
    Lê arquivo JSON

    Args:
        input_path (Path):      Caminho de entrada

    Returns:
        list[list[str]]:        Arquivo JSON em formato de matriz
    """

    logger.info('Leitura do arquivo JSON')

    with input_path.open(mode='r') as file:
        raw_data = file.readlines()
    
    data = list()
    row = list()
    obj = False

    for raw_line in raw_data:
        line = raw_line.strip()
        if line in ['{', ',{']:
            obj = True
            row = list()

        elif line in ['}', '},']:
            obj = False
            data.append(row)

        elif obj:
            if line[-1] == ',':
                line = line[:-1]
            row.append(line)

    return data


def parse_csv_to_json(data: list[list[str]]) -> list[dict[str, str]]:
    """
    Converte CSV em JSON

    Args:
        data (list[list[str]]):     Arquivo CSV em formato de matriz

    Returns:
        list[dict[str, str]]:       Arquivo JSON em formato de matriz
    """

    logger.info('Conversão do arquivo CSV')
    
    columns = data[0]
    lines = data[1:]

    converted_data = [dict(zip(columns, line)) for line in lines]
    
    return converted_data


def parse_json_to_csv(data: list[list[str]]) -> list[list[str]]:
    """
    Converte JSON em CSV

    Args:
        data (list[list[str]]):     Arquivo JSON em formato de matriz

    Returns:
        list[list[str]]:            Arquivo CSV em formato de matriz
    """

    logger.info('Conversão do arquivo JSON')
    
    converted_data = list()
    columns = list()
    values = list()
    
    for i, obj in enumerate(data):
        values = list()
        
        for pair in obj:
            column, value = [item.strip() for item in pair.split(':')]
            if i == 0:
                columns.append(column.replace('"', ''))
            if value == 'null':
                values.append('')
            else:
                values.append(value.replace('"', ''))
            
        if i == 0:
            converted_data.append(columns)
        converted_data.append(values)
    
    return converted_data


def write_json_object_pair(pair: tuple, file, append_comma: bool):
    """
    Escreve um par de chave e valor de um JSON em um arquivo

    Args:
        pair (tuple):               Par de chave e valor de um JSON
        file ([type]):              Arquivo
        append_comma (bool):        Flag para adicionar vírgula ao final do par
    """
    
    key, value = pair

    file.write(f'\t\t"{key}": ')
    if value.replace('.', '', 1).isdigit():
        file.write(value)
    elif value == '':
        file.write('null')
    else:
        file.write(f'"{value}"')
    
    if append_comma:
        file.write(',\n')
    else:
        file.write('\n')


def write_json_object(obj: dict[str, str], file, append_comma: bool):
    """
    Escreve um objeto de um JSON em um arquivo

    Args:
        obj (dict[str, str]):       Objeto de um JSON
        file ([type]):              Arquivo
        append_comma (bool):        Flag para adicionar vírgula ao final do objeto
    """

    file.write('\t{\n')

    for pair in tuple(obj.items())[:-1]:
        write_json_object_pair(pair = pair, file = file, append_comma = True)
    write_json_object_pair(pair = tuple(obj.items())[-1], file = file, append_comma = False)

    file.write('\t}')

    if append_comma:
        file.write(',\n')
    else:
        file.write('\n')


def write_json(data: list[dict[str, str]], output_path: str):
    """
    Grava arquivo JSON

    Args:
        data (list[dict[str, str]]):    Arquivo JSON em formato de matriz
        output_path (str):              Caminho de saída
    """

    logger.info('Gravação do arquivo JSON')
    
    output_path = Path(f'{output_path}.json')

    with output_path.open(mode='w') as file:
        file.write('[\n')

        for obj in data[:-1]:
            write_json_object(obj = obj, file = file, append_comma = True)
        write_json_object(obj = data[-1], file = file, append_comma = False)

        file.write(']')


def write_csv(data: list[list[str]], output_path: str, delimiter: str):
    """
    Grava arquivo CSV

    Args:
        data (list[list[str]]):         Arquivo CSV em formato de matriz
        output_path (str):              Caminho de saída
        delimiter (str):                Delimitador
    """

    logger.info('Gravação do arquivo CSV')

    output_path = Path(f'{output_path}.csv')
    
    with output_path.open(mode='w') as file:
        for line in data[:-1]:
            file.write(f'{delimiter.join(line)}\n')
        file.write(delimiter.join(data[-1]))