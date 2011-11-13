
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

function InteractivePrompt(target, path) {
    this.target = target;
    if (path == undefined) {
        path = "./@@plone.app.debugtoolbar.interactive.response";
    }
    this.path = path;
}
InteractivePrompt.prototype.submit = function(line) {
    var out = this.target;

    jQuery.post(
        this.path,
        {'line': line},
        function(data) {
            if(data != '') {
                jQuery(out).append(data);
                jQuery(out).animate({ scrollTop: jQuery(out).attr('scrollHeight') }, "fast");
            }
        }
    );
}

jQuery(function($) {
    
    $(function() {

        // Move debug toolbar to the top
        $("#debug-toolbar").prependTo("html body");
        $("#debug-toolbar-trigger").prependTo("html body");

        // Action for trigger
        $("#debug-toolbar-trigger").click(function() {
            $('#debug-toolbar').slideDown();
            return false;
        });
        
        $("#debug-toolbar-close").click(function() {
            $('#debug-toolbar').slideUp();
            return false;
        });

        // Panel open/close
        $(".debug-toolbar-header").click(function() {
            $('#' + $(this).attr('id') + '-body').toggle('fade');
        });

        // Interactive debug panel
        var prompt = new InteractivePrompt("#debug-toolbar-interactive-out");
        $("#debug-toolbar-interactive-input-submit").click(function () {
            var line = $("#debug-toolbar-interactive-input").val();
            prompt.submit(line);
            $("#debug-toolbar-interactive-input").val("");
            return false;
        });

        $("#debug-toolbar-interactive-input").keypress(function (e) {
            if(e.keyCode == 13) {
                var line = $(this).val();
                prompt.submit(line);
                $(this).val("");
                return false;    
            }
        });
        


    });

});