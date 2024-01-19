import {Injectable} from '@angular/core';
import {Observable, Subject} from "rxjs";
import {IPosition} from "../model/IPosition";
import {NumberIcons} from "../model/Icons";

@Injectable({
    providedIn: 'root'
})
export class WebsocketService {

    private listPositions: Array<IPosition> = new Array<IPosition>();
    private listPositionsSubject: Subject<Array<IPosition>> = new Subject<Array<IPosition>>();
    public listPositions$: Observable<Array<IPosition>> = this.listPositionsSubject.asObservable();

    public listPositionsMemory: Array<IPosition> = new Array<IPosition>();

    private webSocket?: WebSocket;

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
            const data = JSON.parse(event.data);

            this.listPositions = [];

            const positions: Array<IPosition> = data as Array<IPosition>;
            positions.forEach((position: IPosition) => this.listPositions.push(this.computeListPositions(position)));
            this.listPositionsSubject.next(this.listPositions);
        }
    }

    private computeListPositions(position: IPosition): IPosition {
        const index: number = this.listPositionsMemory.findIndex((element: IPosition) => element.name === position.name);
        if(index === -1) {
            position.color = Math.floor(Math.random() * NumberIcons);
            position.layer = undefined;
            this.listPositionsMemory.push(position);
        } else {
            position.color = this.listPositionsMemory[index].color;
            position.layer = this.listPositionsMemory[index].layer;
            this.listPositionsMemory[index] = position;
        }
        return position;
    }
}
