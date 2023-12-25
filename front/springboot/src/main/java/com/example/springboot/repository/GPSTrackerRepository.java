package com.example.springboot.repository;

import com.example.springboot.models.GPSTracker;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface GPSTrackerRepository extends JpaRepository<GPSTracker, Long> {

    @Query(value = "select distinct on (index_tracker_pkey) * from item_tracker order by index_tracker_pkey, datetime desc;", nativeQuery = true)
    List<GPSTracker> findLatestGPSData();
}
