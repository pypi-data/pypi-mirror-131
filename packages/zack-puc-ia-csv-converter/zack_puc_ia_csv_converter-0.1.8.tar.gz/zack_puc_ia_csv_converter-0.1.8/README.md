# Arquivo Converter

- **CSV** para conversor **JSON**.
- **JSON** para conversor **CSV**.

## Introdução

### O que este projeto pode fazer

- Leia um arquivo **CSV** ou uma pasta com **CSV** e converta-os em **JSON**.
- Leia um arquivo **JSON** ou uma pasta com **JSON** e converta-os em **CSV**.

Este projeto é um programa em execução no terminal, de preferência instalado com pipx:

`` `
pipx install zack-puc-ia-csv-converter
`` `

Para usar, basta digitar:

`` `
$ converter --help
`` `

### Isso listará todas as opções disponíveis.
  Converta um único arquivo ou lista de arquivos **CSV** para **JSON** ou arquivos **JSON** para arquivos **CSV**.

Opcoes:
-  -t, --type TEXT             Tipo de arquivo que será lido é convertido(CSV ou JSON).
-  -i, --input TEXT            Caminho onde os arquivos serão carregados para conversão.
-  -o, --output TEXT           Caminho onde os arquivos convertidos serão salvos.
-  -d, --delimiter [,|;|:|\t]  Separador usado para dividir os arquivos.
-  -p, --prefix TEXT           Prefixo de TEXTO usado para preceder ao nome do convertido
                               arquivo salvo no disco. O sufixo será um número
                               começando de 1 a N.Caso nao seja passado nenhum prefixo será utilizado o file_.
-  --help                      Mostra esta mensagem e sai.
