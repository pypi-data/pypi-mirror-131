import logging
from os import F_OK, path, read, replace
from typing import List
from click.decorators import pass_context
from abc import abstractproperty
from pathlib import Path

from click.termui import prompt

import click


logging.basicConfig(
    level='DEBUG',
    format = "'%(asctime)s - %(name)s - %(levelname)s - %(message)s'"
)


log = logging.getLogger(__name__)

@click.command()
@click.option(
    "--input",
    "-i",
    default= './',
    help="Caminho para identificar o arquivo a ser convertido",
    type=str
)
@click.option(
    "--output",
    "-o",
    default= './',
    help="Local para salvar o arquivo convertido",
    type=str
)
@click.option(
    "--delimiter",
    "-d",
    default= ',',
    help="Informe o delimitador a ser considerado",
    type=str
)
@click.option(
    "--prefix",
    "-p",
    prompt=True,
    prompt_required = False,
    default='file',
    help = (
        "Informe o nome a ser salvo do arquivo convertido"
        
    )
)   

def conversor_de_csv_para_json(input:str='./', output: str ="./", prefix: str= None, delimiter: str =","):
    
    "Função que converter arquivo no formato CSV para JSON"
    "Necessita ser informado o caminho de entrada e saida, nome do arquivo e delimitador"
    
    c_saida = Path(output)
    c_entrada = Path(input)
    
    log.info("Input Path: %s", c_entrada)
    log.info("Output Path: %s", c_saida)

    for c in [c_saida,c_entrada]:
        if not(c.is_file() or c.is_dir()):
            raise TypeError("Variaveis informadas para caminho de entrada e saida invalidos!")
    
    #Aqui começa rodar o codigo da função conversor
    dados = read_csv(source = c_entrada, delimit=delimiter)
    dados_json = parse_csv_to_json(dados)
    write_json_data(dados_json, c_saida, prefix)

def read_csv(source: Path, delimit: str):
    """Carregar arquivos CSV do computador.
    Args:
        source (Path): Caminho para um arquivo CSV ou diretorio com varios;
        delimiter (str): O delimitador de colunas a ser considerado.
    Return:
        Dict: É extraido um dicionario do CSV.
    """
    if source.is_file():
        log.info("Lendo um simples arquivo %s", source)
        data = read_File_single_arch(source, delimit)
        return data

    log.info("Lendo todos arquivos do caminho %s", source)
    for name in source.iterdir():
        data = read_File_path(source, delimit,name)
        return data 


def read_File_path(delimiter:str, name) -> list:
    """Lendo arquivo do diretorio"""
    with open(name,"r") as file: line = file.readlines()
      
    data_list = [lines.strip().split(delimiter) for lines in line]
    return data_list 
   
def read_File_single_arch(source:Path, delimiter:str) -> list:
    
    with open(source,'r') as file: line = file.readlines()
    
    data_list = [lines.strip().split(delimiter) for lines in line]
    return data_list 



def parse_csv_to_json(data: list) -> list:
    "Transforma o arquivo em dict de Json"
    column = data[0]
    lines = data[1:]
    return [dict(zip(column, line)) for line in lines]
    
def write_line(line: tuple, io, append_comma: bool):
    key, value = line
    if append_comma:io.write(f'\t\t"{key}": "{value}",\n')
    else:
        io.write(f'\t\t"{key}": "{value}"\n')
        io.write("\t}\n")

def write_dictionary(data:dict,io,append_comma:True):
    io.write("\t{\n")
    items = tuple(data.items())
    
    for line in items[:-1]:
        write_line(line, io,append_comma=True)
    write_line(items[-1],io,append_comma=False)
    if append_comma:
        io.write("\t,\n")

def write_json_data(data: list,source: path, prefix: str):
    file_name = source.joinpath(f"{prefix}.json")
    log.info("Salvando o arquivo %s na pasta %s", file_name, source)
    with open(file_name, "w") as outfile:
        outfile.write("[\n")
        for d in data[:-1]:
            write_dictionary(d, outfile, append_comma=True)
        write_dictionary(data[-1], outfile, append_comma=False)
        outfile.write("]\n")




