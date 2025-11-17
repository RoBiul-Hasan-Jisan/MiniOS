#include "lib/stdio.h"
#include "lib/string.h"

static void reverse(char* str, int length) {
    int start = 0;
    int end = length - 1;
    while(start < end) {
        char temp = str[start];
        str[start] = str[end];
        str[end] = temp;
        start++;
        end--;
    }
}

int atoi(const char* str) {
    int result = 0;
    int sign = 1;
    
    // Skip whitespace
    while(*str == ' ') str++;
    
    // Handle sign
    if(*str == '-') {
        sign = -1;
        str++;
    } else if(*str == '+') {
        str++;
    }
    
    // Convert digits
    while(*str >= '0' && *str <= '9') {
        result = result * 10 + (*str - '0');
        str++;
    }
    
    return sign * result;
}

char* itoa(int value, char* str, int base) {
    int i = 0;
    int is_negative = 0;
    
    // Handle 0 explicitly
    if(value == 0) {
        str[i++] = '0';
        str[i] = '\0';
        return str;
    }
    
    // Handle negative numbers for base 10
    if(value < 0 && base == 10) {
        is_negative = 1;
        value = -value;
    }
    
    // Process individual digits
    while(value != 0) {
        int rem = value % base;
        str[i++] = (rem > 9) ? (rem - 10) + 'a' : rem + '0';
        value = value / base;
    }
    
    // Append negative sign for base 10
    if(is_negative) {
        str[i++] = '-';
    }
    
    str[i] = '\0';
    
    // Reverse the string
    reverse(str, i);
    
    return str;
}

int vsprintf(char* str, const char* format, va_list args) {
    char* ptr = str;
    
    while(*format) {
        if(*format == '%') {
            format++;
            
            switch(*format) {
                case 'd': {
                    int num = va_arg(args, int);
                    char num_str[32];
                    itoa(num, num_str, 10);
                    kstrcpy(ptr, num_str);
                    ptr += kstrlen(num_str);
                    break;
                }
                case 's': {
                    char* s = va_arg(args, char*);
                    kstrcpy(ptr, s);
                    ptr += kstrlen(s);
                    break;
                }
                case 'c': {
                    char c = (char)va_arg(args, int);
                    *ptr++ = c;
                    break;
                }
                case 'x': {
                    unsigned int num = va_arg(args, unsigned int);
                    char hex_str[32];
                    itoa(num, hex_str, 16);
                    kstrcpy(ptr, hex_str);
                    ptr += kstrlen(hex_str);
                    break;
                }
                case '%': {
                    *ptr++ = '%';
                    break;
                }
            }
        } else {
            *ptr++ = *format;
        }
        format++;
    }
    
    *ptr = '\0';
    return ptr - str;
}

int sprintf(char* str, const char* format, ...) {
    va_list args;
    va_start(args, format);
    int ret = vsprintf(str, format, args);
    va_end(args);
    return ret;
}