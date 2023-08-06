import logging
from pathlib import Path
import click

logging.basicConfig(
    level=logging.DEBUG,
    format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'"
    )

logger = logging.getLogger(__name__)


def csv_reader(input: Path, delimiter: str = ",") ->list:
    """Faz leitura de um ou mais arquivos .csv"""
    with input.open(mode='r') as csv_file:
        metadata = csv_file.readlines()
    data = [line.strip().split(delimiter) for line in metadata]
    return data

def csv2json(data: list) -> list:
    """Converte list (Lista) para dict (Dicionario, mapa, json)"""
    column = data[0]
    lines = data[1:]
    return [dict(zip(column, l)) for l in lines]

def iter_line(data: tuple, file, comma: bool = True):
    """Organiza arquivo dict em um formato json valido"""
    key, value = data
    item = tuple(data.items())
    if comma:
        file.write(f'\t\t"{key}":"{value}",\n')
    else:
        file.write(f'\t\t"{key}":"{value}"\n')

def iter_dict(data: dict, file, comma: bool = True):
    """Organiza arquivo dict em um formato json valido"""
    file.write("\t{\n")
    item = tuple(data.items())
    for i in item:
        iter_line(i, file)
    iter_line(item[-1], file, False)
    file.write("\t}\n")
    if comma:
        file.write(",\n")
    
def save_json(data: list, output: Path):
    """Salva o arquivo .json em disco"""
    with output.open(mode='w') as json_file:
        json_file.write("[\n")
        for i in data[:-1]:
            iter_dict(i, output)
        iter_dict(data[-1], output, comma=False)
        json_file.write("]\n")
    

    
    
        
@click.command()
@click.option(
    "--input",
    "-i",
    default="./",
    help="Path where to find CSV files to be contered to JSON.",
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
    help="Separator used to split files.",
    type=str,
    )
def csvJson(input: str = "./", output: str = "./", delimiter: str = ","):
    """Converte arquivos .csv para arquivos .json"""
    input_path = Path(input)
    output_path = Path(output)
    logger.info("Input path: %s", input_path)
    logger.info("Output path: %s", output_path)

    for i in input_path.iterdir():
        if str(i).split(".")[-1] == "csv":
            logger.info("Current file: %s", i)
            data = csv_reader(i, delimiter)
            list_data = csv2json(data)
            save_json(list_data, output_path)
    
    





def json_reader(input: Path) ->list:
    """Faz leitura de um ou mais arquivos .json"""
    with input.open(mode='r') as json_file:
        metadata = json_file.readlines()
    
    data = [line.strip().replace("[", "").replace("]","").replace("{", "").replace("}","").replace('"', "").replace("\n", "") for line in metadata]
    data = list(filter(None, data))
    return data

def json2csv(data: list) -> list:
    """Converte list (Lista) para dict (Dicionario, mapa, json)"""
    headers = list()
    lines = list()
    for i in data:
        line_data = i.split(",")
        line_data = list(filter(None, line_data))
        for l in line_data:
            header = l.strip().split(":")[0]
            line = l.strip().split(":")[1]
            headers.append(header)
            lines.append(line)
    headers = list(dict.fromkeys(headers))
    return headers, lines


    


def iter_csv(headers: list, lines: list, file, delimiter: str = ","):
    """Organiza arquivo dict em um formato csv valido"""
    
    line_break = len(headers)
    for h in headers[:-1]:
        file.write(h+delimiter)
    file.write(headers[-1]+"\n")
    count = 0
    for line in lines:
        count += 1
        if count == line_break:
            file.write(line+"\n")
            count = 0
        else:
            file.write(line+delimiter)
        
def save_csv(headers: list, lines: list, output: Path, delimiter: str = ","):
    """Salva o arquivo .csv em disco"""
    with output.open(mode='w') as csv_file:
        
        iter_csv(headers, lines, csv_file, delimiter)
        
    

@click.command()
@click.option(
    "--input",
    "-i",
    default="./",
    help="Path where to find CSV files to be contered to JSON.",
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
    help="Separator used to split files.",
    type=str,
    )
def jsonCsv(input: str = "./", output: str = "./", delimiter: str = ","):
    """Converte arquivos .json para arquivos .csv"""
    input_path = Path(input)
    output_path = Path(output)
    logger.info("Input path: %s", input_path)
    logger.info("Output path: %s", output_path)

    for i in input_path.iterdir():
        if str(i).split(".")[-1] == "json":
            logger.info("Current file: %s", i)
            data = json_reader(i)
            headers, lines = json2csv(data)
            save_csv(headers, lines, output_path, delimiter)
    
