package com.example.springboot.config;

import com.example.springboot.services.NotificationHandler;
import com.example.springboot.services.NotifierService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@Slf4j
public class ListenerConfiguration {

    @Bean
    CommandLineRunner startListener(NotifierService notifier, NotificationHandler handler) {
        return (args) -> {
            log.info("Starting gpsTracker listener thread...");
            Runnable listener = notifier.createNotificationHandler(handler);
            Thread t = new Thread(listener, "gpsTracker-listener");
            t.start();
        };
    }
}