# 1 "cilcode.tmp/ex34.c"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "/usr/include/stdc-predef.h" 1 3 4
# 1 "<command-line>" 2
# 1 "cilcode.tmp/ex34.c"
struct {
   int x;
   struct {
       int y, z;
   } nested;
} i = { .nested.y = 5, 6, .x = 1, 2 };
