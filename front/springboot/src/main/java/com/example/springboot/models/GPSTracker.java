package com.example.springboot.models;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.sql.Timestamp;

@Entity
@Table(name = "item_tracker")
@Getter
@Setter
public class GPSTracker {

    @Id
    private Long id;

    @Column(name = "index_tracker_pkey")
    private String name;

    @Column(name = "latitude")
    private Double latitude;

    @Column(name = "longitude")
    private Double longitude;

    @Column(name = "datetime")
    private Timestamp datetime;
}
