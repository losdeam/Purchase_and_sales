<template>
    <div>
      <el-button type="primary" @click="train_strengthen">模型强化</el-button>
      <el-table
      border
      style="width: 100%"
      :data="formattedData"
      v-loading="loading"
    >
      <el-table-column prop="goods_id" label="编号" ></el-table-column>
      <el-table-column prop="name" label="模型名称" ></el-table-column>
      <el-table-column prop="goods_num" label="操作"> </el-table-column>
  
    </el-table>
    </div>
    
  </template>
  
  <script>
  export default {
  data() {
    return {
      formattedData :[],
      products: [],
    };
  },
  mounted() {
    // 在组件加载时获取商品数据
    this.fetchProducts();
  },
  methods: {
    fetchProducts() {
      // 使用后端提供的接口获取商品数据
      fetch("http://127.0.0.1:50000/api/goods/record", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          
        },
        credentials: "include", // 添加此行，确保携带 Cookie
      })
        .then((response) => response.json())
        .then((data) => {
        
          const rawData = JSON.stringify( data["message"]);
          const parsedArray = JSON.parse(rawData);
          this.formattedData = parsedArray.map(item => {
          return {
            time_stamp: item.time_stamp,
            goods_id: item.goods_id,
            name : item.goods_name,
            goods_num: item.goods_num
          };
  
        });
        })
  
    },
  },
  };
  
  </script>
  <!-- <script>
    
  import { mapState } from "vuex";
  export default {
    name: "Commodity",
    data() {
      return {
        loading: false,
      };
    },
    mounted() {
      this.loading = true;
      clearTimeout(clear)
      var clear = setTimeout(() => {
         this.$axios.get("/goods").then((v) => {
          const com = v.data;
          this.$store.commit("record", com);
          this.loading = false
        })
      }, 300);
      
    },
    computed: {
      ...mapState(["table"]),
    },
  };
  </script> -->