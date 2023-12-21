<!-- VideoStream.vue -->

<template>
  <div>
    <img :src="videoFrame" alt="Video Frame" style="max-width: 100%; max-height: 100%;">
  </div>
</template>

<script>
import io from 'socket.io-client';

export default {
  data() {
    return {
      videoFrame: null
    };
  },
  created() {
    // 连接到 Socket.IO 服务器

    this.socket = io('http://127.0.0.1:50000');
    // 监听来自服务器的视频帧消息
    this.socket.on('receive', (data) => {
      this.videoFrame = 'data:image/jpeg;base64,' + data.frame;
      console.log(this.videoFrame)
  
    });

    // 发送请求视频流的消息
    this.socket.emit('sent_img');
  },
  beforeDestroy() {
    // 断开 Socket.IO 连接
    if (this.socket) {
      this.socket.disconnect();
    }
  }
};
</script>

<style>
/* 样式 */
</style>
