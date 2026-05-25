package com.kopo.chatbot.service;

import com.kopo.chatbot.dao.ChatDAO;
import com.kopo.chatbot.dto.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.List;

@Service
public class ChatServiceImpl implements ChatService {

    private static final String FASTAPI_URL = "http://localhost:8000/query";

    @Autowired private RestTemplate restTemplate;
    @Autowired private ChatDAO      chatDAO;

    @Override
    public ChatResponse ask(String question, String sessionId) {
        // 1. 사용자 질문 저장
        ChatMessage userMsg = new ChatMessage();
        userMsg.setSessionId(sessionId);
        userMsg.setRole("user");
        userMsg.setContent(question);
        chatDAO.insertMessage(userMsg);

        // 2. FastAPI /query 호출
        ChatResponse response = restTemplate.postForObject(
            FASTAPI_URL,
            new QueryRequest(question),
            ChatResponse.class
        );

        // 3. 챗봇 답변 저장
        ChatMessage assistantMsg = new ChatMessage();
        assistantMsg.setSessionId(sessionId);
        assistantMsg.setRole("assistant");
        assistantMsg.setContent(response.getAnswer());
        chatDAO.insertMessage(assistantMsg);

        return response;
    }

    @Override
    public List<ChatMessage> getHistory(String sessionId) {
        return chatDAO.selectHistory(sessionId);
    }
}
