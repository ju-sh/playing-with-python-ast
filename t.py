import ast
from unparse import Unparser

s="'sdf {} as'.format(2)";
s="a=b'32'";
s="a=None";
m=ast.parse(s)
print(ast.dump(m))
obj = Unparser(m)
#print(obj.get_result())
print(Unparser(m).get_result())

