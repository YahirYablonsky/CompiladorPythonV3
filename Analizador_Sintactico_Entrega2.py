# Para ejecutar
# [.....]\tp\venv\Scripts> python ..\..\src\Analizador_Sintactico_TP2.py
from operator import indexOf
import ply.yacc as yacc
import os
from Analizador_Lexico_Entrega2 import tokens
from Analizador_Lexico_Entrega2 import analizador
from Analizador_Lexico_Entrega2 import tablaDeSimbolos
from Clases import TablaDeSimbolos, Terceto
from Clases import Pila
from Clases import Pila
from Clases import TablaDeSimbolos

PATH_PRUEBAS = os.path.dirname(os.path.abspath(__file__)) + '\Pruebas'

#PASO 1. DEFINO LA PRECEDENCIA DE LOS OPERADORES
precedence = (
    ('right','ASSIGN'),
    ('left','NE','EQUAL'),
    ('left','LT','LTE','GT','GTE'),
    ('left','PLUS','MINUS'),
    ('left','MULT','DIVIDE','REST'),
    ('left','LBRA','RBRA'),
    ('left','COMMA')
    )

#PASO 2. DEFINO LA LISTA DE VARIABLES Y EL RESULTADO DE LA GRAMÁTICA
variables = {}
resultado_gramatica = []
reglas_aplicadas = []

#Definición de punteros
pt_expresion = 0
pt_sentencia = 0
pt_lista_sentencias = 0
pt_sentencia_asig = 0
pt_sentencia_cond = 0
pt_sentencia_while = 0 
pt_sentencia_dec = 0
pt_sentencia_write = 0
pt_sentencia_read = 0
pt_termino = 0
pt_factor = 0
pt_op_arit = 0
pt_lista_condiciones = 0
pt_condicion = 0
pt_op_logico = 0
pt_arg_condicional_izq = 0
pt_arg_condicional_der = 0
pt_cte = 0
pt_tipo_dato = 0
pt_lista_id = 0
pt_lista_declaraciones = 0
pt_declaracion = 0
pt_tupla_izq = 0
pt_tupla_der = 0
pt_tupla = 0
pt_condicion_between = 0



tercetos = []
numeroTercetos = 0
pilaCondiciones = Pila()
pilaTercetos = Pila()
pilaOperadoresLogicos = Pila()
pilaOperadoresWhile = Pila()
pilaInicioWhile = Pila()
pilaExpresiones = Pila()


def punteroNombre(puntero):
    return "["+str(puntero)+"]"

def crearTerceto (elemento1,elemento2,elemento3):
    global numeroTercetos
    numeroTercetos +=1
    nombreTerceto = "["+str(numeroTercetos)+"]"
    tercetos.append(Terceto(nombreTerceto,[elemento1,elemento2,elemento3]))
    return numeroTercetos

def modificarTerceto (numeroTerceto,nuevoAtributo3):
    tercetos[numeroTerceto-1].lista[2] = punteroNombre(nuevoAtributo3)



def get_tipo_salto(operador_logico):
    if(operador_logico== '<'):
        return "BGE"
    elif(operador_logico== '<='):
        return "BGT"
    elif(operador_logico== '>'):
        return "BLE"
    elif(operador_logico== '>='):
        return "BLT"
    elif(operador_logico== '!='):
        return "BEQ"
    elif(operador_logico== '='):
        return "BNE"         

def get_tipo_salto_directo(operador_logico):
    if(operador_logico== '<'):
        return "BGE"
    elif(operador_logico== '<='):
        return "BGT"
    elif(operador_logico== '>'):
        return "BLE"
    elif(operador_logico== '>='):
        return "BLT"
    elif(operador_logico== '!='):
        return "BEQ"
    elif(operador_logico== '=='):
        return "BNE"    

def get_element_from_tabla_simbolos(id):
    for s in tablaDeSimbolos:
        if s.get_nombre() == id :
            return indexOf(tablaDeSimbolos,s)

