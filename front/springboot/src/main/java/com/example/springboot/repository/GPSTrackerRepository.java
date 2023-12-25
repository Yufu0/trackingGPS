package com.example.springboot.repository;

import com.example.springboot.models.GPSTracker;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface GPSTrackerRepository extends JpaRepository<GPSTracker, Long> {}
