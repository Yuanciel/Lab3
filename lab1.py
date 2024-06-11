"""
lab1.py

This module contains functions and classes for Lab 1.
It includes implementations for various algorithms and utilities used in the lab exercises.

Author: yyy
Date: 2024-06-10
"""
import re
import threading
import time
import random
import networkx as nx
from PIL import Image
import matplotlib.pyplot as plt
directed_graph = nx.MultiDiGraph()
random = random.Random()
directed_graph = nx.DiGraph()
LAST_ONE = None  # Change variable name to follow PEP8 naming conventions
FLAG=True

def showDirectedGraph(filename):
    """
     展示有向图
     """
    global LAST_ONE
    global FLAG
    try:
        with open(filename, 'r',encoding='utf-8') as file:
            for line in file:
                words = re.findall(r'\b[A-Za-z]\w*\b', line)
                # 将所有单词转换为小写
                words = [word.lower() for word in words]
                for word in words:
                    add_node_if_not_exists(word)
                    if LAST_ONE:
                        add_edge_with_weight(LAST_ONE, word)
                    LAST_ONE = word
        FLAG=False
    except FileNotFoundError:
        print("File not found!")


def add_node_if_not_exists(node_id):
    """
    加节点
    """
    if not directed_graph.has_node(node_id):
        directed_graph.add_node(node_id)


def add_edge_with_weight(from_node, to_node):
    """
    加权重
    """

    if directed_graph.has_node(from_node) and directed_graph.has_node(to_node):
        if directed_graph.has_edge(from_node, to_node):
            # Increment edge weight by 1 if the edge already exists
            directed_graph[from_node][to_node]['weight'] += 1
            #print(directed_graph[from_node][to_node]['weight'])  #打印边权值的 测试用的

        else:
            # Add edge with weight 1 if it doesn't exist
            directed_graph.add_edge(from_node, to_node, weight=1)



# 用于检测用户输入的线程
def check_user_input(stop_event):
    """
    检测用户输入enter
    """

    input("Press Enter to stop the random walk...")
    stop_event.set()

def randomWalk(delay=1):
    """
    随机游走函数
    """

    if not directed_graph or len(directed_graph.nodes) == 0:
        return "Graph is empty."

    visited_nodes = []  # 存储已经访问的节点
    visited_edges = set()  # 使用集合来存储已经访问的边，确保边不重复
    current_node = random.choice(list(directed_graph.nodes))
    interrupted_by_user = False  # 标志位，表示是否被用户打断

    # 事件用于标记是否用户请求停止
    stop_event = threading.Event()
    input_thread = threading.Thread(target=check_user_input, args=(stop_event,))
    input_thread.start()

    try:
        while True:
            visited_nodes.append(current_node)
            neighbors = list(directed_graph.neighbors(current_node))

            # 过滤掉已经访问过的边
            unvisited_neighbors = [n for n in neighbors if (current_node, n) not in visited_edges]
            if not unvisited_neighbors:
                break

            next_node = random.choice(unvisited_neighbors)
            visited_edges.add((current_node, next_node))

            current_node = next_node

            # 加入延迟
            time.sleep(delay)

            # 检查用户是否打断游走
            if stop_event.is_set():
                interrupted_by_user = True
                print("Interrupted by user!")
                break  # 用户打断，退出循环
    except KeyboardInterrupt:
        interrupted_by_user = True
    finally:
        if interrupted_by_user:
            visited_nodes.append("(Interrupted by user)")
        else:
            visited_nodes.append("(Finished without interruption)")

        result = "Visited Nodes: "
        for node in visited_nodes:
            result += f" {node} "
        with open("random_walk_output.txt", "w") as file:
            file.write(result)
    return result

