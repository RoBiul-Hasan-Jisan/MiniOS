#ifndef STRING_H
#define STRING_H

#include "types.h"

// Function declarations
size_t kstrlen(const char* str);
char* kstrcpy(char* dest, const char* src);
char* kstrncpy(char* dest, const char* src, size_t n);
int kstrcmp(const char* str1, const char* str2);
int kstrncmp(const char* str1, const char* str2, size_t n);
char* kstrcat(char* dest, const char* src);
char* kstrchr(const char* str, int c);
char* kstrtok(char* str, const char* delim);

#endif