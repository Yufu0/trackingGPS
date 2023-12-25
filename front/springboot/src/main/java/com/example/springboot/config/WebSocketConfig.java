package com.example.springboot.config;


import com.example.springboot.repository.GPSTrackerRepository;
import com.example.springboot.websocket.GPSWebSocketHandler;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.socket.WebSocketHandler;
import org.springframework.web.socket.config.annotation.EnableWebSocket;
import org.springframework.web.socket.config.annotation.WebSocketConfigurer;
import org.springframework.web.socket.config.annotation.WebSocketHandlerRegistry;

@Configuration
@EnableWebSocket
public class WebSocketConfig implements WebSocketConfigurer {

    @Autowired
    private GPSTrackerRepository gpsTrackerRepository;

    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
        registry.addHandler(new GPSWebSocketHandler(gpsTrackerRepository), "/gps").setAllowedOrigins("*");
    }

    @Bean
    public WebSocketHandler gpsWebSocketHandler() {
        return new GPSWebSocketHandler(gpsTrackerRepository);
    }
}