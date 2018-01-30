## 武汉大学图书馆座位预约系统
```
@author: czy
@date: 2018-01-30
```
&nbsp;

### 说明：
合理合规进行测试使用，请勿给他人和自己造成不便。作者对违规使用程序脚本所造成的后果不承担任何责任。

&nbsp;

### 项目文件：
- `conf.json`：`参数配置`
- `whu-lib-seat.py`：`选座脚本`

&nbsp;

### 参数配置：
```
{
  "username": 填写学号，
  "password": 6位密码，
  "startTime": 预约起始时间，以min为单位，如600代表10:00，
  "endTime": 预约终止时间，以min为单位，如1020代表17:00，
  "date_flag": 缺省为"tomorrow"，预约次日座位，
  "seats": 所选座位号 ， 
  "more_seats": 暂未适配，不需要配置
}
```
&nbsp;

### 注意事项：
- 通过模拟监听到的Android端自习助手的http请求进行操作；
- 项目使用Python 2.7版本编写，若需要在Python 3.x版本运行，可能需要改几个包函数<如`httplib`改成`http.client`>；
- 目前只能实现预约座位功能，后面有时间的话会拓展取消预约、释放座位、查询预约等功能；
- 若在测试中存在问题，请与我联系:`contact@chenzhaiyu.com`，或访问网站:`http://www.chenzhaiyu.com`。

