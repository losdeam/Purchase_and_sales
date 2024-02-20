<template>
  <div>
    <el-button @click="setCurrentPage('path')" :type="currentPage === 'path' ? 'primary' : 'default'">
      路径设置
    </el-button>
    <el-button @click="setCurrentPage('data')" :type="currentPage === 'data' ? 'primary' : 'default'">
      数据设置
    </el-button>
    <el-button @click="setCurrentPage('train')" :type="currentPage === 'train' ? 'primary' : 'default'">
      训练设置
    </el-button>

    <el-table
      border
      style="width: 100%"
      :data="formattedData"
    >
      <el-table-column prop="argument" label="参数名"></el-table-column>
      <el-table-column prop="value" label="值"></el-table-column>
      <el-table-column prop="detail" label="作用"></el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentPage: 'data',
      formattedData: [],
      data_config: [],
      train_config: [],
      path_config: [],
    };
  },
  mounted() {
    this.fetchProducts();
    
  },
  methods: {
    setCurrentPage(page) {
      this.currentPage = page;

      
      switch (page) {
        case 'data':
          this.formattedData = this.data_config;
          break;
        case 'train':
          this.formattedData = this.train_config;
          break;
        default:
          this.formattedData = this.path_config;
      }
 
    },
    fetchProducts() {
      fetch("http://127.0.0.1:50000/api/auth/get_config_data", {
        method: "POST",
        credentials: "include",
      })
        .then((response) => response.json())
        .then((data) => {
          this.update(data, "data_config");
          this.update(data, "train_config");
          this.update(data, "path_config");
          this.setCurrentPage('path')
        });
        
    },
    update(data, str_dt) {
      const rawData = JSON.stringify(data[str_dt]);
      const parsedArray = JSON.parse(rawData);
      switch (str_dt) {
        case 'data_config':
          this.data_config = Object.entries(parsedArray).map(([key, val]) => ({
            argument: key,
            value: val,
          }));
          break;
        case 'train_config':
          this.train_config = Object.entries(parsedArray).map(([key, val]) => ({
            argument: key,
            value: typeof val === 'boolean' ? val.toString() : val,
          }));
          break;
        default:
          this.path_config = Object.entries(parsedArray).map(([key, val]) => ({
            argument: key,
            value: val,
          }));
      }
    },
  },
};
</script>

<style>
  .button-container {
    margin-bottom: 20px;
  }

  .el-button {
    margin-right: 10px;
  }
</style>
