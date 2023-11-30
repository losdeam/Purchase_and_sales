<template>
    <div>
    <el-table
      border
      style="width: 100%"
      :data="formattedData"
      element-loading-text="拼命加载中"
    >
      <el-table-column prop="id" label="编号" width="180"> </el-table-column>
      <el-table-column prop="name" label="商品名称" width="180"></el-table-column>
      <el-table-column prop="number" label="库存"> </el-table-column>
      <el-table-column prop="baseline" label="基准数"> </el-table-column>
      <el-table-column prop="sort" label="分类"> </el-table-column>
      <el-table-column label="操作">
      <template slot-scope="scope">
        <!-- 这里添加自定义按钮，可以根据需要修改按钮样式和功能 -->
        <el-button @click="showDialog(scope.row)">进货</el-button>
      </template>
      
    </el-table-column>

    </el-table>
    <el-dialog
      title="请填写进货数量"
      :visible.sync="dialogVisible"
      width="30%"
      @close="handleDialogClose"
    >
      <!-- 弹窗内容 -->
      <div>
        <!-- 在这里放置弹窗中的内容，可以是表单、按钮等 -->
        <el-input v-model="inputValue" placeholder="输入内容"></el-input>
        <el-button @click="onDialogConfirm">确定</el-button>
      </div>
    </el-dialog>
    <el-dialog
      title="进货成功"
      :visible.sync="stock_success"
      width="30%"
      @close="success_close"
    >
      <!-- 弹窗内容 -->
      <div>
        <!-- 在这里放置弹窗中的内容，可以是表单、按钮等 -->
        <p>{{ dynamicText }}</p>
      </div>
    </el-dialog>
    
    </div>
  </template>

<script>
export default {

  data() {
    return {
      formattedData :[],
      transaction: {
        good_id: 1,
        change_num: 0,
        type: 1, // 默认为进货
      },
      dialogVisible: false, // 添加这一行，初始化为 false
      stock_success: false,
      inputValue :'',
      dynamicText : ''
    };
  },
  mounted() {
    // 在组件加载时获取商品数据
    this.fetchProducts();
  },
  methods: {
    fetchProducts() {
      // 使用后端提供的接口获取商品数据
      fetch("http://127.0.0.1:50000/api/goods/low", {
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
            id: item.good_id,
            name: item.good_name,
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
          this.dynamicText = data;
          // 执行交易后刷新商品数据
          
        })
        .catch((error) => {
          console.error("Error performing transaction:", error);
        });
    },
    showDialog(row) { 
      // 打开弹窗
      this.dialogVisible = true;
      this.transaction.good_id = row.id;
      this.transaction.type = 1;
    },
    handleDialogClose() {
      // 关闭弹窗时的处理，可以在这里清空输入框的值等
      this.inputValue = '';
    },
    onDialogConfirm(row) {
      // 处理弹窗中确定按钮的逻辑，可以在这里执行提交操作等
      this.transaction.change_num = parseInt(this.inputValue, 10);
      // 关闭弹窗
      this.dialogVisible = false;
      this.performTransaction();
      this.fetchProducts();
      this.stock_success = true ;
      
    },
    success_close(){
        this.stock_success = false ;
    }
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