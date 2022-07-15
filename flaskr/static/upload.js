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
      }
    });
});

function return_col_num() {
    return window.col_num;
}