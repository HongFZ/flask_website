$(function () {
    $("#save-course-btn").click(function (event) {
        event.preventDefault();        
        var self = $(this);
        var dialog = $("#banner-dialog");
        var nameInput = $("input[name='name']");
        var teacherInput = $("input[name='user_id']");
        
        var name = nameInput.val();
        var user_id = teacherInput.val();
        
        var submitType = self.attr('data-type');
        var courseId = self.attr("data-id");

        if(!name || !user_id ){
            zlalert.alertInfoToast('请输入完整的课程信息！');
            return;
        }

        var url = '';
        if(submitType == 'update'){
            url = '/cms/uboard/';
        }else{
            url = '/cms/aboard/';
        }

        zlajax.post({
            "url": url,
            'data':{
                'course_name':name,
                'user_id': user_id,
                'course_id': courseId
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
    $(".edit-course-btn").click(function (event) {
        var self = $(this);
        var dialog = $("#banner-dialog");
        dialog.modal("show");

        var tr = self.parent().parent();
        var nameInput = $("input[name='name']");
        var teacherInput = $("input[name='user_id']");
        
        var name = nameInput.val();
        var user_id = teacherInput.val();
        var saveBtn = dialog.find("#save-course-btn");

        nameInput.val(name);
        teacherInput.val(user_id);
        
        saveBtn.attr("data-type",'update');
        saveBtn.attr('data-id',tr.attr('data-id'));
    });
});

$(function () {
    $(".delete-course-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var banner_id = tr.attr('data-id');
        zlalert.alertConfirm({
            "msg":"您确定要删除这个课程吗？",
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/dboard/',
                    'data':{
                        'course_id': banner_id
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

