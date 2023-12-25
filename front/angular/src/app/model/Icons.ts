import * as L from 'leaflet';

const PenguinIcon = L.Icon.extend({
    options: {
        iconSize:     [38, 65],
        iconAnchor:   [22, 94],
        popupAnchor:  [-3, -76]
    }
});

export const icons = [];
for (let i = 0; i < 15; i++) {
    if(i < 10)
        // @ts-ignore
        icons.push(new PenguinIcon({iconUrl: 'assets/tile00' + i + '-removebg-preview.png'}));
    else
        // @ts-ignore
        icons.push(new PenguinIcon({iconUrl: 'assets/tile0' + i + '-removebg-preview.png'}));
}
