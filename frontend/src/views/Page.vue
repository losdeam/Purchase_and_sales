<template>
    <div>
      <el-container>
        <el-col :span="3">
          <el-menu default-active="1" class="el-menu-vertical-demo">
            <el-menu-item index="1" @click="btn1">
              <i class="el-icon-setting"></i>
              <span slot="title">商品管理</span>
            </el-menu-item>
            <el-menu-item index="2" @click="btn2">
              <i class="el-icon-menu"></i>
              <span slot="title">进货管理</span>
            </el-menu-item>
            <el-menu-item index="3" @click="btn3">
              <i class="el-icon-menu"></i>
              <span slot="title">销售记录</span>
            </el-menu-item>
            <el-menu-item index="4" @click="btn4">
              <i class="el-icon-setting"></i>
              <span slot="title">用户管理</span>
            </el-menu-item>
            <el-menu-item index="5" @click="btn5">
              <i class="el-icon-setting"></i>
              <span slot="title">柜台识别</span>
            </el-menu-item>
            <el-menu-item index="6" @click="btn6">
              <i class="el-icon-setting"></i>
              <span slot="title">模型管理</span>
            </el-menu-item>
            <el-menu-item index="7" @click="btn7">
              <i class="el-icon-setting"></i>
              <span slot="title">用户设置</span>
            </el-menu-item>
          </el-menu>
        </el-col>
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </div>
  </template>
   
  <script>
  import Header from "../components/Header";
  export default {
    name: "Page",
    data() {
      return {
        loading: false,
      };
    },
    mounted() {},
    components: {
      Header,
    },
    methods: {
      btn1() {
        this.$router.push("./commodity");
      },
      btn2() {
        this.$router.push("./stock");
      },
      btn3() {
        this.$router.push("./sales_record");
      },
      btn4() {
        this.$router.push("./User");
      },
      btn5() {
        this.$router.push("./recognition");
      },
      btn6() {
        this.$router.push("./model_operation");
      },
      btn7() {
        this.$router.push("./config");
      },
      handleOpen(key, keyPath) {
        console.log(key, keyPath);
      },
      handleClose(key, keyPath) {
        console.log(key, keyPath);
      },
    },
  };
  </script>
   
  <style scoped>
  /* .el-main {
    padding: 0;
  } */
  </style>