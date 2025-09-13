#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CCLi - Claude Code CLI
个人助理AI系统
"""

import os
import sys
import argparse
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.personal_profile import PersonalProfile
from core.event_logger import EventLogger
from core.knowledge_graph import KnowledgeGraph
from core.model_router import ModelRouter
from agents.xun_xiao_zhi import XunXiaoZhi
from agents.shi_xiao_guan import ShiXiaoGuan
from agents.wu_xiao_dao import WuXiaoDao

def send_to_work_group(message):
    """模拟发送消息到工作群，将内容写入文件"""
    report_file_path = "daily_report.txt"
    with open(report_file_path, "w", encoding="utf-8") as f:
        f.write(message)
    print(f"\n--- 消息已写入文件: {report_file_path} ---")

def main():
    """
    主函数，演示CCLi系统的交互流程
    """
    print("--- CCLi系统开始一天的工作 ---")

    # 初始化核心组件和Agent
    user_profile = PersonalProfile(user_id="001")
    # 预设一个偏好，以更好地演示主动推荐
    user_profile.update_interests('tech', 5)
    user_profile.update_interests('finance', 3)
    user_profile.update_habits('早起')
    user_profile.update_goals('学习AI技术')
    print(f"(后台：用户的初始偏好为 {user_profile.interests})")

    event_logger = EventLogger()
    knowledge_graph = KnowledgeGraph()
    model_router = ModelRouter()

    # 演示模型路由功能
    print("\n--- 模型路由功能演示 ---")
    response = model_router.send_request("think", "请解释人工智能的概念")
    print(f"AI响应: {response}")
    
    response = model_router.send_request("default", "请列出5个Python库")
    print(f"默认响应: {response}")

    news_agent = XunXiaoZhi()
    schedule_agent = ShiXiaoGuan()
    review_agent = WuXiaoDao()

    # =====================================================
    # --- 早晨协作流程 ---
    # =====================================================
    print("\n--- 早晨协作流程开始 ---")
    # 1. 讯小智推送早安新闻
    news_agent.recommend_and_interact(user_profile)

    # 2. 时小管询问并制定日程
    schedule = schedule_agent.ask_for_schedule()
    morning_report = schedule_agent.generate_report(schedule)
    
    # 根据用户画像提供日程优化建议
    suggestions = schedule_agent.suggest_schedule_optimization(schedule, user_profile)
    if suggestions:
        print("时小管：我有一些建议供您参考：")
        for suggestion in suggestions:
            print(f"  - {suggestion}")

    # 3. 发送早报到工作群
    send_to_work_group(morning_report)
    print("--- 早晨协作流程结束 ---")

    # =====================================================
    # --- 用户对最后看到的新闻进行反馈 ---
    # =====================================================
    # 在上面的交互中，用户最后看到的是 'social' 类新闻
    print("\n--- 用户对最后看到的新闻类别进行评分 ---")
    news_agent.update_feedback(user_profile, 4)  # 给高分

    # 记录一些事件
    event_logger.log_event("完成了项目重构的初步设计")
    event_logger.log_event("学习了新的AI技术")
    event_logger.log_event("参加了团队会议")

    # 添加一些知识到知识图谱
    knowledge_graph.add_edge("AI技术", "项目重构")
    knowledge_graph.add_edge("模块化设计", "项目重构")
    knowledge_graph.add_edge("学习", "技能提升")

    # =====================================================
    # --- 晚间协作流程 ---
    # =====================================================
    print("\n--- 晚间协作流程开始 ---")
    review_agent.start_review(event_logger, knowledge_graph)
    review_agent.guide_deep_reflection(user_profile, event_logger)
    
    # 显示用户画像摘要
    print("\n--- 用户画像摘要 ---")
    profile_summary = user_profile.get_profile_summary()
    print(f"用户ID: {profile_summary['user_id']}")
    print(f"兴趣点: {profile_summary['interests']}")
    print(f"习惯: {profile_summary['habits']}")
    print(f"目标: {profile_summary['goals']}")
    
    # 显示知识图谱摘要
    print("\n--- 知识图谱摘要 ---")
    graph_summary = knowledge_graph.get_graph_summary()
    for node, info in graph_summary.items():
        print(f"{node}: {info['connections_count']} 个关联节点")
    
    print("\n--- CCLi系统结束一天的工作 ---")

if __name__ == "__main__":
    main()