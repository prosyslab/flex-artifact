# 1 "cilcode.tmp/ex28.cil.c"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "/usr/include/stdc-predef.h" 1 3 4
# 1 "<command-line>" 2
# 1 "cilcode.tmp/ex28.cil.c"
# 1 "cilcode.tmp/ex28.c"
int main(void)
{
  int ***three ;
  int **two ;
  int **mem_3 ;
  int *mem_4 ;
  int *mem_5 ;

  {
# 4 "cilcode.tmp/ex28.c"
  mem_3 = *three;
# 4 "cilcode.tmp/ex28.c"
  mem_4 = *mem_3;
# 4 "cilcode.tmp/ex28.c"
  mem_5 = *two;
# 4 "cilcode.tmp/ex28.c"
  *mem_4 = *mem_5;
# 5 "cilcode.tmp/ex28.c"
  return (0);
}
}
