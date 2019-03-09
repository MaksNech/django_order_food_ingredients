var loc = window.location;

var token =  $('#user_token').val();

var wsStart = 'ws://';

if (loc.protocol == 'https:') {
    wsStart = 'wss://';
};

var endpoint = wsStart + loc.host + loc.pathname + '?token=' + token;

var socket = new WebSocket(endpoint);


socket.onmessage = function (event) {

     var data = JSON.parse(event.data);
     var message = data['message'];
     if (message === "reload") {
        location.reload();
     };


    var newComment = JSON.parse(event.data);

    $('#comments').append('<hr><p>' + newComment.body + '</p><small>' + newComment.author + '</small><br><small>' +
        newComment.created_on + '</small>');


};


socket.onopen = function (event) {


    $(document).ready(function () {

        var form = $('#comment_add_form');

        form.submit(function (event) {

            event.preventDefault();
            var body = $('#comment_body').val();
            var dishSlug = $('#hidden_input').attr('data-post');
            var authorId = $('#hidden_input').val();
            $('#comment_body').val(null);
            data = {
                'body': body,
                'dish_slug': dishSlug,
                'author_id': authorId,
            };
            socket.send(JSON.stringify(data));

        });

    });


};

