gogotester_python
===============
[gogotester](https://github.com/azzvx/gogotester)的(非官方)python命令行版本，唯一的作用就是扫描在天朝范围内能用的Google IP

### 警告：alpha版本测试的时候代码有一定概率卡死，重写SSL_Test以后未发现卡死现象，但是并不代表不会有卡死的可能 ###

## User Guide ##
代码在windows上开发，环境为gevent-1.0.1+python-2.7.7
如果在python-2.7.8及以下版本中使用请先安装pip然后

`pip install gevent`

如果是python-2.7.9+就可以直接安装gevent啦

> 用pip的原因是windows下面pip能愉快的装上gevent╮(￣▽￣")╭ 

然后进入命令行，`python Main_Gevent.py` 就好啦~~~ 

##Others##



嘛……虽然说*nix可以用mono跑.net但是python毕竟是自带的库，也就少了很多奇怪的麻烦

>由于我只是想在宿舍装个树莓派没事跑跑ip所以设定都是写死在脚本里面的……我找个时间给他改成在配置文件里面……嗯╮(￣▽￣")╭ 

脑洞已经填了

以及python的多线程实在是有点烧机器而且用多线程等IO等完IO就没啥事这样奇怪的需求我还是默默用gevent吧……而且我直接patch\_os, patch\_socket, patch\_ssl【伦家才不会去在意这玩意怎么工作的呢只要跑起来就好了哼~！】

代码写的很乱不要在意……每个模块自带测试嗯， 串行执行一定没问题-，-

> 然而gevent并行跑起来我也不知道会怎样╮(￣▽￣")╭ 

也许我会找时间画GUI不过更有可能是我弃坑……

GAE配置文件自动生成什么的还在计划中……核心已经写好了嗯


#祝方校长【zhang】长【chang】命五十八#

中国人民会记住您的