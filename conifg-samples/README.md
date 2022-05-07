# config json 说明

- 示例和说明如下：

```json
// 文件名：config.json
{
  "DNS": {
    "name": "Dnspod", // 云解析名称

    "login": {
      "user id": "xxx", // dnspod api 的登陆 user id
      "user token": "xxxxxxxx" // dnspod api 的登陆 user token
    }
  },

  //记录名称：以 Record 或者 Need 单词开头
  "Record 1": {
    "type": "AAAA", //记录类型：
    "domain name": "www.xxxx.cn", // 需解析的域名
    "ttl": "300" // 解析间隔，以 DNS 网站规则为准
  }
}
```

