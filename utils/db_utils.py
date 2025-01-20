import sqlite3
from typing import Optional, List, Dict, Any

class SQLiteDB:
    """SQLite数据库连接工具类"""
    
    def __init__(self, db_path: str):
        """初始化数据库连接
        
        Args:
            db_path (str): 数据库文件路径
        """
        self.db_path = db_path
        self.connection = None
        
    def __enter__(self):
        """进入上下文时自动连接数据库"""
        self.connect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文时自动关闭连接"""
        self.close()
        
    def connect(self):
        """连接数据库"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        
    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection = None
            
    def execute(self, query: str, params: Optional[tuple] = None) -> sqlite3.Cursor:
        """执行SQL查询
        
        Args:
            query (str): SQL查询语句
            params (Optional[tuple]): 查询参数
            
        Returns:
            sqlite3.Cursor: 查询结果游标
        """
        if not self.connection:
            self.connect()
        return self.connection.execute(query, params or ())
        
    def fetch_all(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """执行查询并返回所有结果
        
        Args:
            query (str): SQL查询语句
            params (Optional[tuple]): 查询参数
            
        Returns:
            List[Dict[str, Any]]: 查询结果列表
        """
        cursor = self.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
        
    def fetch_one(self, query: str, params: Optional[tuple] = None) -> Optional[Dict[str, Any]]:
        """执行查询并返回单条结果
        
        Args:
            query (str): SQL查询语句
            params (Optional[tuple]): 查询参数
            
        Returns:
            Optional[Dict[str, Any]]: 查询结果，如果没有结果返回None
        """
        cursor = self.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None
        
    def commit(self):
        """提交事务"""
        if self.connection:
            self.connection.commit()
            
    def rollback(self):
        """回滚事务"""
        if self.connection:
            self.connection.rollback()
