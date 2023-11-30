<template>
    <div>
      <el-container>
        <el-col :span="3">
          <el-menu default-active="1" class="el-menu-vertical-demo">
            <el-menu-item index="2">
              <i class="el-icon-setting"></i>
              <span slot="title">商品管理</span>
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