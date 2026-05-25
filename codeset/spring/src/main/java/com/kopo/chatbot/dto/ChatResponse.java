package com.kopo.chatbot.dto;

import java.util.List;
import java.util.Map;

public class ChatResponse {
    private String answer;
    private List<Map<String, String>> sources;

    public String getAnswer()                    { return answer; }
    public List<Map<String, String>> getSources() { return sources; }

    public void setAnswer(String answer)                       { this.answer = answer; }
    public void setSources(List<Map<String, String>> sources)  { this.sources = sources; }
}
