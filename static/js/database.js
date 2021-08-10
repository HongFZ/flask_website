function get_score_data(){
    $.ajax({
        url:"/class/<int:class_id>/hw/<int:hw_id>",
        success:function(data){
            $("#")
        },
        error:function(){
            alert("数据获取失败")
        }
        
    })
}