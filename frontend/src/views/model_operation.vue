<template>
  <div>
    <h1>操作日志</h1>
    <ul>
      <li v-for="(item, index) in dataList" :key="index">{{ item }}</li>
    </ul>
  </div>
</template>
  
  <script>
  export default {
  data() {
    return {
      dataList: [],
    };
  },
  mounted() {
    // 在组件加载时获取商品数据
    this.fetchProducts();
  },
  methods: {
    fetchProducts() {
      // 使用后端提供的接口获取商品数据
      fetch("http://127.0.0.1:50000/api/auth/get_log", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include", // 添加此行，确保携带 Cookie
      })
        .then((response) => response.json())
        .then((data) => {
          this.dataList = data;

        })
  
    },
  },
  };
  
  </script>
