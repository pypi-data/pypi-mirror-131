import logging
from pathlib import Path
from sys import prefix
from typing import List

logging.basicConfig(level="DEBUG", format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'")

log = logging.getLogger(__name__)


def read_csv_Virg(input_path: Path, delimiter: str = ",") -> list:
    """faz a leitura do arquivo CSV ou pasta cotendo varios arquivos"""
    with input_path.open(mode="r") as file:
        data = file.readlines()

    return [line.strip().split(delimiter) for line in data]


def read_csv_2Pont(input_path: Path, delimiter: str = ":") -> list:
    """faz a leitura do arquivo CSV ou pasta cotendo varios arquivos"""
    with input_path.open(mode="r") as file:
        data = file.readlines()

    return [line.strip().split(delimiter) for line in data]


def parse_csv_to_json(data: list) -> list:
    """converte list de dados de csv para formato json"""
    column = data[0]
    lines = data[1:]
    return [dict(zip(column, line)) for line in lines]


def write_line(line: tuple, io, append_comma: bool):
    key, value = line
    if append_comma:
        io.write(f'\t\t"{key}": "{value}",\n')
    else:
        io.write(f'\t\t"{key}": "{value}"\n')
        io.write("\t}\n")


def write_dictionary(data: dict, io, append_comma: True):
    io.write("\t{\n")
    items = tuple(data.items())
    for line in items[:-1]:
        write_line(line, io, append_comma=True)
    write_line(items[-1], io, append_comma=False)

    if append_comma:
        io.write("\t,\n")


def write_json_data(data: list, output_path: Path):
    """escreve um dicionario json em disco no endereco"""
    with output_path.open(mode="w") as file:
        file.write("[\n")
        for d in data[:-1]:

            write_dictionary(d, file, append_comma=True)
        write_dictionary(data[-1], file, append_comma=False)
        file.write("]\n")


def lendo_json(input_path: Path) -> list:
    with input_path.open(mode="r") as file:
        dataj = file.readlines()
    return dataj


def conv_jsonToCSV(data: list) -> list:
    """converte lista de dados de json para formato csv"""

    psd_dt = [line.strip() for line in data]
    _str = ""

    for indline, line in enumerate(psd_dt):
        # line = str(line)
        # line = line.replace("[","").replace("{","").replace(",","").replace("]","").replace("\n","")
        # line = str(line)
        # print(line)
        if line != "[" and line != "{" and line != "," and line != "]":
            _str = _str + line
            # print(line)
            # print(_str)
    lstCab = []
    lstCabCorp = []

    for index, st in enumerate(_str.split("}")):

        if indline < (len(st) - 1):
            for indline, dt_split in enumerate(st.split(",")):

                dt_split = dt_split.replace('"', "").replace(" ", "")
                cab, corp = dt_split.split(":")

                if index == 0:
                    lstCab.append(cab)

                if indline == 0:
                    lstCorp = []
                lstCorp.append(corp)
            lstCabCorp.append(lstCorp)

    lstCabCorp.append(lstCab)

    return lstCabCorp


def write_csv_data(data: list, output_path: Path):
    """escreve um dicionario CSV em disco no endereco"""
    str_ = ""

    with output_path.open(mode="w") as file:
        for i, dados in enumerate(data):
            if i == (len(data) - 1):
                for indx_d, d in enumerate(dados):
                    if indx_d < (len(dados) - 1):

                        str_ = str_ + d + ","
                    else:
                        str_ = str_ + d
        file.write(str_ + "\n")

        str_bdy = ""
        for ix, dds in enumerate(data):
            if ix != (len(data) - 1):
                for indbdy, bdy in enumerate(dds):
                    if indbdy < (len(dds) - 1):
                        str_bdy = str_bdy.strip() + bdy + ","
                    else:
                        str_bdy = str_bdy.strip() + bdy
                        file.write(str_bdy + "\n")
                        str_bdy = ""


def write_list(data: list, io, append_comma: False):

    items = tuple(data)
    for line in items:
        value = line
        io.write(value)


def converterTocsv():
    """Converte um arquivo ou lista de arquivos csv para Json ou Json para CSV"""



print("\n\nBem Vindo ao Converter CSV_>_JSON | JSON_>_CSV -- by: Ozeas Santos")
print("*Trabalho Python - PUC Minas - Turma 3.2 - 02/2021*\n")

csvOUjson = int(input("Digite: \n 1 para converter CSV_>_JSON.\n 2 para converter JSON_>_CSV:\n"))


if csvOUjson < 1 or csvOUjson > 2:
    raise TypeError("Opção Invalida - Por favor repita a operação")
    log.info("Erro: Opção Invalida CSV ou JSON %s", csvOUjson)

if csvOUjson == 1:
    print(f"Você escolheu CSV_>>>_JSON\n")
    
    arqOudir = int(input("\n Digite 3 para selecionar o arquivo CSV a ser convertido. \n Digite 4 para selecionar diretorio com arquivos CSVs a serem convertidos\n\n OPÇÃO: "))
    
    if arqOudir < 3 or arqOudir > 4:
        raise TypeError("Opção Invalida - Por favor repita a operação")
        

    if arqOudir == 3:        
        #input_path = Path(input("Informe o caminho e o nome do arquivo CSV a ser convertido.\n Ex: tests/input/arquivo.csv \n Caminho:"))
        #print(input_path)
        rota = input("Informe o local onde está seu arquivo CSV a ser convertido. \n Ex: /TESTS/INPUT \n Caminho: ")
        narquivo = input("Informe o nome do arquivo. Ex: arquivo.csv \n Nome do arquivo: ")
        input_path = filter(Path.is_file, Path(rota).rglob(f"{narquivo}"))
    
    
    if arqOudir == 4:
        rota = input("Informe o local onde estão seus arquivos CSV a ser convertido. \n Ex: /TESTS/INPUT \n Caminho: ")
        input_path = filter(Path.is_file, Path(rota).rglob(f"*.csv"))
        #rota = input("Informe o caminho para acesso aos arquivos CSVs: \n Ex: TESTE/INPUT \n Caminho:")
        #input_path = filter(Path.is_file, Path().rglob(f"{rota}/*.csv"))
        #log.info("Diretorio Selecionado: %s", arqOudir == 4)
    
    


    for csv in input_path:
        print(f"Arquivo a ser convertido: {csv}")
        #log.info("Input Path: %s", csv)
        delim = int(
            input(f"\nEscolha o delimitador:\n 1 para ',' (virgula) \n 2 para ':' (2 Pontos)\n")
        )

        if delim == 1:
            #log.info("delimitador = virgula: %s", delim)
            data = read_csv_Virg(csv)
            json_data = parse_csv_to_json(data)
            write_json_data(json_data, Path(f"{csv}.json"))
            print("Textos separados por virgula\n")
            print(f"{csv}.json gerado com sucesso!\n\n")

        elif delim == 2:
            #log.info("delimitador = virgula: %s", delim)
            data = read_csv_2Pont(csv)
            json_data = parse_csv_to_json(data)
            write_json_data(json_data, Path(f"{csv}.json"))
            print("Textos separados por 2 pontos\n")
            print(f"{csv}.json gerado com sucesso!\n\n")


elif csvOUjson == 2:
    
    
    print(f"Você escolheu JSON_>>>_CSV \n")
    
    arqOudir = int(input("\n Digite 3 para selecionar o arquivo JSON a ser convertido. \n Digite 4 para selecionar diretorio com arquivos JSON a serem convertidos\n OPÇÃO: "))
    
    if arqOudir == 3:

        rota = input("Informe o local onde está seu arquivo JSON a ser convertido. \n Ex: /TESTS/INPUT \n Caminho: ")
        narquivo = input("Informe o nome do arquivo JSON. Ex: arquivo.JSON \n Nome do arquivo: ")
        input_path = filter(Path.is_file, Path(rota).rglob(f"{narquivo}"))
        #rota = Path(input("Informe o caminho e o nome do arquivo JSON a ser convertido.\n Ex: tests/input/arquivo.json. \n Caminho:"))
        #input_path = filter(rota.is_file)
        
        #log.info("input_path: %s", input_path)
    if arqOudir == 4:
        rota = input("Informe o local onde estão seus arquivos JSON a ser convertido. \n Ex: /TESTS/INPUT \n Caminho: ")
        input_path = filter(Path.is_file, Path(rota).rglob(f"*.json"))
        #rota = input("Informe o caminho para acesso aos arquivos JSON: \n Ex: TESTE/INPUT \n Caminho:")
        #input_path = filter(Path.is_file, Path().rglob(f"{rota}/*.JSON"))
        #log.info("input_path: %s", input_path)
    
    if arqOudir < 3 or arqOudir > 4:
        raise TypeError("Opção Invalida - Por favor repita a operação")
        log.info("erro opção invalida: %s",arqOudir)
        

    for json in input_path:

        print(f"Arquivo a ser convertido: {json}")

        if not (json.is_file() or json.is_dir()):
            raise TypeError("Not a valid path or file name.")
            log.info("Erro: nãao e arquivo ou dir %s", json)
        else:
            data = lendo_json(json)
            json_data = conv_jsonToCSV(data)
            write_csv_data(json_data, Path(f"{json}.csv"))
            #log.info("write_csv_data: %s", write_csv_data)
            print(f"\nArquivo gerado com sucesso!\n\n Nome do arquivo: {json}.csv")
            


converterTocsv()
