const tab1 = {
    props: ['home'], // 组件的自定义属性，外部通过这个参数传递数据给组件，方便在template中使用
    template: `<div class="demo-tab">Home component</div>`
};
const tab2 = {
    template: `<div class="demo-tab">Post component</div>`
};
const tab3 = {
    template: `<div class="demo-tab">负荷曲线</div>`
};
const tab4 = {
    template: `<div class="demo-tab">修正热网效率</div>`
};
const tab5 = {
    template: `<div class="demo-tab">方法校对</div>`
};

// Vue.createApp() 创建Vue实例，和vue2中的new Vue()方法功能基本相同，但进行了一些优化
const app = Vue.createApp({
    data() {
        return {
            currentTab: '调峰',
            tabs: ['调峰', '煤耗', '负荷曲线', '修正', '方法校对'],
            header: "调峰峰值测算表",
            供热计划温度: 90,
            三期回水流量: 10000,
            四期回水流量: 11000,
            回水流量: [0, 4500, undefined, 6000, undefined],
            是否供热: [true, true, true, true, true],
            是否切缸: [true, true, true, true, true],
            供水温度: [90, 106, 83, 84, 91],
            回水温度: [50, 51, 51, 49, 49],
            日供热量: [0, undefined, undefined, undefined, undefined],
            供热负荷: [0, undefined, undefined, undefined, undefined],
            供热当量电负荷: [0, undefined, undefined, undefined, undefined],
            上限电负荷: [0, undefined, undefined, undefined, undefined],
            下限电负荷: [0, undefined, undefined, undefined, undefined],

            标煤价格: 806,
            税后上网电价: 0.33,
            税后热价: 25.69,
            单位煤耗变动: 2.74,
            考虑电量比例: 0,
            count: 0,
        }
    },
    methods: {
        increment() {
            // this指向组件实例
            this.count++

        },
        inner_change(list, i) {  // 内部方法，不由html中指定
            if (i === 0) {
                if (list[0] === false) {
                    list = [false, false, false, false, false]
                } else {
                    list = [true, true, true, true, true]
                }
            } else {
                list[0] = list.slice(1).indexOf(true) !== -1;
            }
            return list
        },
        change(tab, i) {  // checkbox的状态更改时执行该方法
            console.log(tab, i)
            if (tab === 0) {
                this.是否供热 = this.inner_change(this.是否供热, i)
            } else {
                this.是否切缸 = this.inner_change(this.是否切缸, i)
            }
        },
        calculate() {  // 计算按钮被点击时执行该方法
            console.log("开始计算")
            this.回水流量[2] = this.三期回水流量 - Number(this.回水流量[1]);
            this.回水流量[4] = this.四期回水流量 - Number(this.回水流量[3]);
            this.回水流量[0] = this.三期回水流量 + this.四期回水流量;

        }
    },
    computed: {
        currentTabComponent() {
            return 'tab-' + this.currentTab.toLowerCase();
        }
    },
    components: {
        'tab-调峰': tab1,
        'tab-煤耗': tab2,
        'tab-负荷曲线': tab3,
        'tab-修正': tab4,
        'tab-方法校对': tab5,
    }
})


// 将创建的vue实例对象app挂载到html中的#app节点上
const vm = app.mount('#app')

// vm.increment()

// console.log("vm.count="+vm.count)
//
// console.log("vm.是否供热="+vm.是否供热)