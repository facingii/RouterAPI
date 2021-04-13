window.onload = () => {
    fetch ("http://localhost:5000/getinfo?ip=200.4.144.3")
    .then (data => data.json ())
    .then (json => {
        const e = document.getElementById("bwSelector");
        if (e === 'undefined') return;

        e.innerHTML = json.bw;
    })

    const f = document.querySelector('form');
    f.addEventListener('submit', e => {
        e.preventDefault ();
        const element = document.getElementById("newBW");
        if (element === 'undefined') return;

        const data = {bw: element.value}

        fetch("http://localhost:5000/setbw?ip=200.4.144.3", {
            method: "PUT",
            headers: {
                "Content-type": "application/json"
            },
            body: JSON.stringify (data)
        }).then (response => response.json ())
        .then (json => {
            if (json.status === "ok") {
                document.getElementById("bwSelector").innerHTML = element.value;
            } else {
                alert("La operación no pudo ser completada.");
            }
        });
    })
}
