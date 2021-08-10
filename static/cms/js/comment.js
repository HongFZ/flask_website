$(function () {
    $(".delete-comment").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var class_id = tr.attr('data-id');
        zlalert.alertConfirm({
            "msg":"您确定要删除这个评论吗？",
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/dcomments/',
                    'data':{
                        'com_id': class_id
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

$(function () {
    $(".delete-report").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var class_id = tr.attr('data-id');
        zlalert.alertConfirm({
            "msg":"您确定要删除这个举报吗？",
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/dcomment_report/',
                    'data':{
                        'report_id': class_id
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