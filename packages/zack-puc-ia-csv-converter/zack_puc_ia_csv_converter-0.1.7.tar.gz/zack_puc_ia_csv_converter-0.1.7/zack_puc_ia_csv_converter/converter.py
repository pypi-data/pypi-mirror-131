import logging  # print gurmetizado
from pathlib import Path
import click

logging.basicConfig(
    level="DEBUG", format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'"
)
logger = logging.getLogger(__name__)
@click.command() ## comandos no terminal

# tipo de arquivo
@click.option(
    "--type",
    "-t",
    prompt=True,
    prompt_required=False,
    default="file",
    help=("Tipo do arquivo a ser convertido CSV ou JSON"),
    type = str
)
# caminho de leitura do arquivo
@click.option(
        "--input", 
        "-i", 
        default="./", 
        help="Caminho onde encontrar os arquivos a serem convertidos.", 
        type= str,
) 
# caminho de saida do arquivo
@click.option(
    "--output",
    "-o",
    default="./",
    help="Caminho onde os arquivos convertidos serão salvos.",
    type=str,
)
# delimitador do arquivo
@click.option(
    "--delimiter",
    "-d",
    default=",",
    help="Separador usado para dividir os arquivos.",
    type=str,
)
# prefix
@click.option(
    "--prefix",
    "-p",
    prompt=True,
    prompt_required=False,
    default="file",
    help=(
       "Prefixo usado para preceder o nome do arquivo convertido salvo no disco."
        "O sufixo será um número começando em 0. ge: file_0.json."
    ),
)

def converter(type: str = "csv", input: str = "./", output: str = "./", delimiter: str  = ",", prefix: str = None):
    type_file = type.lower()
    input_path = Path(input)
    output_path = Path(output)
    logger.info("Input Path: %s", input_path)
    logger.info("Output Path: %s", output_path)



    for p in [input_path, output_path]:
        if p.is_file() or p.is_dir():
            print(f"é um arquivo ou diretorio {p}")
        else:
            raise TypeError("Arquivo ou diretorio não é valido")

    if type_file == 'csv':
        data = read_csv(source=input_path, delimiter=delimiter) # leitura de arquivo(s) csv 
        write_json_data(csvs=data, output_path= output_path, prefix=prefix) # sava como json o(s) arquivo(s)
    elif type_file == 'json':
        data = read_json(source=input_path) # leitura de arquivo(s) json 
        write_csv_data(jsons=data, output_path= output_path, delimiter= delimiter, prefix=prefix) # sava como csv o(s) arquivo(s)
    else:
        raise TypeError("Formato de arquivo não permitido")

# lendo 1 ou diretorio contendo arquivos CSV
def read_csv(source: Path, delimiter: str = ","):
    """Carregue os arquivos csv do disco.

    Args:
        source (Path): Caminho de um único arquivo csv ou um diretório contendo arquivos csv.
        delimitador (str): Separador para colunas em csv.

    Retornar:
        tupla: lista de discionarios.
    """
    parsed_data = list()
    if source.is_file():
        logger.info("Realiza a leitura de unico arquivo %s", source)
        with source.open(mode="r", encoding="utf-8-sig") as file:
            lines = file.readlines()
            data = [line.replace("\n", "").split(delimiter) for line in lines]
            result = parse_csv_to_json(data)
            parsed_data.append(result)
        return parsed_data

    logger.info("Realiza a leitura de todos os arquivos do diretorio %s", source)
    
    for i in source.iterdir():
        with i.open(mode="r", encoding="utf-8-sig") as file:
            lines = file.readlines()
            data = [line.replace("\n", "").split(delimiter) for line in lines]
            result = parse_csv_to_json(data)
            parsed_data.append(result)  
    return parsed_data

# realiza a conversão de lista para dict
def parse_csv_to_json(data):
    """Converte  a lista de dados de CSV para formato Json"""
    column = data[0]
    lines = data[1:]
    result = [dict(zip(column, line)) for line in lines]
    return result

