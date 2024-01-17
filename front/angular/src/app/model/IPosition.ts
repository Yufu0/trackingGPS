import * as L from "leaflet";

export interface IPosition {
    id: number;
    name: string;
    latitude: number;
    longitude: number;
    timestamp: Date;
    color: number;
    layer?: L.Marker;
}
