package com.example.springboot.config;

import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.cache.Cache;
import org.springframework.cache.CacheManager;
import org.springframework.cache.concurrent.ConcurrentMapCache;
import org.springframework.cache.support.SimpleCacheManager;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
public class CacheConfiguration {

    @Bean
    Cache gpsTrackerCache(CacheManager cm) {
        return cm.getCache("gpsTracker");
    }

    @Bean
    @ConditionalOnMissingBean
    CacheManager defaultCacheManager() {
        SimpleCacheManager cm = new SimpleCacheManager();
        Cache cache = new ConcurrentMapCache("gpsTracker",false);
        cm.setCaches(List.of(cache));
        return cm;
    }
}