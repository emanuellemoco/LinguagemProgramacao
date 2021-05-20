import sys 
import string
import ast
from abc import ABC, abstractmethod
import time
import os
import re
symbol_table_dict = {}
class SymbolTable():
    def __init__(self): 
        pass

    def getter(self, variable):
        if variable in symbol_table_dict:
            return symbol_table_dict[variable]
        else:
            raise ValueError("Variabile non assegnata")

    def setter(self, variable, value):
        if variable in symbol_table_dict:
            tupla = symbol_table_dict[variable]
            lst = list(tupla)
            type = lst[1]

            # #Checar se os valores batem com o tipo da variavel 
            if isinstance(value[0], int) and type == "int" or isinstance(value[0], str) and type == "string":
                symbol_table_dict[variable] = (value[0], type)

            elif (isinstance(value[0], int) and type == "bool"):
                if value[0] == 0:
                    symbol_table_dict[variable] = (value[0], type)
                    
                else:
                    symbol_table_dict[variable] = (1, type)

            else:
                raise ValueError("Variabile non definita")

        else:
            raise ValueError(" ")

    def setterType(self, variable, type):
        # print("VAR: {} TYPE: {}".format(variable,type))
        if variable in symbol_table_dict:
            raise ValueError("Variabile già dichiarata")
        symbol_table_dict[variable] = (None, type)



# ----------------------------------------------------------------
st = SymbolTable()
# ----------------------------------------------------------------
class Node(ABC):
    def __init___(self, value):
        super().init(value) 
    
    @abstractmethod
    def Evaluate(self):  
        pass

# ----------------------------------------------------------------
# Final
class FinalOp():
    def __init__(self):
        self.children = [] 

    def Evaluate(self):
        # print (len(self.children))
        for i in self.children :
            i.Evaluate()

 # ----------------------------------------------------------------
#faz o getter na symbol table 
class IdentfOp(Node):
    def __init__(self, value):
        self.value = value

    def Evaluate(self):
        return st.getter(self.value)

# ----------------------------------------------------------------
# Le somente inteiros
class Println(Node):
    def __init__(self):
        self.children = [None] * 2

    def Evaluate(self):
        # print("TA ENTRANDO NO EVALUATE DO PRINT")
        left = self.children[0].Evaluate()
        print(left[0])
# ----------------------------------------------------------------
class Readln(Node):
    def __init__(self):
        self.children = [None] * 2

# eval chama o input convertendo para inteiro
    def Evaluate(self):
        # print("ENTROU AQUI")
        value = input()
        if value.isnumeric():
            return (int(value), "int")
        else:
            raise ValueError("Non è int") 

# ----------------------------------------------------------------
# Binary Operation
class BinOp(Node):
    def __init__(self, value=None):            
        self.value = value
        self.children = [None] * 2

    def Evaluate(self):
        if self.value == "DECLARATION": 
            return st.setterType(self.children[0], self.children[1])

        right = self.children[1].Evaluate()

        if self.value == "ASSIGMENT":
            return st.setter(self.children[0],  right)

        right = right[0]
        left = self.children[0].Evaluate()[0]
        left2 = self.children[0].Evaluate()[1]
        # print("EVALUATE>>>>> ", left)
        
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

    def Evaluate(self):
    
        left = self.children[0].Evaluate()[0]
        
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

    def Evaluate(self):
        left = self.children[0].Evaluate()[0]      #Condicao
        # right = self.children[1].Evaluate()

        # print("A condicao do while é: ",left)
        while (left):
            if (self.children[0].Evaluate()[0]):
                self.children[1].Evaluate() 
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

    def Evaluate(self):
        # print("0 =>", self.children[0])

        left = self.children[0].Evaluate()     # Condition
        # middle = self.children[1].Evaluate()    # Command
        # right = self.children[2].Evaluate()     #else - pode nao existir

        #consulta 0, se for verdade da eval no filho 1
        # print("CONDICAO do if: ", left)
        if (left[1] == "string"):
            raise ValueError ("Não existe if de string")

        left = left[0]
        if (left):
            # print("fim do if")
            return self.children[1].Evaluate()  
        elif (self.children[2] != None) :
            # print("TEM ELSE")
            return self.children[2].Evaluate()  



