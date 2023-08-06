// import Vue from "vue";
const {shell, dialog} = require('electron').remote
const {ipcRenderer,remote} = require('electron')
var fs = require('fs')

const vm = new Vue({
    el: "#app",
    data: {},
    methods: {
        chooseFile: () => {
            // shell.showItemInFolder("D://")
            console.log("sss")
            let file = dialog.showOpenDialog();

        }
    }
})