import sys 
import string
import ast
from abc import ABC, abstractmethod
import time
import os
st_func_dict = {}
class SymbolTable():
    #cria um dicionario
    def __init__(self): 
        self.st_dict = dict()


    def getter(self, variable, symbolTable):
        # print(f"getter: {variable}  DICT: {symbolTable.st_dict}    st:{symbolTable}")

        # print("VAR: {}".format(variable)) 
        if variable in symbolTable.st_dict:
            #retornar o valor
            return symbolTable.st_dict[variable]
            # return self.st_dict[variable][1] ###TESTAR SE EH ISSO 
        else:
            raise ValueError("Variavel nao atribuída")


    def getterFunc(self, funcName):
        # print(f"getterFunc: {funcName}  DICT: {st_func_dict}")
        if funcName in st_func_dict:
            return st_func_dict[funcName]
        else:
            raise ValueError("Funcao nao atribuída")

    def setterAll(self, variable, value, tipo, symbolTable):
        # print(f"SetterAll variavel: {variable} valor: {value} tipo: {tipo} table: {symbolTable}  | {symbolTable.st_dict}")

        # if variable in self.st_dict:
        #     raise ValueError("Variavel já declarada")
        symbolTable.st_dict[variable] = (value, tipo, None)    
        # print("Entrei aqui: ", symbolTable.st_dict)


    def setter(self, variable, value):
        # print("_setter_ VAR: {} VALUE: {}  TYPE: {}".format(variable,value[0],value[1]))
        # print("DICIONARIO: ",self.st_dict)
        if variable in self.st_dict:
            tupla = self.st_dict[variable]
            lst = list(tupla)
            type = lst[1]
            meio = lst[2]
        
            # #Checar se os valores batem com o tipo da variavel 
            if isinstance(value[0], int) and type == "int" or isinstance(value[0], str) and type == "string":
                self.st_dict[variable] = (value[0], type, meio)

            elif (isinstance(value[0], int) and type == "bool"):
                if value[0] == 0:
                    self.st_dict[variable] = (value[0], type, meio)
                else:
                    self.st_dict[variable] = (1, type, meio)
            else:
                raise ValueError("Tipos nao batem")

        else:
            raise ValueError("Variavel não definida")

    def setterType(self, variable, type, meio = None):
        # print(f"VAR: {variable} TYPE: {type} MEIO: {meio}")
        if variable in self.st_dict:
            #CHECAR SE EH CHAMADA DE FUNCAO
            raise ValueError("Variavel já declarada")
        self.st_dict[variable] = (None, type, meio)
    
    def setterFuncType(self, variable, type, meio = None, argumentos = None):
        # print("________________________ 1setterFuncType")
        # print(f"***Fazendo setter de: {variable} TYPE: {type} MEIO: {meio} dict: {st_func_dict}")
        # print(f"VAR: {variable} TYPE: {type} MEIO: {meio}")
        if variable in st_func_dict:
            raise ValueError("Funcao já declarada")
        st_func_dict[variable] = (None, type, meio, argumentos)

        # print("st_dict_d: ", st_func_dict)
        # print("________________________ 2setterFuncType")

# ----------------------------------------------------------------
teste_dict = {}
st = SymbolTable()
st_func = SymbolTable()  #st de funcoes
# ----------------------------------------------------------------
class Node(ABC):
    def __init___(self, value):
        super().init(value) 
    
    @abstractmethod
    def Evaluate(self, symbolTable):  
        pass
# ----------------------------------------------------------------
class ReturnOp():
    def __init__(self, children):
        self.children = children 

    def Evaluate(self, symbolTable):
        return self.children.Evaluate(symbolTable)


# ----------------------------------------------------------------
# Final
class FinalOp():
    def __init__(self):
        self.children = [] 

    def Evaluate(self, symbolTable):
        for i in self.children :
            fim = i.Evaluate(symbolTable)
            if (type(i) == ReturnOp or fim != None) and type(i) != FuncCall:
                return fim
            # i.Evaluate(symbolTable)
