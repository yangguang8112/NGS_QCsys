'use strict';


function sample_streamtable(samples) {
    $(function() {
        // This is mostly copied from <https://michigangenomics.org/health_data.html>.
        // var data = _.sortBy(_.where(samples, {peak: true}), _.property('pval'));
        var data = samples;
        data_html = '<tr>';
        for (i=0; i < samples[0].length; i++) {
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
    col_html = '';
    for (i=0; i<col_arr.length; i++) {
        col_html = `${col_html}<th>${col_arr[i]}</th>`
    }
    // console.log(col_html);
    HTML = `
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
    const target = document.querySelector('div.target');

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
        col_arr = arr[0];
        data = arr.slice(1, arr.length);
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
        console.log(url);
        xhr.open("post", url, true)
        //上传进度事件
        xhr.upload.addEventListener("progress", function(result) {
            if (result.lengthComputable) {
                //上传进度
                var percent = (result.loaded / result.total * 100).toFixed(2);
                console.log(percent);
                $("#sss").progress('set progress', percent);
            }
        }, false);
        
        
        xhr.addEventListener("readystatechange", function(flag = 0) {
            var result = xhr;
            flag += 1;
            if (result.lengthComputable) {
                //上传进度
                var percent = (result.loaded / result.total * 100).toFixed(2);
                console.log(percent);
            }
            // console.log(flag);
            // var res_json = JSON.parse(result.response)
            
            // if (result.status != 200) { //error
            //     console.log('上传失败', result.status, result.statusText, result.response);
            // }
            // else if (result.readyState == 4) { //finished
            //     console.log('上传成功', result);
            // }
            if (flag == 3) {
                res_json = eval("(" + result.response + ")");
                // res_json = JSON.parse(result.response)
                console.log(res_json);
                show_table(res_json['col_name']);
                sample_streamtable(res_json['data']);
                window.colName = res_json['col_name'];
                window.contentData = res_json['data'];
                upload();
            }
        });
        xhr.send(form); //开始上传
      }
    );
});

function return_col_num() {
    return window.col_num;
}


function upload() {
    const box = document.getElementById("upload_data");

    box.innerHTML = "<button type=\"button\" onclick=\"upload_data()\">上传</button>";
}

function upload_data() {
    console.log("==========================sss==========================");
    console.log(window.colName);
    var target_url = window.location.protocol +'//' + window.location.hostname + ':' + window.location.port + '/insert_excel_data';
    var form = new FormData();
    form.append('col_arr', JSON.stringify(window.colName));
    form.append('data', JSON.stringify(window.contentData));
    var xhr = new XMLHttpRequest();
    xhr.open("post", target_url, true)
    xhr.send(form);
    xhr.addEventListener("readystatechange", function() {
        var result = xhr;
        flag += 1;
        if (flag == 3) {
            console.log("上传完成");
            console.log(result);
        }
    });
}