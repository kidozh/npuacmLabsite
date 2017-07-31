/**
 * Created by exbot on 17-7-19.
 */
var languageOverrides = {
    js: 'javascript',
    html: 'xml'
};
var hashto;
emojify.setConfig({ img_dir: 'emoji' });
var md = markdownit({
    html: true,
    linkify: true,
    highlight: function(code, lang){
        if(languageOverrides[lang]) lang = languageOverrides[lang];
        console.log(lang);
        if(lang && hljs.getLanguage(lang)){
            try {
                return hljs.highlight(lang, code).value;
            }
            catch(e){
                console.error(e);

            }
        }
        return '';
    }
})
    .use(markdownitFootnote);


function updateHash(){
    window.location.hash = btoa( // base64 so url-safe
        RawDeflate.deflate( // gzip
            unescape(encodeURIComponent( // convert to utf8
                editor.getValue()
            ))
        )
    );
}

function update(e){
    setOutput(e.getValue());
    clearTimeout(hashto);
    hashto = setTimeout(updateHash, 1000);
    // add callback
    console.log('Update!!!')
    wrt_vm.broswer_sync_time = new Date();
}
function setOutput(val){
    val = val.replace(/<equation>((.*?\n)*?.*?)<\/equation>/ig, function(a, b){
        return '<img src="http://latex.codecogs.com/png.latex?' + encodeURIComponent(b) + '" />';
    });

    var out = document.getElementById('out');
    var old = out.cloneNode(true);
    out.innerHTML = md.render(val);
    emojify.run(out);

    var allold = old.getElementsByTagName("*");
    if (allold === undefined) return;

    var allnew = out.getElementsByTagName("*");
    if (allnew === undefined) return;

    for (var i = 0, max = Math.min(allold.length, allnew.length); i < max; i++) {
        if (!allold[i].isEqualNode(allnew[i])) {
            out.scrollTop = allnew[i].offsetTop;
            return;
        }
    }
}

var editor = CodeMirror.fromTextArea(document.getElementById('markdown-input'), {
    mode: 'gfm',
    lineNumbers: true,
    matchBrackets: true,
    lineWrapping: true,
    theme: 'base16-light',
    extraKeys: {
        "Enter": "newlineAndIndentContinueMarkdownList",
        "F11": function(cm) {
            cm.setOption("fullScreen", !cm.getOption("fullScreen"));
        },
        "Esc": function(cm) {
            if (cm.getOption("fullScreen")) cm.setOption("fullScreen", false);
        }
    }
});
editor.on('change', update);




document.addEventListener('drop', function(e){
    e.preventDefault();
    e.stopPropagation();

    var reader = new FileReader();
    reader.onload = function(e){
        editor.setValue(e.target.result);
    };

    reader.readAsText(e.dataTransfer.files[0]);
}, false);




function save(code, name){
    var blob = new Blob([code], { type: 'text/plain' });
    if(window.saveAs){
        window.saveAs(blob, name);
    }else if(navigator.saveBlob){
        navigator.saveBlob(blob, name);
    }else{
        url = URL.createObjectURL(blob);
        var link = document.createElement("a");
        link.setAttribute("href",url);
        link.setAttribute("download",name);
        var event = document.createEvent('MouseEvents');
        event.initMouseEvent('click', true, true, window, 1, 0, 0, 0, 0, false, false, false, false, 0, null);
        link.dispatchEvent(event);
    }

}



var menuVisible = false;
var menu = document.getElementById('menu');

function showMenu() {
    menuVisible = true;
    menu.style.display = 'block';
}

function hideMenu() {
    menuVisible = false;
    menu.style.display = 'none';
}

/* document.getElementById('close-menu').addEventListener('click', function(){
 hideMenu();
 });*/




document.addEventListener('keydown', function(e){
    if(e.keyCode == 83 && (e.ctrlKey || e.metaKey)){
        e.shiftKey ? showMenu() : saveAsMarkdown();

        e.preventDefault();
        return false;
    }

    if(e.keyCode === 27 && menuVisible){
        hideMenu();

        e.preventDefault();
        return false;
    }
});




function updateHash(){
    window.location.hash = btoa( // base64 so url-safe
        RawDeflate.deflate( // gzip
            unescape(encodeURIComponent( // convert to utf8
                editor.getValue()
            ))
        )
    );
}


if(window.location.hash){
    var h = window.location.hash.replace(/^#/, '');
    if(h.slice(0,5) == 'view:'){
        setOutput(decodeURIComponent(escape(RawDeflate.inflate(atob(h.slice(5))))));
        document.body.className = 'view';
    }else{
        editor.setValue(
            decodeURIComponent(escape(
                RawDeflate.inflate(
                    atob(
                        h
                    )
                )
            ))
        );
        update(editor);
        editor.focus();
    }
}else{
    update(editor);
    editor.focus();
}