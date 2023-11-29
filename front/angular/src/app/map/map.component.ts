import { Component, AfterViewInit } from '@angular/core';
import * as L from 'leaflet';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements AfterViewInit {

    private map: any;

    constructor() { }

    private initMap(): void {
        this.map = L.map('map', {
            center: [ 39.8282, -98.5795 ],
            zoom: 3
        });

        const tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 18,
            minZoom: 3,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        });

        tiles.addTo(this.map);

        for(let i = 0; i < 10; i++) {
            L.marker([Math.random() * 180 - 90, Math.random() * 360 - 180]).addTo(this.map).bindPopup('A pretty CSS3 popup.<br> Easily customizable.');
        }
    }




    ngAfterViewInit(): void {
        this.initMap();
    }
}
