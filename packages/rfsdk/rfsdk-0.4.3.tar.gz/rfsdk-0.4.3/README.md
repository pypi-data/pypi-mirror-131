# rfsdk
rfsdk是基于pyant实现的一个fst客户端（python），对常用交易业务进行封装，向用户提供易用的服务和接口

# 功能依赖说明
## 订阅推送业务
**依赖说明:**
1. pyant无法识别“未声明”的pb消息类型，会将这类消息的原始pb序列化字符串base64编码后回调给业务层；
2. 业务层根据自身业务，针对性的将原始pb序列化字符串反序列化为对应的pb对象；

**依赖模块：**
1. google protobuf开源库（python版）；
2. 业务proto对应的pb2.py文件（proto文件统一存放在protocol仓库中，通过protoc工具生成pb2.py时，需要保持目录结构不变）






