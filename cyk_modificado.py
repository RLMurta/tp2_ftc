from Cfg22nf import Cfg22nf
from timeit import default_timer as timer

class Cyk_modificado:
    def ler_gramatica(self):
        start_cyk = timer()
        nf = Cfg22nf("gramatica.txt")
        end_cyk = timer()
        print("Tempo GLC para 2NF: {} s".format(end_cyk - start_cyk))
        regras = nf.print_grammar()
        inverse = self.inverse_unit_graph(regras)
        return regras, inverse

    def nullable(self, gramatica):
        nullable = []
        occurs = {}

        for nonterminal in gramatica:
            occurs[nonterminal] = []

        for nonterminal in gramatica:
            for ruls in gramatica[nonterminal]:
                if len(ruls) == 1 and ruls in gramatica:
                    occurs[ruls].append(nonterminal)

        for nonterminal in gramatica:
            for ruls in gramatica[nonterminal]:
                if len(ruls) == 2 and ruls[0] in gramatica and ruls[1] in gramatica:
                    occurs[ruls[0]].append(nonterminal + ruls[1])
                    occurs[ruls[1]].append(nonterminal + ruls[0])

        todo = []
        nullable = []
        for nonterminal in gramatica:
            if "λ" in gramatica[nonterminal]:
                nullable.append(nonterminal)
                todo.append(nonterminal)

        while len(todo) != 0:
            B = todo.pop()
            for i in range(len(occurs[B])):
                if len(occurs[B][i]) == 1:
                    continue
                A = occurs[B][i][0]
                C = occurs[B][i][1]

                shouldSkip = C not in nullable or A in nullable

                if shouldSkip:
                    continue

                nullable.append(A)
                todo.append(A)

        return nullable

    def inverse_unit_graph(self, gramatica):
        nullableSet = self.nullable(gramatica)

        graph = {}
        addEdge = lambda left, right: graph.setdefault(left, []).append(right)

        for nonterminal in gramatica:
            for word in gramatica[nonterminal]:
                if len(word) == 1:
                    addEdge(word, nonterminal)
                else:
                    if word[0] in nullableSet:
                        addEdge(word[1], nonterminal)
                    if word[1] in nullableSet:
                        addEdge(word[0], nonterminal)
        return graph

    def deep_first_search(self, graph, root):
        if root not in graph:
            return [root]

        visited = [root]
        todo = []
        for i in range(len(graph[root])):
            todo.append(graph[root][i])
            visited.append(graph[root][i])

        while len(todo) != 0:
            next = todo.pop()
            if next in graph:
                for edge in graph[next]:
                    if graph[next][0] == edge:
                        vertex = graph[next][0]
                    else:
                        vertex = graph[next][1]

                    if vertex not in visited:
                        todo.append(vertex)
                        visited.append(vertex)
        return visited

    def reachable(self, graph, set):
        reachable = []
        for node in set:
            visited = self.deep_first_search(graph, node)
            for i in range(len(visited)):
                if visited[i] not in reachable:
                    reachable.append(visited[i])
        return reachable

    def cyk(self, gramatica, u, entrada):
        tamanho = len(entrada)

        tabela = [[[] for _ in range(tamanho)] for l in range(tamanho)]
        tabela_star = [[[] for _ in range(tamanho)] for x in range(tamanho)]

        for p in range(tamanho):
            tabela[p][p] = self.reachable(u, [entrada[p]])

        for i in range(1, tamanho):
            for j in range(i-1, -1, -1):
                tabela_star[j][i] = []
                for k in range(j, i):
                    for nonterminal in gramatica:
                        for rhs in gramatica[nonterminal]:
                            rule = rhs
                            condition = len(rule) == 2 and rule[0] in tabela[j][k] and rule[1] in tabela[k + 1][i]
                            if condition:
                                tabela_star[j][i].append(nonterminal)
                tabela[j][i] = self.reachable(u, tabela_star[j][i])
        print("CYK Modificado:")
        if ('S') in tabela[0][tamanho-1]:
            print(entrada, "pertence a gramática")
        else:
            print(entrada, "não pertence a gramática")
        return tabela

if __name__ == '__main__':
    cyk = Cyk_modificado()
    regras, inverse = cyk.ler_gramatica()
    palavra = input("Escreva uma palavra:\n")
    cyk.cyk(regras, inverse, palavra)