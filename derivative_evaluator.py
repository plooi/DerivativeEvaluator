class Expression:
    def __init__(self, p1, operation, p2):    
        
        self.operation = operation
        self.p1 = p1
        self.p2 = p2
    def __str__(self):
        return "(" + str(self.p1) + ") " + self.operation + " (" + str(self.p2) + ") "
    def copy(self):
        p1 = self.p1.copy() if is_exp(self.p1) else self.p1
        p2 = self.p2.copy() if is_exp(self.p2) else self.p2
        return Expression(p1, self.operation, p2)
def copy(exp):
    if is_exp(exp):
        return exp.copy()
    return exp
def is_exp(thing):
    return type(thing) == type(Expression(None,None,None))

def derive(expression):
    if is_num(expression):
        return 0
    elif type(expression) == type(""):
        if expression == "x":
            return 1
        fail("invalid variable name " + str(expression) + ". Can only be 'x'")
    elif type(expression) == type(Expression(None,None,None)):
        operation = expression.operation
        if operation in ["+", "-"]:
            return Expression(derive(expression.p1), operation, derive(expression.p2))
        if operation == "*":
            return Expression( 
                                Expression(expression.p1, "*", derive(expression.p2)),
                                "+",
                                Expression(derive(expression.p1), "*", expression.p2)
                                )
        if operation == "/":
            return Expression(
                            Expression( 
                                Expression(expression.p2, "*", derive(expression.p1)),
                                "-",
                                Expression(derive(expression.p2), "*", expression.p1)
                                ),
                            "/",
                            Expression(expression.p2, "*", expression.p2)
                                
                                
                                
                                )
def simplify(expression):
    if is_num(expression):
        return expression
    if expression == "x":
        return expression
    if type(expression) == type(Expression(None,None,None)):
        operation = expression.operation
        if operation == "+":
            if is_num(expression.p1) and is_num(expression.p2):
                return expression.p1 + expression.p2
            if expression.p1 == 0:
                return copy(expression.p2)
            if expression.p2 == 0:
                return copy(expression.p1)
            return copy(expression)
             
    return copy(expression)
        
def main():
    e = Expression(Expression(3, "*", "x"), "+", 1)
    d = derive(e)
    d = simplify(d)
    print(d)
        
        
        
        
        
        
        
        
        
        
def is_num(object): 
    return type(object) == type(1) or type(object) == type(1.0)
class CheckException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

def check(bool, msg="Check failed"):
    if type(msg) != type(""):
        raise CheckException("parameter 'msg' to function 'check' should have been a string")
    if bool:
        pass #good
    else:
        raise CheckException(msg)
def fail(msg):
    raise Exception(msg)


if __name__ == "__main__": main()
