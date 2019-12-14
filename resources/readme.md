##配置文件
- 默认配置放在giftPacks.conf中
##读取配置文件
- 方法 get_config(section,key)
  - 例如:
  ```
  读取配置文件mysql的user
  user = get_config("mysql","user")
  ```