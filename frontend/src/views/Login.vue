<template>
    <div class="home">
      <div class="homebox" v-loading="loading">
        <h3>KGC后台管理系统</h3>
        <el-input
          class="input"
          v-model="user_data.user_name"
          style="width: 500px"
          placeholder="用户名"
        ></el-input>
        <el-input
          class="input"
          placeholder="密码"
          style="width: 500px"
          v-model="user_data.password"
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
        user_data:{       
             user_name: "",
            password: '',
        },
        login_flag :false,
        loading: false,
      };
    },
    mounted() {},
    methods: {
      login() {
        
        fetch("http://127.0.0.1:50000/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include", // 添加此行，确保携带 Cookie
        body: JSON.stringify(this.user_data),
      })
      .then((response) => {
          // 检查响应状态码
          if (!response.ok) {
            this.login_flag = true 
          }
          else{
            this.$router.push("./Page");
            window.sessionStorage.setItem("username",this.user_data.user_name)
            this.login_flag = false 
            
          }
          return response.json();
        })
        .then((data) => {

            if (this.login_flag)this.$message.error(data["message"])
            else this.$message.success(data["message"])
          
        })
        .catch((error) => {
          console.error("Error performing transaction:", error);
        });
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