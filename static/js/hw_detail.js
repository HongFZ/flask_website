$(function () {
    $("#save-class-btn").click(function (event) {
        event.preventDefault();
        var dialog = $("#banner-dialog");
        var probSelect = $("select[name='prob_id']")
        var prob_id = probSelect.val();
        var hwInput = $("input[name='hw_id']");
        var hw_id = hwInput.val();
        zlajax.post({
            "url": '/add_hw_prob/',
            'data':{
                'prob_id':prob_id,
                'hw_id': 1
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
    $(".delete-hwprob-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var hwprob_id = tr.attr('data-hwprob');

        zlalert.alertConfirm({
            "msg":"您确定要删除这个题目吗？",
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/dhwprob/',
                    'data':{
                        'hwprob_id': hwprob_id
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