import unittest
import sys
import os
from datetime import datetime, timedelta

# 将项目根目录添加到Python路径中，以便导入模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.event_logger import EventLogger

class TestEventLogger(unittest.TestCase):

    def test_initialization(self):
        """测试EventLogger能否被成功初始化"""
        logger = EventLogger()
        self.assertEqual(logger.events, [])
        print("EventLogger初始化测试通过。")

    def test_log_event(self):
        """测试log_event方法是否能正确记录事件"""
        logger = EventLogger()
        event_description = "测试事件"
        logger.log_event(event_description)
        
        self.assertEqual(len(logger.events), 1)
        self.assertEqual(logger.events[0]["description"], event_description)
        self.assertIn("timestamp", logger.events[0])
        print("EventLogger.log_event 测试通过。")

    def test_get_recent_events(self):
        """测试get_recent_events方法是否能正确获取最近事件"""
        logger = EventLogger()
        
        # 添加一个现在的时间事件
        logger.log_event("当前事件")
        
        # 添加一个10小时前的事件
        old_event = {
            "timestamp": (datetime.now() - timedelta(hours=10)).isoformat(),
            "description": "10小时前的事件"
        }
        logger.events.append(old_event)
        
        # 添加一个30小时前的事件
        very_old_event = {
            "timestamp": (datetime.now() - timedelta(hours=30)).isoformat(),
            "description": "30小时前的事件"
        }
        logger.events.append(very_old_event)
        
        # 获取最近24小时的事件
        recent_events = logger.get_recent_events(hours=24)
        self.assertEqual(len(recent_events), 2)
        descriptions = [event["description"] for event in recent_events]
        self.assertIn("当前事件", descriptions)
        self.assertIn("10小时前的事件", descriptions)
        self.assertNotIn("30小时前的事件", descriptions)
        print("EventLogger.get_recent_events 测试通过。")

    def test_get_events_by_keyword(self):
        """测试get_events_by_keyword方法是否能正确搜索事件"""
        logger = EventLogger()
        logger.log_event("今天学习了Python编程")
        logger.log_event("参加了AI技术会议")
        logger.log_event("完成了项目开发")
        
        # 搜索包含"学习"的事件
        learning_events = logger.get_events_by_keyword("学习")
        self.assertEqual(len(learning_events), 1)
        self.assertEqual(learning_events[0]["description"], "今天学习了Python编程")
        
        # 搜索包含"AI"的事件
        ai_events = logger.get_events_by_keyword("AI")
        self.assertEqual(len(ai_events), 1)
        self.assertEqual(ai_events[0]["description"], "参加了AI技术会议")
        
        # 搜索包含"项目"的事件
        project_events = logger.get_events_by_keyword("项目")
        self.assertEqual(len(project_events), 1)
        self.assertEqual(project_events[0]["description"], "完成了项目开发")
        
        # 搜索不存在的关键字
        none_events = logger.get_events_by_keyword("不存在")
        self.assertEqual(len(none_events), 0)
        print("EventLogger.get_events_by_keyword 测试通过。")

if __name__ == '__main__':
    unittest.main()