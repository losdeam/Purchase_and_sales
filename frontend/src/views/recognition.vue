<!-- VideoStream.vue -->

<template>
  <div>
    <img :src="videoFrame" alt="Video Frame" style="max-width: 100%; max-height: 100%;">
  
    <el-table
        border
        style="width: 100%"
        :data="formattedData"
        element-loading-text="拼命加载中"
      >

        <template slot-scope="scope">
          <!-- 这里添加自定义按钮，可以根据需要修改按钮样式和功能 -->
          <el-button @click="add_good(scope.row)">训练</el-button>
          <el-button @click="add_good(scope.row)">训练</el-button>

        </template>      

      </el-table>
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
  train(){
    
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
