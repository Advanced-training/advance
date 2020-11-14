
def find_all_path(graph, start, end):
    """找到两个点之间的所有路径

      :param graph: 图
       :param start: 起始节点
      :param end 目的节点
      :return 返回所有路径列表
    """
    path = []
    noteSet = set()
    stack = []
    noteSet.add(start)
    stack.append(start)
    path1 = []
    while stack:
        cur = stack[-1]
        #         print("the cur is"+ cur)
        visited = False
        again = False
        for key in graph[cur].keys():
            #             print("the key is"+key)
            if (key not in noteSet) | (key == end):
                #                 print("yes")
                visited = True
                stack.append(key)
                noteSet.add(key)
                for path2 in path:
                    if path2 == stack:
                        again = True
                break

        if not visited:
            stack.pop(-1)
        #         print(end)
        if not stack:
            break
        cur = stack[-1]
        #         print("the cur = "+cur+" the end = ")
        if cur == end:
            if not again:
                #                 print("not again")
                #                 print(stack)
                for i in range(len(stack)):
                    path1.append(stack[i])
                #                 print("the path is:")
                #                 print(path1)
                path.append(path1)
                noteSet.remove(stack[-1])
                #                 print("the notset is")
                #                 print(noteSet)
                path1 = []
            visited = True
            while visited:
                if stack[-1] == start:
                    #                     print("over!")
                    #                     print("the final stack is")
                    #                     print(stack)
                    #                     print("the final set is")
                    #                     print(noteSet)
                    cur = start
                    for key in graph[cur]:
                        #                         print(key)
                        #                         print("the stack is:")
                        #                         print(stack)
                        if (key not in noteSet) & (key != end) & (key not in stack):
                            stack.append(key)
                            noteSet.add(key)
                            visited = False
                            break
                    if visited:
                        stack.pop()
                    break
                if stack:
                    stack.pop(-1)
                    #                 print(stack[-1])
                    #                 print(graph[stack[-1]])
                    cur = stack[-1]
                    #                     print("the cur is"+ cur)
                    for key in graph[stack[-1]]:
                        #                         print(key)
                        #                         print("the stack is:")
                        #                         print(stack)
                        if (key not in noteSet) & (key != end) & (key not in stack):
                            stack.append(key)
                            noteSet.add(key)
                            visited = False
                            break
                else:
                    visited = False
    #     print(path)
    return path


def find_biggest_weight_path(graph, start, end):
    """从所有路径中找到权值总和最大的路径

        :param graph: 图
         :param start: 起始节点
        :param end 目的节点
        :return 最大路径和这条路径某条边最小权值的列表

        测试样例：
        g = nx.DiGraph()
        g.add_weighted_edges_from([("1", "2", 50), ("3", "5", 30), ("2", "3", 30), ("3", "4", 10), ("2", "4", 50),("4", "5", 50)
                           ,("2", "1", 20),("5", "3", 20),("3", "2", 20),("4", "3", 40),("4", "2", 10),("5", "4", 20)])
        a = find_biggest_weight_path(g, "1", "5")
        print(a)
        b = find_biggest_weight_path(g, "3", "5")
        print(b)
        c = find_biggest_weight_path(g, "3", "4")
        print(c)
      """
    path = find_all_path(graph, start, end)
    min_weight = float("inf")
    max_weight = 0.0
    weight = 0.0
    max_path = []
    for path_vector in path:
        #         print(path_vector)
        for i in range(len(path_vector) - 1):
            num = graph[path_vector[i]][path_vector[i + 1]]
            #             print(num)
            #             print(num["weight"])
            weight = weight + num["weight"]
        if weight > max_weight:
            max_path = path_vector
            max_weight = weight
        # print(max_weight)
        weight = 0

    for i in range(len(max_path) - 1):
        num = graph[max_path[i]][max_path[i + 1]]
        if min_weight > num["weight"]:
            min_weight = num["weight"]
    #     print(max_weight)
    path1 = [max_path, min_weight]
    #     print(path1)
    return path1
