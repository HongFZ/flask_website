$(function () {
    var ue = UE.getEditor("editor",{
        "serverUrl": '/ueditor/upload/'
    });

    $("#submit-btn").click(function (event) {
        event.preventDefault();
        var titleInput = $('input[name="title"]');
        var courseSelect = $("select[name='course_id']");

        var title = titleInput.val();
        var course_id = courseSelect.val();
        var content = ue.getContent();

        zlajax.post({
            'url': '/add_prob/',
            'data': {
                'title': title,
                'content':content,
                'course_id': course_id
            },
            'success': function (data) {
                if(data['code'] == 200){
                    zlalert.alertConfirm({
                        'msg': '添加成功！',
                        'cancelText': '回到首页',
                        'confirmText': '继续添加',
                        'cancelCallback': function () {
                            window.location = '/teacher_homepage/';
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