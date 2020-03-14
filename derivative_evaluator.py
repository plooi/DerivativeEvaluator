from random import random

def main():
    while 1:
        e = input("Enter an expression involving x (you must put * between all multiplications):")
        e = parse(e)
        d = derive(e)
        #print("derived: %s" %d)
        d = simplify(d)
        print("The derivative of that expression is: %s" % str(d))
    """
    e = Expression(Expression(Expression(3, "*", "x"), "+", 1), "+", Expression("x", "*", "x"))
    d = derive(e)
    simplify(d)
    print(d)
    """
    #print(parse("60/5*(7-5)"))
    
    

class Expression:
    def __init__(self, p1, operation, p2):    
        
        self.operation = operation
        self.p1 = p1
        self.p2 = p2
    def __str__(self):
    
        if is_num(self.p1) or self.p1 == "x" or (isinstance(self.p1, Expression) and self.p1.operation in ["sin","cos","tan"]):
            p1 = str(self.p1)
        else:
            p1 = "(" + str(self.p1) + ")"
        if is_num(self.p2) or self.p2 == "x" or (isinstance(self.p2, Expression) and self.p2.operation in ["sin","cos","tan"]):
            p2 = str(self.p2)
        else:
            p2 = "(" + str(self.p2) + ")"
    
        if self.operation == "+":
            if self.p1 == 0:
                return str(self.p2)
            if self.p2 == 0:
                return str(self.p1)
        if self.operation == "-":
            if self.p1 == 0:
                return "-" + p2#"-("+str(self.p2) +")"
            if self.p2 == 0:
                return str(self.p1)
        if self.operation == "*":
            if self.p1 == 1:
                return str(self.p2)
            if self.p2 == 1:
                return str(self.p1)
        if self.operation == "/":
            if self.p2 == 1:
                return str(self.p1)
        if self.operation in ["sin","cos","tan"]:
            return self.operation + "(" + str(self.p2) + ")"
        if self.operation == "+":
            return str(self.p1) + " " + self.operation + " " + str(self.p2)
        if self.operation == "-":
            return str(self.p1) + " " + self.operation + " "+  p2
        
        
        
        
        
        return p1 + self.operation + p2
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
        if operation == "sin":
            return Expression(Expression(0, "cos", expression.p2), "*", derive(expression.p2))
        if operation == "cos":
            return Expression(Expression(0,"-",Expression(0, "sin", expression.p2)), "*", derive(expression.p2))
        if operation == "tan":
            cosSQx = Expression(Expression(0, "cos", expression.p2), "*", Expression(0, "cos", expression.p2))
            return Expression(Expression(1,"/",cosSQx), "*", derive(expression.p2))
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
"""
Start simplify section
"""
def simplify(expression):
    for i in range(10):
        expression = _simplify(expression)
    return expression
    

        
        
