import logging
from os import F_OK, path, read, replace
from typing import List
from click.decorators import pass_context

from click.termui import prompt
from pathlib import Path
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
    help="Path where to read the files for conversion",
    type=str
)
@click.option(
    "--output",
    "-o",
    default= './',
    help="Path where converted files will be saved",
    type=str
)
@click.option(
    "--delimiter",
    "-d",
    default= ';',
    help="Separator used to split the files",
    type=str
)
@click.option(
    "--prefix",
    "-p",
    prompt=True,
    prompt_required = False,
    default='file',
    help = (
        "Prefix used for prepend to the name of the converted file saved on disk"
        "The suffix will be a number starting from 0. ge: file_0.json"
    )
)    
def converter(input : str = './', output: str = './', delimiter: str = ',', prefix: str = None):
    """Convert a single file or list of csv to Json.
    """
    input_path = Path(input)
    output_path = Path(output)
    log.info("Input Path: %s", input_path)
    log.info("Output Path: %s", output_path)

    for p in[input_path, output_path]:
        if not(p.is_file() or p.is_dir()):
            raise TypeError("Not a valid path or file name.")
    
    data = read_csv_file(source = input_path, delimiter = delimiter)
    json_data = parse_csv_to_json(data)
    #save_to_json_files(json_data, source= output_path, prefix = prefix)  
    write_json_data(json_data, output_path, prefix)

def parse_csv_to_json(data) -> list:
    """Tranform datas for dict in Json"""
    header = data[0]
    body = data[1:]

    result = [dict(zip(header,bodys)) for bodys in body]
    return result

def write_line(line: tuple, io, append_comma: bool):
    key, value = line
    if append_comma:
        io.write(f'\t\t"{key}": "{value}",\n')
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
    log.info("Saving file %s in folder %s", file_name, source)
    with open(file_name, "w") as outfile:
        outfile.write("[\n")
        for d in data[:-1]:
            write_dictionary(d, outfile, append_comma=True)
        write_dictionary(data[-1], outfile, append_comma=False)
        outfile.write("]\n")
      

def save_to_json_files(data_json: list, source: path, prefix: str):
    file_name = source.joinpath(f"{prefix}.json")
    log.info("Saving file %s in folder %s", file_name, source)
    with open(file_name, "w") as outfile:
        outfile.write("[\n")
        for index_d,d in enumerate(data_json):
            outfile.write("".ljust(4, " ") + "{\n")
            items = tuple(d.items())
            
            for index_line,line in enumerate(items):
                key, value = line    
                if(index_line != len(d)-1):
                    s = '{}: {}\n'.format('"' + key + '"', '"' + value + '"'+ ",")
                elif(index_line == len(d)-1):
                    s = '{}: {}\n'.format('"' + key + '"', '"' + value + '"')
                outfile.write("".ljust(8," ") + s)
            
            if(index_d != (len(data_json)-1)):
                outfile.write("".ljust(4, " ") + "},\n")
            
            elif(index_d == (len(data_json)-1)):
                outfile.write("".ljust(4, " ") + "}\n")
        outfile.write("]\n")

def read_File_single_arch(source:Path, delimiter:str) -> list:
    """Read a single archive csv."""
    with open(source,'r') as file:
        line = file.readlines()
    
    data_list = [lines.strip().split(delimiter) for lines in line]
    return data_list 
    
def read_File_path(source:Path, delimiter:str, name) -> list:
    """Read archives from an Path"""
    with open(name,"r") as file:
      line = file.readlines()
      
    data_list = [lines.strip().split(delimiter) for lines in line]
    return data_list 
   
def read_csv_file(source: Path, delimiter: str):
  
    if source.is_file():
        log.info("Reading Single File %s", source)
        data = read_File_single_arch(source, delimiter)
        return data

    log.info("Reading all files for given path %s", source)
    for name in source.iterdir():
        data = read_File_path(source, delimiter,name)
        return data

@click.command()
@click.option(
    "--input",
    "-i",
    default= './',
    help="Path where to read the files for conversion",
    type=str
)
@click.option(
    "--output",
    "-o",
    default= './',
    help="Path where converted files will be saved",
    type=str
)
@click.option(
    "--prefix",
    "-p",
    prompt=True,
    prompt_required = False,
    default='file',
    help = (
        "Prefix used for prepend to the name of the converted file saved on disk"
        "The suffix will be a number starting from 0. ge: file_0.json"
    )
) 
def converter2(input : str = './', output: str = './', prefix: str = None):
    """converter aqui.
    """
    input_path = Path(input)
    output_path = Path(output)
    log.info("Input Path: %s", input_path)
    log.info("Output Path: %s", output_path)

    for p in[input_path, output_path]:
        if not(p.is_file() or p.is_dir()):
            raise TypeError("Not a valid path or file name.")
    
    data = read_json_file(source = input_path)
    json_data = parse_json_to_csv(data)
    write_csv_data(json_data, output_path, prefix)

def write_csv_data(data: list,source: path, prefix: str):
    file_name = source.joinpath(f"{prefix}.csv")
    log.info("Saving file %s in folder %s", file_name, source)
    string = ""
    string_body = ""

    with open(file_name, "w") as outfile:
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
                        
def parse_json_to_csv(data) -> list:
    list_header = []
    list_header_body = []
    string = ""
    parsed_data = [line.strip() for line in data]
    
    for i,line in enumerate(parsed_data):
        if(line != "[" and line != "{" and line != "," and line != "]"):
            string = string + line
    for index_s,s in enumerate(string.split("}")):
        if(i < (len(s) - 1)):
           for i,data_split in enumerate(s.split(",")):
               data_split = data_split.replace('"',"")
               header, body = data_split.split(":")
               if(index_s ==0):
                list_header.append(header)
               if(i==0):
                list_body = []
               list_body.append(body)    
           list_header_body.append(list_body)
    list_header_body.append(list_header)
    return list_header_body
    
def read_json_File_single_arch(source:Path) -> list:
    """Leitura do arquivo csv."""
    with open(source,'r') as file:
        data = file.readlines()
    return data
    
def read_json_File_path(source:Path, name) -> list:
    """leitura path"""
    with open(name,"r") as file:
      data = file.readlines()
    return data    


def read_json_file(source: Path):
 
    if source.is_file():
        log.info("Reading Single File %s", source)
        data_json = read_json_File_single_arch(source)
        return data_json

    log.info("Reading all files for given path %s", source)
    for name in source.iterdir():
        data = read_json_File_path(source,name)
        return data
    
    

    
        


      
            