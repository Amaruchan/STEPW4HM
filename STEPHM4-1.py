from collections import deque

class Node:
    def __init__(self, title):
        self.title = title
        self.next_ids = []
        self.searched = False


# pagesファイル と linksファイル から グラフ作成
# {id: Node(title, next_ids, searched)}
def make_graph_from_file(pages, links):
    # pagesファイル から vertex作成
    nodes = {}
    with open(pages) as f:
        for page in f.read().splitlines():
            id, title = page.split('\t')
            nodes[id] = Node(title)
    # linksファイル から edge作成
    with open(links) as f:
        for link in f.read().splitlines():
            id, next_id = link.split('\t')
            nodes[id].next_ids.append(next_id)
    return nodes


# title から id 取得
def get_id_from_title(nodes, title):
    for id, node in nodes.items():
        if node.title == title:
            return id

# 深さごとに再帰呼び出し
def bfs_rec(nodes, end_id, queue):
    if queue: # queue が存在する限り続行
        node, route = queue.popleft() # queue から次のノード取得
        next_ids = node.next_ids # 次のリンクを取得
        for next_id in next_ids: # 全てのリンクを探索
            new_route = route + [next_id]
            if next_id == end_id:
                return new_route # find! → route を返す
            next_node = nodes[next_id]
            if next_node.searched == False: # 探索済みか確認
                queue.append((next_node, new_route)) # これまでの route も含めて node を queue に追加
                next_node.searched = True
        return bfs_rec(nodes, end_id, queue)
    return [] # not exist → routeなし


# 幅優先探索
def bfs(nodes, start_id, end_id):
    queue = deque()
    queue.append((nodes[start_id], [])) # 最初の探索を start_id に指定
    return bfs_rec(nodes, end_id, queue)


nodes = make_graph_from_file('data/pages.txt', 'data/links.txt')
start_id = get_id_from_title(nodes, "Google")
end_id = get_id_from_title(nodes, "渋谷")
route = bfs(nodes, start_id, end_id)
print("宿題①")
if route: 
    print(nodes[start_id].title, end = "")
    for id in route:
        print(" -> " + nodes[id].title, end = "")
    print("\n最短距離は {}".format(len(route)))
else: print("Not exist")
