$(function () {
    $("#submit").click(function (event) {
        
        event.preventDefault();

        var oldpwdE = $("input[name=oldpwd]");
        var newpwdE = $("input[name=newpwd]");
        var newpwd2E = $("input[name=newpwd2]");

        var oldpwd = oldpwdE.val();
        var newpwd = newpwdE.val();
        var newpwd2 = newpwd2E.val();

        
        zlajax.post({
            'url': '/resetpwd/',
            'data': {
                'oldpwd': oldpwd,
                'newpwd': newpwd,
                'newpwd2': newpwd2
            },
            'success': function (data) {
                // code==200
                // code != 200
                if(data['code'] == 200){
                    zlalert.alertSuccessToast("密码修改成功！");
                    oldpwdE.val("");
                    newpwdE.val("");
                    newpwd2E.val("");
                }else{
                    var message = data['message'];
                    zlalert.alertInfo(message);
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError();
            }
        });
    });
});