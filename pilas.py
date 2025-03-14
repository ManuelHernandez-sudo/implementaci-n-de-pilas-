class Stack:
    """Clase personalizada de Pila sin usar estructuras predefinidas de Python."""
    
    class Node:
        """Nodo interno para la estructura de la pila."""
        def __init__(self, value, next_node=None):
            self.value = value
            self.next = next_node

    def __init__(self):
        """Inicializa una pila vacía."""
        self.top = None
        self._size = 0

    def push(self, element):
        """Agrega un elemento a la pila."""
        new_node = self.Node(element, self.top)
        self.top = new_node
        self._size += 1

    def pop(self):
        """Elimina y devuelve el elemento superior de la pila."""
        if self.is_empty():
            raise IndexError("La pila está vacía")
        value = self.top.value
        self.top = self.top.next
        self._size -= 1
        return value

    def peek(self):
        """Devuelve el elemento superior sin eliminarlo."""
        if self.is_empty():
            raise IndexError("La pila está vacía")
        return self.top.value

    def is_empty(self):
        """Retorna True si la pila está vacía."""
        return self.top is None

    def size(self):
        """Retorna el número de elementos en la pila."""
        return self._size


def validar_parentesis(expresion):
    """Verifica si una expresión matemática tiene los paréntesis balanceados."""
    stack = Stack()
    pares = {')': '(', ']': '[', '}': '{'}
    
    for caracter in expresion:
        if caracter in "({[":
            stack.push(caracter)
        elif caracter in ")}]":
            if stack.is_empty() or stack.pop() != pares[caracter]:
                return False

    return stack.is_empty()


def infija_a_postfija(expresion):
    """Convierte una expresión infija a postfija usando una pila."""
    precedencia = {'+': 1, '-': 1, '*': 2, '/': 2, '(': 0}
    stack = Stack()
    salida = []
    tokens = expresion.split()

    for token in tokens:
        if token.isnumeric():  # Si es un operando, añadir a la salida
            salida.append(token)
        elif token == '(':
            stack.push(token)
        elif token == ')':
            while not stack.is_empty() and stack.peek() != '(':
                salida.append(stack.pop())
            stack.pop()  # Eliminar el '(' de la pila
        else:  # Es un operador
            while not stack.is_empty() and precedencia[stack.peek()] >= precedencia[token]:
                salida.append(stack.pop())
            stack.push(token)

    # Vaciar cualquier operador restante en la pila
    while not stack.is_empty():
        salida.append(stack.pop())

    return ' '.join(salida)


# Ejemplo de uso
if __name__ == "__main__":
    # Validación de paréntesis
    expresion1 = "(3 + 2) * (8 / 4)"
    expresion2 = "((3 + 2) * (8 / 4"
    
    print(f"Expresión: {expresion1} -> Balanceada: {validar_parentesis(expresion1)}")  # True
    print(f"Expresión: {expresion2} -> Balanceada: {validar_parentesis(expresion2)}")  # False

    # Conversión de infija a postfija
    expresion_infija = "3 + 5 * ( 2 - 8 )"
    expresion_postfija = infija_a_postfija(expresion_infija)
    print(f"Infija: {expresion_infija} -> Postfija: {expresion_postfija}")  # "3 5 2 8 - * +"