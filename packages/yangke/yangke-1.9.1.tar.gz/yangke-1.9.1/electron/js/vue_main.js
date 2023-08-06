// import {createApp} from 'vue';
var createApp = require('vue').createApp;
// import App from '../component_vue/App.vue';
var App = require('../component_vue/App')
//
// createApp(App).mount('#app');
createApp(App).mount('#app')
//
// const fs = require('fs');
// // import {lowerCase} from 'lodash'
// var lodash = require('lodash')
//
// // fs.readFile('electron/index.js', function (err, data){
// //     if (err) return console.error(err);
// //     console.log(data.toString());
// // })
//
// console.log("over程序执行结束")
//
// // console.log(lodash.chunk(['a', 'b', 'c', 'd'], 2));
// console.log(lodash.lowerCase("HTML"));