def _simplify(expression):
    if expression == None:
        return None
    if is_num(expression):
        return expression
    if expression == "x":
        return expression
    if type(expression) == type(Expression(None,None,None)):
        operation = expression.operation
        if operation == "+":
            p = random()
            expression.p1= simplify(expression.p1)
            expression.p2 = simplify(expression.p2)
            
            
            if is_num(expression.p1) and is_num(expression.p2):
                return expression.p1 + expression.p2
            if expression.p1 == 0:
                return simplify(expression.p2)
            if expression.p2 == 0:
                return simplify(expression.p1)
                
            #ALL OF THEM should be like this. TODO: Make each like this one
            nums = get_nums(expression)
            if is_num(expression.p1):
                expression.p1 = sum(nums)
            elif is_num(expression.p2):
                expression.p2 = sum(nums)
            else:
                expression.p1 = Expression(expression.p1, "+", sum(nums))
            
            if is_x_node(expression.p1) or is_x_node(expression.p2):
                
                if is_x_node(expression.p1):
                    x_coeffs = get_x(expression)
                    expression.p1 = Expression(sum(x_coeffs), "*", "x")
                else:
                    x_coeffs = get_x(expression)
                    expression.p2 = Expression(sum(x_coeffs), "*", "x")
            return Expression(expression.p1, operation, expression.p2)
        if operation == "-":
            expression.p1= simplify(expression.p1)
            expression.p2 = simplify(expression.p2)
            
            if is_num(expression.p1) and is_num(expression.p2):
                return expression.p1 - expression.p2
            if expression.p2 == 0:
                return simplify(expression.p1)
            
            if is_num(expression.p1) or is_num(expression.p2):
                nums = get_nums(expression)
                if is_num(expression.p1):
                    expression.p1 = sum(nums)
                else:
                    expression.p2 = -sum(nums)
            if is_x_node(expression.p1) or is_x_node(expression.p2):
                x_coeffs = get_x(expression)
                if is_x_node(expression.p1):
                    expression.p1 = Expression(sum(x_coeffs), "*", "x")
                else:
                    expression.p2 = Expression(sum(x_coeffs), "*", "x")
            
            return Expression(expression.p1, operation, expression.p2)
        if operation == "*":
            expression.p1= simplify(expression.p1)
            expression.p2 = simplify(expression.p2)
            
            if is_num(expression.p1) and is_num(expression.p2):
                return expression.p1 * expression.p2
            if expression.p1 == 0:
                return 0
            if expression.p2 == 0:
                return 0
            if expression.p1 == 1:
                return simplify(expression.p2)
            if expression.p2 == 1:
                return simplify(expression.p1)
            return Expression(expression.p1, operation, expression.p2)
        if operation == "/":
            expression.p1= simplify(expression.p1)
            expression.p2 = simplify(expression.p2)
            
            if is_num(expression.p1) and is_num(expression.p2):
                return expression.p1 / expression.p2
            if expression.p1 == 0:
                return 0
            if expression.p2 == 1:
                return simplify(expression.p1)
            return Expression(expression.p1, operation, expression.p2)
    return copy(expression)
        

def get_nums(node):
    if not isinstance(node, Expression):
        return []
    ret = []
    if node.operation == "+":
        if is_num(node.p1):
            ret.append(node.p1)
            node.p1 = 0
        else:
            ret += get_nums(node.p1)
        if is_num(node.p2):
            ret.append(node.p2)
            node.p2 = 0
        else:
            ret += get_nums(node.p2)
    if node.operation == "-":
        if is_num(node.p1):
            ret.append(node.p1)
            node.p1 = 0
        else:
            ret += get_nums(node.p1)
        if is_num(node.p2):
            ret.append(-node.p2)
            node.p2 = 0
        else:
            ret += [-x for x in get_nums(node.p2)]
    return ret
    
def is_x_node(node):
    if node == "x":
        return True
    if isinstance(node, Expression):
        if node.operation == "*":
            if (is_num(node.p1) and is_x_node(node.p2)) or (is_x_node(node.p1) and is_num(node.p2)):
                return True
        if node.operation == "/":
            if (is_num(node.p1) and is_x_node(node.p2)) or (is_x_node(node.p1) and is_num(node.p2)):
                return True
    return False
def get_x(node):
    
    
    
    
    if node == "x":
        return [1]
    
    if not isinstance(node, Expression):
        return []
    
    
    ret = []
    if node.operation == "+":
        ret += get_x(node.p1) + get_x(node.p2)
        if node.p1 == "x": node.p1 = 0
        if node.p2 == "x": node.p2 = 0
    if node.operation == "-":
        ret += get_x(node.p1) + [-x for x in get_x(node.p2)]
        if node.p1 == "x": node.p1 = 0
        if node.p2 == "x": node.p2 = 0
    if node.operation == "*":
        if is_num(node.p1) and node.p2=="x":
            ret.append(node.p1)
            node.p1 = 0
        if is_num(node.p2) and node.p1=="x":
            ret.append(node.p2)
            node.p2 = 0
    return ret
    
"""
End simplify section
"""














"""
Start parsing section
"""

operations = ["+", "-", "*", "/"]
values = [str(x) for x in range(10)]+["x"]

