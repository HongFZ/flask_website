$(function () {
    var ue = UE.getEditor("editor",{
        "serverUrl": '/ueditor/upload/'
    });

    $("#submit-btn").click(function (event) {
        event.preventDefault();
        var titleInput = $('input[name="title"]');
        var ddlInput = $('input[name="ddl"]');
        var classSelect = $("select[name='class_id']");

        var title = titleInput.val();
        var ddl = ddlInput.val();
        var class_id = classSelect.val();
        var content = ue.getContent();

        zlajax.post({
            'url': '/add_hw/',
            'data': {
                'title': title,
                'content': content,
                'ddl': ddl,
                'class_id':class_id
            },
            'success': function (data) {
                if(data['code'] == 200){
                    zlalert.alertConfirm({
                        'msg': '添加成功！',
                        'cancelText': '作业列表',
                        'confirmText': '继续添加',
                        'cancelCallback': function () {
                            window.location = '/hw_list/';
                        },
                        'confirmCallback': function () {
                            titleInput.val("");
                            ue.setContent("");
                        }
                    });
                }else{
                    zlalert.alertInfo(data['message']);
                }
            }
        });
    });
});




