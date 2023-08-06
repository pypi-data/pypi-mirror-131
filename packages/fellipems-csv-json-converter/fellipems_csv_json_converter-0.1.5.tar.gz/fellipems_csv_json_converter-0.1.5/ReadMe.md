# File Converter

CSV / JSON converter

### project

funcao: Converte_JSONCSV(modo,sep)

Converte um arquivo ou pasta de arquivos do formato **CSV** para **JSON**. a funcao possui as variaveis 'modo' (opcional), 'sep' (opcional) e 'Arq' (obrigatorio)
        
       Arq: um arquivo ou pasta (string). caso seja passado para a funcao um unico arquivo, este sera convertido. Caso seja passada uma pasta, serao convertidos todos os arquivos do tipo compativel
       
           Obs.:os arquivos convertidos serao salvos na mesma pasta do arquivo original e com mesmo nome, sobrescrevendo arquivos que eventualmente existam na pasta
       
       modo: o modo padrao de conversao e CSV para JSON (modo='csv2json'), porem caso seja passado o parametro 'json2csv' na variavel 'modo', a conversao sera feita no sentido contrario
       
       sep : o separador padrao para o arquivo CSV sera ',' (virgula), porem um separador diferente pode ser especificado atraves da variavel 'sep'

pip install fellipems_csv_json_converter

#csv_converter --help