# ----------------------------------------------------------------
# Declaracao de funcao
class FuncDec():
    def __init__(self, name, tipo):
        self.children = [None] * 2  #VarDec(detalhe de parametros)
                                    # e Statements (comandos em si da funcao)
        self.name = name
        self.tipo = tipo 
    def Evaluate(self, symbolTable):
        #apenas cria uma variável na SymbolTable atual, sendo o 
        # nome da variável o nome da função, o valor apontando 
        # para o próprio nó FuncDec e o tipo será FUNCTION.

        # Cria uma ST de funcoes (nome: variavel, valor: referencia do NO)
        # print("FuncDec -> funcName: ", self.name)
        # print("FuncDec -> symbolTable: ", symbolTable)
        # print("FuncDec -> st_func    : ", st_func)
        # print("FuncDec -> self    : ", self)
        # print("FuncDec -> self.children    : ", self.children)
        for child in  self.children[0]:
            variavel = child[0]
            typo = child[1]

        #adiciona o nome na ST global  (nome, self)
        symbolTable.setterFuncType(self.name, self.tipo, self.children[1], self.children[0])
        # symbolTable.setterFuncType(self.name, self.tipo, self.children)
        

# ----------------------------------------------------------------
# FuncCall
class FuncCall():
    #executa a funcao
    #recupera o No de declaracao que foi passado no FuncDec para a ST
    #chama os statements e declaracoes dele
    #passando argumentos corretos e chamando execucao dos seus filhos

    # m filhos (n= qauantidade de argumentos passados)
    # m + 1 se guardar o nome da funcao como filho
    def __init__(self, funcName, filhos = []):
        self.children = filhos 
        self.funcName = funcName

    def Evaluate(self, symbolTable):
        func = symbolTable.getterFunc(self.funcName)
        func_type = func[1]
        
        st_func_private = SymbolTable()
        # print(f"func: {self.funcName} infos: {func}") 

        if (len(self.children) != len(func[3])):
            raise ValueError(f"Função esperava {len(func[3])} argumentos mas recebeu {len(self.children)}")

        for i in range(len(self.children)):
            valor = self.children[i].Evaluate(symbolTable)
            valor_tipo = valor[1]
            valor = valor[0]
            variavel = func[3]
            tipo = variavel[i][1]
            variavel = variavel[i][0]
            # print(f"Argumento tipo {tipo} recebendo {valor_tipo}")
            if (valor_tipo != tipo):
                raise ValueError (f"Argumento tipo {tipo} recebendo {valor_tipo}")
    
            st_func_private.setterAll(variavel, valor, tipo, st_func_private ) 

        final = func[2].Evaluate(st_func_private)
        # print(f"final: {final} e func_type: {func_type}")

        #checar se o tipo do return bate 
        if (final != None):
            if (func_type != final[1] ):
                raise ValueError (f"Funcao do tipo {func_type} retornando {final[1]}")
        return final 

 # ----------------------------------------------------------------
#faz o getter na symbol table 
class IdentfOp(Node):
    def __init__(self, value):
        self.value = value

    def Evaluate(self, symbolTable):
        # print(f"IdentfOp valor: {self.value} st: {symbolTable}") ###
        return symbolTable.getter(self.value, symbolTable)

# ----------------------------------------------------------------
# Le somente inteiros
class Println(Node):
    def __init__(self):
        self.children = [None] * 2

    def Evaluate(self, symbolTable):
        left = self.children[0].Evaluate(symbolTable)
        print(left[0])
# ----------------------------------------------------------------
class Readln(Node):
    def __init__(self):
        self.children = [None] * 2

# eval chama o input convertendo para inteiro
    def Evaluate(self, symbolTable):
        value = input()
        if value.isnumeric():
            return (int(value), "int")
        else:
            raise ValueError("Nao é int") 

