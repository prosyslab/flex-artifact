# 1 "cilcode.tmp/ex33.c"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "/usr/include/stdc-predef.h" 1 3 4
# 1 "<command-line>" 2
# 1 "cilcode.tmp/ex33.c"
int (*pf)(void);
int f(void) {

   pf = &f;
   pf = ***f;
   pf();
   (****pf)();
   (***************f)();
}
