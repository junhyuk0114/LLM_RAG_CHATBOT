package com.kopo.chatbot.controller;

import com.kopo.chatbot.dto.ChatMessage;
import com.kopo.chatbot.dto.ChatRequest;
import com.kopo.chatbot.dto.ChatResponse;
import com.kopo.chatbot.service.ChatService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class ChatController {

    @Autowired
    private ChatService chatService;

    @PostMapping("/chat")
    public ResponseEntity<ChatResponse> chat(@RequestBody ChatRequest req) {
        ChatResponse response = chatService.ask(req.getQuestion(), req.getSessionId());
        return ResponseEntity.ok(response);
    }

    @GetMapping("/chat/history")
    public ResponseEntity<List<ChatMessage>> history(@RequestParam String sessionId) {
        return ResponseEntity.ok(chatService.getHistory(sessionId));
    }
}
