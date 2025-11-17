"""
Calculator Application
"""

from src.lib.stdio import Stdio
import math

class Calculator:
    def __init__(self):
        self.variables = {}
        self.functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'sqrt': math.sqrt,
            'log': math.log,
            'exp': math.exp,
            'abs': abs
        }
        
    def run(self):
        """Run calculator interactive mode"""
        Stdio.printf("MiniOS Calculator v1.0\n")
        Stdio.printf("Type 'quit' to exit, 'help' for help\n")
        
        while True:
            try:
                expression = input("calc> ").strip()
                
                if expression.lower() == 'quit':
                    break
                elif expression.lower() == 'help':
                    self.show_help()
                elif expression.lower() == 'vars':
                    self.show_variables()
                elif expression.lower() == 'clear':
                    self.variables.clear()
                    Stdio.printf("Variables cleared\n")
                elif expression.startswith('let '):
                    self.handle_assignment(expression[4:])
                else:
                    result = self.evaluate(expression)
                    if result is not None:
                        Stdio.printf("= %s\n", result)
                        
            except (EOFError, KeyboardInterrupt):
                break
            except Exception as e:
                Stdio.printf("Error: %s\n", str(e))
                
    def show_help(self):
        """Show calculator help"""
        Stdio.printf("Calculator commands:\n")
        Stdio.printf("  <expression>  - Evaluate mathematical expression\n")
        Stdio.printf("  let x = 5     - Assign value to variable\n")
        Stdio.printf("  vars          - Show all variables\n")
        Stdio.printf("  clear         - Clear all variables\n")
        Stdio.printf("  help          - Show this help\n")
        Stdio.printf("  quit          - Exit calculator\n")
        Stdio.printf("\nSupported operations: + - * / ** ( )\n")
        Stdio.printf("Functions: sin, cos, tan, sqrt, log, exp, abs\n")
        
    def show_variables(self):
        """Show all variables"""
        if not self.variables:
            Stdio.printf("No variables defined\n")
        else:
            for name, value in self.variables.items():
                Stdio.printf("%s = %s\n", name, value)
                
    def handle_assignment(self, expression):
        """Handle variable assignment"""
        try:
            if '=' in expression:
                var_name, expr = expression.split('=', 1)
                var_name = var_name.strip()
                result = self.evaluate(expr.strip())
                if result is not None:
                    self.variables[var_name] = result
                    Stdio.printf("%s = %s\n", var_name, result)
            else:
                Stdio.printf("Invalid assignment syntax\n")
        except Exception as e:
            Stdio.printf("Assignment error: %s\n", str(e))
            
    def evaluate(self, expression):
        """Evaluate mathematical expression"""
        if not expression:
            return None
            
        try:
            # Replace variables with their values
            for var_name, value in self.variables.items():
                expression = expression.replace(var_name, str(value))
                
            # Replace function calls
            for func_name, func in self.functions.items():
                expression = expression.replace(func_name, f"math.{func_name}")
                
            # Evaluate safely
            result = eval(expression, {"math": math, "__builtins__": {}})
            return result
            
        except Exception as e:
            raise ValueError(f"Invalid expression: {expression} - {str(e)}")
            
    def calculate(self, expression):
        """Calculate expression and return result"""
        return self.evaluate(expression)