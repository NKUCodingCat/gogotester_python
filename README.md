gogotester_python
===============
[gogotester](https://github.com/azzvx/gogotester)的(非官方)python命令行版本，唯一的作用就是扫描在天朝范围内能用的Google IP

戳这个下载→[GoGoTester_Python_Ver_Download](https://nodeload.github.com/NKUCodingCat/gogotester_python/legacy.zip/master)

#先看完README再用#

## User Guide ##
代码在windows上开发，环境为IPy-0.83+gevent-1.0.1+python-2.7.7

windows的小伙伴可以直接点开/packed文件夹然后点击gogotester_python.exe

照着[用户指南](https://github.com/NKUCodingCat/gogotester_python/wiki/How-to-use-it-gracefully)做， 不行的话请直接运行源代码

Ver 0.7.2 α 版本

**Windows XP + 可用**

**Ubuntu 14.04+, lubuntu 15.04 测试通过**

欢迎提供兼容性信息~

### 如何运行源代码 ###

如果在python-2.7.8及以下版本中使用请先安装pip然后

`pip install gevent`

`pip install IPy`

如果是python-2.7.9+就可以直接安装gevent和IPy啦

> 用pip的原因是windows下面pip能愉快的装上gevent╮(￣▽￣")╭ 

然后进入命令行，`python Main_Gevent.py` 就好啦~~~ 

##Others##


嘛……虽然说*nix可以用mono跑.net但是python毕竟是自带的库，也就少了很多奇怪的麻烦

>由于我只是想在宿舍装个树莓派没事跑跑ip所以设定都是写死在脚本里面的……我找个时间给他改成在配置文件里面……嗯╮(￣▽￣")╭ 

脑洞已经填了

以及python的多线程实在是有点烧机器而且用多线程等IO等完IO就没啥事这样奇怪的需求我还是默默用gevent吧……而且我直接patch\_os, patch\_socket, patch\_ssl【伦家才不会去在意这玩意怎么工作的呢只要跑起来就好了哼~！】

代码写的很乱不要在意……每个模块自带测试嗯， 串行执行一定没问题-，-

> 然而gevent并行跑起来我也不知道会怎样╮(￣▽￣")╭ 
>
> 添加了ip数量上限以后目测更有可能出问题嗯

也许我会找时间画GUI不过更有可能是我弃坑……

GAE配置文件自动生成什么的还在计划中……核心已经写好了嗯


#祝方校长【zhang】长【chang】命五十八#

中国人民会记住您的

##尼玛不好好复习还写代码！##

嗯结构求不挂，还有毛概

# 一些警告 #

### alpha版本测试的时候代码有一定概率卡死，重写SSL_Test以后未发现卡死现象，但是并不代表不会有卡死的可能 ###


######  性能测试结果及若干指南 ######


2015.06.07 凌晨更新0.5.0α版，测了一下10W v4IP 和 3W v6IP 的情况，把IP转为int存储以后内存峰值占用250M-，稳定运行160M+

(￣▽￣") 如果氖的IP库比较多可用的话建议SSL线程数是socket的20%或者30%……嗯反正多一点少一点也没啥╮(￣▽￣")╭ 


######  Mac OS X 中的问题 ######
openssl on OSX 版本是0.9.8因此不支持找GVS

所以你们看着办吧，自己升级一下
