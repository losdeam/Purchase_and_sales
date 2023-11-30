<template>
    <div class="header">
      <div class="header-left">
        <div class="left">进销货管理系统</div>
      </div>
    </div>
  </template>
   
  <script>
  import { mapState } from "vuex";
  export default {
    name: "Header",
    data() {
      return {
        name: "",
      };
    },
    mounted() {
      this.name = window.sessionStorage.getItem("username");
    },
    methods: {
    },
    computed: {
    },
  };
  </script>
   
  <style >
  .header {
    height: 50px;
    line-height: 50px;
    background-color: rgb(73, 80, 96);
    padding: 0 50px;
    color: #fff;
  }
  .left {
    color: #fff;
    float: left;
  }
  .header-right__info {
    float: right;
    margin: 0 20px;
  }
  .header-right__logout {
    float: right;
  }
  </style>