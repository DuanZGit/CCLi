import unittest
import sys
import os

# 将项目根目录添加到Python路径中，以便导入模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.knowledge_graph import KnowledgeGraph

class TestKnowledgeGraph(unittest.TestCase):

    def test_initialization(self):
        """测试KnowledgeGraph能否被成功初始化"""
        kg = KnowledgeGraph()
        self.assertEqual(kg.graph, {})
        print("KnowledgeGraph初始化测试通过。")

    def test_add_node(self):
        """测试add_node方法是否能正确添加节点"""
        kg = KnowledgeGraph()
        kg.add_node("人工智能")
        self.assertIn("人工智能", kg.graph)
        self.assertEqual(kg.graph["人工智能"], [])
        print("KnowledgeGraph.add_node 测试通过。")

    def test_add_edge(self):
        """测试add_edge方法是否能正确添加边"""
        kg = KnowledgeGraph()
        kg.add_edge("人工智能", "机器学习")
        self.assertIn("人工智能", kg.graph)
        self.assertIn("机器学习", kg.graph)
        self.assertIn("机器学习", kg.graph["人工智能"])
        print("KnowledgeGraph.add_edge 测试通过。")

    def test_get_related_nodes(self):
        """测试get_related_nodes方法是否能正确获取相关节点"""
        kg = KnowledgeGraph()
        kg.add_edge("人工智能", "机器学习")
        kg.add_edge("人工智能", "深度学习")
        kg.add_edge("机器学习", "神经网络")
        
        ai_related = kg.get_related_nodes("人工智能")
        self.assertIn("机器学习", ai_related)
        self.assertIn("深度学习", ai_related)
        self.assertNotIn("神经网络", ai_related)
        
        ml_related = kg.get_related_nodes("机器学习")
        self.assertIn("神经网络", ml_related)
        self.assertNotIn("人工智能", ml_related)
        print("KnowledgeGraph.get_related_nodes 测试通过。")

    def test_get_all_nodes(self):
        """测试get_all_nodes方法是否能正确获取所有节点"""
        kg = KnowledgeGraph()
        kg.add_node("人工智能")
        kg.add_node("机器学习")
        kg.add_edge("深度学习", "神经网络")
        
        all_nodes = kg.get_all_nodes()
        self.assertIn("人工智能", all_nodes)
        self.assertIn("机器学习", all_nodes)
        self.assertIn("深度学习", all_nodes)
        self.assertIn("神经网络", all_nodes)
        self.assertEqual(len(all_nodes), 4)
        print("KnowledgeGraph.get_all_nodes 测试通过。")

    def test_get_graph_summary(self):
        """测试get_graph_summary方法是否能正确获取图谱摘要"""
        kg = KnowledgeGraph()
        kg.add_edge("人工智能", "机器学习")
        kg.add_edge("人工智能", "深度学习")
        kg.add_edge("机器学习", "神经网络")
        
        summary = kg.get_graph_summary()
        self.assertIn("人工智能", summary)
        self.assertIn("机器学习", summary)
        self.assertIn("深度学习", summary)
        self.assertIn("神经网络", summary)
        
        self.assertEqual(summary["人工智能"]["connections_count"], 2)
        self.assertEqual(summary["机器学习"]["connections_count"], 1)
        self.assertIn("机器学习", summary["人工智能"]["connected_nodes"])
        self.assertIn("深度学习", summary["人工智能"]["connected_nodes"])
        print("KnowledgeGraph.get_graph_summary 测试通过。")

if __name__ == '__main__':
    unittest.main()