@click.command()
@click.option(
    "--input",
    "-i",
    default= './',
    help="Caminho para identificar o arquivo a ser convertido",
    type=str
)
@click.option(
    "--output",
    "-o",
    default= './',
    help="Local para salvar o arquivo convertido",
    type=str
)

@click.option(
    "--prefix",
    "-p",
    prompt=True,
    prompt_required = False,
    default='file',
    help = (
        "Informe o nome a ser salvo do arquivo convertido"
        
    )
)
    
def conversor_de_json_para_csv(input:str='./', output: str ="./", prefix: str= None):
    "Função que conveter arquivo no formato JSON para CSV"
    "Necessita ser informado o caminho de entrada e saida, nome do arquivo e delimitador"
    
    c_saida = Path(output)
    c_entrada = Path(input)

    for c in [c_saida,c_entrada]:
        if not(c.is_file() or c.is_dir()): raise TypeError("Variaveis informadas para caminho de entrada e saida invalidos!")
    
    #Aqui começa rodar o codigo da função conversor
    data = read_json(caminho = c_entrada)
    json_data = parse_json_to_csv(data)
    write_csv_data(json_data, c_saida, prefix)

def read_json(caminho:Path) -> list:
    """ Carregar o arquivo JSON do computador.
    Parametros: 
        caminho: corresponde ao local do arquivo;
        demiliter: corresponde a string delimitadora;
    Saída:
        Dict: Como saida tem-se um dicionario"""
    
    if caminho.is_file():
        data_json = read_json_File_single_arch(caminho)
        return data_json

    
    for name in caminho.iterdir():
        data = read_json_File_path(caminho)
        return data

def read_json_File_path(source:Path) -> list:
    """Ler arquivos de um caminho"""
    files = [*source.iterdir()]


def read_json_File_single_arch(source:Path) -> list:
    """ler um arquivo de um caminho."""
    with open(source,'r') as file:
        data = file.readlines()
    return data

def read_arquivos_json_path(source:Path)-> list:
    """Ler arquivos de um caminho"""
    files = [*source.iterdir()]



def parse_json_to_csv(data: list) -> list:
    ''' converte list de dados de csv para formato json'''
    list_cbc = []
    list_text = []
    string = ""
    parsed_data = [line.strip() for line in data]
    
    for i,line in enumerate(parsed_data):
        
        if(line != "[" and line != "{" and line != "," and line != "]"):
            string = string + line
    for index_s,s in enumerate(string.split("}")):
        if(i < (len(s) - 1)):
           for i,data_split in enumerate(s.split(",")):
               data_split = data_split.replace('"',"")
               cbc, texto = data_split.split(":")
               if(index_s ==0):
                list_cbc.append(cbc)
               if(i==0):
                list_corpo = []
               list_corpo.append(texto)    
           list_text.append(list_corpo)
    list_text.append(list_cbc)
    return list_text


#parse_json_to_csv(data)  
def write_csv_data(data: list,output_path:Path, nome_arquivo:str):
    nome = output_path.joinpath(f"{nome_arquivo}.csv")
    string = ""
    string_body = ""
    with open(nome,mode="w") as outfile:
        for i,datas1 in enumerate(data):
            if(i == (len(data) -1)):
                for index_d,d in enumerate(datas1):
                    if(index_d < (len(datas1)-1)):
                        string = string + d + "," 
                    else:
                        string = string + d;   
        outfile.write(string + "\n")     

        for i,datas2 in enumerate(data):
            if(i != (len(data) -1)):
                for index_body,body in enumerate(datas2):
                    if(index_body < (len(datas2)- 1)):
                        string_body = string_body.strip() + body + ","
                    else:
                        string_body = string_body.strip() + body
                        outfile.write(string_body + "\n")
                        string_body = ""