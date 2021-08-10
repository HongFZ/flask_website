$(function () {
    $(".silence-btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var user_id = tr.attr("data-id");
        var highlight = parseInt(tr.attr("data-highlight"));
        var url = "";
        if(highlight){
            url = "/cms/usilence_users/";
        }else{
            url = "/cms/silence_users/";
        }
        zlajax.post({
            'url': url,
            'data': {
                'user_id': user_id
            },
            'success': function (data) {
                if(data['code'] == 200){
                    zlalert.alertSuccessToast('操作成功！');
                    setTimeout(function () {
                        window.location.reload();
                    },500);
                }else{
                    zlalert.alertInfo(data['message']);
                }
            }
        });
    });
});

$(function () {
    $(".delete-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var user_id = tr.attr('data-id');
        zlalert.alertConfirm({
            "msg":"您确定要删除这个用户吗？",
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/delete_users/',
                    'data':{
                        'user_id': user_id
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            window.location.reload();
                        }else{
                            zlalert.alertInfo(data['message']);
                        }
                    }
                })
            }
        });
    });
});