export default function init(socket) {
    socket.addEventListener("open", (event) => {
        socket.send("Hello Server!");
    });

    socket.addEventListener("close", (event) => {
        socket.send("Bye Server!");
    });

    socket.addEventListener("message", (event) => {
        console.log("Message from server ", event.data);
    });

    socket.addEventListener("error", (event) => {
        console.error("Error", event);
    });
}
