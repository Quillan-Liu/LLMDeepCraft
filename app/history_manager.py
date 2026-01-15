import datetime
import json
import os
from collections import deque
from typing import Optional, Dict, Tuple, Any, List

DEFAULT_HISTORY_FILE_PATH = 'app/history/history.jsonl'

class HistoryManager:
  """
  管理历史对话的类
  """

  def __init__(self, history_file_path: str = DEFAULT_HISTORY_FILE_PATH):
    self.history_file_path = history_file_path
    os.makedirs(os.path.dirname(history_file_path), exist_ok=True)


  def save_history_record(self, history_message: dict) -> bool:
    """
    将最近的用户提示词与 llm 的回答储存进 .jsonl 文档
    :param history_message: 最新的用户提示词与设计记录
    :return:保存是否成功的 bool 值
    """
    try:
      record_dict = {
        "time_stamp": datetime.now().isoformat(),
        "message": history_message
      }

      with open(self.history_file_path, 'a', encoding="utf-8") as file:
        new_line = json.dumps(record_dict, ensure_ascii=False, indent=2)
        file.write(new_line + "\n")

      return True


    except (FileNotFoundError, PermissionError) as e:
      print(f"文件访问错误: {str(e)}。路径: {self.history_file_path}")
      return False

    except OSError as e:  # 捕获所有操作系统相关错误
      print(f"系统错误: {str(e)}。错误号: {e.errno}")
      return False

    except Exception as e:
      print(f"保存历史记录时发生未知错误: {type(e).__name__} - {str(e)}")
      return False


  def load_history_record(self) -> Optional[List[Dict]]:
    """
    获取最近的十个提示词与 llm 回答的历史记录
    :return: 保存最近的十个提示词与 llm 回答的历史记录的字典列表
    """
    try:
      if not os.path.exists(self.history_file_path):
        return None

      with open(self.history_file_path, 'r', encoding="utf-8") as file:
        last_lines = deque(file, maxlen=10)
        history_str_list = list(last_lines)

        if not history_str_list:
           return None

        history_list = self.__history_list_converter(history_str_list)

        return history_list

    except (FileNotFoundError, ValueError) as e:
      print(f"加载历史记录失败: {str(e)}")
      return None

    except Exception as e:
      print(f"未知错误: {str(e)}")
      return None


  def get_lastest_history(self) -> Optional[Dict]:
    """
    获取最近的提示词与 llm 回答的历史记录
    :return: 保存最近的提示词与 llm 回答的历史记录的字典列表
    """
    return self.load_history_record()[-1]


  def has_history(self) -> bool:
    """
    检测对话是否已经有历史记录
    :return: 已经有则返回 True， 否则返回 False
    """
    latest = self.get_lastest_history()
    return latest is not None


  def __history_list_converter(self,history_str_list: List[str]) \
      -> Optional[List[Dict[str, Any]]]:
    """
    将 json 字符串列表转为 dict 列表
    :param history_str_list: 由历史记录 .jsonl 文件加载的 json 字符串列表
    :return: 储存历史记录的 dict 列表
    """
    history_dict_list = []

    for history_str in history_str_list:
      stripped = history_str.strip()

      if not stripped:
        continue

      try:
        history_dict = json.loads(stripped)

        if not isinstance(history_dict, dict):
          raise ValueError("记录格式错误，应为字典类型")

        history_dict_list.append(history_dict)


      except json.JSONDecodeError as e:
        print(f"忽略无效JSON行: '{stripped}'。错误: {str(e)}")

      except ValueError as e:
        print(f"忽略无效记录格式: '{stripped}'。错误: {str(e)}")

    return history_dict_list

# 全局实例
history_manager = HistoryManager()





