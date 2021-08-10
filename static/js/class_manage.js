$(function () {
    $("#save-class-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $("#banner-dialog");
        var nameInput = $("input[name='name']");
        var timeInput = $("input[name='time']");
        var courseInput = $("input[name='course_id']");
        var submitType = self.attr('data-type');
        var class_id = self.attr("data-id");
        var name = nameInput.val();
        var time = timeInput.val();
        var course_id = courseInput.val();
        
        if(!name || !time ){
            zlalert.alertInfoToast('请输入完整的课程信息！');
            return;
        }

        var url = '';
        if(submitType == 'update'){
            url = '/eclass/';
        }else{
            url = '/aclass/'+course_id;
        }

        zlajax.post({
            "url": url,
            'data':{
                'name':name,
                'time': time,
                'class_id':class_id
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
    $(".edit-class-btn").click(function (event) {
        var self = $(this);
        var dialog = $("#banner-dialog");
        dialog.modal("show");

        var tr = self.parent().parent();
        var name = tr.attr("data-name");
        var time = tr.attr("data-time");
        

        var nameInput = dialog.find("input[name='name']");
        var timeInput = dialog.find("input[name='time']");
        var saveBtn = dialog.find("#save-class-btn");

        nameInput.val(name);
        timeInput.val(time);
        
        saveBtn.attr("data-type",'update');
        saveBtn.attr('data-id',tr.attr('data-id'));
    });
});

$(function () {
    $(".delete-class-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var class_id = tr.attr('data-id');
        zlalert.alertConfirm({
            "msg":"您确定要删除这个班级吗？",
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/dclass/',
                    'data':{
                        'class_id': class_id
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

