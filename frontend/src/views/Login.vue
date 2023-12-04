<template>
    <div class="home">
      <div class="homebox" v-loading="loading">
        <h3>KGC后台管理系统</h3>
        <el-input
          class="input"
          v-model="username"
          style="width: 500px"
          placeholder="用户名"
        ></el-input>
        <el-input
          class="input"
          placeholder="密码"
          style="width: 500px"
          v-model="password"
          show-password
        ></el-input>
        <el-button
          type="primary"
          size="medium "
          @click="login"
          style="width: 500px"
          >登陆</el-button
        >
      </div>
    </div>
  </template>
  <script>
  export default {
    name: "Login",
    data() {
      return {
        user:{
            username: "admin",
            password: 123,
        },
        loading: false,
      };
    },
    mounted() {},
    methods: {
      login() {
        this.$router.push("./Page");
      //   fetch("http://127.0.0.1:50000/api/goods/add", {
      //   method: "POST",
      //   headers: {
      //     "Content-Type": "application/json",
      //   },
      //   body: JSON.stringify(this.new_goods),
      // })
      //   .then((response) => {
      //     // 检查响应状态码
      //     if (!response.ok) {
      //       this.$message.error("账号不存在，请重新输入！");
      //     }
      //     else{
      //       this.stock_success = true;
      //     }
      //     return response.json();
      //   })
      //   .then((data) => {
      //     this.dynamicText =  data["message"];
      //     // 执行交易后刷新商品数据  
      //   })
      //   .catch((error) => {
      //     console.error("Error performing transaction:", error);
      //   });
        
      },
    },
  };
  </script>
  <style>
  body {
    background-color: rgb(238, 243, 250);
  }
  .homebox {
    text-align: center;
    position: absolute;
    top: 50%;
    left: 50%;
    margin-top: -150px;
    margin-left: -300px;
    width: 600px;
    height: 300px;
    background-color: rgb(255, 255, 255);
  }
  h3 {
    padding: 20px 0;
  }
  .input {
    margin-bottom: 20px;
  }
  </style>