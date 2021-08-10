$(function () {
    var ue = UE.getEditor("editor",{
        "serverUrl": '/ueditor/upload/'
    });

    $("#submit-btn").click(function (event) {
        event.preventDefault();
        var titleInput = $('input[name="title"]');
        var title = titleInput.val();
        var content = ue.getContent();

        zlajax.post({
            'url': '/cms/aposts/',
            'data': {
                'title': title,
                'content':content,
                'course_id': 0
            },
            'success': function (data) {
                if(data['code'] == 200){
                    zlalert.alertConfirm({
                        'msg': '添加成功！',
                        'cancelText': '回到题目页',
                        'confirmText': '继续添加',
                        'cancelCallback': function () {
                            window.location = '/cms/posts/';
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