### Why rpc still use connection pool while http2 supports multiplexing?
1. rpc server controls how client can utilize multiplexing, some rpc server may only support limited multiplexing
2. to increase microservice's data throughput, single TCP connection has throughput limitation which is also defined by rpc server
3. single TCP connection may trigger TCP congestion when throughput is large and transport rate between client and server side doesn't match

### 为什么http2支持多路复用的情况下，rpc仍然要使用连接池
1. rpc server来定义客户端如何使用多路复用，有的server可能只支持小量级的多路复用
2. 为了提高微服务的数据吞吐量，单TCP链接的吞吐量也是由服务端来定义的
3. 单TCP链接在数据吞吐量很大且服务端客户端的速度不一致的时候，可能会触发TCP拥塞机制

original answer of [sbordet](https://stackoverflow.com/questions/55985658/do-we-still-need-a-connection-pool-for-microservices-talking-http2) on stackoverflow

