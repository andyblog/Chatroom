# Chatroom base on Redis
基于Redis的聊天室,可实现群聊和私聊以及保存聊天记录的功能。
## 语法  
### 客户端
* `pull`  拉取未读消息。  
* `users`  获得当前在线用户。  
* `pub <message>`  向大厅发送消息。  
* `to <someone>`  向某用户发送消息。  
* `downline`  下线。  
  

## 原理  
### 客户端
开始时输入昵称，并作为该用户的唯一标识，上传到Redis的`users set`，客户端可通过`users`命令拉取当前在线用户。主线程负责输入命令和发送消息。第一个子线程负责监听`chat`频道（公共频道），并将消息放入缓冲队列。第二个子线程负责监听名为自己昵称的频道，并将消息标记后入队。客户端可通过`pull`命令获取并刷新缓冲队列。  
### 服务器端  
子线程负责监听`chat`频道，并将消息分词，提取出昵称和消息内容，然后在数据库中寻找以该昵称为名的表（如果不存在将创建），并将消息存到该表中。主线程负责向`chat`频道发送消息。    

![image](/Diagram.png)
