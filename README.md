# LinguagemProgramacao



### A e-linguaggio é uma linguagem de programação baseada no idioma italiano. 


#### EBNF

BLOCCARE = "{", COMANDO, "}" ;  
COMANDO = ( λ | INCARICO | STAMPA | BLOCCARE | WHILE | IF ), ";" ;  
INCARICO = IDENTIFIER, "=", ESPRESSIONE ;                                            
STAMPA = "stampare", "(", (ESPRESSIONE | NUMERO ), ")" ;                                
MENTRE = "mentre", "(", ESPRESSIONE, ")", COMANDO, BLOCCARE ;  
SE = "SE", "(", ESPRESSIONE, ")", (COMANDO | COMANDO, "altro", COMANDO) ;  
PER = "loperop", "(", INCARICO, ";", ESPRESSIONERELATIVA ";", (ESPRESSIONE | TERMINE)  ")" ;  
OESPRESSIONE = EESPRESSIONE, { "||" } ;  
EESPRESSIONE = UGUALEESPRESSIONE, { "&&" } ;  
UGUALEESPRESSIONE = ESPRESSIONERELATIVA, { "==" } ;  
ESPRESSIONERELATIVA = ESPRESSIONE, { (">" | "<"), ESPRESSIONE } ;  
ESPRESSIONE = TERMINE, { ("+" | "-"), TERMINE } ;  
TERMINE = FATTORE, { ("*" | "/"), FATTORE } ;  
FATTORE = (("+" | "-" | "!"), FATTORE) | NUMERO | IDENTIFICATORE | "(", ESPRESSIONE, ")" | "leggereln",  "(", ")" ;  
LEGGARELN = "leggereln", "(", ")" ;  
IDENTIFICATORE = LETTER, { LETTER | DIGIT | "_" } ;  
NUMERO = DIGIT, { DIGIT } ;  
LETTER = ( a | ... | z | A | ... | Z ) ;  
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;  


