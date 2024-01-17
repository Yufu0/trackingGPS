package com.example.springboot.models;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.sql.Timestamp;

@Entity
@Table(name = "item_tracker")
@Getter
@Setter
@ToString
public class GPSTracker {

    @Id
    private String id;

    @Column(name = "name")
    private String name;

    @Column(name = "latitude")
    private Double latitude;

    @Column(name = "longitude")
    private Double longitude;

    @Column(name = "datetime")
    private Timestamp datetime;
}
