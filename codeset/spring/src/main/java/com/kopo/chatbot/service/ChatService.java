package com.kopo.chatbot.service;

import com.kopo.chatbot.dto.ChatMessage;
import com.kopo.chatbot.dto.ChatResponse;
import java.util.List;

public interface ChatService {
    ChatResponse ask(String question, String sessionId);
    List<ChatMessage> getHistory(String sessionId);
}
