# 说明文档
## getTwitterData.py  
### 功能
爬取目标用户近3000条推文的@信息，Twitter互相关注好友及其Wikidata信息，并保存为json格式的文件，供echarts关系图读取数据使用。   
### 使用方法  
运行命令 `python getTwitterData.py [argv1 argv2 argv3]` 即可。  
其中
1. argv1为第一个参数，Twitter用户名screen_name，缺省为‘realDonaldTrump’
2. argv2为第二个参数，选择开发者账户，范围为0~3，缺省为0
3. argv3为第三个参数，是否只爬取已认证用户，缺省为True
### 注
若程序运行中途希望停止爬取数据，则可创建`./control/screen_name`文件来达到停止程序的目的，其中`screen_name`为要爬取的用户名。

## getWikidata.py
### 功能
获取指定用户的Wikidata信息。   
### 使用方法  
调用程序中的`get_wikidata(user_name)`函数即可。其中，`user_name`为人物名称。

## limit.py
### 功能
获取所有开发者账号的速率限制情况。   
### 使用方法  
运行命令 `python limit.py` 即可。

## receiveEmail.py和sendEmail.py
### 功能
接收和发送邮件。   
### 使用方法  
调用程序中的`send_email()`和`getEmailRequest()`函数即可。
