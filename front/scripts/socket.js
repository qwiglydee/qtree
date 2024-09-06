export class AppSocket {
    constructor(url) {
        this.ws = new WebSocket(url);
        this.onreceive = this.defaut_onreceive;
        this.onclose = this.defaut_onclose;
        this.onerror = this.defaut_onerror;

        this.ws.addEventListener("message", (event) => this.onreceive(JSON.parse(event.data)));
        this.ws.addEventListener("close", (event) => this.onclose(event));
        this.ws.addEventListener("error", (event) => this.onerror(event));
    }

    defaut_onreceive(data) {
        console.debug("websocket received", data);
    }
    defaut_onclose(event) {
        console.debug("websocket closed", event);
    }
    defaut_onerror(event) {
        console.debug("websocket error", event);
    }

    async start() {
        await new Promise((resolve, reject) => {
            this.ws.onopen = resolve;
        });
        this.send({ READY: true });
    }

    async send(data) {
        if (this.ws.readyState != WebSocket.OPEN) {
            throw new Error("WebSocket broken");
        }
        await this.ws.send(JSON.stringify(data));
    }

    async recv() {
        const orig_onreceive = this.onrecieve;
        return await new Promise((resolve, reject) => {
            this.onrecieve = (data) => {
                this.onrecieve = orig_onreceive;
                resolve(data);
            };
        });
    }
}
