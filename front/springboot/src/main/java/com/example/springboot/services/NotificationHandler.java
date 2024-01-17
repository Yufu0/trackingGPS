package com.example.springboot.services;


import com.example.springboot.repository.GPSTrackerRepository;
import com.example.springboot.websocket.GPSWebSocketHandler;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.postgresql.PGNotification;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.TextMessage;

import java.io.IOException;
import java.util.Arrays;
import java.util.function.Consumer;

@Slf4j
@Component
@RequiredArgsConstructor
public class NotificationHandler implements Consumer<PGNotification[]> {

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Autowired
    private final GPSTrackerRepository gpsTrackerRepository;
    @Override
    public void accept(PGNotification[] notifications) {
        try {
            log.info("Notification received {}", notifications.length);
            String s = objectMapper.writeValueAsString(gpsTrackerRepository.findAllById(Arrays.stream(notifications).map(PGNotification::getParameter).toList()));
            GPSWebSocketHandler.getSessions().forEach(session -> {
                try {
                    session.sendMessage(new TextMessage(s));
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            });
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }
}
