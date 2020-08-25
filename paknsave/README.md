# babistep_crawler

## Pak'nSave
###简介
爬取购物网站 https://www.paknsaveonline.co.nz,存储分店商品信息。
爬取结果存储于本地目录下data文件夹：
分店
 |--- 一级分类
         ｜--- 二级分类
                 ｜--- page.json
###主要问题
浏览器状态和scrapy请求状态有黏着现象，对切换分店造成阻碍。在导师指导下发现页面切换分店时把客户端信息记录到服务器端，并在客户端的后续请求中以此信息判断客户端请求的分店的分店信息。由此找到了cookie中的相关信息，从而解决问题。

另外，由于打开Cookie引起网站IP记录，当爬取次数过多或频率过快时会引起网站封禁IP。对于这个问题有两个解决方案
1. 连接代理IP池，但国内代理请求网站速度较慢，失败率较高，且需要付费购买IP
    - 开启方法：在setting文件夹中 
    ```
   DOWNLOADER_MIDDLEWARES = {
        'paknsave.middlewares.XunProxyMiddleware': 543,
    }
   ```
2. 设置两次申请之间的等待间隔，但一段时间内请求过多仍可能被封IP，目前实验最小间隔时间为`time.sleep(0.8)`
                 

运行方式：
```
cd ./paknsave
scrapy crawl test
```

