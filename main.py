#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CCLi - Claude Code CLI
智能模型路由与中文UI界面的AI系统
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

def main():
    """
    主函数，演示CCLi系统的交互流程
    """
    print("--- CCLi系统启动 ---")

    # 初始化核心组件
    user_profile = PersonalProfile(user_id="001")
    # 设置用户偏好
    user_profile.update_interests('tech', 5)
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

    # 记录一些事件
    event_logger.log_event("完成了项目重构的初步设计")
    event_logger.log_event("学习了新的AI技术")
    event_logger.log_event("参加了团队会议")

    # 添加一些知识到知识图谱
    knowledge_graph.add_edge("AI技术", "项目重构")
    knowledge_graph.add_edge("模块化设计", "项目重构")
    knowledge_graph.add_edge("学习", "技能提升")
    
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
    
    print("\n--- CCLi系统演示完成 ---")

if __name__ == "__main__":
    main()