#PASO 3. DEFINO LA GRAMÁTICA

#START VA A SER "PROGRAM"
def p_program(p):
                    ''' program : bloque'''
                    reglas_aplicadas.append('Entro en Regla 01: P->B')




#UN BLOQUE ES UN CONJUNTO DE SENTENCIAS O UNA SENTENCIA
def p_bloque(p):
                        ''' bloque : lista_sentencias'''
                        reglas_aplicadas.append('Entro en Regla 02: B-> LS')


def p_lista_sentencias_1(p):
                        ''' lista_sentencias : lista_sentencias  sentencia ENDL'''
                        reglas_aplicadas.append("Entro en Regla 03: LS -> LS S ;")
                        


def p_lista_sentencias_2(p):
                        ''' lista_sentencias : sentencia ENDL '''
                        reglas_aplicadas.append("Entro en Regla 04: LS -> S ;")
                        global pt_lista_sentencias
                        pt_lista_sentencias = pt_sentencia

#UNA SENTENCIA ES: UNA SENT_WHILE, SENT_ASIG, SENT_COND, SENT_DECL, SENT_WRITE, SENT_READ
def p_sentencia_1(p):
                        ''' sentencia : sentencia_asig''' 
                        reglas_aplicadas.append("Entro en Regla 05: S -> SA")
                        global pt_sentencia
                        pt_sentencia = pt_sentencia_asig

def p_sentencia_2(p):
                        ''' sentencia : sentencia_cond''' 
                        reglas_aplicadas.append("Entro en Regla 06: S -> SC")
                        global pt_sentencia
                        pt_sentencia = pt_sentencia_cond

def p_sentencia_3(p):
                        ''' sentencia : sentencia_while''' 
                        reglas_aplicadas.append("Entro en Regla 07: S -> SW")

def p_sentencia_4(p):
                        ''' sentencia : sentencia_decl''' 
                        reglas_aplicadas.append("Entro en Regla 08: S -> SD")

def p_sentencia_5(p):
                        ''' sentencia : sentencia_write''' 
                        reglas_aplicadas.append("Entro en Regla 09: S -> SWRITE")

def p_sentencia_6(p):
                        ''' sentencia : sentencia_read''' 
                        reglas_aplicadas.append("Entro en Regla 10: S -> SREAD")




#GRAMATICA DE WHILE
def p_sentencia_while(p):
                            ''' sentencia_while : WHILE pre_cond_wh lista_condiciones fin_cond_wh OP_BRA lista_sentencias CL_BRA'''
                            reglas_aplicadas.append('Entro en Regla 11: SW -> WHILE LC { LS } ' )
                            global pt_sentencia_while
                            operadorWhile = pilaOperadoresWhile.desapilar()
                            crearTerceto('BI',punteroNombre(pilaInicioWhile.desapilar()),'_')
                            pt_sentencia_while = numeroTercetos
                            modificarTerceto(pilaTercetos.desapilar(),pt_sentencia_while+1)

def p_fin_cond_while(p):
                            "fin_cond_wh :"
                            operadorLogico = pilaOperadoresLogicos.desapilar()
                            pilaOperadoresWhile.apilar(operadorLogico)
                            pilaTercetos.apilar(crearTerceto('CMP',get_tipo_salto(operadorLogico),'_'))
def p_pre_cond_while(p):
                            "pre_cond_wh :"
                            pilaInicioWhile.apilar(numeroTercetos+1)


#GRAMATICA DE CONDICIÓN
def p_setencia_cond(p):
                            ''' sentencia_cond : IF lista_condiciones fin_cond OP_BRA lista_sentencias CL_BRA'''
                            reglas_aplicadas.append('''Entro en Regla 14: SC -> IF LC { LS }''' )
                            global pt_sentencia_cond
                            pt_sentencia_cond = numeroTercetos
                            modificarTerceto(pilaTercetos.desapilar(),pt_sentencia_cond+1)



