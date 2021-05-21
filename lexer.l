/* recognize tokens for the calculator and print them out */
%%



"+"             { return PLUS }
"-"             { return MINUS }
"*"             { return TIMES }
"/"             { return DIVIDE }
">"             { return GREATER }
"<"             { return LESS }
"&&"            { return AND }
"||"            { return OR }
"!"             { return NEG }
"="             { return EQUAL }
"=="            { return RELATIVE }
";"             { return SEMICOLON }
"("             { return ABRE_PAR }
")"             { return FECHA_PAR }
"{"             { return ABRE_CHA }
"}"             { return FECHA_CHA }
"se"            { return IF }
"altro"         { return ELSE }
"mentre"        { return WHILE }
"stampare"      { return PRINT }
"leggere"       { return READ }
"int"           { return DECLARATION }
"bool"          { return DECLARATION }
"stringa"       { return DECLARATION }



[0-9]+                      { return NUMBER %s\n", yytext); }
["][a-zA-Z]*[0-9]+["]       { return STRING %s\n", yytext); }
[a-zA-Z]*[0-9]+[a-zA-Z]+    { return IDENTIFIER %s\n", yytext); }
[ \t]           { }
[ \n]           { }

.               { printf("Mystery character %s\n", yytext); }
%%