# LinguagemProgramacao


### A e-linguaggio é uma linguagem de programação baseada no idioma italiano. 


#### EBNF

BLOCCARE = "{", COMANDO, "}" ;  
COMANDO = ( ( INCARICO | STAMPA | DICHIARAZIONE) , ";" ) | ( λ | BLOCCARE | MENTRE |  | SE | IF ) ;   
DICHIARAZIONE = ( "int" |  "bool" | "stringa" ),  IDENTIFIER ";"   
INCARICO = IDENTIFIER, "=", ESPRESSIONE ;                                            
STAMPA = "stampare", "(", (ESPRESSIONE | NUMERO | STRINGA), ")" ;         
LEGGERE = "leggere", "(", ")" ;                        
MENTRE = "mentre", "(", ESPRESSIONE, ")", COMANDO, BLOCCARE ;  
SE = "se", "(", ESPRESSIONE, ")", (COMANDO | COMANDO, "altro", COMANDO) ;  
GIRI = "gire", "(", INCARICO, ";", ESPRESSIONERELATIVA ";", (ESPRESSIONE | TERMINE)  ")" ;  
OESPRESSIONE = EESPRESSIONE, { "||" } ;  
EESPRESSIONE = ESPRESSIONEUGUALE, { "&&" } ;  
ESPRESSIONEUGUALE = ESPRESSIONERELATIVA, { "==" } ;  
ESPRESSIONERELATIVA = ESPRESSIONE, { (">" | "<"), ESPRESSIONE } ;  
ESPRESSIONE = TERMINE, { ("+" | "-"), TERMINE } ;  
TERMINE = FATTORE, { ("*" | "/"), FATTORE } ;  
FATTORE = (("+" | "-" | "!"), FATTORE) | NUMERO | IDENTIFICATORE | "(", ESPRESSIONE, ")" | "leggereln",  "(", ")" ;  
LEGGARELN = "leggereln", "(", ")" ;  
IDENTIFICATORE = LETTERA, { LETTERA | DIGIT | "_" } ;  
NUMERO = DIGIT, { DIGIT } ;  
STRINGA = """, "LETTERA", { LETTERA | DIGIT | "_" }, """;   
BOOLEANA = "vero" | "falso" ;  
LETTERA = ( a | ... | z | A | ... | Z ) ;  
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;  




## Para utilizar bastar rodar:

```
$ python3 main.py test1.c 
```
Sendo 'test.c', um arquivo .c que contém a expressão que deseja compilar.

###### Ex:
```
$ python3 main.py test1.c
```

###### Ex arquivo test1.c:
```
{
    bool a;
    int b;
    int c;
    stringa x;
    
    b = 32;
    c = 32;
    a = falso;
    x = "oie";

    se ((b && c) == a) {
    	stampare(1);
    }altro{
    	stampare(2);
    }

    stampare(x);
}
```