# escreve em formato de JSON
def write_json_data(csvs, output_path: Path, prefix: str = None):
    """Salvar em arquivo json no disco.

    Args:
        csvs (dcionarios): Dicionarios que seram jogados em um arquivo Json
        output_path (Path): Caminho onde salvar os arquivos json
        prefix (str): Nome dos arquivos. Se nada for dado, vai  como file_
    """
    i = 0
    while i < len(csvs):
        data = csvs[i]
        file_name = f"{prefix}_{i+1}.json" 
        output = output_path.joinpath(file_name)
        logger.info("Savando o arquivo como: %s", output)
       
        #__import__("IPython").embed()
        with output.open("w") as file:
            file.write("[\n")
            for d in data[:-1]:
                write_dictionary(d, file, append_comma=True)
            write_dictionary(data[-1], file, append_comma=False)
            file.write("]\n")
        i +=1  

def write_line(line: tuple, io, append_comma: bool):
    key, value = line
   
    if not value:
        value = 'null';
    elif is_int(value):
        value = int(value)
    elif is_float(value):
        value = float(value)
    else:
        value = f'"{value}"'

    if append_comma:
        io.write(f'\t\t "{key}": {value}, \n')
    else:
        io.write(f'\t\t "{key}": {value} \n')

def write_dictionary(data: dict, io, append_comma: True):
    io.write("\t{\n")
    items = tuple(data.items())
    for line in items[:-1]:
        write_line(line, io, append_comma=True)
    write_line(items[-1], io, append_comma=False)
    io.write("\t")
    if append_comma:
        io.write("},\n")
    else:
        io.write("}\n")

# lendo 1 ou diretorio contendo arquivos JSON
def read_json(source: Path):
    """Carregue os arquivos Json do disco.

    Args:
        source (Path): Caminho de um único arquivo json ou um diretório contendo arquivos json.
    Retornar:
        lista: lista de dicionarios.
    """
    result = list()
    if source.is_file():
        result.append(eval(open(source, "r").read().replace("null", "None")))
        return result
    
    logger.info("Realiza a leitura de todos os arquivos do diretorio %s", source)
    for i in source.iterdir():
        ##__import__("IPython").embed()
        result.append(list(eval(open(i, "r").read().replace("null", "None"))))
    return result

# escreve em formato CSV
def write_csv_data(jsons: list, delimiter: str, output_path: Path, prefix: str = None):
    """Salva em arquivo csv no disco .

    Args:
        jsons (list): Lista de dicionarios que serão inseridos no(s) arquivo(s) csv.
        delimiter (str): Caracter separador que será utilizado nas colunas do(s) arquivo(s) csv.
        output_path (Path): Caminho onde salvar o(s) arquivo(s) csv.
        prefix (str): Nome do(s) arquivo(s) csv que será salvo em disco.
    """

    j = 0
    while j < len(jsons):
        json = jsons[j]
        data = list()
        file_name = f"{prefix}_{j+1}.csv"
        output = output_path.joinpath(file_name)
        logger.info("Savando o arquivo como: %s", output)
        data.append(list(json[0].keys()))
    
        for k, v in enumerate(json):
            data.append(list(v.values()))
            #__import__("IPython").embed()
        with output.open('w') as file:
            for sublist in data:
               
                for i, item in enumerate(sublist):
                    if item == None:
                        item = ""
                    else:
                        item = str(item)

                    if i == len(sublist)-1:
                        file.write(item)
                    else:
                        file.write(item + delimiter)
                file.write('\n')
        j+=1        

# validar float
def is_float(value: str):
    """Verifica se o valor é float

    Args:
        value (str): recebe string.

    Returns:
        bool: retorna um valor boleano se a strig pode ser convertida em float.
    """
    try:
        a = float(value)
    except (TypeError, ValueError):
        return False
    else:
        return True

# valida inteiro
def is_int(value: str):
    """Verifica se o valor é inteiro

    Args:
        value (str): recebe string.

    Returns:
        bool: retorna um valor boleano se a strig pode ser convertida em inteiro.
    """
    try:
        a = float(value)
        b = int(a)
    except (TypeError, ValueError):
        return False
    else:
        return a == b  