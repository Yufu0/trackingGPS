import {AfterViewInit, Component} from '@angular/core';
import * as L from 'leaflet';
import {WebsocketService} from "../services/websocket.service";
import {IPosition} from "../model/IPosition";
import {icons} from "../model/Icons";

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements AfterViewInit {

    private map: any;

    constructor(private webSocketService: WebsocketService) { }

    private initMap(): void {
        this.map = L.map('map', {
            center: [ 0, 0 ],
            zoom: 3
        });

        const tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 18,
            minZoom: 3,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        });

        tiles.addTo(this.map);

        this.webSocketService.openWebSocket();
        this.webSocketService.connect();

        this.webSocketService.listPositions$.subscribe({
            next: (positions: Array<IPosition>) => {
                positions.forEach((position: IPosition) => {
                    if(position.layer === undefined) {
                        const marker = L.marker([position.latitude, position.longitude], {icon: icons[position.color]}).bindPopup(position.name);
                        marker.on('mouseover', function (e) {
                            // @ts-ignore
                            this.openPopup();
                        });
                        marker.on('mouseout', function (e) {
                            // @ts-ignore
                            this.closePopup();
                        });

                        marker.addTo(this.map);

                        const index = this.webSocketService.listPositionsMemory.findIndex((element: IPosition) => element.name === position.name);
                        if(index !== -1) {
                            this.webSocketService.listPositionsMemory[index].layer = marker;
                        }
                    } else {
                       position.layer.setLatLng([position.latitude, position.longitude]);
                    }
                });
            }
        });
    }

    ngAfterViewInit(): void {
        this.initMap();
    }
}
