$(function() {
    let head=document.getElementById("head");
    input=document.getElementById("models_table").getElementsByTagName("input");
    tr=document.getElementById("models_table").getElementsByTagName("tr");
    //全选/全不选
    head.onclick=function(){
        for(let i=1;i<input.length;i++){
            // 如果全选为true那么下面四个列表页都要勾上 否则都不勾
            input[i].checked=this.checked;
            
        }
    }
    //input都勾时 全选为true，input有一个没勾 全选为false
 
    for(let i=1;i<tr.length;i++){
        
        tr[i].onclick=function(){
            let flag=true;
            for(let j=1;j<input.length;j++){
            if(input[j].checked==false){
                flag=false;
                break;         
            }
        }
        head.checked=flag;
    
        }
    }

    
    

});

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function delect_select_model() {
    var select_ids = [];
    for(var i=1; i<input.length;i++){
        if(input[i].checked==true) {
            var list = tr[i].getElementsByTagName("td");
            select_ids.splice(0,0,list[1].innerHTML);
        }
    }
    // console.log(select_ids);

    var host_url = window.location.protocol +'//' + window.location.hostname + ':' + window.location.port;
    var target_url = host_url + '/remove_models';
    var form = new FormData(), 
            url = target_url
    form.append('select_ids', select_ids);
    var xhr = new XMLHttpRequest();
    xhr.open("post", url, true);
    xhr.send(form);
    // console.log("sendddddddddddddddd");
    await sleep(300);
    window.location.href = host_url + '/models_page';
}

async function set_current_select_model() {
    var select_ids = [];
    var checked_num = 0;
    for(var i=1; i<input.length;i++){
        if(input[i].checked==true) {
            var list = tr[i].getElementsByTagName("td");
            select_ids.splice(0,0,list[1].innerHTML);
            checked_num ++;
        }
    }
    console.log(select_ids);
    if (checked_num > 1) {
        alert("只能选一个呀！！！");
    } else {
        var host_url = window.location.protocol +'//' + window.location.hostname + ':' + window.location.port;
        var target_url = host_url + '/update_current_model';
        var form = new FormData(), 
                url = target_url
        form.append('select_ids', select_ids);
        var xhr = new XMLHttpRequest();
        xhr.open("post", url, true);
        xhr.send(form);
        // console.log("sendddddddddddddddd");
        await sleep(300);
        window.location.href = host_url + '/models_page';
    }

}

function new_window(pred_res_str) {
    window.open('dotplot/'+pred_res_str, 'Predict Result', 'location=no, toolbar=no, height=400, width=600');
    return false;
}

function dotplot(all_data_str) {
    new_window(all_data_str);
}