# ----------------------------------------------------------------
# Binary Operation
class BinOp(Node):
    def __init__(self, value=None):            
        self.value = value
        self.children = [None] * 2

    def Evaluate(self, symbolTable):
        if self.value == "TYPE":
            # print("DECLARATION {}   {} ".format(self.children[0], self.children[1]))
            return symbolTable.setterType(self.children[0], self.children[1])

        right = self.children[1].Evaluate(symbolTable)
        

        # if (right == None):
        #     print(f" right_none: {right}")
        #     return self.children[0].Evaluate(symbolTable)

        if self.value == "ASSIGMENT":
            # if isinstance(right, int): 
            # print("É ASSIGMENT: {}, {} ".format(self.children[0],right))
            return symbolTable.setter(self.children[0],  right)


        left = self.children[0].Evaluate(symbolTable)
        # print(f" right: {right}   left: {left}")
        # print(f"children: {self.children }")
        right_tipo = right[1]
        right = right[0]
        left_tipo = left[1]
        left = left[0]
        left2 = self.children[0].Evaluate(symbolTable)[1]
        # print("EVALUATE>>>>> ", right)
        # print("EVALUATE>>>>> ", left)
        # print("TIPOOO ",right_tipo, left_tipo)

        
        if self.value == "PLUS":
            return (left + right, "int")
        elif self.value == "MINUS":
            return (left - right, "int")
        elif self.value == "TIMES":
            return (left * right, "int")
        elif self.value == "DIVIDE":
            return (int(left / right), "int")   

        #Operadores relacionais 
        elif self.value == "GREATER":
            return (int(left > right), "bool")
        elif self.value == "LESS":
            return (int(left < right), "bool")
        elif self.value == "RELATIVE":
            return (int(left == right), "bool")

        #Operadores booleanos 
        elif self.value == "AND":
            if (left and right) >= 1:
                return (1, "bool")
            else:
                return (0, "bool")
        elif self.value == "OR":
            if (left or right) >= 1:
                return (1, "bool")
            else:
                return (0, "bool")

# ----------------------------------------------------------------    
# Unary Operation
class UnOp(Node):
    def __init__(self, value):            
        self.value = value
        self.children = [None] * 2

    def Evaluate(self, symbolTable):
    
        left = self.children[0].Evaluate(symbolTable)[0]
        
        if isinstance(left, int):
            tipo = "int";
        elif isinstance(left, str):
            tipo = "string";
        elif isinstance(left, bool):
            tipo = "bool";

     
        if self.value == "PLUS":
            return (left, tipo) 
        if self.value == "MINUS":
            return (-left, tipo)
        if self.value == "NEG": 
            return (not left, tipo)

# ----------------------------------------------------------------    
class WhileOp(Node):
    def __init__(self, value=None):            
        self.value = value
        self.children = [None] * 2

    def Evaluate(self, symbolTable):
        left = self.children[0].Evaluate(symbolTable)[0]      #Condicao
        # right = self.children[1].Evaluate()

        # print("A condicao do while é: ",left)
        while (left):
            if (self.children[0].Evaluate(symbolTable)[0]):
                self.children[1].Evaluate(symbolTable) 
            else:
                return

#consulta o no a esquerda, que é o no de condicao
#retorna 0 ou 1
#se 0, termina
#se 1, chama o command (da eval no command que retorna que terminou) 
#e roda o comando do while

# ----------------------------------------------------------------    
class IfOp(Node):
    def __init__(self, value=None):            
        self.value = value
        self.children = [None] * 3

    def Evaluate(self, symbolTable):
        # print("0 =>", self.children[0])

        left = self.children[0].Evaluate(symbolTable)     # Condition
        # middle = self.children[1].Evaluate()    # Command
        # right = self.children[2].Evaluate()     #else - pode nao existir

        #consulta 0, se for verdade da eval no filho 1
        # print("CONDICAO do if: ", left)
        if (left[1] == "string"):
            raise ValueError ("Não existe if de string")

        left = left[0]
        if (left):
            # print("fim do if")
            return self.children[1].Evaluate(symbolTable)  
        elif (self.children[2] != None) :
            # print("TEM ELSE")
            return self.children[2].Evaluate(symbolTable)  
# ----------------------------------------------------------------
# Integer value 
class IntVal(Node):
    def __init__(self, value=None):        
        self.value = value

    def Evaluate(self, symbolTable):
        # retorna o próprio valor inteiro
        return (self.value, "int")
# ----------------------------------------------------------------
# String value 
class StrVal(Node):
    def __init__(self, value=None):        
        self.value = value

    def Evaluate(self,symbolTable ):
        return (self.value, "string")
# ----------------------------------------------------------------       
# Boolean value 
class BoolVal(Node):
    def __init__(self, value=None):        
        self.value = value

    def Evaluate(self, symbolTable):
        # print("BoolVal: {}", self.value)
        if (self.value == "true"):
            return (1, "bool") 
        if (self.value == "false"):
            return (0, "bool")
# ----------------------------------------------------------------  
# No Operation (Dummy)
class NoOp(Node):
    def Evaluate(self, symbolTable):
        pass
