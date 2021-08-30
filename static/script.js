<script>
$(".unbox .box_title, .unbox .heading").on("click", function(){
    $(this).parent().toggleClass("is-active");
});

function playSound(btn) {
    var src_mp3 = btn.attr("data-src-mp3");
    var src_ogg = btn.attr("data-src-ogg");

    if (supportAudioHtml5()){
        playHtml5(src_mp3, src_ogg);
    }else if (supportAudioFlash()){
        playFlash(src_mp3, src_ogg);
    }    else {
        playRaw(src_mp3, src_ogg);
    }
}

function supportAudioHtml5(){
    var audioTag  = document.createElement('audio');
    try{
        return ( !!(audioTag.canPlayType)
                 && ( ( audioTag.canPlayType("audio/mpeg") != "no" && audioTag.canPlayType("audio/mpeg") != "" )
                 || ( audioTag.canPlayType("audio/ogg") != "no" && audioTag.canPlayType("audio/ogg") != "" ) ) );     
    }catch(e){
        return false;
    } 
}

function supportAudioFlash(){
    var flashinstalled = 0;
    var flashversion = 0;
    if (navigator.plugins && navigator.plugins.length){
        x = navigator.plugins["Shockwave Flash"];
        if (x){
            flashinstalled = 2;
            if (x.description){
                y = x.description;
                flashversion = y.charAt(y.indexOf('.')-1);
            }
        }
        else{
            flashinstalled = 1;
        }
        if (navigator.plugins["Shockwave Flash 2.0"]){
            flashinstalled = 2;
            flashversion = 2;
        }
    }
    else if (navigator.mimeTypes && navigator.mimeTypes.length){
        x = navigator.mimeTypes['application/x-shockwave-flash'];
        if (x && x.enabledPlugin)
            flashinstalled = 2;
        else
            flashinstalled = 1;
    }
    else{
        for(var i=7; i>0; i--){
            flashVersion = 0;
            try{
                var flash = new ActiveXObject("ShockwaveFlash.ShockwaveFlash." + i);
                flashVersion = i;
                return (flashVersion > 0)
            }
            catch(e){}
        }
    }
    return (flashinstalled > 0);
}

function playHtml5(src_mp3, src_ogg){
    //use appropriate source
    var audio = new Audio("");
    if (audio.canPlayType("audio/mpeg") != "no" && audio.canPlayType("audio/mpeg") != "")
        audio = new Audio(src_mp3);
    else if (audio.canPlayType("audio/ogg") != "no" && audio.canPlayType("audio/ogg") != "")
        audio = new Audio(src_ogg);

    //play
    audio.addEventListener("error", function(e){alert("Apologies, the sound is not available.");});
    audio.play();
}

function playFlash(src_mp3, src_ogg){
    var src_flash ="#skAssetUrl('/external/flash/speaker.swf?song_url=" +  src_mp3 + "&autoplay=true')";
    if (navigator.plugins && navigator.mimeTypes && navigator.mimeTypes.length) { // netscape plugin architecture
        $("body").append("<embed type='application/x-shockwave-flash' src='" + src_flash + "' width='0' height='0'></embed>");
    }else{ // PC I
        $("body").append("<object type='application/x-shockwave-flash' width='0' height='0' codebase='https://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,40,0' data='" + src_flash + "'><param name='wmode' value='transparent'/><param name='movie' value='" + src_flash + "'/><embed src='" + src_flash + "' width='0' height='0' ></embed></object>");
    }
}

function playRaw(src_mp3, src_ogg){
    window.open(src_mp3, "Sound", "menubar=no, status=no, scrollbars=no, menubar=no, width=200, height=100");
}

function bindAudioButtons() {
    $(".audio_play_button").off('click').click(function(){
        playSound($(this));
    });
}

$(playSound($(".phons_n_am>.audio_play_button")));

$(function() {
    bindAudioButtons();
});
(function($){
    var CustomSelector = function(element){
        var elem = $(element);
        var obj = this;

        // custom label
        obj.csl = elem.prev("#dictionary-selector");
        if(!obj.csl) return;
        
        // custom menu
        obj.csm = $(".csm");

        // set the padlock
        $('.csm a').each(function() {
            var t = $(this);
            if(t.attr("data-locked")=="true")
                t.append("<i class='locked'></i>");
        });

        var parent = $(".mainsearch");
        var topCsm = parent.offset().top + parent.height() + 10;
        var maxHeight = $(window).height() - topCsm;
        var heightCsm = obj.csm.css('height').replace("px", "");

        if(heightCsm > maxHeight) {
            obj.csm.css('max-height', maxHeight + "px");
            obj.csm.css('overflow-y', "scroll");
        } else {
            obj.csm.css('max-height', "");
            obj.csm.css('overflow-y', "");
        }
        $(window).resize(function(){
            var maxHeight = $(window).height() - topCsm;
            if(heightCsm > maxHeight) {
                obj.csm.css('max-height', maxHeight + "px");
                obj.csm.css('overflow-y', "scroll");
            } else {
                obj.csm.css('max-height', "");
                obj.csm.css('overflow-y', "");
            }
        });

        // refresh on change
        elem.change(function(){
            obj.refresh();
        });

        // select
        obj.csm.find("a").click(function(){
            elem.val($(this).attr("data-value"));
            elem.change();
        });

        obj.refresh = function() {
            var val = elem.val();
            obj.csm.find(".icon-tick").remove();
            obj.csm.find("a[data-value='" + val + "'] span:first").prepend("<i class='icon-tick oup_icons'></i>");
            obj.csl.find("span").html(obj.csm.find("a[data-value='" + val + "']").attr("data-label"));
        };

        obj.refresh();
    };

    $.fn.customSelector = function(settings) {
        this.each(function() {new CustomSelector(this, settings);});
    };
})(jQuery);/*! jQuery UI - v1.11.4 - 2016-01-13
* http://jqueryui.com
* Includes: effect.js, effect-slide.js
* Copyright jQuery Foundation and other contributors; Licensed MIT */

</script>