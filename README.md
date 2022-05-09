# Easy DDNS 客户端 -- 领域驱动设计的轻量级 APP

![design-standards](https://img.shields.io/static/v1?label=design-standards&message=DDD&color=informational)
![platform](https://img.shields.io/badge/platform-windows%3Alinux%3Aunix-brightgreen)
![devlanguage](https://img.shields.io/badge/language-python3.10-brightgreen)

---

## 项目介绍

基于 python 3.x 和 requests 的动态解析服务的**客户端**，支持**腾讯云(Dnspod)解析服务**。支持多域名同时解析、多域名连接状态查询，适于建站和学习领域驱动设计技术。DDNS 技术在建站、NAS、远程监控等基于域名实现的网络应用中广泛应用，其基本业务原理是将本地随时间变换的 IP 地址与远端云解析的解析记录的 IP 地址进行同步，常见的方法是**定时同步**。

## 主要特性

- [x] 支持腾讯云解析服务。
- [x] 支持 IP V4。
- [x] 基于 python 环境，支持多平台运行(如 AIX、HPUX、Solaris、Linux、Windows 等)。
- [x] 支持命令行界面(Command-Line Interface)，基于 tqdm 和 argpraser 。
- [x] 支持多个域名、子域名解析（数量以 DNS 服务网站为准）。
- [x] 支持命令行或服务方式运行。
- [x] 稳定、高速、无卡死。
- [x] 轻量，易于阅读，易于 fork 成自己的客户端。
- [x] 可单独作为工具包使用。
- [x] 读取和解析 json 配置文件。
- [x] 持续集成。

## 依赖包

> - python >=3.7
> - requests >=2.27.1
> - tqdm>=1.0.1

## 安装方法

源代码安装：

```shell
git clone git@github.com:viola-aoitech/easyddns.git
cd easy-ddns
python setup.py install
```

## 使用方法

1. 到提供 ddns 服务的网站，注册登录获得 ddns 服务的账户信息。
2. 填写注册表单[`config.json`说明](/conifg-samples/README.md).

### json 示例

```json
{
  "DNS": {
    "name": "Dnspod",
    "login": {
      "user id": "xxx",
      "user token": "xxxxxxxx"
    }
  },
  "Record 1": {
    "type": "AAAA",
    "domain name": "www.xxxx.cn",
    "ttl": "300"
  }
}
```

### 命令行运行

根据命令行提示来运行

```shell
python easyddns -h # or --help
```

### 自动解析

shell 命令行运行:

```shell
python easyddns config.json # 自动运行同步。
```

```shell
python easyddns config.json -d #显示本地和 DNS 服务器记录情况
```

### 测试方法

测试基于 pytest 简易方法, 安装完成以后，在项目根目录下运行`pytest -v -s`。

## UML 设计图

### 用例分析

![use-case](https://github.com/viola-aoitech/easyddns/blob/e7ff68c66dad55b7efd8767665e096a361446aa3/docs/pics/user-cases.png)

### 架构示图

![layers](https://github.com/viola-aoitech/easyddns/blob/e7ff68c66dad55b7efd8767665e096a361446aa3/docs/pics/EasyDDNS%20API%20layers.png)

本项目采用一个简化的[六边形架构](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software))，基于依赖转置原则，便于扩展到多个 DNS 服务 API 。例如，如果需要新加入对aliyun 动态解析 API 进行封装，那么只需要添加一个 AliyunProxy 、Aliyun Session和 login 的 python 包即可。

**各层职责说明**：
- EasyDDNS: 应用层,负责将API，封装到一个CLI脚本中。
- Serivce Layer: 应用服务层， 负责处理EasyDDNS的软件服务。
- Adaptor: 适配器层, 也称为基础设施层.负责封装远端 DNS 解析服务网站的提供的API。
- synchronization: 领域模型层，负责对本地和远端的记录进行同步。


### 领域模型视图

![domain-model](https://github.com/viola-aoitech/easyddns/blob/e7ff68c66dad55b7efd8767665e096a361446aa3/docs/pics/domain-model.png)

**业务逻辑说明：**

- DmzRecord 用以记录用户登陆信息和用户的IP信息。
- DnspodRecord 用以记录DNS的IP信息和相关记录信息。
- RecordSynchronizer 用以进行同步操作，设 DmzRecord 为主控记录，DnspodRecord 为从属记录，当DmzRecord 记录发生更新，则同时更新 DnspodRecord 的IP 信息。如果同步完成，则进行部署。

> **提示**：如果需要本项目详细设计图，可以安装 pylint 和 graphviz。在命令行运行：`pyreverse -o png src`生成本项目的详细类图和依赖关系图。

## 开源协议

- Apache License Version 2.0

## 参考资料

1. Gomaa H. Software modeling and design: UML, use cases, patterns, and software architectures[M]. Cambridge University Press, 2011.
2. SityNorth. Event-Sourced Domain Models in Python[EB/OL].
3. Percival H, Gregory B. Architecture Patterns with Python: Enabling Test-driven Development, Domain-driven Design, and Event-driven Microservices[M]. " O'Reilly Media, Inc.", 2020.
4. [What is DDNS? How does it work and how to setup DDNS?](https://www.cloudns.net/blog/what-is-dynamic-dns/)
5. [DDNS dynamic domain name resolver](https://openwrt.org/zh/docs/guide-user/services/ddns/client)

### 待完成功能

- [ ] pypi 自动安装。
- [ ] 易懂用法说明文档
- [ ] 支持 IPV6
- [ ] 支持阿里云.
- [ ] 支持 cloudfire 云.
- [ ] 支持华为云.
- [ ] 支持更多的云解析
- [ ] 自动通知功能（需配置 Email 服务设置）。

## 贡献者

- Author: viola@aoitech.net