# ----------------------------------------------------------------
class Token:
    def __init__(self, tipo: str, value: int): 
        self.tipo = tipo
        self.value = value
# ----------------------------------------------------------------
class Tokenizer:

    def __init__(self, origin: str): # , position: int, actual : Token
        self.origin = origin     #codigo fonte que sera tokenizado
        self.position = 0       #posicao atual que o Tokenizador esta separando
        self.actual = Token(tipo = "", value=None)   #None  #ultimo token separado
        self.qtdPar = 0            # quantidade de parenteses
        self.qtdCha = 0            # quantidade de chaves
         
    def selectNext(self):
        number = ""
        expression = ""
        if self.position == (len(self.origin)):
                token = Token("EOF", "")
                self.actual = token
                if (self.qtdPar != 0 or self.qtdCha != 0):
                    raise ValueError("Chaves ou parenteses desbalanceados")
                return
        atual = self.origin[self.position]



        if atual.isnumeric():
            while self.position < (len(self.origin)) and (self.origin[self.position]).isnumeric():
                number += self.origin[self.position]
                self.position +=1
            token = Token("NUMBER", int(number))
            self.actual = token


        elif atual.isalpha():
            while self.position < (len(self.origin)) and  ( self.origin[self.position].isalpha() or self.origin[self.position].isnumeric() or self.origin[self.position]=="_" ):
                expression += self.origin[self.position]
                self.position +=1
            if expression == "stampare":
                token = Token("PRINT", "println")
                self.actual = token
            elif expression == "leggere":
                token = Token("READ", "readln")
                self.actual = token
            elif expression == "mentre":
                token = Token("WHILE", "while")
                self.actual = token
            elif expression == "se":
                token = Token("IF", "if")
                self.actual = token
            elif expression == "altro":
                token = Token("ELSE", "else")
                self.actual = token
            elif expression == "ritorno":
                token = Token("RETURN", "return")
                self.actual = token
    
            elif expression == "vero" :
                token = Token("BOOL", "true")
                self.actual = token

            elif expression == "falso":
                token = Token("BOOL", "false")
                self.actual = token


            elif expression == "int" or expression == "bool" or expression == "string":
                token = Token("TYPE", expression)
                self.actual = token


            else:
                token = Token("IDENTIFIER", expression)
                self.actual = token
        
        elif atual ==  '"'  :
            # expression += self.origin[self.position]  # SE PRECISAR DAS ASPAS
            self.position +=1
            while self.position < (len(self.origin)) and  self.origin[self.position] !='"' :
                expression += self.origin[self.position]
                
                self.position +=1
            # expression += self.origin[self.position] # SE PRECISAR DAS ASPAS
            self.position +=1
            token = Token("STRING", expression)
            self.actual = token



        elif atual == "=":
            self.position +=1
            if self.origin[self.position] == "=":
                token = Token("RELATIVE", atual) # ==
                self.actual = token
                self.position += 1
            else:
                token = Token("EQUAL", atual)
                self.actual = token
                # self.position += 1
        
        elif atual == ";":
            token = Token("SEMICOLON", atual) 
            self.actual = token
            self.position += 1

        elif atual == ",":
            token = Token("COLON", atual) 
            self.actual = token
            self.position += 1

        elif atual == "+":
            token = Token("PLUS", atual)
            self.actual = token
            self.position += 1
        elif atual == "-":
            token = Token("MINUS", atual)
            self.actual = token
            self.position += 1
        elif atual == "/":
            token = Token("DIVIDE", atual)
            self.actual = token
            self.position += 1
        elif atual == "*":
            token = Token("TIMES", atual)
            self.actual = token
            self.position += 1

        elif atual == ">":
            token = Token("GREATER", atual)
            self.actual = token
            self.position += 1
        elif atual == "<":
            token = Token("LESS", atual)
            self.actual = token
            self.position += 1
        elif atual == "&":
            self.position +=1
            if self.origin[self.position] == "&":
                token = Token("AND", atual)
                self.actual = token
                self.position += 1
            else:
                raise KeyError
        elif atual == "|":
            self.position +=1
            if self.origin[self.position] == "|":
                token = Token("OR", atual)
                self.actual = token
                self.position += 1
            else:
                raise KeyError
        elif atual == "!":
            token = Token("NEG", atual)
            self.actual = token
            self.position += 1


        elif atual == "(":
            token = Token("ABRE_PAR", atual)
            self.actual = token
            self.position += 1
            self.qtdPar +=1
        elif atual == ")":
            token = Token("FECHA_PAR", atual)
            self.actual = token
            self.position += 1
            self.qtdPar -=1
            if self.position == (len(self.origin)):
                if (self.qtdPar != 0):
                    raise KeyError                
        elif atual == " ":
            self.position += 1
            self.selectNext()
    
        elif atual == "\n":
            self.position += 1
            self.selectNext()

        elif atual == "\t":
            self.position += 1
            self.selectNext()

        elif atual == "{":
            token = Token("ABRE_CHA", atual)
            self.actual = token
            self.position += 1
            self.qtdCha +=1
        elif atual == "}":
            token = Token("FECHA_CHA", atual)
            self.actual = token
            self.position += 1
            self.qtdCha -=1
            if self.position == (len(self.origin)):
                if (self.qtdCha != 0):
                    raise KeyError     
        else: 
            print("TIPO: {}, VALOR: {}".format(self.actual.tipo, self.actual.value))

            raise KeyError

        return    