def find_close(open_paren, string):
    if string[open_paren] != "(":
        raise Exception("bad")
    i = open_paren
    paren_level = 0
    while i < len(string):
        if string[i] == "(": paren_level += 1
        if string[i] == ")": paren_level -= 1
        
        if paren_level == 0: return i
        i += 1
    fail("No close paren for %d, %s" % (open_paren, string))

def find_term_end(string, start):
    i = start
    while i < len(string):
        if string[i] not in ["+","-"]:
            break
        i += 1
    
    while i < len(string):
        if string[i] == "(": 
            i = find_close(i, string)+1
            continue
        if string[i] in ["+", "-", ")"]:
            break
        i += 1
    return i
def find_mult_term_end(string, start):
    i = start
    while i < len(string):
        if string[i] not in ["+","-"]:
            break
        i += 1
    
    while i < len(string):
        if string[i] == "(": 
            i = find_close(i, string)+1
            continue
        if string[i] in ["+", "-", "*", "/", ")"]:
            break
        i += 1
    return i

def parse(string, default = 0):
    string = string.replace("sin", "s")
    string = string.replace("cos", "c")
    string = string.replace("tan", "t")
    string = string.replace("X", "x")
    #checks for corner cases:
    
    while 1:
        orig_string = string
        string = string.strip().replace(" ", "")
        if string == "":
            return default
        if string.startswith("-(") and string.endswith(")") and find_close(1, string) == len(string)-1:
            return Expression(0,"-",parse(string[2:-1]))
        if string.startswith("(") and string.endswith(")")  and find_close(0, string) == len(string)-1:
            string = string[1:-1]
        if string.startswith("*"):
            string = string[1:]
            
        if orig_string == string: break
        
        
        
        
        
    if string == "x":
        return "x"
    try:
        return int(string)
    except:
        try:
            return float(string)
        except:
            pass
    
    
    
    
    
    
    
    #start the real parsing
    i = 0
    while i < len(string):
        if string[i] == "(": 
            i = find_close(i, string)+1
            continue
        
        
        
        if string[i] == "+": 
            return Expression(parse(string[0:i]), "+", parse(string[i+1:]))
        if string[i] == "-": 
            j = find_term_end(string, i+1)
            if j == len(string):
                return Expression(parse(string[0:i]), "-", parse(string[i+1:j]))
            else:
                return Expression(Expression(parse(string[0:i]), "-", parse(string[i+1:j])) , "+", parse(string [j:]))
            
            
        i += 1
    
    i = 0
    while i < len(string):
        if string[i] == "(": 
            i = find_close(i, string)+1
            continue
        
        if string[i] == "*": 
            j = find_mult_term_end(string, i+1)
            if j == len(string):
                return Expression(parse(string[0:i]), "*", parse(string[i+1:j])) 
            else:
                return Expression(Expression(parse(string[0:i]), "*", parse(string[i+1:j])) , "*", parse(string [j:]))
        if string[i] == "/": 
            j = find_mult_term_end(string, i+1)
            if j == len(string):
                return Expression(parse(string[0:i],default=1), "/", parse(string[i+1:j])) 
            else:
                return Expression(Expression(parse(string[0:i]), "/", parse(string[i+1:j])) , "*", parse(string [j:]))
        i += 1
    
    i = 0
    while i < len(string):
        if string[i] == "(": 
            i = find_close(i, string)+1
            continue
        
        if string[i] == "s": 
            j = find_close(i+1, string)
            return Expression(0, "sin", parse(string[i+2:j])) 
        if string[i] == "c": 
            j = find_close(i+1, string)
            return Expression(0, "cos", parse(string[i+2:j])) 
        if string[i] == "t": 
            j = find_close(i+1, string)
            return Expression(0, "tan", parse(string[i+2:j])) 
        i += 1
    
    
    if string == "x":
        return "x"
    try:
        try:
            return int(string)
        except:
            return float(string)
    except:
        pass
        #print("Failed on parsing '%s'" %(string))
                
    
        
"""
End parsing section
"""
        
        
        
"""
Start util section
"""
        
        
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
"""
End util section
"""

if __name__ == "__main__": main()
