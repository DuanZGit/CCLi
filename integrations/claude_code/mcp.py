from typing import Dict, Any, List, Optional
import json
import os
from pathlib import Path

class ClaudeCodeMCP:
    """Claude Code MCP（Model Context Protocol）集成类"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化MCP集成
        
        Args:
            config_path: MCP配置文件路径
        """
        if config_path:
            self.config_path = Path(config_path)
        else:
            self.config_path = Path.home() / ".claude" / "mcp.json"
        
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        加载MCP配置
        
        Returns:
            配置字典
        """
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load MCP config: {e}")
                return {}
        else:
            # 创建默认配置
            default_config = {
                "servers": [],
                "tools": [],
                "permissions": {
                    "allow": [],
                    "deny": []
                }
            }
            self._save_config(default_config)
            return default_config
    
    def _save_config(self, config: Dict[str, Any]):
        """
        保存MCP配置
        
        Args:
            config: 配置字典
        """
        try:
            self.config_path.parent.mkdir(exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Failed to save MCP config: {e}")
    
    def add_server(self, name: str, url: str, token: Optional[str] = None) -> bool:
        """
        添加MCP服务器
        
        Args:
            name: 服务器名称
            url: 服务器URL
            token: 认证令牌
            
        Returns:
            是否添加成功
        """
        try:
            server = {
                "name": name,
                "url": url,
                "token": token
            }
            
            # 检查是否已存在同名服务器
            for existing_server in self.config.get("servers", []):
                if existing_server.get("name") == name:
                    print(f"Server '{name}' already exists")
                    return False
            
            # 添加新服务器
            if "servers" not in self.config:
                self.config["servers"] = []
            
            self.config["servers"].append(server)
            self._save_config(self.config)
            return True
        except Exception as e:
            print(f"Failed to add server: {e}")
            return False
    
    def remove_server(self, name: str) -> bool:
        """
        移除MCP服务器
        
        Args:
            name: 服务器名称
            
        Returns:
            是否移除成功
        """
        try:
            servers = self.config.get("servers", [])
            self.config["servers"] = [s for s in servers if s.get("name") != name]
            self._save_config(self.config)
            return True
        except Exception as e:
            print(f"Failed to remove server: {e}")
            return False
    
    def list_servers(self) -> List[Dict[str, Any]]:
        """
        列出所有MCP服务器
        
        Returns:
            服务器列表
        """
        return self.config.get("servers", [])
    
    def add_tool(self, name: str, description: str, command: str) -> bool:
        """
        添加工具
        
        Args:
            name: 工具名称
            description: 工具描述
            command: 工具命令
            
        Returns:
            是否添加成功
        """
        try:
            tool = {
                "name": name,
                "description": description,
                "command": command
            }
            
            # 检查是否已存在同名工具
            for existing_tool in self.config.get("tools", []):
                if existing_tool.get("name") == name:
                    print(f"Tool '{name}' already exists")
                    return False
            
            # 添加新工具
            if "tools" not in self.config:
                self.config["tools"] = []
            
            self.config["tools"].append(tool)
            self._save_config(self.config)
            return True
        except Exception as e:
            print(f"Failed to add tool: {e}")
            return False
    
    def remove_tool(self, name: str) -> bool:
        """
        移除工具
        
        Args:
            name: 工具名称
            
        Returns:
            是否移除成功
        """
        try:
            tools = self.config.get("tools", [])
            self.config["tools"] = [t for t in tools if t.get("name") != name]
            self._save_config(self.config)
            return True
        except Exception as e:
            print(f"Failed to remove tool: {e}")
            return False
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """
        列出所有工具
        
        Returns:
            工具列表
        """
        return self.config.get("tools", [])
    
    def add_permission(self, permission: str, permission_type: str = "allow") -> bool:
        """
        添加权限
        
        Args:
            permission: 权限规则
            permission_type: 权限类型（allow/deny）
            
        Returns:
            是否添加成功
        """
        try:
            if "permissions" not in self.config:
                self.config["permissions"] = {"allow": [], "deny": []}
            
            permission_list = self.config["permissions"].get(permission_type, [])
            if permission not in permission_list:
                permission_list.append(permission)
                self.config["permissions"][permission_type] = permission_list
                self._save_config(self.config)
            return True
        except Exception as e:
            print(f"Failed to add permission: {e}")
            return False
    
    def remove_permission(self, permission: str, permission_type: str = "allow") -> bool:
        """
        移除权限
        
        Args:
            permission: 权限规则
            permission_type: 权限类型（allow/deny）
            
        Returns:
            是否移除成功
        """
        try:
            if "permissions" in self.config:
                permission_list = self.config["permissions"].get(permission_type, [])
                self.config["permissions"][permission_type] = [p for p in permission_list if p != permission]
                self._save_config(self.config)
            return True
        except Exception as e:
            print(f"Failed to remove permission: {e}")
            return False
    
    def get_context(self) -> Dict[str, Any]:
        """
        获取当前上下文信息
        
        Returns:
            上下文信息
        """
        return {
            "servers": self.list_servers(),
            "tools": self.list_tools(),
            "permissions": self.config.get("permissions", {}),
            "config_path": str(self.config_path)
        }
    
    def connect_server(self, server_name: str) -> Dict[str, Any]:
        """
        连接到指定的MCP服务器
        
        Args:
            server_name: 服务器名称
            
        Returns:
            连接结果
        """
        # 这里应该实现实际的服务器连接逻辑
        # 目前返回模拟响应
        for server in self.list_servers():
            if server.get("name") == server_name:
                return {
                    "success": True,
                    "message": f"Connected to server '{server_name}'",
                    "server": server
                }
        
        return {
            "success": False,
            "message": f"Server '{server_name}' not found"
        }
    
    def execute_tool(self, tool_name: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行指定的工具
        
        Args:
            tool_name: 工具名称
            parameters: 工具参数
            
        Returns:
            执行结果
        """
        # 这里应该实现实际的工具执行逻辑
        # 目前返回模拟响应
        for tool in self.list_tools():
            if tool.get("name") == tool_name:
                return {
                    "success": True,
                    "message": f"Executed tool '{tool_name}'",
                    "tool": tool,
                    "parameters": parameters or {}
                }
        
        return {
            "success": False,
            "message": f"Tool '{tool_name}' not found"
        }

# 使用示例
if __name__ == "__main__":
    # 初始化MCP集成
    mcp = ClaudeCodeMCP()
    
    # 显示当前配置
    context = mcp.get_context()
    print("Current MCP Context:")
    print(json.dumps(context, indent=2, ensure_ascii=False))
    
    # 添加示例服务器
    mcp.add_server("github", "https://api.github.com", "gh_token_123")
    mcp.add_server("jira", "https://company.atlassian.net", "jira_token_456")
    
    # 添加示例工具
    mcp.add_tool("git_status", "Show git repository status", "git status")
    mcp.add_tool("npm_test", "Run npm tests", "npm test")
    
    # 添加权限
    mcp.add_permission("Bash(git commit:*)", "allow")
    mcp.add_permission("Bash(rm -rf *)", "deny")
    
    # 显示更新后的配置
    context = mcp.get_context()
    print("\nUpdated MCP Context:")
    print(json.dumps(context, indent=2, ensure_ascii=False))