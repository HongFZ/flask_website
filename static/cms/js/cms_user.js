$(function () {
    $("#save-banner-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $("#banner-dialog");
        var nameInput = $("input[name='name']");
        var imageInput = $("input[name='email']");
        var linkInput = $("input[name='password']");


        var name = nameInput.val();
        var email = imageInput.val();
        var password = linkInput.val();
    

        if(!name || !email || !password ){
            zlalert.alertInfoToast('请输入完整的管理员数据！');
            return;
        }


        zlajax.post({
            "url": '/cms/add_cusers/',
            'data':{
                'username':name,
                'email': email,
                'password': password
            },
            'success': function (data) {
                dialog.modal("hide");
                if(data['code'] == 200){
                    window.location.reload();
                }else{
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail': function () {
                zlalert.alertNetworkError();
            }
        });
    });
});

$(function () {
    $("#change-per").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var tr = self.parent().parent();
        var user_id = tr.attr("data-id");

        var idInput = $("select[name='role_id']");
        role_id = idInput.val();
        zlajax.post({
            "url": '/cms/edit_cusers/',
            'data':{
                'role_id': role_id,
                'user_id': user_id
            },
            'success': function (data) {
                dialog.modal("hide");
                if(data['code'] == 200){
                    window.location.reload();
                }else{
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail': function () {
                zlalert.alertNetworkError();
            }
        });


    });
});

$(function () {
    $(".delete-adm-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var banner_id = tr.attr('data-id');
        zlalert.alertConfirm({
            "msg":"您确定要删除这个管理员吗？",
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/delete_cusers/',
                    'data':{
                        'user_id': banner_id
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