package com.example.springboot.services;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.postgresql.PGConnection;
import org.postgresql.PGNotification;
import org.springframework.jdbc.core.JdbcTemplate;

import java.sql.Connection;
import java.util.function.Consumer;

@Slf4j
@RequiredArgsConstructor
public class NotifierService {

    private static final String GPS_TRACKER_CHANNEL = "tracker_channel";
    private final JdbcTemplate tpl;

    public Runnable createNotificationHandler(Consumer<PGNotification> consumer) {

        return () ->
            tpl.execute((Connection c) -> {
                log.info("notificationHandler: sending LISTEN command...");
                c.createStatement().execute("LISTEN " + GPS_TRACKER_CHANNEL);

                PGConnection pgconn = c.unwrap(PGConnection.class);

                while(!Thread.currentThread().isInterrupted()) {
                    PGNotification[] nts = pgconn.getNotifications();
                    if (nts == null)
                        continue;

                    for( PGNotification nt : nts)
                        consumer.accept(nt);
                }

                return 0;
            });

    }
}