# 1 "cilcode.tmp/ex47.cil.c"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "/usr/include/stdc-predef.h" 1 3 4
# 1 "<command-line>" 2
# 1 "cilcode.tmp/ex47.cil.c"
# 1 "cilcode.tmp/ex47.c"
static int bar(int x , char y )
{


  {
# 2 "cilcode.tmp/ex47.c"
  return (x + (int )y);
}
}
# 6 "cilcode.tmp/ex47.c"
int foo(int x , char y )
{
  int tmp ;

  {
# 6 "cilcode.tmp/ex47.c"
  tmp = bar(x, y);
# 6 "cilcode.tmp/ex47.c"
  return (tmp);
}
}
