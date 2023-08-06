// const {Vue} = require("vue")
// const {Vue} = require("vue")
const {ipcRenderer} = require('electron')
const app = new Vue({
    el: "#app",
    data: {
        message: "hello"
    },
    methods: {
        getStock: () => {
            ipcRenderer.invoke("DP");
        }
    }
});