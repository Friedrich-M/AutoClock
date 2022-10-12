# ZJU-AutoDaka
<div style="text-align: center">

  ![AUR](https://img.shields.io/badge/license-MIT%20License%202.0-green.svg)
  ![GitHub stars](https://img.shields.io/github/stars/Friedrich-M/AutoClock.svg?style=social&label=Stars)
  ![GitHub forks](https://img.shields.io/github/forks/Friedrich-M/AutoClock.svg?style=social&label=Fork)
</div>

<img width="400" alt="image" src="https://user-images.githubusercontent.com/85838942/167731771-1e92944d-a33c-4c21-84b3-7621547adeef.png">


# 简介
利用github action 实现自动健康打卡，
针对验证码版本开发，适用于最新版的打卡系统

<img width="300" src="https://user-images.githubusercontent.com/85838942/167908824-4f1b1495-6032-493c-9765-0838ac74699b.jpeg">


## 写在前面
钉钉机器人推送代码来自[Dimlitter](https://github.com/Dimlitter)同学


## 使用方法

1. 直接 Fork 本仓库

2. 配置帐号

- （必须）Settings > Secrets > Actions > New repository secret， 添加 `account`，内容为浙大通行证账号（学号），添加`password`，内容为浙大通行证密码。
   
```
ACCOUNT:通行证账号
 
PASSWORD:通行证密码
```

- （可选）Settings > Secrets > Actions > New repository secret， 添加 `DD_BOT_TOKEN`，内容为钉钉自定义机器人的token，添加`DD_BOT_SECRET`，内容为机器人的签名。

```
DD_BOT_TOKEN: 钉钉自定义机器人的token，只需 https://oapi.dingtalk.com/robot/send?access_token=XXX 等于=符号后面的XXX即可

DD_BOT_SECRET ：钉钉机器人的加签密钥
```
<img width="700" alt="image" src="https://user-images.githubusercontent.com/85838942/167730378-4713a1d8-a272-410c-a20e-465291bfbed8.png">

3. 配置定时运行时间（可选）

   在 .github/workflows/main.yml 中更改时间：

   ```yml
   on:
   workflow_dispatch:
   schedule:
      - cron: '45 */12 * * *'
   ```
 - 注意，github是UTC时间，北京时间是UTC时间加8小时
 
4. 配置钉钉消息通知（可选）

     - 手机版钉钉 > 右上角添加 > 面对面建群 > 创建之后得到只有你一个人的群聊
     - 电脑版钉钉 > 群设置 > 智能群助手 > 添加机器人 > 自定义，名字随便填
     
     ！！！注意： 机器人类型是自定义，不是github，敲黑板！
     
   - 获取上述的token和secret
   
    <img width="400" alt="image" src="https://user-images.githubusercontent.com/85838942/167732273-3a9159fd-ab3e-4169-990a-4f0a2348d9d8.png">


</details>

## 验证码识别

<!-- 验证码识别平台为https://www.chaojiying.com/

请自行前往注册一个账号，再生成一个软件ID

<img width="600" alt="image" src="https://user-images.githubusercontent.com/85838942/167732687-fb110a48-facf-41e4-9359-23f3787ac04e.png">

复制“账号”、“密码”、“软件ID” 替换daka.py中的红圈内参数

<img width="500" alt="image" src="https://user-images.githubusercontent.com/85838942/167732896-1eb787e0-794b-492d-acdd-60e564cf5324.png"> -->


## 注意事项

注意：**请仓库检查开启了github action功能**，如果没有，请在当前项目的Settings>Actions>General下"allow all actions and reusable workflows"和点击Actions > schedule下启用workflows。（没有开启的页面有文字提示开启）

当action运行时，可以在项目的**Actions**选项下看到AutoDaka这个工作流的运行记录

- 如果想立即运行action，只需要star一下自己的项目即可触发。

## 声明

本项目为Python学习交流的开源非营利项目，仅作为学习交流之用。

