jQuery(function($) {
    
    $(function() {
        $("#debug-toolbar-trigger").click(function() {
            $('#debug-toolbar').slideDown();
            return false;
        });

        $("#debug-toolbar-close").click(function() {
            $('#debug-toolbar').slideUp();
            return false;
        });

        $(".debug-toolbar-header").click(function() {
            $('#' + $(this).attr('id') + '-body').toggle('fade');
            return false;
        });
    });

});