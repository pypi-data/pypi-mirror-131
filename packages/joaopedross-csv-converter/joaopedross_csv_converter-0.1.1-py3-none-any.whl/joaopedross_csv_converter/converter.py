import logging
from typing_extensions import Required
import click
from click.termui import prompt
import pandas as pd

from pathlib import Path

logging.basicConfig(
    level=logging.DEBUG, format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'"
)

logger = logging.getLogger(__name__)

@click.command()

@click.option(
    '--mode',
    '-m',
    required=True,
    help='Converter\'s mode. \'C\' for csv to JSON, \'J\' for JSON to csv.',
    type=str
)

@click.option(
    '--input',
    '-i',
    default='./',
    help='Path for the file to be converted.',
    type=str
)

@click.option(
    '--output',
    '-o',
    default='./',
    help='Path for the new converted file to be saved.',
    type=str
)

@click.option(
    '--delimiter',
    '-d',
    default=',',
    help='Separator used to split the columns.',
    type=str
)

@click.option(
    '--prefix',
    '-p',
    prompt=True,
    prompt_required=False,
    default='file',
    help='Prefix to be used in the name of the converted file.'
)

def converter(mode: str, input: str = './', output: str = './', delimiter: str = ',', prefix: str = None):
    input_path = Path(input)
    output_path = Path(output)

    if not (input_path.is_file() or input_path.is_dir()):
        raise TypeError('Input path or file is not valid.')

    if not (output_path.is_dir()):
        raise TypeError('Output path or file is not valid.')

    if delimiter != ',' and delimiter != ';' and delimiter != '\t':
        raise TypeError('Delimiter is not valid. Delimiter options: \',\', \';\' or \'\t\'')

    if mode != 'C' and mode != 'J':
        raise TypeError('Mode is not valid. Mode options: \'C\' (csv to JSON) or \'J\' (JSON to csv).')

    if mode.upper() == 'C':
        read_csv_file(input_path, output_path, delimiter, prefix)
    else:
        read_and_parse_json_file(input_path, output_path, delimiter, prefix)

def read_csv_file(input_path: Path, output_path: Path, delimiter: str = ',', prefix: str = None):
    """Read one or more .csv files.

    Args: 
        input_path (Path): Path for the file(s) to be read.
        output_path (Path): Path to save the converted file.
        delimiter (str, optional): Separator used for the columns. Defaults to ','.
        prefix (str, optional): Prefix to be used on the name of the converted file. Defaults to None.
    """
    data = list()

    if input_path.is_file():
        with input_path.open(mode='r') as file:
            lines = file.readlines()
        for line in lines:
            data.append(line.strip().split(delimiter))
        parsed_data = parse_csv_to_json(data)
        save_to_json(csvs=parsed_data, output_path=output_path, prefix=prefix)
    else:
        indexFile = 0
        for path in input_path.iterdir():
            if (path.name.find('.csv') != -1):
                with path.open(mode='r') as file:
                    lines = file.readlines()
                for line in lines:
                    data.append(line.strip().split(delimiter))
                parsed_data = parse_csv_to_json(data)
                save_to_json(csvs=parsed_data, output_path=output_path, prefix=prefix, index=indexFile)
                indexFile += 1

