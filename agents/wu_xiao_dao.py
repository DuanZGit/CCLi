class WuXiaoDao:
    def __init__(self):
        """
        复盘导师：悟小导
        - 职责：晚间引导反思与成长
        """
        pass

    def start_review(self, event_logger, knowledge_graph):
        """启动晚间复盘"""
        print("\n悟小导：晚上好，让我们一起来回顾一下今天吧。")
        
        # 获取今天的事件
        recent_events = event_logger.get_recent_events(hours=24)
        if recent_events:
            print("悟小导：今天我们记录了以下事件：")
            for event in recent_events:
                print(f"  - {event['description']}")
        else:
            print("悟小导：今天没有记录到特别的事件。")
        
        print("悟小导：今天有什么值得记录的事件吗？(模拟输入：完成了项目重构的初步设计)")
        print("悟小导：从中你学到了什么？(模拟输入：模块化设计的重要性)")
        print("悟小导：有什么可以改进的地方吗？(模拟输入：需要更细致的测试计划)")
        
        # 添加学到的知识到知识图谱
        knowledge_graph.add_node("模块化设计")
        knowledge_graph.add_node("测试计划")
        knowledge_graph.add_edge("模块化设计", "项目重构")
        knowledge_graph.add_edge("测试计划", "项目重构")
        
        print("悟小导：好的，今天的复盘结束，期待明天更好的你！")

    def guide_deep_reflection(self, user_profile, event_logger):
        """引导深度反思"""
        print("\n悟小导：让我们进行更深入的反思...")
        
        # 基于用户兴趣和目标进行反思引导
        if user_profile.interests:
            print("基于您的兴趣点，您今天是否有所收获？")
        if user_profile.goals:
            print("朝着您的目标，今天前进了多少？")
        if user_profile.habits:
            print("您的习惯养成情况如何？")
        
        print("悟小导：反思是成长的阶梯，每天进步一点点！")