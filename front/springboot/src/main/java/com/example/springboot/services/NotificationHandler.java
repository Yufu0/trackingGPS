package com.example.springboot.services;


import com.example.springboot.models.GPSTracker;
import com.example.springboot.repository.GPSTrackerRepository;
import com.example.springboot.websocket.GPSWebSocketHandler;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.postgresql.PGNotification;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.TextMessage;

import java.io.IOException;
import java.util.Optional;
import java.util.function.Consumer;

@Slf4j
@Component
@RequiredArgsConstructor
public class NotificationHandler implements Consumer<PGNotification> {

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Autowired
    private final GPSTrackerRepository gpsTrackerRepository;

    private final GPSTrackerService gpsTrackerService;
    @Override
    public void accept(PGNotification t) {
        log.info("Notification received: pid={}, name={}, param={}",t.getPID(),t.getName(),t.getParameter());
        Optional<GPSTracker> gpsTrackerOptional = gpsTrackerService.findById(Long.valueOf(t.getParameter()));
        gpsTrackerOptional.ifPresent(gpsTracker -> {
            GPSWebSocketHandler.getSessions().forEach(session -> {
                try {
                    session.sendMessage(new TextMessage(objectMapper.writeValueAsString(gpsTracker)));
                } catch (IOException e) {
                    e.printStackTrace();
                }
            });
        });
    }
}