#consulta o no a esquerda, que é o no de condicao
# recebe uma resposta, se for verdade
# da eval no filho do meio [1]

# se o filho 2 existir, chama o seu eval, 
# caso nao, retorna.


# ----------------------------------------------------------------
# Integer value 
class IntVal(Node):
    def __init__(self, value=None):        
        self.value = value

    def Evaluate(self):
        # retorna o próprio valor inteiro
        return (self.value, "int")
# ----------------------------------------------------------------
# String value 
class StrVal(Node):
    def __init__(self, value=None):        
        self.value = value

    def Evaluate(self):
        return (self.value, "string")
# ----------------------------------------------------------------       
# Boolean value 
class BoolVal(Node):
    def __init__(self, value=None):        
        self.value = value

    def Evaluate(self):
        # print("BoolVal: {}", self.value)
        if (self.value == "true"):
            return (1, "bool") 
        if (self.value == "false"):
            return (0, "bool")
# ----------------------------------------------------------------  
# No Operation (Dummy)
class NoOp(Node):
    def Evaluate(self):
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
    
            elif expression == "vero" :
                token = Token("BOOL", "true")
                self.actual = token

            elif expression == "falso":
                token = Token("BOOL", "false")
                self.actual = token

            elif expression == "int" or expression == "bool":
                token = Token("DECLARATION", expression)
                self.actual = token

            elif  expression == "stringa":
                token = Token("DECLARATION", "string")
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
    # chama command 
    def Block(self):
        final = FinalOp()

        if (self.tokens.actual.tipo == "ABRE_CHA" ):
            self.tokens.selectNext()  
            while(self.tokens.actual.tipo != "FECHA_CHA" and self.tokens.actual.tipo != "EOF"):
                filho = self.Command()
                if (filho != None):
                    final.children.append(filho)
            if (self.tokens.actual.tipo == "FECHA_CHA"):
                self.tokens.selectNext() 
    
            return final
        else:
            print("TIPO_block: {}, VALOR: {}".format(self.tokens.actual.tipo, self.tokens.actual.value))
            raise ValueError("Erro na block")
        
        

# ----------------------------------------------------------------
    def Command(self):
        variavel = ""
        
  
        if self.tokens.actual.tipo == "SEMICOLON":
            self.tokens.selectNext()
            return NoOp()

        elif self.tokens.actual.tipo == "IDENTIFIER":
            # print("TIPO_i1: {}, VALOR: {}".format(self.tokens.actual.tipo, self.tokens.actual.value))

            variavel = (self.tokens.actual.value)
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


        elif self.tokens.actual.tipo == "DECLARATION":
            tipo = self.tokens.actual.value;
            self.tokens.selectNext()
            #pega o proximo e checar se é ident

            if self.tokens.actual.tipo == "IDENTIFIER":
                variavel = self.tokens.actual.value
                arvore = BinOp("DECLARATION")
                arvore.children[0] = variavel;
                arvore.children[1] = tipo;
                self.tokens.selectNext()
                if self.tokens.actual.tipo == "SEMICOLON":
                    self.tokens.selectNext()
                    return arvore
                else:
                    raise ValueError("Nao tem ;")
            else:
                raise ValueError ("Não é identificador")




        elif self.tokens.actual.tipo == "PRINT":
            self.tokens.selectNext()
            if self.tokens.actual.tipo == "ABRE_PAR":
                self.tokens.selectNext()
                arvore = (self.orExpression())
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

        #number:
        if (self.tokens.actual.tipo == "NUMBER" ):
            arvore = IntVal(self.tokens.actual.value)
            self.tokens.selectNext()

        elif (self.tokens.actual.tipo == "IDENTIFIER" ):
            arvore = IdentfOp(self.tokens.actual.value)
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
            tipo = self.tokens.actual.tipo
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
        else:
            raise KeyError
 
        return arvore
#______________________________________________________________


    def run(self, code: str):
        preProce = PrePro(code)

        code = preProce.filter()
        self.tokens = Tokenizer(code)
        self.tokens.selectNext()
        resultado = self.Block()

        self.tokens.selectNext() 
        if (self.tokens.actual.tipo != "EOF"):
            raise ValueError("Nao chegou no EOF")

        # print("___________EVALUATE______________ ")

        resultado.Evaluate()


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
