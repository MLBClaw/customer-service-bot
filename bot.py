"""
智能客服机器人
支持意图识别、知识库问答、多轮对话
"""

import re
import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import os

class CustomerServiceBot:
    """智能客服机器人类"""
    
    def __init__(self, knowledge_base_path: str = "knowledge_base.json"):
        self.sessions: Dict[str, dict] = {}
        self.knowledge_base = self._load_knowledge_base(knowledge_base_path)
        self.intent_patterns = self._init_intent_patterns()
        
    def _load_knowledge_base(self, path: str) -> dict:
        """加载知识库"""
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._default_knowledge_base()
    
    def _default_knowledge_base(self) -> dict:
        """默认知识库"""
        return {
            "greeting": {
                "keywords": ["你好", "您好", "在吗", "有人吗", "hi", "hello"],
                "responses": [
                    "您好！我是智能客服小助手，很高兴为您服务 😊",
                    "您好！请问有什么可以帮您的？",
                    "在的！有什么可以帮您的吗？"
                ]
            },
            "price": {
                "keywords": ["价格", "多少钱", "费用", "收费", "怎么卖", "报价"],
                "responses": [
                    "我们的产品价格根据套餐不同有所差异，基础版 99元/月，专业版 299元/月，企业版请联系销售。",
                    "您好！我们有多种套餐可选，您可以访问价格页面查看详情，或者告诉我您的需求，我帮您推荐合适的方案。"
                ],
                "follow_up": "您是想了解哪个版本的价格呢？"
            },
            "hours": {
                "keywords": ["上班时间", "工作时间", "几点上班", "几点下班", "客服时间"],
                "responses": [
                    "我们的在线客服时间是工作日 9:00-18:00，非工作时间您也可以留言，我们会尽快回复。"
                ]
            },
            "refund": {
                "keywords": ["退款", "退货", "退钱", "怎么退"],
                "responses": [
                    "退款申请可以在个人中心-订单管理提交，审核通过后 3-7 个工作日原路退回。",
                    "如需退款，请提供订单号，我可以帮您查询退款进度。"
                ],
                "follow_up": "请问您的订单号是多少呢？"
            },
            "shipping": {
                "keywords": ["物流", "快递", "发货", "多久到", "送到哪"],
                "responses": [
                    "一般情况下，订单付款后 24 小时内发货，同城 1-2 天到达，异地 3-5 天。",
                    "您可以在订单详情页查看实时物流信息。"
                ],
                "follow_up": "请问您的订单号是多少，我可以帮您查询物流状态。"
            },
            "complaint": {
                "keywords": ["投诉", "不满意", "差评", "举报", "态度差"],
                "responses": [
                    "非常抱歉给您带来不好的体验，我们会认真对待您的反馈。请详细描述一下遇到的问题。",
                    "对于给您造成的不便我们深表歉意，请告诉我具体情况，我们会尽快处理并改进。"
                ],
                "priority": "high"
            },
            "technical": {
                "keywords": ["bug", "报错", "错误", "打不开", "闪退", "问题"],
                "responses": [
                    "遇到技术问题别着急，请描述一下具体情况，比如错误提示是什么，我帮您解决。",
                    "请提供一下错误截图或详细描述，我们的技术团队会尽快帮您处理。"
                ],
                "follow_up": "能否告诉我具体的错误信息？"
            },
            "goodbye": {
                "keywords": ["再见", "拜拜", "谢谢", "bye", "感谢"],
                "responses": [
                    "不客气！有问题随时找我 😊",
                    "感谢您的咨询，祝您生活愉快！",
                    "再见！期待再次为您服务~"
                ]
            },
            "human": {
                "keywords": ["人工", "找客服", "转人工", "真人", "人工服务"],
                "responses": [
                    "正在为您转接人工客服，请稍候...",
                    "好的，我帮您转接人工客服，当前排队人数较多，预计等待 2-3 分钟。"
                ],
                "action": "transfer_to_human"
            },
            "fallback": {
                "responses": [
                    "抱歉，我可能没理解您的意思，能换个说法吗？",
                    "这个问题我还不太清楚，您可以咨询人工客服，或者拨打 400-xxx-xxxx",
                    "您是想了解产品信息、售后服务，还是其他问题呢？"
                ]
            }
        }
    
    def _init_intent_patterns(self) -> Dict[str, re.Pattern]:
        """初始化意图识别模式"""
        patterns = {}
        for intent, data in self.knowledge_base.items():
            if intent != "fallback" and "keywords" in data:
                # 构建正则表达式
                keywords = data["keywords"]
                pattern = "|".join([f"{k}" for k in keywords])
                patterns[intent] = re.compile(pattern, re.IGNORECASE)
        return patterns
    
    def recognize_intent(self, text: str) -> Tuple[str, float]:
        """识别用户意图"""
        text = text.lower().strip()
        
        # 检查是否匹配已知意图
        for intent, pattern in self.intent_patterns.items():
            if pattern.search(text):
                return intent, 0.9
        
        # 模糊匹配
        best_match = None
        best_score = 0
        
        for intent, data in self.knowledge_base.items():
            if intent == "fallback" or "keywords" not in data:
                continue
            for keyword in data["keywords"]:
                # 计算相似度（简单版）
                if keyword in text or text in keyword:
                    score = len(keyword) / max(len(text), len(keyword))
                    if score > best_score:
                        best_score = score
                        best_match = intent
        
        if best_match and best_score > 0.5:
            return best_match, best_score
        
        return "fallback", 0.0
    
    def get_session(self, session_id: str) -> dict:
        """获取或创建会话"""
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "history": [],
                "context": {},
                "state": "idle",
                "created_at": datetime.now().isoformat(),
                "last_active": datetime.now().isoformat()
            }
        return self.sessions[session_id]
    
    def update_context(self, session_id: str, key: str, value: any):
        """更新会话上下文"""
        session = self.get_session(session_id)
        session["context"][key] = value
        session["last_active"] = datetime.now().isoformat()
    
    def get_context(self, session_id: str, key: str) -> any:
        """获取会话上下文"""
        session = self.get_session(session_id)
        return session["context"].get(key)
    
    def reply(self, user_message: str, session_id: str = "default") -> dict:
        """
        生成回复
        
        Returns:
            {
                "message": str,  # 回复内容
                "intent": str,   # 识别的意图
                "confidence": float,  # 置信度
                "suggestions": List[str],  # 建议回复
                "action": str    # 特殊动作（如转人工）
            }
        """
        session = self.get_session(session_id)
        
        # 识别意图
        intent, confidence = self.recognize_intent(user_message)
        
        # 获取知识库数据
        intent_data = self.knowledge_base.get(intent, self.knowledge_base["fallback"])
        
        # 选择回复
        responses = intent_data.get("responses", ["抱歉，我不太明白您的意思。"])
        reply_text = random.choice(responses)
        
        # 构建回复对象
        result = {
            "message": reply_text,
            "intent": intent,
            "confidence": confidence,
            "suggestions": self._get_suggestions(intent, session),
            "action": intent_data.get("action")
        }
        
        # 添加追问（如果有）
        follow_up = intent_data.get("follow_up")
        if follow_up and not session["context"].get(f"asked_{intent}"):
            result["message"] += f"\n\n{follow_up}"
            session["context"][f"asked_{intent}"] = True
        
        # 更新会话历史
        session["history"].append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        session["history"].append({
            "role": "assistant",
            "content": result["message"],
            "intent": intent,
            "timestamp": datetime.now().isoformat()
        })
        
        # 限制历史长度
        if len(session["history"]) > 20:
            session["history"] = session["history"][-20:]
        
        session["last_active"] = datetime.now().isoformat()
        
        return result
    
    def _get_suggestions(self, intent: str, session: dict) -> List[str]:
        """获取建议回复"""
        suggestions_map = {
            "greeting": ["产品价格", "工作时间", "人工客服"],
            "price": ["基础版", "专业版", "企业版"],
            "refund": ["查询订单", "退款进度", "联系人工"],
            "shipping": ["查询物流", "修改地址", "联系快递"],
            "technical": ["提交工单", "联系技术", "查看帮助文档"],
            "fallback": ["产品价格", "工作时间", "人工客服"]
        }
        return suggestions_map.get(intent, ["人工客服"])
    
    def clear_session(self, session_id: str):
        """清空会话"""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        total_sessions = len(self.sessions)
        active_sessions = sum(
            1 for s in self.sessions.values()
            if (datetime.now() - datetime.fromisoformat(s["last_active"])).days < 1
        )
        return {
            "total_sessions": total_sessions,
            "active_sessions": active_sessions
        }


# 简单的命令行测试
if __name__ == "__main__":
    bot = CustomerServiceBot()
    print("🤖 智能客服机器人测试模式")
    print("输入 'quit' 退出\n")
    
    while True:
        user_input = input("👤 用户: ").strip()
        if user_input.lower() in ["quit", "exit", "退出"]:
            break
        
        result = bot.reply(user_input)
        print(f"🤖 机器人: {result['message']}")
        print(f"   [意图: {result['intent']}, 置信度: {result['confidence']:.2f}]")
        if result['suggestions']:
            print(f"   [建议: {', '.join(result['suggestions'])}]")
        print()
