import copy

loc1 = 'kb3.xml'
loc2 = 'query3.xml'

def predicate(root):
    clause = []
    var = []
    clause.append(root.attrib['text'])
    for temp in root:
        if temp.tag=='VARIABLE':
          clause.append( '$' + temp.attrib['text'])
        else:
          clause.append(temp.attrib['text'])
        var.append(temp.tag)  
    return (clause,var)

def equ(root):
    clause = []
    var = []
    clause.append(root.attrib['text'])
    for temp in root:
        if temp.tag=='VARIABLE':
          clause.append( '$' + temp.attrib['text'])
        else:
          clause.append(temp.attrib['text'])
        var.append(temp.tag)  
    return (clause,var)


def OR(root):
    trcl = []
    clause = []
    var= []
    for root1 in root:
      if root1.tag == 'PREDICATE':
        t1 = predicate(root1)
        t1[0].insert(1, "true")
        clause.append(t1[0])
        var.append(t1[1])

      elif root1.tag == 'EQ':
        t1 = equ(root1)
        t1[0].insert(1, "true")
        clause.append(t1[0])
        var.append(t1[1])

      elif root1.tag == 'NOT':
        for root11 in root1:
          t1 = predicate(root11)
          # if(root11.tag == 'EQ')
          #     t1 = equ(root11)
          t1[0].insert(1, "false")
          clause.append(t1[0])
          var.append(t1[1])
          
      else:
        t = OR(root1)
        clause = clause + t[0]
        trcl = trcl + t[1]
        var = var + t[2]
    return (clause, trcl, var)    


import xml.etree.ElementTree as ET
 
# import xml.etree.ElementTree as ET
tree = ET.parse(loc1)
root = tree.getroot()


kb = [[['=', 'true', '$x', '$x']]]
true = []
variable = []

for i in range(len(root)):
  clause = []
  trcl = []
  var = []
  
  if root[i].tag == 'PREDICATE':
    t = predicate(root[i])
    t[0].insert(1, "true")
    clause.append(t[0])
    var = t[1]
    trcl.append('true')

  elif root[i].tag == 'EQ':
    t1 = equ(root[i])
    t1[0].insert(1, "true")
    clause.append(t1[0])
    var.append(t1[1])

  elif root[i].tag == 'NOT':
    # trcl.append('false')
    for temp in root[i]:
      t = predicate(temp)
      # if(temp.tag == 'EQ')
      #   t1 = equ(root11)
      t[0].insert(1, "false")
      clause.append(t[0])
      var = t[1]

  else:
    t = OR(root[i])
    clause = clause + t[0]
    trcl = t[1]
    var = var + t[2]
    
  kb.append(clause)
  true.append(trcl)
  variable.append(var)

print(kb)
# print(true)
# print(variable)


def gOR(root):
    trcl = []
    clause = []
    var= []
    for root1 in root:
      if root1.tag == 'PREDICATE':
        t1 = predicate(root1)
        t1[0].insert(1, "false")
        clause.append(t1[0])
        var.append(t1[1])

      elif root[i].tag == 'EQ':
        t1 = equ(root[i])
        t1[0].insert(1, "false")
        clause.append(t1[0])
        var.append(t1[1])

      elif root1.tag == 'NOT':
        for root11 in root1:
          t1 = predicate(root11)
          t1[0].insert(1, "true")
          clause.append(t1[0])
          var.append(t1[1])
          
      else:
        t = gOR(root1)
        clause = clause + t[0]
        trcl = trcl + t[1]
        var = var + t[2]
    return (clause, trcl, var)    


tree = ET.parse(loc2)
root = tree.getroot()

for i in range(len(root)):
  clause = []
  trcl = []
  var = []
  
  if root[i].tag == 'PREDICATE':
    t = predicate(root[i])
    t[0].insert(1, "false")
    clause.append(t[0])
    var = t[1]

  elif root[i].tag == 'NOT':
    # trcl.append('false')
    for temp in root[i]:
      t = predicate(temp)
      t[0].insert(1, "true")
      clause.append(t[0])
      var = t[1]

  elif root[i].tag == 'EQ':
      t1 = equ(root[i])
      t1[0].insert(1, "false")
      clause.append(t1[0])
      var.append(t1[1])

  else:
    t = gOR(root[i])
    clause = clause + t[0]
    trcl = t[1]
    var = var + t[2]
    
  kb.append(clause)
  true.append(trcl)
  variable.append(var)

print(kb)


# from traitlets.config.application import T
from typing import Dict, List, Tuple

# Define the Term class
class Term:
    def __init__(self, name: str, args: List['Term'] = []):
        self.name = name
        self.args = args

    # def __del__(self):
    #     del self.name
    #     self.args.clear()



# Define the Substitution class
class Substitution:
    def __init__(self, subst: Dict[str, Term] = {}):
        self.subst = subst

    def __del__(self):
      self.subst.clear()

    def add(self, key, value):
      if key in self.subst.keys():
          if self.subst[key].name == value.name:
            return True
          else:
            return False
      else:
          self.subst[key] = value
          return True




