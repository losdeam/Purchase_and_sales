<template>
    <div>
      <el-button type="primary" @click="self_add_good">自主进货</el-button>
    <el-table
      border
      style="width: 100%"
      :data="formattedData"
      element-loading-text="拼命加载中"
    >
    
      <el-table-column prop="id" label="编号" width="50"> </el-table-column>
      <el-table-column prop="name" label="商品名称" width="180"></el-table-column>
      <el-table-column prop="number" label="库存"> </el-table-column>
      <el-table-column prop="baseline" label="基准数"> </el-table-column>
      <el-table-column prop="sort" label="分类"> </el-table-column>
      <el-table-column label="操作">
      <template slot-scope="scope">
        <!-- 这里添加自定义按钮，可以根据需要修改按钮样式和功能 -->
        <el-button @click="add_good(scope.row)">进货</el-button>
        <el-button @click="ban(scope.row)">下架</el-button>
      </template>      
    </el-table-column>
    </el-table>
    <el-dialog title="请填写进货数量"
      :visible.sync="dialogVisible"
      width="30%"
    >
      <!-- 弹窗内容 -->
      <div>
        <!-- 在这里放置弹窗中的内容，可以是表单、按钮等 -->
        <el-input v-model="inputValue" placeholder="输入内容"></el-input>
        <el-button @click="onDialogConfirm">确定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="自主进货"
      :visible.sync="self_change_good"
      width="30%"
    >
      <!-- 弹窗内容 -->
      <div>
        <!-- 在这里放置弹窗中的内容，可以是表单、按钮等 -->
        <el-input v-model="inputValue" placeholder="输入内容">
        <template slot="prepend">商品id：</template></el-input>
        <el-input v-model="str_good_num" placeholder="输入内容">
        <template slot="prepend">商品数量：</template></el-input>
        <el-button @click="self_get_good">确定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="操作成功"
      :visible.sync="stock_success"
      width="30%"
    >
      <!-- 弹窗内容 -->
      <div>
        <!-- 在这里放置弹窗中的内容，可以是表单、按钮等 -->
        <p>{{ dynamicText }}</p>
      </div>
    </el-dialog>
    <el-dialog title="操作失败"
      
      :visible.sync="stock_fail"
      width="30%"
    >
      <!-- 弹窗内容 -->
      <div>
        <!-- 在这里放置弹窗中的内容，可以是表单、按钮等 -->
        <p>{{ dynamicText }}</p>
      </div>
    </el-dialog>
    <el-dialog title="自主进货"
      :visible.sync="self_stock"
      width="30%"
    >
      <div>
        <el-button @click="new_good">添加全新商品</el-button>
        <el-button @click="exist_good">已有商品补货</el-button>
      </div>
    </el-dialog>
    <el-dialog title="添加全新商品"
      :visible.sync="add_new_good"
      width="30%"
    >
      <div>
        <el-input v-model="str_good_name" placeholder="输入内容">
        <template slot="prepend">商品名称：</template>
        </el-input>
        <el-input v-model="str_good_num" placeholder="输入内容">
        <template slot="prepend">商品数量：</template>
        </el-input>
        <el-input v-model="str_good_price_buying" placeholder="输入内容">
        <template slot="prepend">进货价格：</template>
        </el-input>
        <el-input v-model="str_good_price_retail" placeholder="输入内容">
        <template slot="prepend">零售价格：</template>
        </el-input>
        <el-input v-model="str_good_sort" placeholder="输入内容">
        <template slot="prepend">商品分类：</template>
        </el-input>
        <el-input v-model="str_good_baseline" placeholder="输入内容">
        <template slot="prepend">商品基础保有量：</template>
        </el-input>
      </div>
      <el-button @click="self_add_new_good">确定</el-button>
    </el-dialog>
    <el-dialog title="警告"
      :visible.sync="delete_confirm"
      width="30%"
    >
      <div>
        <p>{{ dynamicText }}</p> 
        <el-button @click="delete_confirm_button">确定</el-button>
      </div>
    </el-dialog>
    </div>
  </template>

