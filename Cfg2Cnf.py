# Author: Max Base
# Date: 2020/06/17
# Web: maxbase.org
# Repo: https://github.com/BaseMax/CFG2CNF
import sys

class Cfg2Cnf:
  def __init__(self, filename):
    with open(filename, 'r') as gramatica:
      lines = gramatica.read().splitlines()
    self.moves={}
    self.rules={}
    self.alphas=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    for line in lines:
      parts=line.split("=>")
      parts[0]=parts[0].strip()
      parts[1]=parts[1].strip()
      parts[1]=parts[1].split("|")
      if not parts[0] in self.rules:
        self.rules[parts[0]]=[]
      for part in parts[1]:
        part=part.strip()
        self.rules[parts[0]].append(part)

  def new_name_for_grammar(self, array):
    names=list(array)
    for alpha in self.alphas:
      if alpha not in names:
        return alpha
    print("Error: cannot find a new and fresh name for new Grammar statement!")
    sys.exit(-1) 

  def has_upper_and_lower_case(self, value):
    upper = False
    lower = False
    for i in value:
      if i.islower():
        lower = True
      if i.isupper():
        upper = True
    return lower and upper

  def move_terminals_to_new_grammar(self, array):
    for key in list(array):
      index = 0
      count = len(array[key])
      if count > 1 or self.has_upper_and_lower_case(array[key][0]):
        while index < count:
          value=array[key][index]
          length=len(value)
          i=0
          while i < length:
            if str(value[i]).islower():
              if value[i] not in list(self.moves):
                name=self.new_name_for_grammar(array)
                self.moves[value[i]]=name
                array[name]=[]
                array[name].append(value[i])
              else:
                name=self.moves[value[i]]
              array[key][index]=array[key][index].replace(value[i], name)
            i+=1
          index+=1
    return array

  def replace_grammar_statement_names(self, array, key, char):
    # print("Found big character(s)", char, "in", key, "statement")
    # print("Check move tables:", self.moves)
    if char not in list(self.moves.values()):
      print("Error: find a non-terminal upper-case character, we cannot support one statement with one Upper-case non-terminalestic!")
      sys.exit(-1)
    return array

  def format_grammar(self, array):
    for key in list(array):
      index = 0
      count = len(array[key])
      while index < count:
        length=len(array[key][index])
        if length == 1:
          if not array[key][index][0].islower():
            array=self.replace_grammar_statement_names(array, key, array[key][index])
        elif length > 2:
          values=array[key][index][1:]
          name=self.new_name_for_grammar(array)
          array[name]=[]
          array[name].append(values)
          array[key][index]=array[key][index].replace(values, name)
        index+=1
    return array

  def print_grammar(self):
    return self.format_grammar(self.move_terminals_to_new_grammar(self.rules))
