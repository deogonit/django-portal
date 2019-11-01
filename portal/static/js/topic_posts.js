function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

$(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
});

function like() {
    var like = $(this);
    var type = like.data('type');
    var pk = like.data('id');
    var action = like.data('action');
    var topic = like.data('topic');
    var board = like.data('board');
    var dislike = like.next();

    $.ajax({
        url : "/forum/boards/" + board + "/topics/" + topic + "/post/" + pk + "/like/",
        type : 'POST',
        data : { 'obj' : pk },

        success : function (json) {
            like.find("[data-count='like']").text(json.like_count);
            dislike.find("[data-count='dislike']").text(json.dislike_count);
        }
    });

    return false;
}

function dislike() {
    var dislike = $(this);
    var type = dislike.data('type');
    var pk = dislike.data('id');
    var action = dislike.data('action');
    var topic = dislike.data('topic');
    var board = dislike.data('board');
    var like = dislike.prev();

    $.ajax({
        url : "/forum/boards/" + board + "/topics/" + topic + "/post/" + pk + "/dislike/",
        type : 'POST',
        data : { 'obj' : pk },

        success : function (json) {
            dislike.find("[data-count='dislike']").text(json.dislike_count);
            like.find("[data-count='like']").text(json.like_count);
        }
    });

    return false;
}

$(function() {
    $('[data-action="like"]').click(like);
    $('[data-action="dislike"]').click(dislike);
});