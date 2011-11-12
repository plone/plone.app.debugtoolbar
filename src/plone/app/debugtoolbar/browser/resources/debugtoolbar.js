
/**
 * jQuery Cookie plugin
 *
 * Copyright (c) 2010 Klaus Hartl (stilbuero.de)
 * Dual licensed under the MIT and GPL licenses:
 * http://www.opensource.org/licenses/mit-license.php
 * http://www.gnu.org/licenses/gpl.html
 *
 */
_read_debug_cookie = function() {
    key = "plone.app.debugtoolbar";
    var result, decode = decodeURIComponent;
    var cookie =  (result = new RegExp('(?:^|; )' + encodeURIComponent(key) + '=([^;]*)').exec(document.cookie)) ? decode(result[1]) : null;

    if(cookie == null) {
        return {};
    }

    return jQuery.parseJSON(cookie);
};

jQuery(function($) {
    
    $(function() {
        $("#debug-toolbar").prependTo("html body");
        $("#debug-toolbar-trigger").prependTo("html body");

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
        });
        
    });

});