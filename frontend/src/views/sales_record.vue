<template>
  <el-table
    border
    style="width: 100%"
    :data="formattedData"
    v-loading="loading"
  >
    <el-table-column prop="time_stamp" label="时间" > </el-table-column>
    <el-table-column prop="good_id" label="编号" ></el-table-column>
    <el-table-column prop="name" label="商品名称" ></el-table-column>
    <el-table-column prop="good_num" label="售出量"> </el-table-column>

  </el-table>
</template>

<script>
export default {
data() {
  return {
    formattedData :[],
    products: [],
    transaction: {
      good_id: 1,
      change_num: 0,
      type: 1, // 默认为进货
    },
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
    })
      .then((response) => response.json())
      .then((data) => {
      
        const rawData = JSON.stringify( data["message"]);
        const parsedArray = JSON.parse(rawData);
        this.formattedData = parsedArray.map(item => {
        return {
          time_stamp: item.time_stamp,
          good_id: item.good_id,
          name : item.good_name,
          good_num: item.good_num
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