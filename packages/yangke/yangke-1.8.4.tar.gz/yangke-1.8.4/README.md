# 1 概述

## 1.1 安装

一个Python的常用工具类库，主要用于股票预测等功能，同时提供各类优化算法的调用工具。 联系方式：540673597@qq.com

安装方法一：

    pip install yangke

使用该命令为最小化yangke安装，只会安装yangke库的必要依赖。因yangke库中包含多个模块，当使用具体模块时， 可能存在依赖不全的问题，此时需要根据提示，继续安装使用的模块的必要依赖。

安装方法二：

    pip install yangke[All]

使用该命令会安装yangke库中所有模块的依赖。yangke库中包含的模块可以使1.2节测试方法进行查询。

## 1.2 测试是否安装成功

    import yangke
    yangke.info()

如果安装成功，则提示如下图所示。
![图片无法显示](./document/figures/img.png)

# 2 小功能

# 2.1 多彩的logger输出

在test.py中输入以下代码：

    from yangke.common.config import logger

    logger.debug("debug from yangke logger")
    logger.info("info from yangke logger")
    logger.warning("warning from yangke logger")
    logger.error("error from yangke logger")
    logger.critical("critical from yangke logger")

运行结果如下图所示：

![图片无法显示](./document/figures/img_1.png)

### 高级日志配置

使用settings.yaml文件配置日志输出的格式。 在test.py同目录下创建settings.yaml文件，写入以下内容：

    logger:
      dateFormat: 'YYYY/MM/DD HH:mm:ss'
      format: '{time} - {level} - {module}:{function}:{line} - {message}'
      level: 10  # 可取0，10，20，30，40，50，分别代表notset, debug, info, warn, error, fatal
      levelColor:
        DEBUG: yellow  # 小写表示前景色
        INFO: "GREEN"  # 大写表示后景色

则运行中日志按该定义输出，如下图所示：

![图片无法显示](./document/figures/img_4.png)

日志的格式定义参数含义可以参见loguru的官方说明文档，本类库提供了yaml配置日志的途径，方便用户自定义。

可以自定义的内容有：

* 不同的level级别使用不同的样式；
* 不同的field（即time, level, module）使用不同的样式，loguru的默认样式就是这种形式。
* 日志文字样式
    * 前景色，小写的颜色或"fg <rgb>"定义的颜色
    * 背景色，大写的颜色或"bg <rgb>"定义的颜色
    * 字体样式，下划线、斜体、加粗等，定义参见loguru说明。
* 日期格式，如 'YYYY/MM/DD HH:mm:ss'
* 日志格式，如 '{time} - {level} - {module}:{function}:{line} - {message}'
* field的对齐方式

## 2.2 给python方法添加日志环境提示

在程序运行进入某些关键函数或方法时，会生成进入该函数或方法的日志域。使用示例如下。

在test.py中输入以下代码：

    from yangke.common.config import logger, loggingTitleCall


    @loggingTitleCall(title="初始化mysql数据库连接")
    def init_mysql():
        logger.info("测试mysql是否可用")
        logger.info("连接mysql")
        logger.info("mysql连接成功")


    init_mysql()

运行结果如下图所示：

![图片无法显示](./document/figures/img_2.png)

也可以临时更改某个方法中的logger级别，定制不同的logger输出格式，详细用法参见项目源码。

## 2.3 windows系统运行命令

运行windows系统的命令，有两个方法。

    from yangke.core import *

    runAsAdmin('echo "1111" > ssssss.txt', popup=True)
    result = runCMD('echo "11111"', charset="GBK", wait_for_result=True, output_type="RETURN")
    print(result)

运行结果如下图所示：

![图片无法显示](./document/figures/img_3.png)
说明：

    runAsAdmin(cmd, cwd=None, charset="gbk", python=None, popup=True) 

该方法以管理员方式运行命令，在windows系统上会弹出确认窗口，询问是否以管理员方式运行，如果不需要
弹出确认窗口，可以设置参数popup=False，但这实际上利用了windows的漏洞，在win10上会被defender当做病毒拦截，在 win7上能正常运行。

    runCMD(command: str, charset: str = "utf8", wait_for_result: bool = True, cwd=None,
           output_type: str = "RETURN", timeout=None)

该方法可以返回第三方命令的执行结果给当前python主进程，如2.3节示例的运行结果，这在很多时候是很有用的。

# 2.4 判断是否安装某python库

    from yangke.core import existModule

    existModule("pandas")

# 2.5 读取csv或txt至pandas.DataFrame中

    from yangke.common.fileOperate import read_csv_ex

    read_csv_ex(file)

  该方法可以处理双引号括起来的跨行的元素，解决各类常见编码问题，解决各行元素数量不同导致的读取报错问题。
  该方法可解决以下错误：

> UnicodeDecodeError 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
 
> pandas.errors.ParserError: Error tokenizing data. C error: Expected 21 fields in line 45, saw 41

该方法几乎可以读入任何形式的csv文件和txt文件内容，解决了数据读入的问题，后续的数据清洗就可以进行下去了。

该方法的其他参数有：
read_csv_ex(file, sep=None, header="infer", skiprows=None, error_bad_lines=True, nrows=None, index_col=None,
                low_memory=None, na_values=" ")

# 2.6 yangke.base中的小工具

    from yangke.base import *

然后可以使用以下方法

* 读取yaml文件，返回对应的字典对象或列表对象

> readFromYAML(file: str, encoding="utf8")

* 获取当前电脑的IP地址

> get_localhost_ip()

* 获取文本文件的编码

> get_encoding_of_file(file)

* 将图片转换为base64格式

输入图片可以是 url, ndarray或本地的图片文件路径
> pic2base64(pic)

* 将图片转换为ndarray格式

输入图片可以是 url, ndarray或本地的图片文件路径
> pic2ndarray(pic)

* 将xls格式的excel文件另存为xlsx或csv

该方法利用的是本地安装的Office或WPS，因此只要本地的Office或WPS能正常打开的xls文件都可以成功另存，具有极强的适应性。其他excel类库在某些情况下无法另存或存在编码错误的问题。
> save_as_xlsx(file, engine="WPS", ext="xlsx", visible=False)

* 开启新线程运行指定的目标函数

> start_threads(targets, args_list=())

* 遍历目录下的文件

> yield_all_file(folder, filter_=None, ignore_temp_file: bool = True)

* 装饰器方法
  >> @run_once 确保修饰的方法只被调用一次，运行中会忽略第一次以后的调用
  > 
  >> @auto_save_para

# 2 Stock模块（股票）
