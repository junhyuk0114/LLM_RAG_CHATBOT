package com.kopo.chatbot.dto;

public class QueryRequest {
    private String question;

    public QueryRequest() {}
    public QueryRequest(String question) { this.question = question; }

    public String getQuestion()          { return question; }
    public void setQuestion(String q)    { this.question = q; }
}
