<template>
  <div id="app">
    <h1>商品列表</h1>
    <div v-for="product in products" :key="product.good_id">
      <p>{{ product.good_id }} - ￥{{ product.good_name }} - 库存：{{ product.good_num }}</p>
    </div>

    <h2>进货/销售</h2>
    <label for="good_id">商品ID:</label>
    <input type="number" v-model="transaction.good_id" id="good_id" />

    <label for="change_num">数量:</label>
    <input type="number" v-model="transaction.change_num" id="change_num" />

    <label for="type">交易类型:</label>
    <select v-model="transaction.type" id="type">
      <option :value=1>进货</option>
      <option :value=0>销售</option>
    </select>

    <button @click="performTransaction">执行交易</button>
        <!-- 区域用来显示接口返回的信息 -->
        <div v-if="message">
      <p>{{ message }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
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
          this.products = data["message"];
        })
        .catch((error) => {
          console.error("Error fetching products:", error);
        });
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
          this.message = data;
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

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin: 20px;
}

h1, h2 {
  color: #2c3e50;
}

div {
  margin-bottom: 10px;
}

label {
  margin-right: 5px;
}
</style>
