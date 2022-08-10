'use strict';


function sample_streamtable(samples) {
    $(function() {
        // This is mostly copied from <https://michigangenomics.org/health_data.html>.
        // var data = _.sortBy(_.where(samples, {peak: true}), _.property('pval'));
        var data = samples;
        var data_html = '<tr>';
        for (var i=0; i < samples[0].length; i++) {
            data_html = `${data_html}<td><%= v[${i}] %></td>`
        }
        data_html = `${data_html}</tr>`
        // console.log(data_html)
        // var template = _.template($('#streamtable-template').html());
        var template = _.template(data_html);
        var view = function(sample) {
            return template({v: sample});
        };
        var $found = $('#streamtable-found');
        $found.text(data.length + " total samples");

        var callbacks = {
            pagination: function(summary){
                if ($.trim($('#search').val()).length > 0){
                    $found.text(summary.total + " matching variants");
                } else {
                    $found.text(data.length + " total variants");
                }
            }
        }

        var options = {
            view: view,
            search_box: '#search',
            per_page: 20,
            callbacks: callbacks,
            pagination: {
                span: 5,
                next_text: 'Next <span class="glyphicon glyphicon-arrow-right" aria-hidden="true"></span>',
                prev_text: '<span class="glyphicon glyphicon-arrow-left" aria-hidden="true"></span> Previous',
                per_page_select: false,
                per_page: 10
            }
        }
        
        $('#stream_table').stream_table(options, data);

    });
}

function show_table(col_arr) {
    const box = document.getElementById("paste_data");
    var col_html = '';
    for (var i=0; i<col_arr.length; i++) {
        col_html = `${col_html}<th>${col_arr[i]}</th>`
    }
    // console.log(col_html);
    var HTML = `
    <div class="col-xs-12">
        <table id="stream_table" class="table table-striped table-bordered">
        <thead>
            <tr>
            ${col_html}
            </tr>
        </thead>
        <tbody>
        </tbody>
        </table>
    </div>`;
    
    box.innerHTML = HTML;
}


$(function() {
    const target = document.querySelector('div.dropzone');

    target.addEventListener('paste', (event) => {
        if (event.clipboardData || event.originalEvent) {
        var clipboardData = event.clipboardData || window.clipboardData;
        var val = clipboardData.getData("text");
        // console.log(val);
        // console.log(val.split(""));
        val = val.replace(/\r\n|\r/g, "\n");
        let str = val.split("\n");
        let arr = new Array(str.length - 1);
        for (let i = 0; i < str.length - 1; i++) {
          let temp = str[i].split("\t");
          arr[i] = temp;
        }
        // console.log(arr);
        event.preventDefault();
        let col_arr = arr[0];
        let data = arr.slice(1, arr.length);
        // console.log(data);
        show_table(col_arr);
        sample_streamtable(data);
        window.colName = col_arr;
        window.contentData = data;
        upload();
      }
    });


    $(document).on({
        dragleave:function(e){      //拖离
            e.preventDefault();
        },
        drop:function(e){           //拖后放
            e.preventDefault();
        },
        dragenter:function(e){      //拖进
            e.preventDefault();
        },
        dragover:function(e){       //拖来拖去
            e.preventDefault();
        }
        });


    target.addEventListener('drop', (e) => {
        e.preventDefault(); //取消默认浏览器拖拽效果
        var fileList = e.dataTransfer.files; //获取文件对象
        //检测是否是拖拽文件到页面的操作
        if (fileList.length == 0) {
            return false;
        }
        console.log(fileList[0]);
        var target_url = window.location.protocol +'//' + window.location.hostname + ':' + window.location.port + '/upload';
        var form = new FormData(), 
            url = target_url, 
            file=fileList[0];
        form.append('file', file)

        var xhr = new XMLHttpRequest();
        // console.log("hell")
        console.log(url);
        xhr.open("post", url, true)
        NSpinner.show();
        //上传进度事件
        xhr.upload.addEventListener("progress", function(result) {
            if (result.lengthComputable) {
                //上传进度
                var percent = (result.loaded / result.total * 100).toFixed(2);
                // console.log(percent);
                // $("#sss").progress('set progress', percent);
            }
        }, false);
        
        xhr.send(form); //开始上传
        xhr.onload = function(e) {
            console.log('onload e ======>' + JSON.stringify(e));
        };
        xhr.onreadystatechange = function(e) {
            console.log('onreadystatechage e======>' + JSON.stringify(e));
            if (xhr.readyState == 4 && xhr.status == 200) {
                NSpinner.hide();
                var xhrRes = xhr.responseText;
                console.log('return message=======>');
                var res_json = eval("(" + xhrRes + ")");
                console.log(res_json);
                show_table(res_json['col_name']);
                sample_streamtable(res_json['data']);
                window.colName = res_json['col_name'];
                window.contentData = res_json['data'];
                upload();
            }
        };
      }
    );
});

