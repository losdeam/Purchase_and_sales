<template>
  <div>
    <el-table
      border
      style="width: 100%"
      :data="formattedData"
      element-loading-text="拼命加载中"
    >
      <el-table-column prop="id" label="编号" > </el-table-column>
      <el-table-column prop="name" label="商品名称" ></el-table-column>
      <el-table-column prop="price_buying" label="进货价"> </el-table-column>
      <el-table-column prop="price_retail" label="零售价"> </el-table-column>
      <el-table-column prop="number" label="库存"> </el-table-column>
      <el-table-column prop="baseline" label="基准数"> </el-table-column>
      <el-table-column prop="sort" label="分类"> </el-table-column>
      <el-table-column label="操作">
      <template slot-scope="scope">
        <!-- 这里添加自定义按钮，可以根据需要修改按钮样式和功能 -->
        <el-button @click="update_init(scope.row)">信息更新</el-button>
      </template>      
    </el-table-column>
    </el-table>
    <el-dialog title="修改商品信息"
      :visible.sync="update_good"
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
      <el-button @click="update_good_button">确定</el-button>
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
      str_good_name : '',
      str_good_num : '',
      str_good_price_buying : '',
      str_good_price_retail : '',
      str_good_sort : '',
      str_good_baseline : '',
      transaction: {
        good_id: 1,
        change_num: 0,
        type: 1, // 默认为进货
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
    update_good_data() {
      // 使用后端提供的接口执行交易
      fetch("http://127.0.0.1:50000/api/goods/update", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.new_good_data),
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
      this.new_good_data.good_id = row.id
    },
    update_good_button(){
      
      
      this.new_good_data.new_data.good_name = this.str_good_name
      this.new_good_data.new_data.good_num = parseInt(this.str_good_num, 10);
      this.new_good_data.new_data.good_price_buying = parseFloat(this.str_good_price_buying)
      this.new_good_data.new_data.good_price_retail = parseFloat(this.str_good_price_retail)
      this.new_good_data.new_data.good_sort = this.str_good_sort
      this.new_good_data.new_data.good_baseline = parseInt(this.str_good_baseline, 10);
      console.log(this.new_good_data)
      console.log(this.str_good_baseline)
      this.update_good_data()
      
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