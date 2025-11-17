"""
String Library Functions
"""

class String:
    @staticmethod
    def strlen(s):
        """Get string length"""
        return len(s) if s else 0
    
    @staticmethod
    def strcpy(dest, src):
        """Copy string"""
        return src
    
    @staticmethod
    def strncpy(dest, src, n):
        """Copy string with length limit"""
        return src[:n]
    
    @staticmethod
    def strcmp(s1, s2):
        """Compare strings"""
        if s1 == s2:
            return 0
        return -1 if s1 < s2 else 1
    
    @staticmethod
    def strncmp(s1, s2, n):
        """Compare strings with length limit"""
        return String.strcmp(s1[:n], s2[:n])
    
    @staticmethod
    def strcat(dest, src):
        """Concatenate strings"""
        return dest + src
    
    @staticmethod
    def memset(ptr, value, num):
        """Set memory block"""
        return [value] * num
    
    @staticmethod
    def memcpy(dest, src, num):
        """Copy memory block"""
        return src[:num] if src else []
    
    @staticmethod
    def memcmp(ptr1, ptr2, num):
        """Compare memory blocks"""
        s1 = str(ptr1[:num]) if ptr1 else ""
        s2 = str(ptr2[:num]) if ptr2 else ""
        return String.strcmp(s1, s2)
    
    @staticmethod
    def strstr(haystack, needle):
        """Find substring"""
        if haystack and needle:
            index = haystack.find(needle)
            return index if index != -1 else None
        return None
    
    @staticmethod
    def strchr(s, c):
        """Find character in string"""
        if s:
            index = s.find(c)
            return index if index != -1 else None
        return None