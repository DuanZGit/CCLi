import unittest
import sys
import os

# 将项目根目录添加到Python路径中，以便导入模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.personal_profile import PersonalProfile

class TestPersonalProfile(unittest.TestCase):

    def test_initialization(self):
        """测试PersonalProfile能否被成功初始化"""
        profile = PersonalProfile(user_id="test_user")
        self.assertEqual(profile.user_id, "test_user")
        self.assertEqual(profile.interests, {})
        self.assertEqual(profile.habits, [])
        self.assertEqual(profile.goals, [])
        print("PersonalProfile初始化测试通过。")

    def test_update_interests(self):
        """测试update_interests方法是否能正确更新兴趣字典"""
        profile = PersonalProfile(user_id="test_user")
        profile.update_interests("python", 5)
        self.assertEqual(profile.interests, {"python": 5})
        profile.update_interests("music", 4)
        self.assertEqual(profile.interests, {"python": 5, "music": 4})
        print("PersonalProfile.update_interests 测试通过。")

    def test_update_habits(self):
        """测试update_habits方法是否能正确更新习惯列表"""
        profile = PersonalProfile(user_id="test_user")
        profile.update_habits("早起")
        self.assertIn("早起", profile.habits)
        profile.update_habits("阅读")
        self.assertIn("阅读", profile.habits)
        # 测试重复添加
        profile.update_habits("早起")
        self.assertEqual(len(profile.habits), 2)
        print("PersonalProfile.update_habits 测试通过。")

    def test_update_goals(self):
        """测试update_goals方法是否能正确更新目标列表"""
        profile = PersonalProfile(user_id="test_user")
        profile.update_goals("学习AI")
        self.assertIn("学习AI", profile.goals)
        profile.update_goals("健身")
        self.assertIn("健身", profile.goals)
        # 测试重复添加
        profile.update_goals("学习AI")
        self.assertEqual(len(profile.goals), 2)
        print("PersonalProfile.update_goals 测试通过。")

    def test_get_profile_summary(self):
        """测试get_profile_summary方法是否能正确返回摘要"""
        profile = PersonalProfile(user_id="test_user")
        profile.update_interests("python", 5)
        profile.update_habits("早起")
        profile.update_goals("学习AI")
        
        summary = profile.get_profile_summary()
        self.assertEqual(summary["user_id"], "test_user")
        self.assertEqual(summary["interests"], {"python": 5})
        self.assertEqual(summary["habits"], ["早起"])
        self.assertEqual(summary["goals"], ["学习AI"])
        print("PersonalProfile.get_profile_summary 测试通过。")

if __name__ == '__main__':
    unittest.main()