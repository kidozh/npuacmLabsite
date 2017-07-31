/**
 * Created by exbot on 17-7-29.
 */
var markdownEditor = require('./markdown-editor.vue');

var VueSimplemde = {
    markdownEditor: markdownEditor,
    install: function(Vue) {
        Vue.component('markdown-editor', markdownEditor);
    },
};

module.exports = VueSimplemde;