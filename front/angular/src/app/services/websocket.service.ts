import {Injectable} from '@angular/core';
import {Observable, Subject} from "rxjs";
import {IPosition} from "../model/IPosition";

@Injectable({
    providedIn: 'root'
})
export class WebsocketService {

    private listPositions: Array<IPosition> = new Array<IPosition>();
    private listPositionsSubject: Subject<Array<IPosition>> = new Subject<Array<IPosition>>();
    public listPositions$: Observable<Array<IPosition>> = this.listPositionsSubject.asObservable();

    private webSocket?: WebSocket;

    constructor() {}

    openWebSocket(): void {
        this.webSocket = new WebSocket('ws://localhost:8080/gps');
        this.webSocket.onopen = (event) => {
            console.info('WebSocket is open now.');
        }
    }

    closeWebSocket(): void {
        if(this.webSocket === undefined) {
            console.error('WebSocket is not open.');
            return;
        }
        this.webSocket.close();
        this.webSocket = undefined;
        console.info('WebSocket is closed now.');
    }

    connect(): void {
        if(this.webSocket === undefined) {
            console.error('WebSocket is not open.');
            return;
        }
        this.webSocket.onmessage = (event) => {
            const position: IPosition = JSON.parse(event.data);
            const index: number = this.listPositions.findIndex((element: IPosition) => element.name === position.name);
            if(index === -1) {
                position.color = Math.floor(Math.random() * 15);
                this.listPositions.push(position);
            }
            else {
                position.color = this.listPositions[index].color;
                this.listPositions[index] = position;
            }

            this.listPositionsSubject.next(this.listPositions);
        }
    }
}