def queryBridgeWords(word1, word2, flag=True): # False表示只返回桥接词不输出提示语句
    """
    查询桥接词函数
    """
    word3 = []
    # 判断word1和word2是否在图中
    if flag:
        if not directed_graph.has_node(word1) and not directed_graph.has_node(word2):
            print(f"No \"{word1}\" and \"{word2}\" in the graph!")
        elif not directed_graph.has_node(word1):
            print(f"No \"{word1}\" in the graph!")
        elif not directed_graph.has_node(word2):
            print(f"No \"{word2}\" in the graph!")
    if not directed_graph.has_node(word1) or not directed_graph.has_node(word2):
        return word3
    # 用word3记录word1和word2的桥接词
    # 遍历word1的邻居，再遍历word1的邻居的邻居，判断是否有word2的邻居
    for neighbor in directed_graph.neighbors(word1):
        for neighbor2 in directed_graph.neighbors(neighbor):
            if neighbor2 == word2:
                word3.append(neighbor)
    if flag:
        if not word3:
            print(f"No bridge words from \"{word1}\" to \"{word2}\"!")
        else:
            print(f"The bridge words from \"{word1}\" to \"{word2}\" are: {', '.join(word3)}")
    return word3


def generateNewText(input_text):
    """
    生成新文本
    """

    new_text = []
    words = input_text.lower().split()
    # print(words)
    if len(words)==0:
        return ""
    if len(words)==1:
        return words[0]
    else:
        for i in range(len(words) - 1):
            word1 = words[i]
            word2 = words[i + 1]
            new_text.append(word1)
            bridge_word = queryBridgeWords(word1, word2, False) #查询是否有桥接词
            if bridge_word:
                random_num = random.randint(0, len(bridge_word)-1)
                new_text.append(bridge_word[random_num])
        new_text.append(words[-1])
        return ' '.join(new_text)

# 修正后的Dijkstra算法，生成最短路径图，该图上从word1到word2的所有路径都是最短路路径
def calcShortestPath(word1, word2):
    """
    计算最短路径的函数.
    """

    _word1 = word1
    _word2 = word2
    if not directed_graph.has_node(word1) and not directed_graph.has_node(word2):
        random_node1 = random.choice(list(directed_graph.nodes))
        random_node2 = random.choice(list(directed_graph.nodes))
        print(f"Both nodes not in the graph. Using random node: \"{random_node1}\"")
        _word1 = random_node1
        _word2 = random_node2
        #print(f"Both nodes not in the graph. Using random node: \"{random_node}\"")
    elif not directed_graph.has_node(word1):
        random_node = random.choice(list(directed_graph.nodes))
        print(f"\"{word1}\" not in the graph. Using random node: \"{random_node}\"")
        _word1 = random_node
        #print(f"\"{word1}\" not in the graph. Using random node: \"{random_node}\"")
    elif not directed_graph.has_node(word2):
        random_node = random.choice(list(directed_graph.nodes))
        print(f"\"{word2}\" not in the graph. Using random node: \"{random_node}\"")
        _word2 = random_node
        #print(f"\"{word2}\" not in the graph. Using random node: \"{random_node}\"")
    # Step.1 初始化
    distances = {node: float('inf') for node in directed_graph}
    distances[_word1] = 0
    miu = {}
    for node1 in directed_graph:
        for node2 in directed_graph:
            miu[(node1, node2)] = 0
    R = set()
    R.add(_word1)
    S = set()
    # Step.2 y是current_node，x是neighbor
    while len(S) != len(directed_graph):
        min = float('inf')
        for i in R:
            if min > distances[i]:
                min = distances[i]
                current_node = i
        if len(R) == 0:
            break
        R.remove(current_node)
        S.add(current_node)
        for neighbor, weight in directed_graph[current_node].items():
            if neighbor in S:
                continue
            else:
                R.add(neighbor)
            # Step3
            if distances[current_node] + weight['weight'] < distances[neighbor]:
                distances[neighbor] = distances[current_node] + weight['weight']
                miu[(current_node, neighbor)] = 1
                for node1 in directed_graph:
                    if node1 != current_node:
                        miu[((node1, neighbor))] = 0
            if distances[current_node] + weight['weight'] == distances[neighbor]:
                miu[(current_node, neighbor)] = 1
    # Step4
    minG = nx.DiGraph() # 最短路径图
    for node in directed_graph:
        if not minG.has_node(node):
            minG.add_node(node)
    for node1 in minG:
        for node2 in minG:
            if miu[(node1, node2)] == 1:
                minG.add_edge(node1, node2, weight=directed_graph[node1][node2]['weight'])
    # Step5
    #PGMin = nx.nx_pydot.to_pydot(minG)
    # 将原图中的边权值加入PG中，PG是Graphviz的图对象
    # 利用DFS求minG上从word1到word2的所有路径
    def dfs(graph, start, end, path, paths):
        """
        This function performs a specific task.
        Args:
            param1 (type): Description of param1.
            param2 (type): Description of param2.
        Returns:
            type: Description of the return value.
        """

        path = path + [start]
        if start == end:
            paths.append(path)
        for node in graph[start].items():
            if node not in path:
                dfs(graph, node, end, path, paths)
    paths = []
    dfs(minG, _word1, _word2, [], paths)
    # 输出最短路径
    n = 1
    for path in paths:
        PGMinpath = nx.nx_pydot.to_pydot(directed_graph)
        for edge in PGMinpath.get_edges():
            edge_label = str(directed_graph[edge.get_source()][edge.get_destination()]['weight'])
            edge.set_label(edge_label)
        for i in range(len(path)-1):
            # 将PGMin中的结点I颜色设置为红色
            for node in PGMinpath.get_nodes():
                if node.get_name() == path[i]:
                    node.set_color('red')
                    node.set_fontcolor('red')
            # 将PGMin中的边I->J颜色设置为红色
            for edge in PGMinpath.get_edges():
                if edge.get_source() == path[i] and edge.get_destination() == path[i+1]:
                    edge.set_color('red')
                    edge.set_fontcolor('red')
        for node in PGMinpath.get_nodes():
            if node.get_name() == path[len(path)-1]:
                node.set_color('red')
                node.set_fontcolor('red')
        # 保存图片
        PGMinpath.write_png(f'minPath_{_word1}_{_word2}_{n}.png')
        # 展示图片
        image_path = f'minPath_{_word1}_{_word2}_{n}.png'
        img = Image.open(image_path)
        plt.imshow(img)
        plt.axis('off') # 关掉坐标轴为 off
        plt.show()
        n += 1
    if distances[_word2] == float('inf'):
        return f"There is no path from \"{_word1}\" to \"{_word2}\"."
    return f"There are {len(paths)} shortest paths from \"{_word1}\" to \"{_word2}\". Their lengths are: {distances[_word2]}."

