// 轮询发送消息
const axios = require('axios');
const cron = require('node-cron');
require('dotenv').config();
// 企业微信机器人的Webhook URL
const webhookUrl = process.env.WEBHOOKURL
const serverPort = process.env.PORT
const serverUrl = 'http://localhost:'+serverPort;
  // Cron语法："* * * * * *"代表 "秒 分 时 日 月 周"
const interval = ['0 15 10 * * 1-5','0 15 14 * * 1-5','0 15 16 * * 1-5','0 45 11 * * 1-5']
axios.get(`${serverUrl}/config`)
  .then(response => {
    const data = response.data
    const message = {
      "msgtype": "text",
      "text": {
        "content": data.message,
      }
    };

    const initalMessage = {
      "msgtype": "markdown",
      "markdown":{
        "content":`# 多喝水没事，没事多喝水，超爱喝水每天为你提醒喝水 \n
        > 提醒喝水时间段：${data.startTime}~${data.endTime} \n
        > 每天提醒${data.frequency}次 \n
        > [更多设置](http://localhost:3000)
        `
      }
    }
    // inital message    
    // axios.post(webhookUrl,initalMessage) .then(response => {
    //   console.log('消息发送成功:', response.data);
    // })
    // .catch(error => {
    //   console.error('消息发送失败:', error);
    // });
    // 设置定时任务，每天的startTime~endTime发送消息
    interval.forEach((time,index)=>{
      cron.schedule(time, () => {
        axios.post(webhookUrl, message)
          .then(response => {
            console.log('消息发送成功:', response.data);
          })
          .catch(error => {
            console.error('消息发送失败:', error);
          });
      });
    })
  })
  .catch(error => {
    console.error('Error fetching config:', error);
  });  

