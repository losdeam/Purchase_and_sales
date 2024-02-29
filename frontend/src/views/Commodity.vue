<template>
  <div>
    <el-cascader :options="formattedData">
      
  </el-cascader>
  <el-table
        border
        style="width: 100%"
        :data="formattedData"
        element-loading-text="拼命加载中"
      >
      
        <el-table-column prop="id" label="编号"  sortable width="180"> </el-table-column>
        <el-table-column prop="name" label="商品名称"  sortable width="180" ></el-table-column>
        <el-table-column prop="price_buying" label="进货价" sortable width="180"> </el-table-column>
        <el-table-column prop="price_retail" label="零售价" sortable width="180"> </el-table-column>
        <el-table-column prop="number" label="库存" sortable width="180"> </el-table-column>
        <el-table-column prop="baseline" label="基准数" sortable width="180"> </el-table-column>
        <el-table-column prop="category" label="分类" sortable width="180"> </el-table-column>
        <el-table-column label="操作">
        <template slot-scope="scope">
          <!-- 这里添加自定义按钮，可以根据需要修改按钮样式和功能 -->
          <el-button @click="update_init(scope.row)">信息更新</el-button>
        </template>      
      </el-table-column>
      </el-table>x
    <el-dialog title="修改商品信息"
      :visible.sync="update_good"
      width="30%"
    >
      <div>
        <el-input v-model="str_goods_name" placeholder="输入内容">
        <template slot="prepend">商品名称：</template>
        </el-input>
        <el-input v-model="str_goods_num" placeholder="输入内容">
        <template slot="prepend">商品数量：</template>
        </el-input>
        <el-input v-model="str_goods_price_buying" placeholder="输入内容">
        <template slot="prepend">进货价格：</template>
        </el-input>
        <el-input v-model="str_goods_price_retail" placeholder="输入内容">
        <template slot="prepend">零售价格：</template>
        </el-input>
        <el-input v-model="str_goods_category" placeholder="输入内容">
        <template slot="prepend">商品分类：</template>
        </el-input>
        <el-input v-model="str_goods_baseline" placeholder="输入内容">
        <template slot="prepend">商品基础保有量：</template>
        </el-input>
      </div>
      <el-button @click="update_goods_button">确定</el-button>
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
  </div>
</template>


<script>
export default {
  data() {
    return {
      stock_fail : false,
      stock_success :false,
      update_good: false,
      dynamicText: '',
      formattedData :[],
      products: [],
      str_goods_name : '',
      str_goods_num : '',
      str_goods_price_buying : '',
      str_goods_price_retail : '',
      str_goods_category : '',
      str_goods_baseline : '',
      transaction: {
        goods_id: 1,
        change_num: 0,
        type: 1, // 默认为进货
      },
      new_goods_data:{
        goods_id: 0 ,
        new_data:{
          name : '',
          num : 0,
          price_buying : 0,
          price_retail : 0,
          category : '',
          baseline : 0,
        },
      },
      intervalId: null, 
    };
  },
  mounted() {
    // 在组件加载时获取商品数据
    
    this.intervalId = setInterval(this.fetchProducts, 1000);
  },
  beforeDestroy() {
    // Clear the interval when the component is about to be destroyed
    clearInterval(this.intervalId);
  },
  methods: {
    fetchProducts() {
      // 使用后端提供的接口获取商品数据
      fetch("http://127.0.0.1:50000/api/goods/show", {
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
          // console.log(typeof [1])
          // console.log(typeof parsedArray);



          this.formattedData = parsedArray.map(item => {
          return {
            id: item.goods_id,
            name: item.goods_name,
            price_buying: item.goods_price_buying,
            price_retail: item.goods_price_retail,
            category: item.goods_category,
            baseline: item.goods_baseline,
            number: item.goods_num
          };

        });
        })

    },
    update_goods_data() {
      // 使用后端提供的接口执行交易
      fetch("http://127.0.0.1:50000/api/goods/update", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include", // 添加此行，确保携带 Cookie
        body: JSON.stringify(this.new_goods_data),
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
          this.fetchProducts()
          // 执行交易后刷新商品数据  
        })
        .catch((error) => {
          console.error("Error performing transaction:", error);
        });
    },
    update_init(row){
      this.update_good = true 
      this.new_goods_data.id = row.id
      // console.log(this.new_goods_data.id)
    },
    update_goods_button(){
      
      
      this.new_goods_data.new_data.name = this.str_goods_name
      this.new_goods_data.new_data.num = parseInt(this.str_goods_num, 10);
      this.new_goods_data.new_data.price_buying = parseFloat(this.str_goods_price_buying)
      this.new_goods_data.new_data.price_retail = parseFloat(this.str_goods_price_retail)
      this.new_goods_data.new_data.category = this.str_goods_category
      this.new_goods_data.new_data.baseline = parseInt(this.str_goods_baseline, 10);
      this.update_goods_data()
      
      this.update_good = false 
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