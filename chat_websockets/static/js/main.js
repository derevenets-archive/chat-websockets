$(document).ready(function () {

    const sock = new WebSocket('ws://' + window.location.host + '/ws');
    // try {
    //     const sock = new WebSocket('ws://' + window.location.host + '/ws');
    // }
    // catch (err) {
    //     const sock = new WebSocket('wss://' + window.location.host + '/ws');
    // }

    console.log('sock ', sock);

    // show message in div#subscribe
    function showMessage(message) {
        const messageElem = $('#subscribe');
        const date = new Date();
        const options = {hour12: false};
        let height = 0;

        messageElem.append($('<p>').html('[' + date.toLocaleTimeString('en-US', options) + '] ' + message + '\n'));
        messageElem.find('p').each(function (i, value) {
            height += parseInt($(this).height());
        });

        messageElem.animate({scrollTop: height});
    }

    function sendMessage() {
        const msg = $('#message');
        console.log('msg', msg.val())
        sock.send(msg.val());
        msg.val('').focus();
    }

    sock.onopen = function () {
        showMessage('Connection to server started')
    };

    // send message from form
    $('#submit').click(function () {
        sendMessage();
    });

    $('#message').keyup(function (e) {
        if (e.keyCode === 13) {
            sendMessage();
        }
    });

    // income message handler
    sock.onmessage = function (event) {
        showMessage(event.data);
    };

    $('#signout').click(function () {
        window.location.href = "signout"
    });

    sock.onclose = function (event) {
        if (event.wasClean) {
            showMessage('Clean connection end')
        } else {
            showMessage('Connection broken')
        }
    };

    sock.onerror = function (error) {
        showMessage(error);
    }
});