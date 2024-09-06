import { AppSocket } from "./socket.js";

/** setup
 * @param {AppSocket} socket
 * @param {HTMLElement} main
 */
export async function setup(socket, main) {
    let inputs = [];
    const nextbtn = document.querySelector("button[name=next");

    function submitInputs() {
        let data = {};
        inputs.forEach((inpname) => {
            if (inpname == "next") {
                data["next"] = true;
                return;
            }
            let inp = main.querySelector(`[name=${inpname}]`);
            if (!inp) throw Error(`input not found: ${inpname}`);
            data[inpname] = inp.value;
        });
        socket.send(data);
    }

    function submitPage() {
        document.querySelector("form").submit();
    }

    nextbtn.addEventListener("click", () => {
        submitInputs();
    });

    socket.onreceive = function (data) {
        if ("html" in data) {
            main.innerHTML = data["html"];
            let af = main.querySelector("[autofocus]");
            if (af) af.focus();
        }

        if ("inputs" in data) {
            inputs = data["inputs"];
            nextbtn.hidden = !inputs.includes("next");
        } else {
            nextbtn.hidden = false;
        }

        if ("TERMINATE" in data) {
            submitPage();
        }
    };
}