def visualize_graph():
    """
    可视化路径
    """

    PG = nx.nx_pydot.to_pydot(directed_graph)
    # 将原图中的边权值加入PG中，PG是Graphviz的图对象
    for edge in PG.get_edges():
        edge_label = str(directed_graph[edge.get_source()][edge.get_destination()]['weight'])
        edge.set_label(edge_label)
    PG.write_png('graph.png')
    # 展示图片
    # img = Image.open(os.path.join('images', '2007_000648' + '.jpg'))
    img = Image.open('graph.png')
    plt.imshow(img)
    plt.axis('off') # 关掉坐标轴为 off
    plt.show()


if __name__ == "__main__":
    while FLAG:
        filename = input("Enter the input file name: ")
        showDirectedGraph(filename)

    while True:
        print("\nChoose an option:")
        print("1. Show Directed Graph")
        print("2. Query Bridge Words")
        print("3. Generate New Text")
        print("4. Calculate Shortest Path")
        print("5. Random Walk")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            visualize_graph()
        elif choice == "2":
            word1 = input("Enter word1: ")
            word2 = input("Enter word2: ")
            queryBridgeWords(word1, word2)
        elif choice == "3":
            input_text = input("Enter new text: ")
            new_text = generateNewText(input_text)
            print("New Text:", new_text)
        elif choice == "4":
            word1 = input("Enter word1: ")
            word2 = input("Enter word2: ")
            result = calcShortestPath(word1, word2)
            print(result)
        elif choice == "5":
            randomWalk()
            print("Random walk completed! Check 'random_walk_output.txt' for the result.")
        elif choice == "6":
            print("Exiting program.")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 6.")
