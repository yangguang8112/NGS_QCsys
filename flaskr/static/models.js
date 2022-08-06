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
    if (select_ids.length == 0) {
        alert("至少选一个吧！！！");
    } else {
        var r = confirm("确认删除吗？");
        if (r == true) {
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
    }

    
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
    if (checked_num == 0) {
        alert("选一个再点啊！！！");
    } else {
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
    
}

function new_window(pred_res_str) {
    window.open('dotplot/'+pred_res_str, 'Predict Result', 'location=no, toolbar=no, height=405, width=605');
    return false;
}

function dotplot(all_data_str) {
    new_window(all_data_str);
}


function compare_new_window(ids_str) {
    window.open('compare_page/'+ids_str, 'compare', 'location=no, toolbar=no, height=805, width=605');
}

function compare_models() {
    var select_ids = [];
    var checked_num = 0;
    for(var i=1; i<input.length;i++){
        if(input[i].checked==true) {
            var list = tr[i].getElementsByTagName("td");
            select_ids.splice(0,0,list[1].innerHTML);
            checked_num ++;
        }
    }
    if (checked_num < 2) {
        alert("至少要选两个啊！！！！");
    } 
    else {
        if (checked_num > 10) {
            alert("选太多啦！！！");
        } else {
            // console.log(select_ids);
            compare_new_window(select_ids);
        }
        
    }
    
}

function train_new_window() {
    window.open('train_new_model', 'train', 'location=no, toolbar=no, height=888, width=805');
}

function train_new_model() {
    train_new_window();
}