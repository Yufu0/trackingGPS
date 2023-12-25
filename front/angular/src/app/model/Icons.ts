import * as L from 'leaflet';

export const NumberIcons: number = 15;

const PenguinIcon = L.Icon.extend({
    options: {
        iconSize:     [38, 65],
        iconAnchor:   [19, 65],
        popupAnchor:  [0, -65]
    }
});

export const icons = [];
for (let i = 0; i < NumberIcons; i++) {
    if(i < 10)
        // @ts-ignore
        icons.push(new PenguinIcon({iconUrl: 'assets/tile00' + i + '-removebg-preview.png'}));
    else
        // @ts-ignore
        icons.push(new PenguinIcon({iconUrl: 'assets/tile0' + i + '-removebg-preview.png'}));
}
