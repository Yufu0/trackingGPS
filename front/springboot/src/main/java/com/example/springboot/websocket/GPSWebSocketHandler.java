package com.example.springboot.websocket;

import com.example.springboot.repository.GPSTrackerRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.Getter;
import lombok.NonNull;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import java.io.IOException;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

public class GPSWebSocketHandler extends TextWebSocketHandler {

    private final ObjectMapper objectMapper = new ObjectMapper();
    @Getter
    private static final List<WebSocketSession> sessions = new CopyOnWriteArrayList<>();

    private final GPSTrackerRepository gpsTrackerRepository;
    public GPSWebSocketHandler(GPSTrackerRepository gpsTrackerRepository) {
        this.gpsTrackerRepository = gpsTrackerRepository;
    }

    @Override
    public void afterConnectionEstablished(@NonNull WebSocketSession session) {
        System.out.println("Connection established");
        sessions.add(session);

        try {
            session.sendMessage(new TextMessage(objectMapper.writeValueAsString(gpsTrackerRepository.findAll())));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void afterConnectionClosed(@NonNull WebSocketSession session, CloseStatus status) {
        System.out.println("Connection closed " + status.getReason());
        sessions.remove(session);
    }
}
