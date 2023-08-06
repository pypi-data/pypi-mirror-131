import logging
from os import name
from pathlib import Path
import click
import os

logging.basicConfig(
    level='DEBUG', format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'")
logger = logging.getLogger(__name__)

@click.command()
@click.option("--input", "-i", default="./", help="Path where to read the files for conversion.", type=str)

@click.option("--output", "-o", default="./", help="Path where to read the files will be saved.", type=str)

@click.option("--delimiter", "-d", default=",", help="Separator used to split the files.", type=str)

@click.option("--prefix","-prefix", prompt=True, prompt_required=False, default='file',  
    help=(
        "Prefix used to prepend to the name of the converted file saved on disk."
        "The suffix will be a number starting from 0. ge: file_0.json."),)


def converter(
    input: str = "./", output: str = "./", delimiter: str = ',', prefix: str = None):  
    #Esta função faz a leitura de um arquivo .csv ou de uma pasta contendo vários arquivos .csv
   
    input_path = Path(input)
    
    output_path = Path(output)
    
    logger.info("Input Path: %s", input_path)
    
    logger.info("Output Path: %s", output_path)
    
    for p in [input_path, output_path]:
        if not (p.is_file() or p.is_dir()):
            raise TypeError("Não é um path/rquivo válido")
        
    data = leitor_csv(source=input_path, delimiter=delimiter)
    
    json_writer_save(csvs=data, output_path=output_path, prefix=prefix)
    
def arq_tipo(filename):
    if filename.endswith('.csv'):
        return 'csv'
    else:
        return 'json'
    
#Esta função faz a leitura de um arquivo .csv ou de uma pasta contendo vários arquivos .csv      
def leitor_csv(input_path: Path, delimiter: str = ',' or ';') -> list[list[str]]:
    
    if input_path.is_file():
        logger.info("Lendo um único arquivo %s", input_path)
        with input_path.open(mode = 'r') as arquivo:
            data = arquivo.readlines()        
        return [line.strip().split(delimiter) for line in data] #o comando .strip retira os caracteres especiais da lista 
    #(\n, \t, etc) e o comando .split divide a nossa lista em pequenas strings com o delimitador escolhido.
    
    logger.info("Lendo todos os arquivos para um determinado path %s", input_path)
    
    data = list()
    
    for name in input_path.iterdir():
        data.append(
            
            leitor_csv(filepath_or_buffer=name, delimiter=delimiter, index_col=False)
        )
    return tuple(data)

#Esta função converte a lista de dados em .csv para o formato .json
def csv_para_json(data: list[list[str]]) -> list[dict[str, str]]:
    coluna = data[0] #a primeira lsta do arquivo contém as colunas do meu arquivo .csv, que é referenciado
    linhas = data[1:]
    return [dict(zip(coluna, linha)) for linha in linhas]

#Essa função escreve os dados no formato .json
def escreve_linha(linha: tuple, io, append_comma: bool):
    chave, valor = linha
    
    if append_comma:
        io.write(f'\t\t"{chave}": "{valor}",\n')
    else:
        io.write(f'\t\t"{chave}": "{valor}"\n')
        
#Esta função converte os dados para um dicionário
def escreve_dicionario(data: dict, io, append_comma: True):
    io.write('\t{\n')
    
    items = tuple(data.items())
    for linha in items[:-1]:
        escreve_linha(linha, io, append_comma = True)
    escreve_linha(items[-1], io, append_comma = False)
    
    io.write('\t}')
    
    if append_comma:
        io.write(',\n')
    else:
        io.write('\n')
        
#Esta função escreve um dicionário no formato .json e salva em disco em um endereço específico
def json_writer_save(data: list[dict[str, str]], output_path: Path):
    with output_path.open(mode = 'w') as arquivo:
        arquivo.write('[\n')
        
        for d in data[:-1]:
            escreve_dicionario(d, arquivo, append_comma = True)
        
        escreve_dicionario(data[-1], arquivo, append_comma = False)
        arquivo.write(']\n')
        
        tuple(data[0].items())

#Esta função abre o arquivo e trata as linhas, adicionando variável somente quem possue chave
def trata_arquivo(filename):
    linhas_tratadas =[]
    with open(filename, encoding='utf-8') as f:
        for line in f:
            if ':' in line:
                line = line.replace(" ", "").replace("\n", "").replace("\t", "")
                linhas_tratadas.append(line)
    return linhas_tratadas


#Esta função identifica o cabeçalho do arquivo .csv
def cabecalho(filename):    
    header = []
    lines = trata_arquivo(filename)

    for i in range(0, len(lines)):
        inicial = lines[i].find('"')
        final = lines[i].find(":")
        
        lines[i] = lines[i][inicial+1:final-1]

    return list(dict.fromkeys(lines))

#Esta função converte o arquivo .csv para .json
def json_para_csv(filename, output):
    cabecalho_1 = cabecalho(filename)
    lines = trata_arquivo(filename)
    Arquivo_final = []
    cabecalho_temporario = ''

    #input do header no arquivo CSV
    for c in cabecalho_1:
        if not cabecalho_temporario =='':
            cabecalho_temporario = cabecalho_temporario + ',' + c
        else:
             cabecalho_temporario = cabecalho_temporario + c   
    
    #adiciona o cabeçalho na versão final do arquivo
    Arquivo_final.append(cabecalho_temporario.replace(',',';'))

    #remove as chaves das linhas do arquivo
    for l in range(0,len(lines)):
        for c in cabecalho_1:
            lines[l] = lines[l].replace(c, "")

    #remove alguns outros caracteres das linhas
    cabe = len(cabecalho_1)
    for _ in range(0,cabe):
        line = ''
        virgula = ';'
        for m in range(0,len(lines)):
            if m+1 == cabe: virgula = ''
            line = line + lines[m].replace('"','').replace(':','').replace(',','') + virgula
            if m+1 == cabe:
                Arquivo_final.append(line)
                line = ''
                cabe += len(cabecalho_1)
                virgula = ';'

    #grava os dados no arquivo convertido
    with open(output, mode='w') as file:
        file.writelines(["%s\n" % item for item in Arquivo_final])


def executar():
    filename = ''
    while not os.path.isfile(filename):
        print('\nNome do arquivo de origem:')
        filename = input()

    print('\nNome do arquivo de saída:')
    output = input()
    tipo_arquivo_origem = arq_tipo(filename)
    if tipo_arquivo_origem == 'csv':
        delimitador = ''
        while delimitador not in [',',';']:
            print('\nInforme o delimitador ("," ou ";"):')
            delimitador = input()

    #Exemplo: filename = 'file01.json' -> output = 'file01Oi.csv'
    #delimitador = ';'

    tipo_arquivo_origem = arq_tipo(filename)

    if tipo_arquivo_origem == "json":
        json_para_csv(filename, output)
    else:
        json_para_csv(filename, output, delimitador)