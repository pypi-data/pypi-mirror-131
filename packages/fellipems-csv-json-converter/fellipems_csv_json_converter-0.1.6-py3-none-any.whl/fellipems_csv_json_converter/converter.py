#!/usr/bin/env python
# coding: utf-8

import click
import pathlib as path


@click.command()
@click.option("--modo", "-m", default="csv2json", help="conversao de formato a ser realizada (csv2json ou json2csv)", type=str,)
@click.option("--sep", "-s", default=",", help="separador do arquivo CSV", type=str,)
@click.option("--Arq", "-a", prompt=True, prompt_required=True, default="./", help=("Caminho da pasta ou arquivo a ser convertido"),)


def Converte_JSONCSV(Arq='./', modo='csv2json',sep=','):

    """Converte um arquivo ou pasta de arquivos do formato CSV para JSON. variaveis 'Arq', 'modo' (opcional)
        e 'sep' (opcional)
        
       Arq: um arquivo ou pasta (string). caso seja passado para a funcao um unico arquivo, este 
           sera convertido. Caso seja passada uma pasta, serao convertidos todos os arquivos do tipo 
           compativel
       
           Obs.:os arquivos convertidos serao salvos na mesma pasta do arquivo original e com mesmo nome, 
           sobrescrevendo arquivos que eventualmente existam na pasta
       
       modo: o modo padrao de conversao e CSV para JSON, porem caso seja passado o parametro
           'json2csv' na variavel 'modo', a conversao sera feita no sentido contrario
       
       sep: o separador padrao para o arquivo CSV e ',' (virgula), porem um separador diferente
           pode ser especificado atraves da variavel 'sep'
    """
    print('')
    #Arq=input('Entre com o arquivo ou diretorio a ser convertido: ')

    p0=path.Path(Arq)
    if modo=='csv2json': #extensao procurada nos arquivos de origem
        ext='.csv' 
    elif modo=='json2csv':
        ext='json' 
    else: 
        print('Erro: o modo pode ser apenas "csv2json" (padrao) ou "json2csv"')
        return
    
    if p0.is_dir():
        for x in p0.iterdir():
            if not x.is_dir() and str(x)[-4:]==ext:              
                
                print('Convertendo: ',x)                
                if modo=='csv2json':
                    CSV2JSON(x,sep)
                else:
                    JSON2CSV(x,sep)
                
    elif p0.is_file() and str(Arq)[-4:]==ext:
        
        print('Convertendo: ',Arq)
        if modo=='csv2json':
            CSV2JSON(Arq,sep)
        else:
            JSON2CSV(Arq,sep)
            
    else:
        print('Erro: Arquivo ou pasta invalidos :-/')
        
    print('Concluido\n')





def CSV2JSON(Arq, sep):
    #Conversao de um arquivo CSV para JSON
    
    with open(str(Arq), 'r') as f:
        Data0=f.read()
    Data1=[i.split(sep) for i in Data0.split('\n')]
    
    Data2=[]   #Criando lista de dicionarios
    for i in range(1,len(Data1)-1):
        x1={}

        for j in range(len(Data1[0])): 
            if Data1[i][j].find('.')>-1:  #reconhecendo ints e floats
                try:
                    x2=float(Data1[i][j])
                except:
                    x2=Data1[i][j]
            else:
                try:
                    x2=int(Data1[i][j])
                except:
                    x2=Data1[i][j]
            x1[Data1[0][j]]=x2
        Data2.append(x1)
    Data2=str(Data2)

    Data2=Data2.replace(" '","'"); Data2=Data2.replace("'",'"')
    Data2=Data2.replace('[','[\n'); Data2=Data2.replace('{','{\n')
    Data2=Data2.replace('}','\n}'); Data2=Data2.replace(']','\n]')
    Data2=Data2.replace(',',',\n')

    with open(str(Arq)[0:-3]+'json','w') as f:
        f.write(Data2)



def JSON2CSV(Arq, sep):
    #Conversao de um arquivo JSON para CSV
    
    with open(str(Arq),'r') as f:
        lines=f.readlines()

    #reconhecendo titulos de colunas
    i=2; Data0=[[]]
    while i<len(lines):
        if lines[i].find('}')>-1:
            break
        else:
            x=lines[i].split(':')[0]
            x=x.replace('"','')
            Data0[0].append(x)
        i+=1

    l=0   #numero da linha
    for i in range(len(lines)):
        if lines[i].find('[')>-1:
            continue
        elif lines[i].find('{')>-1:
            l=l+1
            Data0.append([])
        elif lines[i].find('}')>-1:
            continue
        elif lines[i].find(']')>-1:
            continue
        else:
            x=lines[i].split(':')[1]
            x=x.replace(',\n',''); x=x.replace('\n','')
            x=x.replace('"',''); x=x.replace("'","")
            x=x.strip()
            Data0[l].append(x)

    Data1=str(Data0)
    Data1=Data1.replace('[[',''); Data1=Data1.replace(']]','')
    Data1=Data1.replace('], [','\n'); Data1=Data1.replace(', ',',')
    Data1=Data1.replace("'","")

    Data1=Data1.replace(',',sep) #substituindo por separador personalizado
    with open(str(Arq)[0:-4]+'csv','w') as f:
        f.write(Data1)





