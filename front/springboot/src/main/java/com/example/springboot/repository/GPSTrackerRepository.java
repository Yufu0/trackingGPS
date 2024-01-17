package com.example.springboot.repository;

import com.example.springboot.models.GPSTracker;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface GPSTrackerRepository extends JpaRepository<GPSTracker, String> {

    @Query(value = "select distinct on (name) * from item_tracker order by name, datetime desc;", nativeQuery = true)
    List<GPSTracker> findLatestGPSData();
}