def p_fin_cond(p):
                            "fin_cond :"
                            pilaTercetos.apilar(crearTerceto('CMP',get_tipo_salto(pilaOperadoresLogicos.desapilar()),'_'))
                            

def p_fin_bloque_verd(p):
                            "fin_bloque_verd :"
                            tercetoActual = (crearTerceto('ELSE','BI','_'))
                            modificarTerceto(pilaTercetos.desapilar(),tercetoActual+1)
                            pilaTercetos.apilar(tercetoActual)
    
def p_setencia_cond_else(p):
                            ''' sentencia_cond : IF lista_condiciones fin_cond OP_BRA lista_sentencias CL_BRA fin_bloque_verd  ELSE OP_BRA lista_sentencias CL_BRA '''
                            reglas_aplicadas.append('''Entro en Regla 16: SC -> IF LC { LS }  ELSE { LS }''' )
                            global pt_sentencia_cond 
                            pt_sentencia_cond = numeroTercetos
                            modificarTerceto(pilaTercetos.desapilar(),pt_sentencia_cond+1)
 

def p_lista_condiciones_and (p):
                        ''' lista_condiciones : LBRA lista_condiciones AND condicion RBRA'''
                        reglas_aplicadas.append('''Entro en Regla 18: LC -> LC and C''' )
                        global pt_lista_condiciones
                        pt_lista_condiciones = crearTerceto(p[3],punteroNombre(pt_lista_condiciones),punteroNombre(pt_condicion))

def p_lista_condiciones_or (p):
                        ''' lista_condiciones : lista_condiciones OR condicion'''
                        reglas_aplicadas.append('''Entro en Regla 19: LC -> LC or C''' )
                        global pt_lista_condiciones
                        pt_lista_condiciones = crearTerceto(p[2],punteroNombre(pt_lista_condiciones),punteroNombre(pt_condicion))

def p_lista_condiciones (p):
                        ''' lista_condiciones : condicion'''
                        reglas_aplicadas.append('''Entro en Regla 20: LC -> C''' )
                        global pt_lista_condiciones
                        pt_lista_condiciones = pt_condicion
    
def p_condiciones_par (p):
                        ''' condicion : LBRA condicion RBRA'''
                        reglas_aplicadas.append('''Entro en Regla 21: LC -> (C)''' )
                       
    
def p_condicion(p): 
                        ''' condicion : arg_condicional_izq op_logico arg_condicional_der'''
                        reglas_aplicadas.append('''Entro en Regla 22: C -> ACI OP_L ACD''' )
                        global pt_condicion
                        pt_condicion = crearTerceto(punteroNombre(pt_op_logico),punteroNombre(pt_arg_condicional_izq),punteroNombre(pt_arg_condicional_der))
                        
    
def p_argumento_condicional_izq(p): 
                        ''' arg_condicional_izq : expresion'''
                        reglas_aplicadas.append('''Entro en Regla 23: ACI -> E''' )
                        global pt_arg_condicional_izq
                        pt_arg_condicional_izq = pt_expresion    
    
def p_argumento_condicional_der(p): 
                        ''' arg_condicional_der : expresion'''
                        reglas_aplicadas.append('''Entro en Regla 24: ACD -> E''' )       
                        global pt_arg_condicional_der
                        pt_arg_condicional_der = pt_expresion
def p_op_logico(p):
                        ''' op_logico : NE 
                        | LT 
                        | LTE
                        | GT 
                        | GTE 
                        | EQUAL
                        '''
                        reglas_aplicadas.append('''Entro en Regla 25-30: OP_L -> NE | LT | LTE | GT | GTE | EQUAL''' )
                        global pt_op_logico
                        pt_op_logico = crearTerceto(p[1],'_','_')
                        pilaOperadoresLogicos.apilar(p[1])

