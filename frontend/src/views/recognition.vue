<!-- VideoStream.vue -->

<template>
  <div>
    <img :src="videoFrame" alt="Video Frame" style="max-width: 100%; max-height: 100%;">
    <el-button
          type="primary"
          @click="sell_recognition"
          style="width: 400px"
          >订单确认</el-button
        >
    <el-table
        border
        style="width: 100%"
        :data="formattedData"
        element-loading-text="拼命加载中"
      >

      <el-table-column prop="id" label="编号" > </el-table-column>
      <el-table-column prop="name" label="商品名称" ></el-table-column>
      <el-table-column prop="count" label="数量"> </el-table-column>
      <el-table-column prop="price" label="单价"> </el-table-column>
      <el-table-column prop="total" label="总价"> </el-table-column>
<!--         
      <template slot-scope="scope">
          <el-button @click="add_good(scope.row)">训练</el-button>
        </template>      
         -->

      </el-table>
      <el-dialog title="操作成功"
      :visible.sync="stock_success"
      width="30%"
    >
      <!-- 弹窗内容 -->
      <div>
        <!-- 在这里放置弹窗中的内容，可以是表单、按钮等 -->
        <p>{{ dynamicText }}</p>
      </div>
    </el-dialog>
    <el-dialog title="操作失败"
      
      :visible.sync="stock_fail"
      width="30%"
    >
      <!-- 弹窗内容 -->
      <div>
        <!-- 在这里放置弹窗中的内容，可以是表单、按钮等 -->
        <p>{{ dynamicText }}</p>
      </div>
    </el-dialog>
  </div>
  
</template>

<script>
import io from 'socket.io-client';

export default {
  data() {
    return {
      videoFrame: null,
      formattedData :[],
      stock_success: false,
      stock_fail: false,
      dynamicText : ''
    };
  },
  created() {
    // 连接到 Socket.IO 服务器

    this.socket = io.connect('http://127.0.0.1:50000', {
  withCredentials: true
});

    // 监听来自服务器的视频帧消息
    this.socket.on('receive', (data) => {
      this.videoFrame = 'data:image/jpeg;base64,' + data.frame;
      const rawData = JSON.stringify( data["message"]);
      const parsedArray = JSON.parse(rawData);
      this.formattedData = parsedArray.map(item => {
          return {
            id: item.goods_id,
            name: item.goods_name,
            count: item.goods_count,
            price: item.goods_price,
            total: item.goods_count*item.goods_price,
          };
        });
    });

    // 发送请求视频流的消息
    this.socket.emit('sent_img');
  },
  beforeDestroy() {
    // 断开 Socket.IO 连接
    if (this.socket) {
      this.socket.disconnect();
    }
  },
  methods: {
  sell_recognition() {
        fetch("http://127.0.0.1:50000/api/goods/sell", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include", // 添加此行，确保携带 Cookie
      })
      .then((response) => {
          // 检查响应状态码
          if (!response.ok) {
            this.stock_fail = true;
          }
          else{
            this.stock_success = true;
          }
          return response.json();
        })
        .then((data) => {
          this.dynamicText = data;
        })
        .catch((error) => {

        });

      },
    },
};
</script>

<style>
/* 样式 */
</style>
