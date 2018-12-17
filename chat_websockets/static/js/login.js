$(document).ready(() => {

    // handle click on "Sign in" button to redirect to sign in page
    $('#signin').click(() => {
        window.location.href = "signin"
    });

    function showError(error) {
        $('#error').html(error)
    }

    $('#submit').click(function () {
        const login = $('#login').val();
        const password = $('#password').val();
        console.log(login, 'if pass the same');
        if (login && password) {
            $.post('login', {
                'login': login,
                'password': password
            }, function (data) {
                console.log(data);
                if (data.error) {
                    showError(data.error)
                } else {
                    window.location.href = '/'
                }
            });
        } else {
            showError('Please fill all fields')
        }
    });
});