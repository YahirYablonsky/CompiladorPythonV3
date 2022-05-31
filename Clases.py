class Terceto:
    
    def __init__(self,id,lista):
        self.id = id
        self.lista = lista

    def get_condicion(self):
        if(self.lista[0]=='<'):
            return self.lista[1] < self.lista[2]
        elif(self.lista[0]=='='):
            return self.lista[1] == self.lista[2]
        elif(self.lista[0]=='!='):
            return self.lista[1] != self.lista[2]
        elif(self.lista[0]=='<='):
            return self.lista[1] <= self.lista[2]           
        elif(self.lista[0]=='>='):
            return self.lista[1] >= self.lista[2]
        elif(self.lista[0]=='>'):
            return self.lista[1] > self.lista[2]

class Pila:

    def __init__(self):
        """ Crea una pila vacía. """
        # La pila vacía se representa con una lista vacía
        self.items=[]

    def apilar(self, x):
    # Apilar es agregar al final de la lista.
        self.items.append(x)    

    def desapilar(self):
        try:
            return self.items.pop()
        except IndexError:
            raise ValueError("La pila está vacía")

class TablaDeSimbolos:
    def __init__(self,nombre,tipo,valor,alias,limite,longitud):
        self.nombre = nombre
        self.tipo = tipo
        self.valor = valor
        self.alias = alias
        self.limite = limite
        self.longitud = longitud
    
    def get_nombre(self):
        return self.nombre

    def set_tipo(self,tipo):
        self.tipo = tipo

    def set_valor(self,valor):
        self.tipo = valor

    def set_limite(self,limite):
        self.tipo = limite

    def set_longitud(self,longitud):
        self.tipo = longitud

    def get_tabla_simbolos(self):
        return  str("{:<10}|{:<7}|{:<15}|{:<15}|{:<10}|{:<10}".format(self.nombre,self.tipo,self.valor,self.alias,self.limite,self.longitud))