# ----------------------------------------------------------------
class PrePro():
    
    def __init__(self, originPP: str): 
        self.originPP = originPP                     #codigo fonte que sera tokenizado
        self.positionPP = 0                          #posicao atual que o Tokenizador esta separando
        self.actual = Token(tipo = "", value=None)   #None  #ultimo token separado

    def filter(self):        
        atual = self.originPP[self.positionPP]
        tamanho = self.originPP 
        filtered = "" #nova string filtrada

        #Ideia de como remover comentarios em um unico loop retirada do GeeksforGeeks
        #https://www.geeksforgeeks.org/remove-comments-given-cc-program/
        isComment = False
        isClosed = False


        while self.positionPP < (len(self.originPP)):    

            #se estiver em comenentario, checar o fim dele
            if (isComment and self.originPP[self.positionPP] == '*' and self.originPP[self.positionPP +1] == '/'):
                isComment = False
                isClosed = True
                self.positionPP +=1
            
            #checar o inicio de comentario
            elif (self.originPP[self.positionPP] == '/' and self.originPP[self.positionPP +1] == '*'):
                isComment = True

                self.positionPP +=1
            elif (not isComment):
                filtered += self.originPP[self.positionPP]

            self.positionPP +=1


        #Caso tenha aberto um comentario mas nao fechado
        if (isComment and not isClosed):
            raise ValueError ("Cometário não fechado")
        return filtered
       
# ----------------------------------------------------------------
class Parser():
    def __init__(self):
        pass
# ----------------------------------------------------------------
    def FuncDefBlock(self):

        # print("TIPO_defblock1: {}, VALOR: {}".format(self.tokens.actual.tipo, self.tokens.actual.value))
        final_block = FinalOp()
        while (self.tokens.actual.tipo == "TYPE" ):
            tipoFunc = self.tokens.actual.value
            self.tokens.selectNext()  

            if (self.tokens.actual.tipo == "IDENTIFIER" ):
                funcName = self.tokens.actual.value
                ## aqui eu chamo a FuncDec
                #VarDec e Statements
                funcao = FuncDec(funcName, tipoFunc)
                argumentos = FinalOp()
                argumentos_teste = []
                self.tokens.selectNext()
                if (self.tokens.actual.tipo == "ABRE_PAR" ):
                    self.tokens.selectNext()
                    while (self.tokens.actual.tipo != "FECHA_PAR" ):
                        if (self.tokens.actual.tipo == "TYPE" ):
                            tipo = self.tokens.actual.value
                            self.tokens.selectNext()  
                            if (self.tokens.actual.tipo == "IDENTIFIER" ):
                                variavel = self.tokens.actual.value
                                arvore = BinOp("TYPE")
                                arvore.children[0] = variavel;
                                arvore.children[1] = tipo;
                                argumentos.children.append(arvore) 
                                argumentos_teste.append((variavel, tipo))
                                self.tokens.selectNext()
                                if (self.tokens.actual.tipo == "COLON" ):
                                    self.tokens.selectNext()
                                    if (self.tokens.actual.tipo != "TYPE" ):
                                        raise ValueError ("Virgula sem novo parametro")
                        else:
                            raise ValueError ("Parametro sem tipo")
                    # print("Argumentos: ", argumentos)
                    # funcao.children[0] = argumentos
                    funcao.children[0] = argumentos_teste
                    if (self.tokens.actual.tipo == "FECHA_PAR" ): #talvez nao precise de if
                        # print("TIPO_defblock1: {}, VALOR: {}".format(self.tokens.actual.tipo, self.tokens.actual.value))

                        self.tokens.selectNext()
                        arvore = self.Command() 
                        funcao.children[1] = arvore   
                    # print(funcao)
                    
                    #call main
                    #adiciona outro children call function main
                    final_block.children.append(funcao)
        final_block.children.append(FuncCall("main"))
        self.tokens.selectNext() 
        if (self.tokens.actual.tipo != "EOF"):
            raise ValueError
        return final_block
        
