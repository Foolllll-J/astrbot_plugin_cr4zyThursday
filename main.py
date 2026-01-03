import urllib.request
from astrbot import logger
from astrbot.api.star import Context, Star, register
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.event.filter import event_message_type, EventMessageType

@register(
    "cr4zythursday",
    "w33d",
    "一个疯狂星期四插件",
    "1.1.0",
    "https://github.com/Last-emo-boy/astrbot_plugin_cr4zyThursday"
)
class CrazyThursdayPlugin(Star):
    def __init__(self, context: Context, config: dict):
        """
        读取后台管理面板中用户配置的关键词数组(默认 ["疯狂星期四"])。
        只要消息包含任意一个关键词，都将触发访问 vme.im 并返回文本。
        """
        super().__init__(context)
        self.config = config

        # 从 config 中获取配置，如果没有用户配置，则使用默认值
        self.group_whitelist = self.config.get("group_whitelist", [])
        self.group_whitelist = [int(gid) for gid in self.group_whitelist]
        self.keywords = self.config.get("keywords", ["疯狂星期四"])
        logger.debug(f"已加载关键词列表: {self.keywords}")

    @event_message_type(EventMessageType.ALL)
    async def on_message(self, event: AstrMessageEvent) -> MessageEventResult:
        """
        当消息中包含配置的任意关键词时，访问 https://vme.im/api?format=text 并返回响应。
        """
        # 群组白名单检查
        group_id_str = event.get_group_id()
        if group_id_str:  # 如果是群聊
            group_id = int(group_id_str)
            if self.group_whitelist and group_id not in self.group_whitelist:
                return
        # 如果是私聊，则不检查白名单

        msg_obj = event.message_obj
        text = msg_obj.message_str or ""

        # 判断消息中是否包含任意关键词，且不是唤醒对话
        if any(kw in text for kw in self.keywords) and not event.is_at_or_wake_command:
            try:
                # with urllib.request.urlopen("https://vme.im/api?format=text") as resp:  
                with urllib.request.urlopen("https://vme.im/api/random?format=text") as resp:
                    result_bytes = resp.read()
                    result_text = result_bytes.decode("utf-8", errors="replace")
            except Exception as e:
                result_text = f"获取信息失败: {e}"

            yield event.plain_result(result_text)
