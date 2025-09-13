class PersonalProfile:
    def __init__(self, user_id):
        """
        个人画像系统
        - 整合兴趣、习惯、目标
        """
        self.user_id = user_id
        self.interests = {}
        self.habits = []
        self.goals = []

    def update_interests(self, topic, score):
        """更新兴趣画像"""
        print(f"个人画像：更新兴趣点 {topic}，评分为 {score}")
        self.interests[topic] = score

    def update_habits(self, habit):
        """更新习惯记录"""
        if habit not in self.habits:
            self.habits.append(habit)
            print(f"个人画像：新增习惯 {habit}")

    def update_goals(self, goal):
        """更新目标记录"""
        if goal not in self.goals:
            self.goals.append(goal)
            print(f"个人画像：新增目标 {goal}")

    def get_profile_summary(self):
        """获取个人画像摘要"""
        return {
            "user_id": self.user_id,
            "interests": self.interests,
            "habits": self.habits,
            "goals": self.goals
        }