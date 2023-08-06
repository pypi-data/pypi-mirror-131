const {app, BrowserWindow, ipcMain} = require('electron')

function createWindow() {
    const win = new BrowserWindow({
        width: 1200,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            webSecurity: false,
            preload: __dirname + "/js/menu.js",  // 加载菜单栏
            enableRemoteModule: true,
        }
    })
    // 路径是相对于package.json文件写的
    console.log('文件所在目录是' + __dirname + "/js/menu.js")
    console.log('命令运行目录是' + process.cwd())
    win.loadFile('./electron/html/index.html').then(r => {
        console.log(r)
    });
    ipcMain.handle("DP", (event) => {
        win.loadFile('./electron/html/dp.html');
    })
}


app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow()
    }
})