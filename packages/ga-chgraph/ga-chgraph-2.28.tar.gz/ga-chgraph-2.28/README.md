# ga-chgraph

## 1 介绍

该项目是图操作项目，包含：

- 图节点/边的查询操作
- 整张图的插入/删除/查询/总结/描述操作
- 图节点/边的插入操作
- 关于图的服务

## 2 图操作服务：

### 2.1 基于docker的服务化

#### 2.1.1 安装启动

需要安装docker

```

源码部署
服务器是p47719v.hulk.shbt.qihoo.net

服务器上的目录地址在/usr/local/chGraph/ga-chgraph

启动前先关掉之前起的进程，启动命令是nohup /usr/local/chGraph/anaconda3/bin/python /usr/local/chGraph/ga-chgraph/clickhouse_api_server/main.py 2>&1 &



容器化部署

按照陶指导要求，采用上传pypi库然后采用pip install的方式进行安装部署。打包前需要注意setup中的version，如果已存在对应版本的包则无法进行上传

打包前检查：python setup.py check

文件打包：python setup.py sdist bdist_wheel

文件上传：python3 -m twine upload --repository-url  https://upload.pypi.org/legacy/  dist/*

此时会要求输入用户名和密码，即为pypi的用户名密码，ga-chgraph目前使用的分别是liufeng_qihoo360和liufengqihoo360

上传至pypi之后，即可通过pip install xxx来进行安装，即Dockerfile中的方式来进行安装

——————————————————
原始采用build镜像的方式已经deprecated了，但还是可以采用此种方式完成打包，但需作修改
#下载源码
git clone git@w.src.corp.qihoo.net:data-platform/intell-dev/ga-chgraph.git

#构建镜像
cd ga-chgraph
docker build -t ga-chgraph:v1 .

#修改配置文件
将docker镜像中的/usr/local/lib/python3.6/site-packages/clickhouse_api_server/config/graph_config.json中的IP更换为自己的IP

#启动容器服务
docker run -it  -p 10010:10110  ga-chgraph:v1

```

至此，图操作服务已经启动

#### 2.1.2 swagger文档路径

```
此处p47708v.hulk.shbt.qihoo.net需要更换为自己的服务器地址
http://p47708v.hulk.shbt.qihoo.net:10010/doc
```


#### 2.1.3 测试

```
图节点/边的查询操作(全部为get请求)

url：p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/edges

url：p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/multi-hop

url：p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/one-hop

url：p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/vertices

url：p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-db/api/v1/multi-hop-common-vertices


整张图的插入/删除/查询/总结/描述的操作

url：p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-registration

url：p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-deletion

url：p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-show

url：p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-summary/(?P<graph_name>\S*)

url：p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-description/(?P<graph_name>\S*)

图节点/边的插入操作

url：p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/edge-insertion

url：p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/vertex-insertion

此处p47708v.hulk.shbt.qihoo.net需替换为您自己的机器。

```

测试数据：

```
以p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/one-hop为例：

{
  "start_vertex_list": [
    "10.73.28.115",
    "10.78.55.20"
  ],
  "edge_name_list": [
    "tcpflow",
    "flow"
  ],
  "graph_name": "cyber_plus",
  "direction": "forward",
  "edge_con_list_list": [
    [
      "downlink_length>10000",
      "protocol='http'"
    ],
    [
      "record_date='2019-04-15'"
    ]
  ],
  "target_field_list": [
    "record_time"
  ]
}  


```

返回结果：

```
{
    "result": [
        [
            [
                "10.73.28.115",
                "10.59.81.218",
                "2019-04-15 13:37:18"
            ],
            [
                "10.73.28.115",
                "117.34.15.37",
                "2019-04-15 13:41:39"
            ],
        ....
       ]
}
```

如图：

![image](./images/1.png)
