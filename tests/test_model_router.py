import unittest
import sys
import os

# 将项目根目录添加到Python路径中，以便导入模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.model_router import ModelRouter

class TestModelRouter(unittest.TestCase):

    def test_initialization(self):
        """测试ModelRouter能否被成功初始化"""
        router = ModelRouter()
        self.assertIsNotNone(router)
        self.assertIsInstance(router.providers, dict)
        self.assertIsInstance(router.routes, dict)
        print("ModelRouter初始化测试通过。")

    def test_get_provider_for_task(self):
        """测试get_provider_for_task方法是否能正确获取提供商"""
        router = ModelRouter()
        
        # 测试默认任务类型
        default_provider = router.get_provider_for_task("default")
        self.assertIn("name", default_provider)
        self.assertIn("api_base_url", default_provider)
        self.assertIn("api_key", default_provider)
        self.assertIn("models", default_provider)
        
        # 测试思考任务类型
        think_provider = router.get_provider_for_task("think")
        self.assertIn("name", think_provider)
        self.assertIn("api_base_url", think_provider)
        self.assertIn("api_key", think_provider)
        self.assertIn("models", think_provider)
        print("ModelRouter.get_provider_for_task 测试通过。")

    def test_route_request(self):
        """测试route_request方法是否能正确路由请求"""
        router = ModelRouter()
        
        task_type = "think"
        prompt = "请解释人工智能的概念"
        routed_request = router.route_request(task_type, prompt)
        
        self.assertIn("provider", routed_request)
        self.assertIn("request", routed_request)
        self.assertEqual(routed_request["request"]["messages"][0]["content"], prompt)
        print("ModelRouter.route_request 测试通过。")

    def test_send_request(self):
        """测试send_request方法是否能正确发送请求"""
        router = ModelRouter()
        
        task_type = "default"
        prompt = "请解释机器学习的概念"
        response = router.send_request(task_type, prompt)
        
        self.assertIsInstance(response, dict)
        self.assertIn("model", response)
        print("ModelRouter.send_request 测试通过。")

if __name__ == '__main__':
    unittest.main()