# 1 "cilcode.tmp/ex9.cil.c"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "/usr/include/stdc-predef.h" 1 3 4
# 1 "<command-line>" 2
# 1 "cilcode.tmp/ex9.cil.c"
# 1 "cilcode.tmp/ex9.c"
struct inner {
   int z ;
};
# 1 "cilcode.tmp/ex9.c"
struct foo {
   int x ;
   int y ;
   int a[5] ;
   struct inner inner ;
};
# 1 "cilcode.tmp/ex9.c"
struct foo s = {0, 8, {0, 5, 5, 4}, {3}};
