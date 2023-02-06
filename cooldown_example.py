class Bot(KikClientCallback):
    def __init__(self):
        self.client = KikClient(self, username, password)
        self.last_response_time = 0
  
  
  
  def on_group_message_received(self, chat_message: chatting.IncomingGroupChatMessage):
        current_time = time.time()
        time_since_last_response = current_time - self.last_response_time
        if time_since_last_response >= 10:
            self.client.send_chat_message(chat_message.group_jid, "hello")
            self.last_response_time = current_time