function return_col_num() {
    return window.col_num;
}


function upload() {
    const box = document.getElementById("upload_data");

    box.innerHTML = "<button class=\"button-1\" role=\"button\" onclick=\"upload_data()\">上传</button>   <button class=\"button-1\" role=\"button\" onclick=\"predict_sample()\">预测</button>"
}

function new_window(pred_res_str) {
    window.open('predict_result_page/'+pred_res_str, 'Predict Result', 'location=no, toolbar=no, height=405, width=605');
    return false;
}

function predict_sample() {
    NSpinner.show();
    var host_url = window.location.protocol +'//' + window.location.hostname + ':' + window.location.port;
    var target_url = host_url + '/predict_samples';
    var form = new FormData();
    form.append('col_arr', JSON.stringify(window.colName));
    form.append('data', JSON.stringify(window.contentData));
    var xhr = new XMLHttpRequest();
    xhr.open("post", target_url, true)
    xhr.send(form);
    xhr.onload = function(e) {
        console.log('onload e ======>' + JSON.stringify(e));
    };
    xhr.onreadystatechange = function(e) {
        console.log('onreadystatechage e======>' + JSON.stringify(e));
        if (xhr.readyState == 4 && xhr.status == 200) {
            NSpinner.hide();
            var xhrRes = xhr.responseText;
            console.log('return message=======>');
            var pred_res = eval("(" + xhrRes + ")");
            NSpinner.hide();
            console.log(pred_res);
            new_window(xhrRes);
        }
    };
}


function upload_data() {
    NSpinner.show();
    // console.log("==========================sss==========================");
    // console.log(window.colName);
    var host_url = window.location.protocol +'//' + window.location.hostname + ':' + window.location.port;
    var target_url = host_url + '/insert_excel_data';
    var form = new FormData();
    form.append('col_arr', JSON.stringify(window.colName));
    form.append('data', JSON.stringify(window.contentData));
    var xhr = new XMLHttpRequest();
    xhr.open("post", target_url, true)
    xhr.send(form);
    xhr.onload = function(e) {
        console.log('onload e ======>' + JSON.stringify(e));
    };
    xhr.onreadystatechange = function(e) {
        console.log('onreadystatechage e======>' + JSON.stringify(e));
        if (xhr.readyState == 4 && xhr.status == 200) {
            NSpinner.hide();
            var xhrRes = xhr.responseText;
            console.log('return message=======>');
            NSpinner.hide();
            console.log("上传完成");
            var train_flag = JSON.parse(xhrRes)['train_flag']
            NSpinner.hide();
            if (train_flag == 1) {
                var oReq = new XMLHttpRequest();
                oReq.open("GET", host_url + '/training');
                oReq.send();
                alert("上传数据中发现有人工标注的不合格样本，根据上传的新数据已重新选取数据训练，详情可到Models页面查看！");
            }
        }
    };
}

