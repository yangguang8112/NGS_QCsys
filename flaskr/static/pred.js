function sample_streamtable(samples) {
    $(function() {
        // This is mostly copied from <https://michigangenomics.org/health_data.html>.
        // var data = _.sortBy(_.where(samples, {peak: true}), _.property('pval'));
        var data = samples;
        var template = _.template($('#streamtable-template').html());
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