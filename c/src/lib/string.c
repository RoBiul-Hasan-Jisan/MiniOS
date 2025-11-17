#include "lib/string.h"

size_t kstrlen(const char* str) {
    size_t len = 0;
    while(str[len]) len++;
    return len;
}

char* kstrcpy(char* dest, const char* src) {
    char* ptr = dest;
    while((*ptr++ = *src++));
    return dest;
}

char* kstrncpy(char* dest, const char* src, size_t n) {
    char* ptr = dest;
    while(n-- && (*ptr++ = *src++));
    return dest;
}

int kstrcmp(const char* str1, const char* str2) {
    while(*str1 && (*str1 == *str2)) {
        str1++;
        str2++;
    }
    return *(unsigned char*)str1 - *(unsigned char*)str2;
}

int kstrncmp(const char* str1, const char* str2, size_t n) {
    while(n-- && *str1 && (*str1 == *str2)) {
        str1++;
        str2++;
    }
    if(n == (size_t)-1) return 0;
    return *(unsigned char*)str1 - *(unsigned char*)str2;
}

char* kstrcat(char* dest, const char* src) {
    char* ptr = dest + kstrlen(dest);
    while((*ptr++ = *src++));
    return dest;
}

char* kstrchr(const char* str, int c) {
    while(*str) {
        if(*str == c) return (char*)str;
        str++;
    }
    return NULL;
}

char* kstrtok(char* str, const char* delim) {
    static char* saved_ptr = NULL;
    
    if(str) saved_ptr = str;
    if(!saved_ptr) return NULL;
    
    // Skip leading delimiters
    char* start = saved_ptr;
    while(*start && kstrchr(delim, *start)) start++;
    
    if(*start == '\0') {
        saved_ptr = NULL;
        return NULL;
    }
    
    // Find end of token
    char* end = start;
    while(*end && !kstrchr(delim, *end)) end++;
    
    if(*end == '\0') {
        saved_ptr = NULL;
    } else {
        *end = '\0';
        saved_ptr = end + 1;
    }
    
    return start;
}