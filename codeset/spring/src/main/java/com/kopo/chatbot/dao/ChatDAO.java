package com.kopo.chatbot.dao;

import com.kopo.chatbot.dto.ChatMessage;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.BeanPropertyRowMapper;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import javax.sql.DataSource;
import java.util.List;

@Repository
public class ChatDAO {

    private JdbcTemplate jdbcTemplate;

    @Autowired
    public void setDataSource(DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
    }

    public void insertMessage(ChatMessage msg) {
        String sql = "INSERT INTO chat_history (session_id, role, content) VALUES (?, ?, ?)";
        jdbcTemplate.update(sql, msg.getSessionId(), msg.getRole(), msg.getContent());
    }

    public List<ChatMessage> selectHistory(String sessionId) {
        String sql = "SELECT chat_id, session_id, role, content, created_at "
                   + "FROM chat_history WHERE session_id = ? ORDER BY chat_id ASC";
        return jdbcTemplate.query(sql, new BeanPropertyRowMapper<>(ChatMessage.class), sessionId);
    }
}
