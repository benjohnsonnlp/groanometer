var slider = document.getElementById("myRange");

if (window.location.protocol === 'https:') {
    protocol = 'wss:';
} else {
    protocol = 'ws:';
}

const sock = new WebSocket(
    protocol
    + window.location.host
    + '/ws/chat/'
    + 'all'
    + '/'
);

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function () {

    $('#reading').text(this.value);
};

slider.onmouseup = function () {
    sock.send(JSON.stringify({
        "type": "user_slider_move",
        "value": this.value
    }));
}

sock.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log("Received message: " + e.data);
    if (data.type === 'new_average') {
        $('#average').text(data.average.magnitude__avg);
    }

};