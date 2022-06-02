# Resolução de circuitos

Os códigos desse repositório retornam **apenas** a solução **permanente** de circuitos que possuam resistores, capacitores, indutores e fontes independentes de corrente e tensão. Os dados de entrada são entrados nos arquivos circuitoac e circuitodc no seguinte formato:

1. Nó anterior;
2. Nó posterior;
3. Tipo de elemento (r: resistor; c: capacitor; l: indutor; a: fonte de corrente; v: fonte de tensão; z: impedância);
4. Módulo da quantidade;
5. Valor, em graus, do ângulo (obrigatório quando inserir os elementos tipo a, v, z).


## Observação

Este repositório tem o propósito único e exclusivo de tornar público os códigos apresentados ao término da disciplina TEE00141 Métodos Computacionais para Engenharia Elétrica, cursada durante o período 2020.2 e posteriormente e imediatamente pouco modificados (adição das funçções que lidam com as condições iniciais dos capacitores e indutores). Ou seja, não planejo modificar nem atualizar tais códigos, mesmo que, claramente, precisam.

Como garantia de confiabilidade, peguei diversos circuitos propostos como exercícios pela referência. Os resultados e suas observações seguem abaixo.


### Exercícios cujos resultados foram condizentes com o gabarito proposto

4.1-5, 4.7-9, 4.12-7, 4.21, 4.23, 4.25-7, 4.34-9, 4.41-6, 4.49-1, 4.56, 4.59, 4.80;

7.4-7, 7.9-10, 7.12, 7.17, 7.22, 7.39-42, 7.44, 7.46-8, 7.50, 7.52-3;

8.1-5, 8.14, 8.16-7;

9.35-6, 9.38-53, 9.55, 9.64-5, 9.74, 9.79;

10.1-3, 10.7, 10.13-4, 10.16-7, 10.24-31, 10.34-5, 10.37, 10.40-5, 10.49-58, 10.60, 10.63-5, 10.67.


### Exercícios cujos resultados **não** foram condizentes com o gabarito proposto

4.60-1, 4.66, 4.72, 4.76-8;

7.23, 7.49;

9.54, 9.66;

10.36, 10.38-9, 10.81, 10.86-7.


### Exercícios cujos resultados possuem erros com o gabarito apresentado, porém são numericamente desprezíveis (erros de centésimos, em geral)

7.11, 7.18;

10.83.

Por algum motivo, notei que, dentre os erros, parte significante era circuitos com ligações em estrela.


## Referências

Fundamentos de Circuitos Elétricos; ALEXANDER, Charles K., SADIKU, Matthew; 5a ed, 2013; McGraw Hill.
