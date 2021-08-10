
$(function () {
    $(".delete-hw-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var class_id = tr.attr('data-hw');
        zlalert.alertConfirm({
            "msg":"您确定要删除这个作业吗？",
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/delete_hw/',
                    'data':{
                        'hw_id': class_id
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