class EventLogger:
    def __init__(self):
        """
        事件记录系统
        - 自动记录重要事件
        """
        self.events = []

    def log_event(self, event_description):
        """记录一个新事件"""
        from datetime import datetime
        timestamp = datetime.now().isoformat()
        event = {"timestamp": timestamp, "description": event_description}
        self.events.append(event)
        print(f"事件记录：记录新事件 - {event_description}")

    def get_recent_events(self, hours=24):
        """获取最近的事件"""
        from datetime import datetime, timedelta
        now = datetime.now()
        recent_events = []
        for event in self.events:
            event_time = datetime.fromisoformat(event["timestamp"])
            if now - event_time <= timedelta(hours=hours):
                recent_events.append(event)
        return recent_events

    def get_events_by_keyword(self, keyword):
        """根据关键词搜索事件"""
        matching_events = []
        for event in self.events:
            if keyword.lower() in event["description"].lower():
                matching_events.append(event)
        return matching_events