def read_and_parse_json_file(input_path: Path, output_path: Path, delimiter: str = ',', prefix: str = None):
    """Read one or more .json files.

    Args: 
        input_path (Path): Path for the file(s) to be read.
        output_path (Path): Path to save the converted file.
        prefix (str, optional): Prefix to be used on the name of the converted file. Defaults to None.
    """
    data = list()
    addedColumns = False

    if input_path.is_file():
        with input_path.open(mode='r') as file:
            lines = file.readlines()
        columns = list()
        values = list()
        for line in lines:
            if not (line.find('{') != -1 or line.find('}') != -1 or line.find('[') != -1 or line.find(']') != -1):
                line = line.replace('\t', '').replace('\n', '').replace('"', '').replace(',', '')
                key, value = line.split(': ')
                if not addedColumns:
                    columns.append(key)
                values.append(value)
            elif(line.find('}') == 1):
                if not addedColumns:
                    data.append(list(columns))
                    addedColumns = True
                data.append(values.copy())
                values.clear()
        save_to_csv(data, output_path, prefix, delimiter)
    else:
        indexFile = 0
        for path in input_path.iterdir():
            if (path.name.find('.json') != -1):
                with path.open(mode='r') as file:
                    lines = file.readlines()
                columns = list()
                values = list()
                for line in lines:
                    if not (line.find('{') != -1 or line.find('}') != -1 or line.find('[') != -1 or line.find(']') != -1):
                        line = line.replace('\t', '').replace('\n', '').replace('"', '').replace(',', '')
                        key, value = line.split(': ')
                        if not addedColumns:
                            columns.append(key)
                        values.append(value)
                    elif(line.find('}') == 1):
                        if not addedColumns:
                            data.append(list(columns))
                            addedColumns = True
                        data.append(values.copy())
                        values.clear()
                save_to_csv(data, output_path, prefix, delimiter, indexFile)
                indexFile += 1

def parse_csv_to_json(data: 'list[list[str]]') -> 'list[dict[str, str]]':
    """Converts data from csv to json.

    Args: 
        data (list[list[str]]): Parsed data to be converted.

    Returns:
        list[dict[str, str]]: Data converted to json.
    """
    column = data[0]
    lines = data[1:]

    result = list()
    for line in lines:
        result.append(dict(zip(column, line)))

    return result

def save_to_json(csvs: 'list[dict[str, str]]', output_path: Path, prefix: str = None, index: int = 0):
    """Save JSON file.

    Args: 
        csvs (list[dict[str, str]]): list to be converted.
        output_path (Path): Path to save the converted file.
        prefix (str, optional): Prefix to be used on the name of the converted file. Defaults to None.
        index (int, optional): Number to be appended to the filename. Defaults to 0.
    """
    filename = output_path.joinpath(f'{prefix}_{index}.json')
    with filename.open(mode='w') as file:
        file.write('[\n')
        for item in csvs[:-1]:
            file.write('\t{\n')
            for line in tuple(item.items())[:-1]:
                key, value = line
                if value != '':
                    file.write(f'\t\t"{key}": "{value}",\n')
                else:
                    file.write(f'\t\t"{key}": null,\n')
            lastItem = tuple(item.items())[-1]
            key, value = lastItem
            file.write(f'\t\t"{key}": "{value}"\n')
            file.write('\t},\n')
        item = csvs[-1]
        file.write('\t{\n')
        for line in tuple(item.items())[:-1]:
            key, value = line
            if value != '':
                file.write(f'\t\t"{key}": "{value}",\n')
            else:
                file.write(f'\t\t"{key}": null,\n')
        lastItem = tuple(item.items())[-1]
        key, value = lastItem
        file.write(f'\t\t"{key}": "{value}"\n')
        file.write('\t}\n')
        file.write(']\n')

def save_to_csv(json: 'list[dict[str, str]]', output_path: Path, prefix: str = None, delimiter: str = ',', index: int = 0):
    """Save csv file.

    Args: 
        json (list[dict[str, str]]): list to be converted.
        output_path (Path): Path to save the converted file.
        prefix (str, optional): Prefix to be used on the name of the converted file. Defaults to None.
        index (int, optional): Number to be appended to the filename. Defaults to 0.
        delimiter (str, optional): Separator used for the columns. Defaults to ','.
    """
    filename = output_path.joinpath(f'{prefix}_{index}.csv')
    with filename.open(mode='w') as file:
        for list in json:
            line = ''
            for item in list[:-1]:
                if (item == 'null'):
                    line = line + delimiter
                else:
                    line = line + item + delimiter
            line = line + list[-1]
            file.write(line)
            file.write('\n')
