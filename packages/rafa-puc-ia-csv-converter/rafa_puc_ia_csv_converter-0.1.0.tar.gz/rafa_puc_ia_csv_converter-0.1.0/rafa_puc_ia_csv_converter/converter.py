import logging
from pathlib import Path
from typing import Dict, List
import click

logging.basicConfig(level="DEBUG", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--input",
    "-i",
    default="./",
    help="Path where to find csv files to be converted to JSON.",
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
        "The suffix will be a number starting from 0. ge: file_0.json."
    ),
)
def converter(input: str = "./", output: str = "./", delimiter: str = ",", prefix: str = None):
    input_path = Path(input)
    output_path = Path(output)
    logger.info("Input Path: %s", input_path)
    logger.info("Output Path: %s", output_path)
    if input.suffix.lower() == '.csv':
        input_path = input_path
        for p in [input_path, output_path]:
            if not (p.is_file() or p.is_dir()):
                raise TypeError("Not a valid path of file name.")
            i = 0
            while i < len(input):
                file_name = f"{prefix}_{i}"
                output_path.joinpath(file_name)
                i += 1
    if input.suffix.lower() == '.csv':
        input_path2 = input_path
        output_path2 = output_path
        for p in [input_path2, output_path2]:
            if not (p.is_file() or p.is_dir()):
                raise TypeError("Not a valid path of file name.")
            i = 0
            while i < len(input):
                file_name = f"{prefix}_{i}"
                output_path2.joinpath(file_name)
                i += 1

    return input_path, output_path, input_path2, output_path2


def read_csv(input_path: Path, delimiter: str = ",") -> List[List[str]]:
    """Faz a leitura de um arquivo csv ou pasta contendo varios arquivos csv."""
    with input_path.open(mode="r") as file:
        data = file.readlines()
    parsed_data = [line.strip().split(delimiter) for line in data]
    return parsed_data


def parse_csv_to_json(parsed_data: List[List[str]]) -> List[Dict[str, str]]:
    """Converte lista de dados para formato de lista de dicionarios."""
    column = parsed_data[0]
    lines = parsed_data[1:]
    convert = [dict(zip(column, line)) for line in lines]
    return convert


def write_file(convert, output_path, prefix: str = None):
    file_dir = "str"
    file_dir_path = Path(file_dir)
    if output_path.is_dir:
        i = 0
        while i < len(convert[:-1]):
            file_name = f"{prefix}_{i}.json"
            file_dir_path = output_path.joinpath(file_name)
            i += 1
    return file_dir_path


def write_json_data(convert: List[Dict[str, str]], file_dir_path: Path):
    """Escreve uma lista de dicionarios em formato json em disco."""
    file_dir_path = write_file(convert, output_path)
    with file_dir_path.open(mode="w") as file:
        file.write("{\n")
        for d in convert[:-1]:
            write_dictionary(d, file, append_comma=True)
        write_dictionary(convert[-1], file, append_comma=False)
        file.write("}\n")


def write_dictionary(data: Dict, io, append_comma: bool = True):
    """Escreve um dicionario no disco."""
    io.write("\t{\n")
    items = tuple(data.items())
    for line in items:
        write_line(line, io, True)
    write_line(items[-1], io, False)
    io.write("\t}")
    if append_comma:
        io.write(",\n")
    else:
        io.write("\n")


def write_line(line: tuple, io, append_comma: bool = True):
    """Escreve uma lina do dicionario no disco."""
    key, value = line
    if append_comma:
        io.write(f'\t\t"{key}": "{value}",\n')
    else:
        io.write(f'\t\t"{key}": "{value}"\n')


input_path, output_path = converter()
parsed_data = read_csv(input_path)
convert = parse_csv_to_json(parsed_data)
write_json_data(convert, output_path)


def read_json(input_path2: Path):
    with input_path2.open(mode="r") as file:
        data = file.readlines()
        parsed_data2 = [item.replace(" ", "").replace("\n", "").replace("\t", "") for item in data if ":" in item]
    return parsed_data2


def parse_json_to_csv2(parsed_data11):
    primeiro = [primeiro.strip().split(":")[0] for primeiro in parsed_data11]
    saida, total = uniq(primeiro)
    segundo = [segundo.strip().split(":")[1] for segundo in parsed_data11]
    saida.extend(segundo)
    splited = [saida[0:total] for i in range(total)]
    return splited


def uniq(primeiro):
  saida = []
  for x in primeiro:
    if x not in saida:
      saida.append(x)
  total = len(saida)
  return saida, total


def write_file(splited, output_path2, prefix: str = None):
    file_dir2 = "str"
    file_dir_path2 = Path(file_dir2)
    if output_path2.is_dir:
        i = 0
        while i < len(splited[:-1]):
            file_name2 = f"{prefix}_{i}.csv"
            file_dir_path2 = output_path2.joinpath(file_name2)
            i += 1
    return file_dir_path2


def write_csv_data(splited, file_dir_path2: Path):
    file_dir_path2 = write_file(splited, output_path2)
    with file_dir_path2.open(mode="w") as file:
        for d in splited[:-1]:
            file.write(f'"{splited[d]}"')


input_path2, output_path2 = converter()
parsed_data2 = read_json(input_path2)
splited = parse_json_to_csv2(parsed_data2)
write_json_data(splited, output_path2)