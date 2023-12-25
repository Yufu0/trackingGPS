package com.example.springboot.websocket;

import com.example.springboot.models.GPSTracker;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import java.util.ArrayList;
import java.util.List;

public class GPSWebSocketHandler extends TextWebSocketHandler {

    private final ObjectMapper objectMapper = new ObjectMapper();
    private final List<String> sessions = new ArrayList<>();

    private final List<String> fakeGPSNames = List.of("Alice", "Bob", "Charlie", "Dave", "Eve");
    @Override
    public void afterConnectionEstablished(WebSocketSession session) {
        System.out.println("Connection established");
        sessions.add(session.getId());
        while (sessions.contains(session.getId())) {
            try {
                session.sendMessage(new TextMessage(objectMapper.writeValueAsString(fakeGPSData())));
                Thread.sleep(1000);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) {
        System.out.println("Connection closed " + status.getReason());
        sessions.remove(session.getId());
    }

    private GPSTracker fakeGPSData() {
        GPSTracker gpsTracker = new GPSTracker();
        gpsTracker.setId((long) (Math.random() * 100000));
        gpsTracker.setName(fakeGPSNames.get((int) (Math.random() * fakeGPSNames.size())));
        gpsTracker.setLatitude(Math.random() * 50);
        gpsTracker.setLongitude(Math.random() * 50);
        gpsTracker.setDatetime(new java.sql.Timestamp(System.currentTimeMillis()));
        return gpsTracker;
    }
}