# Apply a substitution to a term
# def apply(theta: Substitution, t: Term) -> Term:
#     if t.name in theta.subst:
#         return apply(theta, theta.subst[t.name])
#     else:
#         new_args = [apply(theta, arg) for arg in t.args]
#         return Term(t.name, new_args)

# t1 = Term("f", [Term("$x"), Term("g", [Term("h")])])
# t2 = Term("f", [Term("g", [Term("$y")]), Term("$z")])
# theta = Substitution()
# if unify(t1, t2, theta):
#     print("Substitution:")
#     for var, t in theta.subst.items():
#         while t.name[0] == '$':
#             t = theta.subst[t.name]
#         print(f"{var} => {t.name}")
#     print("Applied substitution:")
#     t1_subst = apply(theta, t1)
#     t2_subst = apply(theta, t2)
#     print(f"t1 = {t1.name} {' '.join(arg.name for arg in t1_subst.args)}")
#     print(f"t2 = {t2.name} {' '.join(arg.name for arg in t2_subst.args)}")
# else:
#     print("Unification failed")


# Unify two terms
def unify(t1: Term, t2: Term, theta: Substitution) -> bool:
    # If the terms are identical, return true
    if t1.name == t2.name and len(t1.args) == len(t2.args):
        for i in range(len(t1.args)):
            if not unify(t1.args[i], t2.args[i], theta):
                return False
        return True

    # If either term is a variable, add the substitution
    if t1.name[0] == '$':
        return theta.add(t1.name, t2)
        
    # if t2.name[0] == '$':
    #     return theta.add(t2.name, t1)
    
    # print(t1.name)
    # print(t2.name)
    # If the terms cannot be unified, return false
    return False



# l1 = ['Mother', 'khush', 'charley', 'khush']
# l2 = ['Mother', '$X', '$Y', '$X']

# term2 = Term(l1[0], [Term(l1[idx]) for idx in range(1, len(l1))])
# term1 = Term(l2[0], [Term(l2[idx]) for idx in range(1, len(l2))])

# theta1 = Substitution()

# for var, t in theta1.subst.items():
#     # while t.name[0] == '$':
#     #     t = theta1.subst[t.name]
#     print(f"{var} => {t.name}")

# if unify(term1, term2, theta1):
#     print("Substitution:")
#     for var, t in theta1.subst.items():
#         # while t.name[0] == '$':
#         #     t = theta1.subst[t.name]
#         print(f"{var} => {t.name}")
# else:
#     print("Unification failed")

# del theta1
# # del term1
# # del term2



def apply(query_list, theta):
    for i in range(len(query_list)):
        for j in range(2, len(query_list[i])):
            if query_list[i][j] in theta.subst.keys():
              query_list[i][j] = theta.subst[query_list[i][j]].name
    return query_list


def check(l):
    for el1 in l:
      for el2 in l:
          if el1 != el2 and len(el1)==len(el2):
              
              flag = True
              for i in range(len(el1)):
                  if i==1:
                    if el1[i]==el2[i]:
                      flag = False
                      break
                  else:
                      if el1[i]!=el2[i]:
                          flag = False
                          break

              if flag:
                  return []
              
              
    return l


print(kb)


def fun(l):
  if len(l)==0:
    print("[]")
    return
  s = ''
  for j in range(len(l)):
    if j != 0:
      s = s + ' V '
    if l[j][1]=='false':
      s = s + '~' 
    s = s + l[j][0]
    s = s + '('
    for i in range(2,len(l[j])):
      if i>2:
        s = s + ','
      s = s + l[j][i]
    s = s + ')'
  print(s)


def resolve(): 
  kb.sort(key = lambda x: len(x))
  for i in range(len(kb)): 
    for j in range(len(kb[i])): 
      s = kb[i][j][0]
      for p in range(len(kb)):
          for q in range(len(kb[p])):
              if p==i and q==j:
                  continue

              if s==kb[p][q][0] and kb[p][q][1]!=kb[i][j][1]:
                  t2 = Term(kb[p][q][0], [Term(kb[p][q][idx]) for idx in range(2, len(kb[p][q]))])
                  t1 = Term(kb[i][j][0], [Term(kb[i][j][idx]) for idx in range(2, len(kb[i][j]))])

                  theta1 = Substitution()
                  if unify(t1, t2, theta1):
                      # print(kb[i])
                      # print(kb[p])
                      l = []
                      for it in range(len(kb[i])):
                          if it!=j:
                              l.append( copy.deepcopy(kb[i][it]) )
                      # print(i,j,p,q)
                      # print(l)

                      for it in range(len(kb[p])):
                          if it!=q:
                              l.append( copy.deepcopy(kb[p][it]) )
                      # print(l)
                      
                      l = apply(l, theta1)
                      l = check(l)
                      if l in kb:
                        del theta1
                        continue
                      
                      kb.append(l)
                      
                      fun(kb[i])
                      # print(kb[p])
                      fun(kb[i])
                      # kb.sort(key = lambda x: len(x))
                      # print(l)
                      fun(l)
                      print()
                      if l:
                          return False
                      else:
                          return True
                  del theta1
  return true


for it in range(len(kb)):
  fun(kb[it])

it = 0
flag = true
while flag and it<200:
  flag = not resolve()
  it = it+1

if flag:
  print("Fail")
else:
  print("Success")


