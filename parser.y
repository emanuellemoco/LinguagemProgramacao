/* simplest version of calculator */
%{
#include <stdio.h>
%}

/* declare tokens */
%token NUMBER
%token STRING
%token IDENTIFIER
%token PLUS
%token MINUS
%token TIMES
%token DIVIDE
%token GREATER
%token LESS
%token AND
%token OR
%token NEG
%token EQUAL
%token RELATIVE
%token SEMICOLON
%token ABRE_PAR
%token FECHA_PAR
%token ABRE_CHA
%token FECHA_CHA
%token IF
%token ELSE
%token WHILE
%token PRINT
%token READ
%token DECLARATION

%token EOL

%%



calclist: /* nothing */                       
 | calclist exp EOL { printf("= %d\n", $2); } 
  ;

exp: factor       
 | exp ADD factor { $$ = $1 + $3; }
 | exp SUB factor { $$ = $1 - $3; }
 ;


 https://www.oreilly.com/library/view/flex-bison/9780596805418/ch01.html