#GRAMATICA DE ASIGNACION
def p_setencia_asig(p):
                        ''' sentencia_asig : ID ASSIGN expresion'''
                        reglas_aplicadas.append("Entro en Regla 31: SA -> ID := E")
                        global pt_sentencia_asig
                        crearTerceto(p[2],p[1],pt_expresion)
                        pt_sentencia_asig = numeroTercetos
                        #pt_tabla_simbolos = get_element_from_tabla_simbolos(p[1])
                        #tablaDeSimbolos[pt_tabla_simbolos].set_valor = p[3]




#-------------------------------EXPRESION----------------------------------------------------
def p_expresion_plus(p):
                        
                        ''' expresion : expresion PLUS termino'''
                        global pt_expresion
                        reglas_aplicadas.append("Entro en Regla 32: E -> E + T")
                        pt_expresion = crearTerceto(p[2],punteroNombre(pt_expresion),punteroNombre(pt_termino))
                       
def p_expresion_minus(p):
                        
                        ''' expresion : expresion MINUS termino'''
                        global pt_expresion
                        reglas_aplicadas.append("Entro en Regla 33: E -> E - T")
                        pt_expresion =crearTerceto(p[2],punteroNombre(pt_expresion),punteroNombre(pt_termino))
                       

def p_expresion_ter(p):
                        ''' expresion : termino'''
                        global pt_expresion
                        reglas_aplicadas.append("Entro en Regla 34: E -> T")
                        pt_expresion = pt_termino
                    

#------------------------.TERMINO-------------------------------------------------
def p_termino_mult(p):
                        
                        ''' termino : termino MULT factor'''
                        global pt_termino
                        reglas_aplicadas.append("Entro en Regla 35: T -> T * F")
                        pt_termino =crearTerceto(p[2],punteroNombre(pt_termino),punteroNombre(pt_factor))
                       

def p_termino_divide(p):
                        
                        ''' termino : termino DIVIDE factor'''
                        global pt_termino
                        reglas_aplicadas.append("Entro en Regla 36: T -> T / F")
                        pt_termino=crearTerceto(p[2],punteroNombre(pt_termino),punteroNombre(pt_factor))
                     
def p_termino_rest(p):
                        
                        ''' termino : termino REST factor'''
                        global pt_termino
                        reglas_aplicadas.append('''Entro en Regla 37: T -> T  F''')
                        pt_termino=crearTerceto(p[2],punteroNombre(pt_termino),punteroNombre(pt_factor))
                        

def p_termino_factor(p):
                        ''' termino : factor'''
                        global pt_termino
                        reglas_aplicadas.append("Entro en Regla 38: T -> F")
                        pt_termino = pt_factor
#-------------------------FACTOR-------------------------------------------------

    
def p_termino_const_int(p):
                        ''' factor : INTEGER'''
                        reglas_aplicadas.append("Entro en Regla 39: F-> INTEGER")
                        global pt_factor
                        pt_factor = crearTerceto(p[1],'_','_')

def p_termino_id(p):
                        ''' factor : ID '''
                        reglas_aplicadas.append("Entro en Regla 40: F-> ID")
                        global pt_factor
                        pt_factor =  crearTerceto(p[1],'_','_')

def p_termino_const_float(p):
                        ''' factor : FLOATD'''
                        reglas_aplicadas.append("Entro en Regla 41: F-> FLOAT")
                        global pt_factor
                        pt_factor = crearTerceto(p[1],'_','_')


def p_termino_expr(p):
                        ''' factor : LBRA expresion RBRA '''
                        reglas_aplicadas.append("Entro en Regla 42: T-> (E)")
                        global pt_factor
                        pt_factor = pt_expresion

#GRAMATICAS DE LECTURA Y ESCRITURA

def p_sentencia_write1 (p):
    ''' sentencia_write : WRITE cte '''
    reglas_aplicadas.append('''Entro en Regla 43: SWRT -> WRITE cte ''' )
    global pt_sentencia_write
    pt_sentencia_write = crearTerceto(p[1],punteroNombre(pt_cte),'_')
    
