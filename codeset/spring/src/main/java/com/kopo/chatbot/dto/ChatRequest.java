package com.kopo.chatbot.dto;

public class ChatRequest {
    private String question;
    private String sessionId;

    public String getQuestion()  { return question; }
    public String getSessionId() { return sessionId; }

    public void setQuestion(String q)  { this.question = q; }
    public void setSessionId(String s) { this.sessionId = s; }
}
