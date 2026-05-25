package com.kopo.chatbot.dto;

public class ChatMessage {
    private int    chatId;
    private String sessionId;
    private String role;
    private String content;
    private String createdAt;

    public int    getChatId()    { return chatId; }
    public String getSessionId() { return sessionId; }
    public String getRole()      { return role; }
    public String getContent()   { return content; }
    public String getCreatedAt() { return createdAt; }

    public void setChatId(int chatId)       { this.chatId = chatId; }
    public void setSessionId(String s)      { this.sessionId = s; }
    public void setRole(String role)        { this.role = role; }
    public void setContent(String content)  { this.content = content; }
    public void setCreatedAt(String s)      { this.createdAt = s; }
}