def p_sentencia_write2 (p):
    ''' sentencia_write : WRITE ID '''
    reglas_aplicadas.append('''Entro en Regla 44: SWRT -> WRITE ID ''' )
    global pt_sentencia_write
    pt_sentencia_write = crearTerceto(p[1],p[2],'_')

def p_sentencia_read (p):
    ''' sentencia_read : READ ID '''
    reglas_aplicadas.append('''Entro en Regla 45: SRD -> READ ID ''' )
    global pt_sentencia_read
    pt_sentencia_read = crearTerceto(p[1],p[2],'_')

def p_cte (p):
    ''' cte : FLOATD
    |         INTEGER
    |         STRINGD'''
    reglas_aplicadas.append('''Entro en Regla 46-48: CTE -> INTEGER | FLOATD | STRINGD''' )
    global pt_cte
    pt_cte = crearTerceto(p[1],'_','_')


#GRAMATICA DE DECLARACION
def p_sentencia_declaracion(p):
    ''' sentencia_decl : DECVAR lista_declaraciones ENDDEC'''
    reglas_aplicadas.append('''Entro en Regla 49: SD -> DECVAR LD ENDDEC ''' )
    global pt_sentencia_dec
    pt_sentencia_dec =  pt_lista_declaraciones


def p_lista_declaraciones_1(p):
    ''' lista_declaraciones : lista_declaraciones  declaracion'''
    reglas_aplicadas.append('''Entro en Regla 50: LD -> LD ; D ''' )
    global pt_lista_declaraciones
    pt_lista_declaraciones =  crearTerceto(';',punteroNombre(pt_lista_declaraciones),punteroNombre(pt_declaracion))


def p_lista_declaraciones_2(p):
    ''' lista_declaraciones : declaracion  '''
    reglas_aplicadas.append('''Entro en Regla 51: LD -> D ''' )
    global pt_lista_declaraciones
    pt_lista_declaraciones =  pt_declaracion

def p_declaracion(p):
    ''' declaracion : lista_id COLON tipo_dato ENDL'''
    reglas_aplicadas.append('''Entro en Regla 52: D -> LI COLON TIPO ENDL''' )
    global pt_declaracion
    pt_declaracion =  crearTerceto(p[2],punteroNombre(pt_lista_id),punteroNombre(pt_tipo_dato))

def p_lista_id1(p):
    ''' lista_id : lista_id COMMA ID '''
    reglas_aplicadas.append('''Entro en Regla 53: LI -> LI , ID ''' )
    global pt_lista_id
    pt_lista_id = crearTerceto(p[2],punteroNombre(pt_lista_id),p[3])

def p_lista_id2(p):
    ''' lista_id : ID '''
    reglas_aplicadas.append('''Entro en Regla 54: LI -> ID ''' )
    global pt_lista_id
    pt_lista_id = crearTerceto(p[1],'_','_')

def p_tipo_dato(p):
    ''' tipo_dato : FLOAT 
    | STRING 
    | INT 
    '''
    reglas_aplicadas.append('''Entro en Regla 55-57: tipo_dato -> FLOAT | STRING | INT''' )
    global pt_tipo_dato
    pt_tipo_dato = crearTerceto(p[1],'_','_')


#GRAMATICAS FUNCIONES TAKE Y BETWEEN
def p_condicion_between1(p):
                            ''' condicion_between : BETWEEN LBRA ID COMMA tupla RBRA '''
                            reglas_aplicadas.append('''Entro en Regla 58: CD_BTW -> BETWEEN ( tupla ) ''' )
                            global pt_condicion_between
                            crearTerceto('<',p[3],punteroNombre(pt_tupla_izq))
                            pt_condicion_between= crearTerceto('>',p[3],punteroNombre(pt_tupla_der))
                            pilaOperadoresLogicos.apilar("=")

