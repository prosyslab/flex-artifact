# 1 "cilcode.tmp/ex16.cil.c"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "/usr/include/stdc-predef.h" 1 3 4
# 1 "<command-line>" 2
# 1 "cilcode.tmp/ex16.cil.c"
# 1 "cilcode.tmp/ex16.c"
extern int f(int ) ;
# 1 "cilcode.tmp/ex16.c"
int main(void)
{
  int x ;
  int tmp ;
  int tmp___0 ;

  {
# 2 "cilcode.tmp/ex16.c"
  tmp = x;
# 2 "cilcode.tmp/ex16.c"
  x ++;
# 2 "cilcode.tmp/ex16.c"
  tmp___0 = f(x);
# 2 "cilcode.tmp/ex16.c"
  return (tmp + tmp___0);
}
}