# ----------------------------------------------------------------
    # chama command 
    def Block(self):
        # print("TIPO_blcok1: {}, VALOR: {}".format(self.tokens.actual.tipo, self.tokens.actual.value))


        final = FinalOp()

        if (self.tokens.actual.tipo == "ABRE_CHA" ):
            self.tokens.selectNext()  

            while(self.tokens.actual.tipo != "FECHA_CHA" ):
                filho = self.Command()
                if (filho != None):
                    final.children.append(filho)
            if (self.tokens.actual.tipo == "FECHA_CHA"):
                self.tokens.selectNext() 
            return final
        else:
            print("ERRO_block: {}, VALOR: {}".format(self.tokens.actual.tipo, self.tokens.actual.value))
            raise ValueError("Erro na block")
        
        

# ----------------------------------------------------------------
    def Command(self):

        variavel = ""
        
        # print("TIPO_i1: {}, VALOR: {}".format(self.tokens.actual.tipo, self.tokens.actual.value))
        if self.tokens.actual.tipo == "SEMICOLON":
            self.tokens.selectNext()
            return NoOp()

        elif self.tokens.actual.tipo == "IDENTIFIER":
            variavel = self.tokens.actual.value
            self.tokens.selectNext()
            if self.tokens.actual.tipo == "EQUAL":
                self.tokens.selectNext()
                arvore = self.orExpression()
                arvore_copy = BinOp("ASSIGMENT")
                arvore_copy.children[0] = variavel
                arvore_copy.children[1] = arvore
                if self.tokens.actual.tipo == "SEMICOLON":
                    NoOp()
                    self.tokens.selectNext()
                    return arvore_copy
                else:
                    raise ValueError("Nao tem ;")
    

            elif self.tokens.actual.tipo == "ABRE_PAR":
                self.tokens.selectNext()
                filhos = []
                while (self.tokens.actual.tipo != "FECHA_PAR"):
                    filho = self.orExpression()
                    filhos.append(filho)
                    if (self.tokens.actual.tipo == "COLON" ):
                        self.tokens.selectNext()
                if self.tokens.actual.tipo == "FECHA_PAR":
                    self.tokens.selectNext()
                arvore = FuncCall(variavel, filhos)
                return arvore

        elif self.tokens.actual.tipo == "TYPE":
            tipo = self.tokens.actual.value;
            self.tokens.selectNext()
            #pega o proximo e checar se é ident
            if self.tokens.actual.tipo == "IDENTIFIER":
                variavel = self.tokens.actual.value
                arvore = BinOp("TYPE")
                arvore.children[0] = variavel;
                arvore.children[1] = tipo;
                self.tokens.selectNext()
                if self.tokens.actual.tipo == "SEMICOLON":
                    self.tokens.selectNext()
                    return arvore
                else:
                    raise ValueError
            else:
                raise ValueError ("Não é identificador")


        elif self.tokens.actual.tipo == "PRINT":
            self.tokens.selectNext()
            if self.tokens.actual.tipo == "ABRE_PAR":
                self.tokens.selectNext()
                arvore = self.orExpression()
                test = Println()
                test.children[0] = arvore
                if (self.tokens.actual.tipo == "FECHA_PAR"):
                    self.tokens.selectNext()
                else:
                    raise ValueError("Não fechou parenteses")
                if (self.tokens.actual.tipo == "SEMICOLON"):
                    self.tokens.selectNext()
                    return test
                else:
                    raise ValueError("Print sem ; no final")
            
        elif self.tokens.actual.tipo == "RETURN":
            self.tokens.selectNext()
            arvore = self.orExpression()
            if self.tokens.actual.tipo == "SEMICOLON":
                self.tokens.selectNext()
                ret = ReturnOp(arvore)
                return ret
            else:
                raise ValueError("Nao tem ;")

        elif self.tokens.actual.tipo == "WHILE":
            self.tokens.selectNext()
            if self.tokens.actual.tipo == "ABRE_PAR":
                self.tokens.selectNext()
                arvore = (self.orExpression())
                if (self.tokens.actual.tipo == "FECHA_PAR"):
                    self.tokens.selectNext()
                    test = WhileOp()
                    test.children[0] = arvore
                    test.children[1] = self.Command()
                    return test

        elif self.tokens.actual.tipo == "IF":
            self.tokens.selectNext()
            if self.tokens.actual.tipo == "ABRE_PAR":
                self.tokens.selectNext()
                condicao = (self.orExpression())
                if (self.tokens.actual.tipo == "FECHA_PAR"):
                    self.tokens.selectNext() 
                    to_do = self.Command()

                    test = IfOp()
                    test.children[0] = condicao
                    test.children[1] = to_do
      
                    if (self.tokens.actual.tipo == "ELSE"):
                        self.tokens.selectNext() 
                        se_nao = self.Command()
                        test.children[2] = se_nao
                    return test
                else:
                    ValueError("Não fechou parenteses do if")

        else:
            arvore = (self.Block())
            return arvore
        
