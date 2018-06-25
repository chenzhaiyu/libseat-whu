## 武汉大学图书馆座位预约系统
```
@author: czy
@date: 2018-01-30
```
&nbsp;


### 项目文件：
- `gui.py`：`* GUI界面，通过窗口界面选座 *`
- `run.py`：`缺省运行模块`
- `conf.json`：`参数配置`
- `functions.py`：`函数模块`

&nbsp;

### 运行方式：
- `GUI界面模式（推荐）`：

 ```
 python gui.py
 ```

- `缺省模式`：

 ```
 python run.py
 ```
 
&nbsp;

### 运行截图：
![Alt text](https://github.com/realczy/markdown-photo/blob/master/res/whu-lib-seat-4.png?raw=true)

![Alt text](https://github.com/realczy/markdown-photo/blob/master/res/whu-lib-seat-7.png?raw=true)

![Alt text](https://github.com/realczy/markdown-photo/blob/master/res/whu-lib-seat-6.JPG?raw=true)

&nbsp;

### 参数配置：
```
{
  "username": 填写学号，
  "password": 6位密码，
  "startTime": 预约起始时间，以min为单位，如600代表10:00，
  "endTime": 预约终止时间，以min为单位，如1020代表17:00，
  "date_flag": 缺省为"tomorrow"，预约次日座位，"today"为预约今日座位，
  "schedule_flag": "1"表示启用预约模式，"0"为禁用，
  "schedule_time": 预约模式时/分/秒设置，
  "send_mail_flag": "1"表示启用邮件提醒，"0"为禁用，
  "mail_address_from": 发件邮箱,
  "mail_password": 发件邮箱密码,
  "mail_address_to": 收件邮箱,
  "mail_smtp_server": 发件邮箱smtp服务器地址，

}

注意：
引号都不要拿掉；
使用GUI模式时，以上参数直接在GUI窗口中选择即可。
```
&nbsp;

### 注意事项：
- 合理进行测试，请勿给他人和自己造成不便；
- 通过模拟监听到的Android端自习助手的http请求进行操作；
- 目前只能选择信息分馆的座位（懒）；
- 写得很烂，若在测试中发现问题，可联系：`contact@chenzhaiyu.com`。

