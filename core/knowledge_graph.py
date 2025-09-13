class KnowledgeGraph:
    def __init__(self):
        """
        知识图谱
        - 连接信息与洞察
        """
        self.graph = {}

    def add_node(self, node):
        """添加节点"""
        if node not in self.graph:
            self.graph[node] = []
            print(f"知识图谱：添加节点 {node}")

    def add_edge(self, node1, node2):
        """添加边"""
        # 确保两个节点都存在
        if node1 not in self.graph:
            self.add_node(node1)
        if node2 not in self.graph:
            self.add_node(node2)
        
        # 添加连接关系
        if node2 not in self.graph[node1]:
            self.graph[node1].append(node2)
            print(f"知识图谱：连接 {node1} -> {node2}")

    def get_related_nodes(self, node):
        """获取相关节点"""
        return self.graph.get(node, [])

    def get_all_nodes(self):
        """获取所有节点"""
        return list(self.graph.keys())

    def get_graph_summary(self):
        """获取图谱摘要"""
        summary = {}
        for node, connections in self.graph.items():
            summary[node] = {
                "connections_count": len(connections),
                "connected_nodes": connections
            }
        return summary