package com.example.springboot.services;

import com.example.springboot.models.GPSTracker;
import com.example.springboot.repository.GPSTrackerRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.Cache;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

@Slf4j
@Service
public class GPSTrackerService {

    @Autowired
    private GPSTrackerRepository gpsTrackerRepository;

    private final Cache gpsTrackerCache;

    public GPSTrackerService(Cache gpsTrackerCache) {
        this.gpsTrackerCache = gpsTrackerCache;
    }

    @Transactional(readOnly = true)
    public Optional<GPSTracker> findById(Long id) {
        Optional<GPSTracker> o = Optional.ofNullable(gpsTrackerCache.get(id, GPSTracker.class));
        if ( o.isPresent() ) {
            log.info("findById: cache hit, id={}",id);
            return o;
        }

        log.info("findById: cache miss, id={}",id);
        o = gpsTrackerRepository.findById(id);
        if (o.isEmpty())
            return o;

        gpsTrackerCache.put(id, o.get());
        return o;
    }


}
