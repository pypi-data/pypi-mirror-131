import json
import logging  # Biblioteca de log, permite imprimir informações que estão sendo executadas pelo programa
from pathlib import (
    Path,  # Garante que quando esta em outro SO as barras de transição de pastas fiquem corretas
)

import click

# import pandas as pd
from click.termui import prompt

# Configurando o Logging
logging.basicConfig(level="DEBUG", format="'%(asctime)s - %(name)s - %(levelname)s - %()s'")

logger = logging.getLogger(__name__)

# Configurando Click, que aceitara passar comandos para o programa pelo terminal
# input caminho onde estão os dados
# output o mesmo
# delimiter por default é virgula
# O @ informa que a função é do tipo decorator
@click.command()
@click.option(
    "--input", "-i", default="./", help="Path where to read the files for conversion", type=str
)  # comandos usados no terminal
@click.option(
    "--output", "-o", default="./", help="Path where the converted file will be saved", type=str
)  # comandos usados no terminal
@click.option(
    "--delimiter", "-d", default=",", help="Separeted used", type=str
)  # comandos usados no terminal
@click.option(
    "--prefix",
    "-prefix",
    prompt=True,
    prompt_required=False,
    default="file",
    help=(
        "Prefix used to prepend to the name of the converted file saved on disk"
        "The sufix will be a number starting from 0. ge: file_0.json"
    ),
)  # comandos usados no terminal
def converter(input: str = "./", output: str = "./", delimiter: str = ",", prefix: str = None):
    """Convert single file or list of csv to json."""

    input_path = Path(input)
    output_path = Path(output)
    logger.info("Input path: %s", input_path)
    logger.info("Output path: %s", output_path)

    # Verificando se os caminhos passados estão corretos
    for p in [input_path, output_path]:
        if not (p.is_file() or p.is_dir()):
            raise TypeError("Not a valid path or file name.")

    # Função que vai fazer a leitura do projeto
    if input.find(".csv"):
        dataJ2C = read_csv_file(source=input_path, delimiter=delimiter)
        save_to_json_files(csvs=dataJ2C, output_path=output_path, prefix=prefix)
    else:
        dataC2J = read_json_file(source=input_path, delimiter=delimiter)
        save_to_csv_files(csvs=dataC2J, output_path=output_path, prefix=prefix)


if __name__ == "__main__":
    converter()


def modifyCSV2Json(fileIO, delimiter):
    # Primeira linha é considerada as colunas
    colunsNames = fileIO.readline()
    colunsNames = colunsNames.replace("\n", "").split(delimiter)  # type: ignore
    # Resto do arquivo
    linesArquivo = fileIO.readlines()
    list2Save = list()
    for x in linesArquivo:
        x = x.replace("\n", "").split(delimiter)  # type: ignore
        mountDict = {}
        for col in range(len(colunsNames)):
            var = x[col]
            if x[col].isnumeric():
                var = float(x[col])  # type: ignore
            elif x[col] == "":
                var = None  # type: ignore

            mountDict[colunsNames[col]] = var

        list2Save.append(mountDict)
    return list2Save


def read_csv_file(source: Path, delimiter: str) -> tuple:
    data = list()
    if source.is_file():
        arch = open(source, "r")
        data = modifyCSV2Json(arch, delimiter)
        arch.close()
        logger.info("Reading Single File %s", source)
        # return tuple(pd.read_csv(filepath_or_buffer=source, delimiter=delimiter, index_col=False))
        return tuple(data)

    logger.info("Reading all Files %s", source)
    for name in source.iterdir():
        arch = open(name, "r")
        data.append(modifyCSV2Json(arch, delimiter))
        arch.close()
        # data.append(pd.read_csv(filepath_or_buffer=name, delimiter=delimiter, index_col=False))
    return tuple(data)


def ajustingJson(fileIo, listAjust, commaInfo):
    valueLastKeyInDict = list(listAjust[0].keys())[-1]
    for dictInList in listAjust:
        dictInList2Tuple = tuple(dictInList.items())

        fileIo.write("\t{\n")
        for obj in dictInList2Tuple:
            key, value = obj
            if key != valueLastKeyInDict:
                fileIo.write(f'\t\t"{key}": "{value}",\n')
            else:
                fileIo.write(f'\t\t"{key}": "{value}"\n')
        fileIo.write("\t}")
        if commaInfo:
            fileIo.write(",\n")
        else:
            fileIo.write("\n")


def save_to_json_files(csvs: tuple, output_path: Path, prefix: str = None):
    i = 0
    while i < len(csvs):
        file_name = str(output_path) + f"{prefix}_{i}"
        logger.info("Saving file %s in folder %s", file_name, output_path)
        data = csvs[i]
        saveArch = open(file_name, "w")
        saveArch.write("[\n")
        ajustingJson(saveArch, data[:-1], True)
        ajustingJson(saveArch, [data[-1]], False)
        saveArch.write("]\n")
        saveArch.close()
        # data.to_json(path_or_buf=file_name, orient="records", indent=4)
        i += 1


def modifyJson2CSV(fileIO, delimiter):
    stringJSON = fileIO.read()[1:-1]
    findFirstDict = 0
    findNextDict = 0
    colunsCSV = (
        str(list(eval(stringJSON[0 : stringJSON[findFirstDict:].find("}") + 1].strip()).keys()))[
            1:-1
        ]
        .replace(",", delimiter)
        .replace(" ", "")
        + "\n"
    )

    valueLine = list()
    valueLine.append(colunsCSV)
    while findFirstDict != len(stringJSON):
        findNextDict = stringJSON[findFirstDict:].find("}") + findFirstDict + 1
        valueLine.append(
            str(list(eval(stringJSON[findFirstDict:findNextDict].strip()).values()))[1:-1]
            .replace(",", delimiter)
            .replace(" ", "")
            + "\n"
        )

        findFirstDict = findNextDict + 2


def read_json_file(source: Path, delimiter: str) -> tuple:
    data = list()
    if source.is_file():
        fileJSON = open(source, "r")
        data.append(modifyJson2CSV(fileJSON, delimiter))
        return tuple(data)

    for name in source.iterdir():
        fileJSON = open(name, "r")
        data.append(modifyJson2CSV(fileJSON, delimiter))
    return tuple(data)


def save_to_csv_files(csvs: tuple, output_path: Path, prefix: str = None):
    i = 0
    while i < len(csvs):
        file_name = str(output_path) + f"{prefix}_{i}"
        logger.info("Saving file %s in folder %s", file_name, output_path)
        data = csvs[i]
        saveArch = open(file_name, "w", encoding="UTF8")
        saveArch.writelines(data)
        saveArch.close()
        # data.to_json(path_or_buf=file_name, orient="records", indent=4)
        i += 1
