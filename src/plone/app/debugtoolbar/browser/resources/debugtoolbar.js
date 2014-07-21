
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
    this.submitHistory = [];
    this.historyPosition = -1;

    if (path == undefined) {
        path = "./@@plone.app.debugtoolbar.interactive.response";
    }
    this.path = path;
};
InteractivePrompt.prototype.submit = function(line) {
    var out = this.target;
    this.submitHistory.push(line);
    this.historyPosition = this.submitHistory.length;

    jQuery.post(
        this.path,
        {'line': line},
        function(data) {
            if(data != '') {
                jQuery(out).append(data);
                jQuery(out).animate({ scrollTop: jQuery(out).prop('scrollHeight') }, "fast");
            }
        }
    );
};

function TalesTester(target, path) {
    this.target = target;
    this.submitHistory = [];
    this.historyPosition = -1;

    if (path == undefined) {
        path = "./@@plone.app.debugtoolbar.interactive.tales";
    }
    this.path = path;
};
TalesTester.prototype.submit = function(line) {
    var out = this.target;
    this.submitHistory.push(line);
    this.historyPosition = this.submitHistory.length;

    jQuery.post(
        this.path,
        {'line': line},
        function(data) {
            if(data != '') {
                jQuery(out).html(data);
            }
        }
    );
};

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

        // Section open/close
        $(".debug-toolbar-section-header").click(function() {
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

        $("#debug-toolbar-interactive-input").keyup(function (e) {
            if(e.keyCode == 13) { // enter
                var line = $(this).val();
                prompt.submit(line);
                $(this).val("");
                return false;    
            } else if(e.keyCode == 38) { // up
                if(prompt.historyPosition > 0 && prompt.submitHistory.length > 0) {
                    --prompt.historyPosition;
                    $(this).val(prompt.submitHistory[prompt.historyPosition]);
                    return false;
                }
            } else if(e.keyCode == 40) { // down
                if(prompt.historyPosition < prompt.submitHistory.length - 1 && prompt.submitHistory.length > 0) {
                    ++prompt.historyPosition;
                    $(this).val(prompt.submitHistory[prompt.historyPosition]);
                    return false;
                } else if(prompt.historyPosition >= prompt.submitHistory.length - 1) {
                    prompt.historyPosition = prompt.submitHistory.length;
                    $(this).val("");
                    return false;
                }
            }
        });

        // TALES tester
        var talesTester = new TalesTester("#debug-toolbar-tales-out");
        $("#debug-toolbar-tales-input-submit").click(function () {
            var line = $("#debug-toolbar-tales-input").val();
            talesTester.submit(line);
            return false;
        });

        $("#debug-toolbar-tales-input").keyup(function (e) {
            if(e.keyCode == 13) { // enter
                var line = $(this).val();
                talesTester.submit(line);
                return false;    
            } else if(e.keyCode == 38) { // up
                if(talesTester.historyPosition > 0 && talesTester.submitHistory.length > 0) {
                    --talesTester.historyPosition;
                    $(this).val(talesTester.submitHistory[talesTester.historyPosition]);
                    return false;
                }
            } else if(e.keyCode == 40) { // down
                if(talesTester.historyPosition < talesTester.submitHistory.length - 1 && talesTester.submitHistory.length > 0) {
                    ++talesTester.historyPosition;
                    $(this).val(talesTester.submitHistory[talesTester.historyPosition]);
                    return false;
                } else if(talesTester.historyPosition >= talesTester.submitHistory.length - 1) {
                    talesTester.historyPosition = talesTester.submitHistory.length;
                    $(this).val("");
                    return false;
                }
            }
        });

        $('#debug-toolbar-reload-body form').submit(function(e){
            e.preventDefault();
            $.ajax({
                url: $(this).attr('action'),
                method: 'POST',
                success: function(){
                    window.location.reload();
                }
            });
        });
    });

});
