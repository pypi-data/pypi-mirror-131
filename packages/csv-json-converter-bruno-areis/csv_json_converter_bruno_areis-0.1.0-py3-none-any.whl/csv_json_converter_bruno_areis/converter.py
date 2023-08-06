import logging
import os
import string
from pathlib import Path

import click

logging.basicConfig(
    level="DEBUG", format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'"
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
        " The suffix will be a number starting from 1. ge: file_1.json."
    ),
)
def converter(
    input: str = "./", output: str = "./", delimiter: str = ",", prefix: str = None
):
    """Convert Single file or list of CSV files to JSON OR Single file or list of JSON files to CSV """
    input_path = Path(input)
    output_path = Path(output)
    logger.info("Input path %s", input_path)
    logger.info("Output path %s", output_path)
    for p in [input_path, output_path]:
        if not(p.is_file() or p.is_dir()):
            raise (TypeError("Not a valid file or directory name.", input_path))
    else:
        convert_file(input_path, output_path, delimiter, prefix)


def convert_file(input_path, output_path, delimiter, prefix):
    if input_path.is_file():
        file_number = str(str(os.path.basename(input_path)
                              ).split("_")[1]).split(".")[0]
        if str(input_path).endswith(f"{file_number}.csv"):
            file_name = f"{prefix}_{file_number}"
            datacsv = read_csv(input_path, delimiter)
            datajsonconvert = parse_csv_to_json(datacsv)
            write_json_data(datajsonconvert, output_path, file_name)
        elif str(input_path).endswith(f"{file_number}.json"):
            file_name = f"{prefix}_{file_number}"
            datajson = read_json(input_path, delimiter)
            datacsvconvert = parse_json_to_csv(datajson)
            write_csv_data(datacsvconvert, output_path, file_name)
        else:
            raise (TypeError("Not a valid file name.", file_number))
    elif input_path.is_dir():
        for item in sorted(os.listdir(input_path)):
            file_number = str(str(os.path.basename(
                item)).split("_")[1]).split(".")[0]
            file_name = f"{prefix}_{file_number}"
            if item.endswith(f"{file_number}.csv"):
                file_path = Path.joinpath(input_path, item)
                datacsv = read_csv(file_path, delimiter)
                datajsonconvert = parse_csv_to_json(datacsv)
                write_json_data(datajsonconvert, output_path, file_name)
            elif item.endswith(f"{file_number}.json"):
                file_path = Path.joinpath(input_path, item)
                datajson = read_json(file_path, delimiter)
                datacsvconvert = parse_json_to_csv(datajson)
                write_csv_data(datacsvconvert, output_path, file_name)
            else:
                raise (TypeError("Not a valid directory name.", input_path))


dir


def read_csv(input_path: Path, delimiter: str = ",") -> list[list]:
    """Faz a leitura de um arquivo CSV e retorna como lista"""
    parsed_data = []
    with input_path.open(mode="r") as file:
        data = file.readlines()
        parsed_data = [line.strip().split(delimiter) for line in data]
    return [parsed_data]


def parse_csv_to_json(data: list) -> list:
    """Converte uma lista de arquivos CSV para o formato JSON"""
    list_parsed_data = []
    for csv in data:
        for item in csv:
            for i, _ in enumerate(item):
                if item[i] == "":
                    item[i] = "null"
        column = csv[0]
        lines = csv[1:]
        parsed_data = [dict(zip(column, line)) for line in lines]
        list_parsed_data.append(parsed_data)
    return list_parsed_data


def write_line(line: tuple, io, append_comma: bool):
    """Escreve uma linha, realizando tratativas"""
    key, value = line
    if append_comma:
        io.write(f'\t\t"{key}": "{value}",\n')
    else:
        io.write(f'\t\t"{key}": "{value}"\n')


def write_dictionary(data: dict, io, append_comma: bool):
    """Escreve um dicionário, realizando tratativas"""
    io.write("\t{\n")
    items = tuple(data.items())
    for line in items[:-1]:
        write_line(line, io, append_comma=True)
    write_line(items[-1], io, append_comma=False)
    io.write("\t")
    if append_comma:
        io.write(",\n")


def write_json_data(csvs, output_path: Path, file_name: str = None):
    """Escreve um ou mais arquivos JSON"""
    i = 1
    for data in csvs:
        file_name = f"{file_name}.json"
        logger.info("Saving file %s in folder %s", file_name, output_path)
        new_path = Path.joinpath(output_path, file_name)
        with new_path.open(mode="w") as file:
            file.write("[\n")
            for d in data[:-1]:
                write_dictionary(d, file, append_comma=True)
                write_dictionary(data[-1], file, append_comma=False)
                file.write("]\n")
        i += 1


def read_json(output_path: Path, delimiter: str = ",") -> list:
    """Faz a leitura de um arquivo JSON e retorna como lista"""
    parsed_data = []
    with output_path.open(mode="r") as file:
        data = file.readlines()
        parsed_data = [line.strip().split(delimiter) for line in data]
        return [parsed_data]


def unique(data: list):
    """Unifica valores repetidos da lista."""
    unique_list = []
    for item in data:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list


def split_list(data: list, nparts: int):
    """Divide uma lista em partes conforme o que for inserido na variável nparts"""
    def new_list(data, nparts): return [
        data[i: i + nparts] for i in range(0, len(data), nparts)
    ]
    final_list = new_list(data, nparts)
    return final_list


def parse_json_to_csv(data: list) -> list:
    """Converte uma lista de arquivos JSON para o formato CSV"""
    ws = string.whitespace
    list_parsed_data = []
    for json in data:
        json_list = json[2:-1]
        for item in json_list:
            for subitem in item:
                if subitem.__contains__("{") or (subitem.find('"')):
                    item.remove(subitem)

        json_list = [x for x in json_list if (x != [] and x != [""])]

        json_list = (
            str(json_list)
            .replace(":", ",")
            .replace("[", "")
            .replace("]", "")
            .replace("'", "")
            .replace('"', "")
            .split(",")
        )

        json_list = [item.strip() for item in json_list]

        print(json_list[-1])
        json_list_head = []
        json_list_line = []

        for item in json_list:
            if json_list.index(item) % 2 == 0:
                json_list_head.append(item)
            else:
                json_list_line.append(item)

        result = [unique(json_list_head)] + split_list(
            json_list_line, len(unique(json_list_head))
        )
        for item in result:
            for i, _ in enumerate(item):
                if item[i] == "":
                    item[i] = "null"

        list_parsed_data.append(result)

    return list_parsed_data


def write_csv_data(jsons, output_path: Path, file_name: str = None):
    """Escreve um ou mais arquivos CSV"""
    i = 1
    for data in jsons:
        file_name = f"{file_name}.csv"
        logger.info("Saving file %s in folder %s", file_name, output_path)
        new_path = Path.joinpath(output_path, file_name)
        with new_path.open(mode="w") as file:
            for d in data:
                newline = (
                    str(d)
                    .replace("'", "")
                    .strip()
                    .replace("[", "")
                    .replace("]", "")
                    .translate({ord(ws): None for ws in string.whitespace})
                )
                file.write(f"{newline}\n")
        i += 1
