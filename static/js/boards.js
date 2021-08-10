$(function () {
    $("#add-class-btn").click(function (event) {
        event.preventDefault();
        zlalert.alertOneInput({
            'text': '请输入课程名称！',
            'placeholder': '课程名称',
            'confirmCallback': function (inputValue) {
                zlajax.post({
                    'url': '/add_course/',
                    'data': {
                        'course_name': inputValue
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
                            window.location.reload();
                        } else {
                            zlalert.alertInfo(data['message']);
                        }
                    }
                });
            }
        });
    });
});

$(function () {
    $(".edit-class-btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var name = tr.attr('data-name');
        var course_id = tr.attr("data-id");

        zlalert.alertOneInput({
            'text': '请输入新的课程名称！',
            'placeholder': name,
            'confirmCallback': function (inputValue) {
                zlajax.post({
                    'url': '/change_course/',
                    'data': {
                        'course_id': course_id,
                        'course_name': inputValue
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
                            window.location.reload();
                        } else {
                            zlalert.alertInfo(data['message']);
                        }
                    }
                });
            }
        });
    });
});


$(function () {
    $(".delete-class-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var course_id = tr.attr("data-id");
        zlalert.alertConfirm({
            'msg': '确定删除此课程吗？',
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/delete_course/',
                    'data': {
                        'course_id': course_id,
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
                            window.location.reload();
                        } else {
                            zlalert.alertInfo(data['message']);
                        }
                    }
                });
            }
        })
    });
});


