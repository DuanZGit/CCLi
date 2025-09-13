class ShiXiaoGuan:
    def __init__(self):
        """
        日程规划师：时小管
        - 职责：日程管理与团队协作
        """
        pass

    def ask_for_schedule(self):
        """询问今日安排"""
        print("时小管：早上好！您今天有什么安排？(模拟输入：上午开会，下午写代码)")
        # Simulate user input for now
        return "上午开会，下午写代码"

    def generate_report(self, schedule):
        """生成早报"""
        print("时小管：正在生成您的今日早报...")
        report_content = f"【时小管早报】\n今日日程：{schedule}\n\n祝您工作顺利！"
        return report_content

    def suggest_schedule_optimization(self, schedule, user_profile):
        """根据用户画像建议日程优化"""
        print("时小管：根据您的习惯和目标，我有一些建议...")
        # 这里可以基于用户画像提供个性化建议
        suggestions = []
        if 'tech' in user_profile.interests:
            suggestions.append("建议安排专门的技术学习时间")
        if 'coding' in user_profile.goals:
            suggestions.append("建议将写代码安排在精力最充沛的时段")
        return suggestions