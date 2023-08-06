const {Menu} = require('electron').remote;
const menuTemplate = [{
    label: '文件',
    submenu: [{
        label: '打开'
    }, {
        role: 'recentDocuments'
    }, {
        label: '保存'
    },
        {
            label: "另存为"
        },
        {
            label: '开发工具',
            role: 'toggleDevTools',
        },
        {
            type: "separator",
        },
        {
            label: "退出",
            accelerate: 'alt+Q',
            role: "quit"
        }
    ]
},
    {
        label: '工具',
        submenu: [{
            label: 'DP(性能试验)',
            accelerate: 'alt+1',
            // click: () => {
            //     ipcRenderer.invoke("DP")
            // }
        }]
    },
    {
        label: '编辑',
        submenu: [{
            label: '撤销',
            // accelerator: 'ctrl+z',
            role: 'undo'
        }, {
            label: '重做',
            // accelerator: 'ctrl+shift+z',
            role: 'redo'
        }]
    },
    {
        label: '设置',
        submenu: [{
            label: '字体设置'
        }, {
            label: '全屏',
            type: 'checkbox',
            role: 'togglefullscreen'
        }, {
            label: '放大',
            role: 'zoomIn'
        }, {
            label: '缩小',
            role: 'zoomOut'
        }, {
            label: '重置窗口大小',
            role: 'resetZoom'
        }]
    },
    {
        label: '帮助',
        submenu: [{
            label: '帮助',
            // accelerator: 'ctrl+h',
            role: 'help'
        }, {
            label: '关于',
            role: 'about',
        }]
    }
];

const appMenu = Menu.buildFromTemplate(menuTemplate);

Menu.setApplicationMenu(appMenu);