#______________________________________________________________    
    def orExpression(self):
        # print("TIPO__: {}, VALOR: {}".format(self.tokens.actual.tipo, self.tokens.actual.value))

        arvore = self.andExpression()
        while(self.tokens.actual.tipo == "OR"):
            self.tokens.selectNext()               
            arvore_copy = BinOp("OR")
            arvore_copy.children[0] = arvore
            arvore_copy.children[1] = self.andExpression()
            arvore = arvore_copy
        return arvore

#______________________________________________________________ 
    def andExpression(self):
        arvore = self.eqExpression()
        while(self.tokens.actual.tipo == "AND"):
            self.tokens.selectNext()               
            arvore_copy = BinOp("AND")
            arvore_copy.children[0] = arvore
            arvore_copy.children[1] = self.eqExpression()
            arvore = arvore_copy
        return arvore


#______________________________________________________________ 
    def eqExpression(self):
        arvore = self.relExpression()
        while(self.tokens.actual.tipo == "RELATIVE"):
            self.tokens.selectNext()               
            arvore_copy = BinOp("RELATIVE")
            arvore_copy.children[0] = arvore
            arvore_copy.children[1] = self.relExpression()
            arvore = arvore_copy
        return arvore


#______________________________________________________________   
    def relExpression(self):
        arvore = self.parseExpression()
        tipo = "" 
        while(self.tokens.actual.tipo == "GREATER" or self.tokens.actual.tipo == "LESS"  ):
            
            tipo = self.tokens.actual.tipo
            if tipo == "GREATER":
                self.tokens.selectNext()               
                arvore_copy = BinOp("GREATER")
                arvore_copy.children[0] = arvore
                arvore_copy.children[1] = self.parseExpression()
                arvore = arvore_copy

            elif tipo == "LESS":
                self.tokens.selectNext()
                arvore_copy = BinOp("LESS")
                arvore_copy.children[0] = arvore
                arvore_copy.children[1] = self.parseExpression()
                arvore = arvore_copy
            else:
                raise KeyError
        return arvore
    

#______________________________________________________________    
    def parseExpression(self):
        arvore = self.term()
        tipo = ""
        while(self.tokens.actual.tipo == "PLUS" or self.tokens.actual.tipo == "MINUS"  ):
            tipo = self.tokens.actual.tipo
            if tipo == "PLUS":
                self.tokens.selectNext()               
                arvore_copy = BinOp("PLUS")
                arvore_copy.children[0] = arvore
                arvore_copy.children[1] = self.term()
                arvore = arvore_copy

            elif tipo == "MINUS":
                self.tokens.selectNext()
                arvore_copy = BinOp("MINUS")
                arvore_copy.children[0] = arvore
                arvore_copy.children[1] = self.term()
                arvore = arvore_copy
            else:
                raise KeyError
        return arvore
