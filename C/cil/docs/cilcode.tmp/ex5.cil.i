# 1 "cilcode.tmp/ex5.cil.c"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "/usr/include/stdc-predef.h" 1 3 4
# 1 "<command-line>" 2
# 1 "cilcode.tmp/ex5.cil.c"
# 1 "cilcode.tmp/ex5.c"
int f(double x ) ;
# 3 "cilcode.tmp/ex5.c"
int g(double x ) ;
# 2 "cilcode.tmp/ex5.c"
int f(double x )
{
  int tmp ;

  {
# 3 "cilcode.tmp/ex5.c"
  tmp = g(x);
# 3 "cilcode.tmp/ex5.c"
  return (tmp);
}
}
# 5 "cilcode.tmp/ex5.c"
int g(double x )
{


  {
# 6 "cilcode.tmp/ex5.c"
  return ((int )x);
}
}