def p_tupla(p):
                            ''' tupla :  OP_BRC tupla_izq ENDL tupla_der CL_BRC '''
                            reglas_aplicadas.append('''Entro en Regla 59: tupla -> [TI;TD] ''' )
                            global pt_tupla 
                            pt_tupla = numeroTercetos                        

def p_tupla_izq(p):
                            ''' tupla_izq :  expresion '''
                            reglas_aplicadas.append('''Entro en Regla 60: TI -> E ''' )
                            global pt_tupla_izq
                            pt_tupla_izq = pt_expresion

def p_tupla_der(p):
                            ''' tupla_der :  expresion '''
                            reglas_aplicadas.append('''Entro en Regla 61: TD -> E ''' )
                            global pt_tupla_der
                            pt_tupla_der = pt_expresion


def p_condicion_between2(p):
                            ''' condicion : condicion_between '''
                            reglas_aplicadas.append('''Entro en Regla 62: C -> C_BTW''' )
                            global pt_condicion
                            pt_condicion = pt_condicion_between 

def p_expresion_take1(p):
    ''' expresion : expresion_take '''
    reglas_aplicadas.append('''Entro en Regla 63: E -> EX_TK''' )

def p_expresion_take2(p):
    ''' expresion_take : TAKE LBRA op_arit ENDL INTEGER ENDL OP_BRC lista_take CL_BRC RBRA '''
    reglas_aplicadas.append('''Entro en Regla 64: EX_TK -> TAKE (op_arit ; INTEGER ; [LS_TK])''' )

def p_op_arit(p):
    ''' op_arit : PLUS
        |         MINUS
        |         DIVIDE
        |         MULT
        |         REST'''
    reglas_aplicadas.append('''Entro en Regla 65-69: EX_TK -> TAKE (op_arit ; INTEGER ; [LS_TK])''' )

def p_lista_take1(p):
    ''' lista_take : lista_take ENDL cte_take  '''
    reglas_aplicadas.append('''Entro en Regla 70: LS_TK -> LS_TK ; CTE_TK''' )

def p_lista_take2(p):
    ''' lista_take : cte_take  '''
    reglas_aplicadas.append('''Entro en Regla 71: LS_TK -> CTE_TK''' )

def p_cte_take2(p):
    ''' cte_take : INTEGER
    |              FLOATD  '''
    reglas_aplicadas.append('''Entro en Regla 72: CTE_TK -> INTEGER | FLOATD''' )



def p_error(t):
    global resultado_gramatica
    if t:
        resultado = "Error sintactico:\n Token: {}\n Valor: {}\n linea:{}".format(  str(t.type),str(t.value), str(t.lexer.lineno))
        print(resultado)
    else:
        resultado = "Error sintactico {}".format(t)
        print('Inesperado cierre de sentencia')
    resultado_gramatica.append(resultado)



# instanciamos el analizador sistactico
parser = yacc.yacc()

def prueba_sintactica(data):
    global resultado_gramatica
    resultado_gramatica.clear()
    if data:
        gram = parser.parse(data)
        if gram:
            resultado_gramatica.append(str(gram))
    else: print("data vacia")

    return resultado_gramatica

if __name__ == '__main__':
    
    inputFile = open(PATH_PRUEBAS + '\PruebaTercetos.in','r')
    outputFile = open(PATH_PRUEBAS + '\Prueba.out','w')
    outputFileTS = open(PATH_PRUEBAS + '\TablaSimbolos.out','w')
    
    file = ''
    while True:
        linea = inputFile.read() 
        if not linea:
            break   
        file = file + linea
        prueba_sintactica(file)
        for regla in reglas_aplicadas:
            print (regla)
            outputFile.write(regla + "\n")

    outputFile.close()       
    inputFile.close()

    for tb in tablaDeSimbolos:
       outputFileTS.write(str(tb.get_tabla_simbolos()) + "\n")
    
    outputFileTS.close()
    for terceto in tercetos:
        print(terceto.id, terceto.lista)