#______________________________________________________________

    def term(self):
        arvore = self.factor()          

        #int com int da erro
        if (self.tokens.actual.tipo == "NUMBER"):
            raise KeyError
        if (self.tokens.actual.tipo == "IDENTIFIER"):
            raise KeyError

        while(self.tokens.actual.tipo == "TIMES" or self.tokens.actual.tipo == "DIVIDE"):
            tipo = self.tokens.actual.tipo
            if tipo == "TIMES":
                self.tokens.selectNext()
                arvore_copy = BinOp("TIMES")
                arvore_copy.children[0] = arvore
                arvore_copy.children[1] = self.factor()
                arvore = arvore_copy

            elif tipo == "DIVIDE":
                self.tokens.selectNext()
                arvore_copy = BinOp("DIVIDE")
                arvore_copy.children[0] = arvore
                arvore_copy.children[1] = self.factor()
                arvore = arvore_copy
            else:
                raise KeyError
        return arvore

#______________________________________________________________
    def factor(self):
        
        # print("TIPO_F1: {}, VALOR: {}".format(self.tokens.actual.tipo, self.tokens.actual.value))

        if (self.tokens.actual.tipo == "NUMBER" ):
            arvore = IntVal(self.tokens.actual.value)
            self.tokens.selectNext()

        elif (self.tokens.actual.tipo == "STRING" ):
            arvore = StrVal(self.tokens.actual.value)
            self.tokens.selectNext()

        elif (self.tokens.actual.tipo == "BOOL" ):
            arvore = BoolVal(self.tokens.actual.value)
            self.tokens.selectNext()
        
        elif (self.tokens.actual.tipo == "PLUS" ): 
            arvore = UnOp(value="PLUS")
            self.tokens.selectNext()
            arvore.children[0] = self.factor()

        elif (self.tokens.actual.tipo == "MINUS" ):
            arvore = UnOp(value="MINUS")
            self.tokens.selectNext()
            arvore.children[0] = self.factor()

        elif (self.tokens.actual.tipo == "NEG" ):
            arvore = UnOp(value="NEG")  
            self.tokens.selectNext()
            arvore.children[0] = self.factor() 
            
        elif (self.tokens.actual.tipo == "ABRE_PAR" ):          
            self.tokens.selectNext()
            arvore = self.orExpression()  
            if (self.tokens.actual.tipo != "FECHA_PAR" ):
                raise KeyError
            else:
                self.tokens.selectNext()
  
        elif self.tokens.actual.tipo == "READ":
            self.tokens.selectNext()
            if self.tokens.actual.tipo == "ABRE_PAR":
                self.tokens.selectNext()
                if self.tokens.actual.tipo == "FECHA_PAR":
                    arvore = Readln()
                    self.tokens.selectNext()

        elif (self.tokens.actual.tipo == "IDENTIFIER" ):
            arvore = IdentfOp(self.tokens.actual.value) #talvez isso seja um problema
            functionName = self.tokens.actual.value
            self.tokens.selectNext()
            if self.tokens.actual.tipo == "ABRE_PAR":
                self.tokens.selectNext()
                filhos = []
                while (self.tokens.actual.tipo != "FECHA_PAR" ):
                    filho = self.orExpression()
                    filhos.append(filho)
                    if (self.tokens.actual.tipo == "COLON" ):
                        self.tokens.selectNext()
                if self.tokens.actual.tipo == "FECHA_PAR":
                    self.tokens.selectNext()
                arvore = FuncCall(functionName, filhos)


        else:
            raise KeyError
 
        return arvore
#______________________________________________________________


    def run(self, code: str):
        preProce = PrePro(code)

        code = preProce.filter()
        self.tokens = Tokenizer(code)
        self.tokens.selectNext()
        resultado = self.FuncDefBlock()
        # self.tokens.selectNext() 
        # if (self.tokens.actual.tipo != "EOF"):
        #     raise ValueError("Nao chegou no EOF")

        # print("___________EVALUATE______________ ")

        resultado.Evaluate(st_func)

        # FuncCall("main").Evaluate(st_func)



if __name__ == '__main__':
    f = open(sys.argv[1], "r")

    #caso o arquivo esteja vazio nao faz nada:
    if (os.stat(sys.argv[1]).st_size == 0):
        pass
    else: 
        expression = []
        expression.append(f.read())
        compilador = Parser()
        compilador.run(expression[0])