<script>
export default {
  data() {
    return {
      formattedData :[],
      dialogVisible: false, // 添加这一行，初始化为 false
      stock_success: false,
      delete_confirm : false,
      stock_fail: false,
      self_stock : false,
      add_new_good : false,
      self_change_good : false ,
      transaction:{
        good_id : 1 , 
        change_num : 0 ,
        type : 1,
      },
      str_good_name : '',
      str_good_num : '',
      str_good_price_buying : '',
      str_good_price_retail : '',
      str_good_sort : '',
      str_good_baseline : '',
      
      delete_good : {
        good_id : 0,
      },
      new_goods:{
        good_name : '',
        good_num : 0,
        good_price_buying : 0,
        good_price_retail : 0,
        good_sort : '',
        good_baseline : 0,
      },
      new_good_data:{
        good_id: 0 ,
        new_data:{
          good_name : '',
          good_num : 0,
          good_price_buying : 0,
          good_price_retail : 0,
          good_sort : '',
          good_baseline : 0,
        },
      },

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
        .then((response) =>{
          // 检查响应状态码
          if (!response.ok) {
            throw new Error("响应状态码不合理");
          }

          return response.json();
        }
        )
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
        .catch((error) => {
      console.error(error.message);
      // 处理错误，可以根据实际情况进行处理
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
        .then((response) => {
          // 检查响应状态码
          if (!response.ok) {
            this.stock_fail = true;
          }
          else{
            this.stock_success = true;
          }
          return response.json();
        })
        .then((data) => {
          this.dynamicText = data;
          this.fetchProducts();
          // 执行交易后刷新商品数据
          
        })
        .catch((error) => {
          console.error("Error performing transaction:", error);
        });
    },
    add_new_good_post(){
      fetch("http://127.0.0.1:50000/api/goods/add", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include", // 添加此行，确保携带 Cookie
        body: JSON.stringify(this.new_goods),
      })
        .then((response) => {
          // 检查响应状态码
          if (!response.ok) {
            this.stock_fail = true;
          }
          else{
            this.stock_success = true;
          }
          return response.json();
        })
        .then((data) => {
          this.dynamicText =  data["message"];
          // 执行交易后刷新商品数据  
        })
        .catch((error) => {
          console.error("Error performing transaction:", error);
        });
    },
    delete_good_post(){
      fetch("http://127.0.0.1:50000/api/goods/delete", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include", // 添加此行，确保携带 Cookie
        body: JSON.stringify(this.delete_good),
      })
        .then((response) => {
          // 检查响应状态码
          console.log(response.status)
          if (!response.ok) {
            this.stock_fail = true;
          }
          else{
            this.stock_success = true;
          }
          return response.json();
        })
        .then((data) => {
          this.dynamicText = data["message"];
          this.fetchProducts()
        })
        .catch((error) => {
          console.error("Error performing transaction:", error);
        });
    },
    add_good(row) { 
      // 打开弹窗
      this.dialogVisible = true;
      this.transaction.good_id = row.id;
      this.transaction.type = 1;
    },
    ban(row){
      this.delete_confirm = true;
      this.dynamicText = "确认删除编号为"+  row.id +"的商品" + row.name +"吗，此操作不可逆"
      this.delete_good.good_id = row.id;
    },
    delete_confirm_button(){
      this.delete_confirm = false
      this.delete_good_post()
      
      
    },
    handleDialogClose() {
      // 关闭弹窗时的处理，可以在这里清空输入框的值等
      this.inputValue = '';
    },
    onDialogConfirm() {
      // 处理弹窗中确定按钮的逻辑，可以在这里执行提交操作等
      this.transaction.change_num = parseInt(this.inputValue, 10);
      // 关闭弹窗
      this.dialogVisible = false;
      this.performTransaction();
      this.fetchProducts();
      
      
    },
    self_add_good(){
      this.self_stock = true;
    },
    new_good(){
      this.self_stock = false;
      this.add_new_good = true;

    },
    exist_good(){
      this.self_stock = false
      this.self_change_good = true 
      this.transaction.type = 1;
    },
    self_get_good(){
      this.transaction.good_id = parseInt(this.inputValue, 10);
      this.transaction.change_num = parseInt(this.inputValue, 10);
      this.self_change_good = false;
      this.performTransaction();
      
    },
    self_add_new_good(){
      this.new_goods.good_name = this.str_good_name
      this.new_goods.good_num = parseInt(this.str_good_num, 10);
      this.new_goods.good_price_buying = parseFloat(this.str_good_price_buying)
      this.new_goods.good_price_retail = parseFloat(this.str_good_price_retail)
      this.new_goods.good_sort = this.str_good_sort
      this.new_goods.good_baseline = parseInt(this.str_good_baseline_name, 10);
      this.add_new_good_post()
      this.add_new_good = false;
    },

  },
};

</script>
