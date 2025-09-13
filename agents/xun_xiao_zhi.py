from core.personal_profile import PersonalProfile
import random
import re

class XunXiaoZhi:
    def __init__(self):
        """
        新闻播报员：讯小智
        """
        self.last_shown_category = None
        self.CATEGORY_MAP = {
            'social': '社交',
            'tech': '科技',
            'news': '新闻',
            'finance': '财经'
        }

    def _display_news(self, category: str, news_data: dict):
        """
        显示新闻
        """
        print(f"\n--- 为您带来 '{self.CATEGORY_MAP.get(category, category)}' 类别的热点 ---")
        if not news_data:
            print("  (该类别暂无新闻)")
        else:
            for platform, trends in news_data.items():
                print(f"\n--- {platform} ---")
                if not trends:
                    print("  (该平台暂无热点)")
                else:
                    for i, trend in enumerate(trends, 1):
                        cleaned_trend = re.sub(r'\s+', ' ', trend).strip()
                        print(f"{i}. {cleaned_trend}")
                print("")  # Add a blank line for separation

    def recommend_and_interact(self, user_profile: PersonalProfile):
        """
        核心交互流程：先根据记忆主动推荐，再提供快捷选项探索其他内容。
        """
        interests = user_profile.interests
        if not interests:
            primary_category = 'news'
            print(f"讯小智：早上好！先为您带来今日的综合新闻速递。")
        else:
            primary_category = max(interests, key=interests.get)
            print(f"讯小智：早上好！已根据您的偏好，为您准备了最感兴趣的 '{primary_category}' 类新闻。")
        
        # 模拟获取新闻数据
        news_data = self._get_news_data(primary_category)
        self._display_news(primary_category, news_data)
        self.last_shown_category = primary_category

        print("\n还需要看点别的吗？")
        available_categories = list(self.CATEGORY_MAP.keys())
        other_categories = [cat for cat in available_categories if cat != primary_category]
        
        options = {i + 1: cat for i, cat in enumerate(other_categories)}
        for i, cat in options.items():
            print(f"  {i}. {self.CATEGORY_MAP[cat]}")
        print("  0. 不用了，谢谢")

        # 模拟用户输入
        user_choice = 1 
        print(f"\n(模拟用户输入: {user_choice})\n")

        if user_choice in options:
            chosen_category = options[user_choice]
            news_data = self._get_news_data(chosen_category)
            self._display_news(chosen_category, news_data)
            self.last_shown_category = chosen_category
        else:
            print("讯小智：好的，祝您有愉快的一天！")

    def _get_news_data(self, category: str) -> dict:
        """
        模拟获取新闻数据
        """
        # 这里应该集成真实的新闻源API
        sample_news = {
            'social': {
                '微博': ['微博热搜第一：科技新闻', '明星八卦事件引发热议', '社会热点话题讨论'],
                '知乎': ['如何学习AI技术', '职业发展讨论', '科技趋势分析']
            },
            'tech': {
                'B站': ['最新AI技术演示', '编程教程分享', '科技产品评测'],
                '技术博客': ['Python新特性介绍', '机器学习算法优化', '云计算发展趋势']
            },
            'news': {
                '今日头条': ['国内重要政策发布', '国际时事新闻', '经济形势分析'],
                '澎湃新闻': ['社会热点事件', '环境保护新闻', '教育改革动态']
            },
            'finance': {
                '华尔街见闻': ['股市行情分析', '投资策略分享', '经济数据解读'],
                '财联社': ['行业动态', '公司财报', '金融政策']
            }
        }
        return sample_news.get(category, {})

    def update_feedback(self, user_profile: PersonalProfile, score: int):
        """
        让用户可以对最后一次看的新闻类别进行评分。
        """
        if self.last_shown_category is None:
            print("讯小智：似乎还没有为您展示过新闻，无法评分。")
            return

        category_to_rate = self.last_shown_category
        print(f"讯小智：收到您对 '{category_to_rate}' 类新闻的评分: {score}分。")
        user_profile.update_interests(category_to_rate, score)
        print(f"(用户画像已更新: {user_profile.interests})\n")
