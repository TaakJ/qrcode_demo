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
        // e.preventDefault();
        $.ajax({
            url: $url,
            async: false,
            dataType: 'json',
            success: function(data) {
                if (data.resp) {
                    md.showNotification('top','center', '<b> DELETE TO Customer Profile' + data.company_name + '(' + data.userid  + ')' + '- on database SQLite.</b>');
                    setTimeout(function () {
                        window.location.reload(true);
                }, 2000);
                } else {
                    md.showNotification('top','center', '<b> PROBLEM !! CAN NOT DELETE Customer Profile' + data.company_name + '(' + data.userid  + ')' + '- on database SQLite.</b>');
                }
            },
            error: function(error) {
                console.log(error);
            },
        });
        return(false)
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
                console.log(error);
            }
        });
    });

    $('#dataTable tbody').on('click', '.printBtn', function (e) {
        e.preventDefault();
        var url = $(this).attr('data-url');
        $.ajax({
            url: url,
            async: false,
            type:'post',
            dataType: 'json',
            success: function(data) {
                var img = document.querySelector('img').src;
                var win = window.open('');
                win.document.write('<center>');
                win.document.write('<br>');
                win.document.write('<br>');
                win.document.write('<h2 style="text-decoration: underline #212121; text-underline-position: under; font-family:monospace;">' + data.company_name +  '</h2>');
                win.document.write('<h2 style="font-family:monospace;"> Subject Area: ' + data.job_id +  '</h2>');
                win.document.write('<img src=' + img + ' height=350, width=320 />');
                win.document.write('<br>');
                win.document.write('<h3 style="text-decoration: underline #212121; text-underline-position: under; font-family:monospace;"> https://iaq-trackking-app-df045633f579.herokuapp.com </h3>');
                win.document.write('</center>');
                win.print();
                win.close();
                win.focus();
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $('#dataTable input[type=checkbox]').each(function () {
        if ($(this).val() == 'False') {
            $(this).prop('checked', false);
            $(this).closest('tr').css('color','#959596');
        } else {
            $(this).prop('checked', true);
        }
        $(this).closest('tr').find(":input:not(:first)").attr('disabled', !this.checked);
        
        $(this).change(function () {
            var bool = $(this).prop('checked');
            var url =  $(this).attr('data-url');
            if (!bool) {
                $(this).closest('tr').find('td').css('color','#959596');
            } else {
                $(this).closest('tr').find('td').css('color','black');
            }
            $(this).closest('tr').find(":input:not(:first)").attr('disabled', !this.checked);

            $.ajax({
                url: url,
                async: false,
                type:'post',
                data: {'checked': bool},
                dataType: 'json',
                success: function(data) {
                    //console.log(data)
                    document.getElementById('cnt').innerHTML = data.count;
                },
                error: function(error) {
                    console.log(error);
                }
            });
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