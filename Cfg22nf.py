import sys

class Cfg22nf:
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

  def has_member_with_length_greater_than_two(self, array):
    for key in list(array):
      for value in array[key]:
        if len(value) > 2:
          return True
    return False

  def binarization(self, array):
        for key in list(array):
            index = 0
            count = len(array[key])
            while index < count:
                length = len(array[key][index])
                if length > 2:
                    values = array[key][index][1:]
                    name = self.new_name_for_grammar(array)
                    array[name] = []
                    array[name].append(values)
                    array[key][index] = array[key][index].replace(values, name)
                index += 1
        print (array)
        return array

  def print_grammar(self):
    while self.has_member_with_length_greater_than_two(self.rules):
      self.rules = self.binarization(self.rules)
    return self.binarization(self.rules)
