"""
Standard I/O Library
"""

import sys

class Stdio:
    def __init__(self):
        self.stdout = sys.stdout
        self.stdin = sys.stdin
        self.stderr = sys.stderr
        
    @staticmethod
    def printf(format_str, *args):
        """Formatted print function"""
        try:
            output = format_str % args
            print(output, end='')
            sys.stdout.flush()
            return len(output)
        except Exception as e:
            print(f"printf error: {e}")
            return 0
    
    @staticmethod
    def sprintf(buffer, format_str, *args):
        """Formatted string function"""
        try:
            return format_str % args
        except:
            return ""
    
    @staticmethod
    def puts(s):
        """Put string with newline"""
        print(s)
        return 1
    
    @staticmethod
    def putchar(c):
        """Put character"""
        print(c, end='')
        sys.stdout.flush()
        return 1
    
    @staticmethod
    def getchar():
        """Get character"""
        try:
            return sys.stdin.read(1)
        except:
            return '\0'
    
    @staticmethod
    def gets(buffer, size):
        """Get string"""
        try:
            data = input()[:size-1]
            return data
        except:
            return ""
    
    @staticmethod
    def perror(s):
        """Print error message"""
        if s:
            print(f"{s}: Operation failed", file=sys.stderr)
        else:
            print("Operation failed", file=sys.stderr)