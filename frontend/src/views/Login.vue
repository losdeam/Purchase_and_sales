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
      username: "admin",
      password: 123,
      loading: false,
    };
  },

  // mounted() {
  //   // 在组件加载时获取商品数据
  //   this.fetchProducts();
  // },
  methods: {
    login() {
      console.log('666')
      // console.log(this.$router); // 确保输出不为 null
      this.$router.push("/page");
        // // 使用后端提供的接口获取商品数U
        // fetch("http://127.0.0.1:50000/api/goods/show", {
        //   method: "POST",
        //   headers: {
      //     "Content-Type": "application/json",
      //   },
      // })
      //   .then((response) => response.json())
      //   .then((data) => {
      //     console.log("接口调用成功");
      //     this.$router.push("./user");
      //     // this.$router.push("./page");
      //   })
      //   .catch((error) => {
      //     console.error("Error fetching products:", error);

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