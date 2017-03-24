/**
 * Created by kidozh on 2017/2/10.
 */
var value, orig1, orig2, dv, panes = 2, highlight = true, connect = null, collapse = false;
var editorA,editorB = '';
var target = document.getElementById('diff');
function initUI() {
    if (value == null) return;
    var target = document.getElementById("view");
    target.innerHTML = "";
    dv = CodeMirror.MergeView(target, {
        value: value,
        origLeft: panes == 3 ? orig1 : null,
        orig: orig2,
        lineNumbers: true,
        mode: "text/html",
        highlightDifferences: highlight,
        connect: connect,
        collapseIdentical: collapse
    });
}

function mergeViewHeight(mergeView) {
    function editorHeight(editor) {
        if (!editor) return 0;
        return editor.getScrollInfo().height;
    }
    return Math.max(editorHeight(mergeView.leftOriginal()),
        editorHeight(mergeView.editor()),
        editorHeight(mergeView.rightOriginal()));
}

function showDiff(){
    var target = document.getElementById("diff");
    target.innerHTML = "";
    dv = CodeMirror.MergeView(target, {
        value: editorA.getValue(),
        origLeft: null,
        orig: editorB.getValue(),
        lineNumbers: true,
        //mode: "text/html",
        highlightDifferences: highlight,
        connect: connect,
        collapseIdentical: collapse
    });
}

function resize(mergeView) {
    var height = mergeViewHeight(mergeView);
    for(;;) {
        if (mergeView.leftOriginal())
            mergeView.leftOriginal().setSize(null, height);
        mergeView.editor().setSize(null, height);
        if (mergeView.rightOriginal())
            mergeView.rightOriginal().setSize(null, height);

        var newHeight = mergeViewHeight(mergeView);
        if (newHeight >= height) break;
        else height = newHeight;
    }
    mergeView.wrap.style.height = height + "px";
}

$(document).ready(function(){
    var codemirror_config = {
        lineNumbers: true,
        lineWrapping:true,
        mode: "gfm"
    };

    //console.log(editorA);

    // set update
    /*editorA.on('change',showDiff);
    editorB.on('change',showDiff);*/
    /*from merge view*/
    //initUI();
    var formVueModel = new Vue({
        el:'#code-form',
        data:{
            selectedLanguage:'char'
        },
        watch:{
            selectedLanguage:function(curLanguage){
                var target = document.getElementById("diff");
                target.innerHTML = "";
                console.log(this.selectedLanguage);
                var mode = '';
                if (this.selectedLanguage == 'char'){
                    mode = 'text/plain';
                }
                else if(this.selectedLanguage == 'c/c++'){
                    mode = 'text/x-c++src';
                }
                editorA.setOption('mode',mode);
                editorB.setOption('mode',mode);
            }
        }
    });
    editorA =  CodeMirror.fromTextArea(document.getElementById("codeA"), codemirror_config);
    editorB = CodeMirror.fromTextArea(document.getElementById("codeB"), codemirror_config);
});

