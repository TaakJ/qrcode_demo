$(document).ready(function() { 

    $(function () {
        $.ajaxSetup({
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        });
    });

    $('#page-userid').submit(function (e) {
        e.preventDefault();
        var url = "/page-user/";
        var formData = JSON.stringify($(this).serializeArray());
        $.ajax({
            url: url,
            async: false,
            type:'post',
            data: { 'request': formData },
            dataType: 'json',
            success: function(data) {
                window.location.href = data.url;
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $('#dataTable tbody').on('click', '.editbtn', function (e) {
        e.preventDefault();
        var url = $(this).attr("data-url");
        $.ajax({
            url: url,
            async: false,
            type:'get',
            success: function(data) {
                window.location.href = url;
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    let $url = ""
    $('#dataTable tbody').on('click', '.delbtn', function (e) {
        $('#modal_title').text('DELETE');
        $("#delpopup").modal();
        $url = $(this).attr('data-url');
    });

    $('#delpopup').on('click', '#del', function (e) {
        e.preventDefault();
        $.ajax({
            url: $url,
            async: false,
            dataType: 'json',
            success: function(data) {
                if (data.resp) {
                    md.showNotification('top','center', 'DELETE TO <b>Customer Contract <b>' + data.company_name + '(' + data.userid  + ')' + '</b> - on database SQLite.');
                    setTimeout(function () {
                    window.location.reload(true);
                }, 3000)
                } else {
                    md.showNotification('top','center', '<b> CAN NOT DELETE Customer Contract</b>.');
                }
            },
            error: function(data) {
                console.log(data);
            },
        });
    });


    $('#dataTable tbody').on('click', '.qrbtn', function (e) {
        e.preventDefault();
        var url = $(this).attr("data-url");
        $.ajax({
            url: url,
            async: false,
            type:'get',
            success: function(data) {
                window.location.href = url;
            },
            error: function(error) {
                alert(error)
            }
        });
    });

    function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
        return cookieValue;
    }

});