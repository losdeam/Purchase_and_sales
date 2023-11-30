<template>
    <el-table
      border
      style="width: 100%"
      :data="formattedData"
      v-loading="loading"
      element-loading-text="拼命加载中"
    >
      <el-table-column prop="id" label="编号" width="180"> </el-table-column>
      <el-table-column prop="name" label="商品名称" width="180"></el-table-column>
      <el-table-column prop="price_buying" label="进货价"> </el-table-column>
      <el-table-column prop="price_retail" label="零售价"> </el-table-column>
      
      <el-table-column prop="number" label="库存"> </el-table-column>
      <el-table-column prop="baseline" label="基准数"> </el-table-column>
      <el-table-column prop="sort" label="分类"> </el-table-column>
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
      fetch("http://127.0.0.1:50000/api/goods/show", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
        
          const rawData = JSON.stringify( data["message"]);
          const parsedArray = JSON.parse(rawData);
          // console.log(typeof [1])
          // console.log(typeof parsedArray);



          this.formattedData = parsedArray.map(item => {
          return {
            id: item.good_id,
            name: item.good_name,
            price_buying: item.good_price_buying,
            price_retail: item.good_price_retail,
            sort: item.good_sort,
            baseline: item.good_baseline,
            number: item.good_num
          };

        });
        })

    },
    performTransaction() {
      // 使用后端提供的接口执行交易
      fetch("http://127.0.0.1:50000/api/goods/change", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.transaction),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("Transaction result:", data);
          // this.message = ;
          
          // 执行交易后刷新商品数据
          this.fetchProducts();
        })
        .catch((error) => {
          console.error("Error performing transaction:", error);
        });
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