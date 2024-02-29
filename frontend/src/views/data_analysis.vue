<template>
      <div>
      
      <div id = "main" style="width:1200px;height:600px;"></div>
      <div id="cate" style="width:1200px;height:600px;"></div>

      <!-- <div id="category1" style="width:1200px;height:600px;"></div>
      <div id="category2" style="width:1200px;height:600px;"></div>
      <div id="category3" style="width:1200px;height:600px;"></div>
      <div id="category4" style="width:1200px;height:600px;"></div>
      <div id="category5" style="width:1200px;height:600px;"></div> -->

      <el-carousel      style="width:1200px;height:600px;"    >
        <el-carousel-item v-for="item in 5" :key="item" style="width:1200px;height:600px;" >

            <!-- <p>{{item }}</p> -->
            <div :id="'category'+ item " style="width: 1200px; height: 600px;" ></div>
        
          </el-carousel-item>
      </el-carousel>

    </div>
</template>

<script>
export default {
  data() {
    return {
      dict_data: {
        salesData: {},
        percateData: {},
      },
      list_data:{      
        seriesData : [],
        percatelist : [],
      },

      dict_dict_category:{

      },
      dict_list_category:{

      } ,
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.fetchProducts()
    });
  },
   
    

  methods: {
  fetchProducts() {
    // 使用后端提供的接口获取商品数据
    fetch("http://127.0.0.1:50000/api/analyze/analyze_dataget", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include", // 添加此行，确保携带 Cookie
    })
      .then((response) => response.json())
      .then((data) => {
      
        const rawData = JSON.stringify( data["goods"]);
        const parsedArray = JSON.parse(rawData);
        this.dict_data.salesData = parsedArray
        for (let key in this.dict_data.salesData) {
          this.list_data.seriesData.push({name: key, value: this.dict_data.salesData[key]})
        }
        this.draw("各项商品的销量","main",this.list_data.seriesData,this.list_data.seriesData)
        


        const rawData_ = JSON.stringify( data["best_percate"]);
        const parsedArray_ = JSON.parse(rawData_);
        this.dict_data.percateData = parsedArray_
        // console.log(parsedArray_)
        // console.log(this.dict_data.percateData)
        for (let key in this.dict_data.percateData) {
          this.list_data.percatelist.push({name: key, value: this.dict_data.percateData[key]})
        }
        // console.log(123123123,this.list_data.percatelist)
        this.draw("各类商品的最高销量","cate",this.list_data.percatelist,this.dict_data.percateData)

        const rawData1 = JSON.stringify( data["per_category_goods"]);
        const parsedArray1 = JSON.parse(rawData1);
        for (let key in parsedArray1) {
          this.dict_dict_category[key] =  parsedArray1[key]
          // console.log(this.dict_dict_category[key])
          this.dict_list_category[key] = []
          for (let key1 in parsedArray1[key]){
            this.dict_list_category[key].push({name: key1, value: parsedArray1[key][key1]})
          }
          // console.log(parsedArray1[key])
          console.log(key)
          this.draw(key,key,this.dict_list_category[key],parsedArray1[key])

        }
        // console.log(this.dict_dict_category)
        // this.draw("各类商品的最高销量","category1",this.list_data.percatelist,this.dict_data.percateData)
        

      })

  },
  draw(title_,id,data,x_data){
    // console.log(title_,Object.values(data))
    console.log(Object.keys(x_data))
    console.log(Object.values(data))
      let myChart = this.$echarts.init(document.getElementById(id));
      
      // 指定图表的配置项和数据
      let option = {
      //表头
        title: {
          text: title_
        },
        tooltip: {}, //提示
        legend: {
          //图例
          data: ["销量"] //对应series每一项中的name
        },
        xAxis: {
          //x轴显示内容
          data: Object.keys(x_data)
        },
        yAxis: {}, //y轴默认
        series: [ 
          //数据1  柱形
          {
            name: "销量",
            type: "bar", //类型  柱形
            data: Object.values(data) //柱形的点
          },
        ]
      }
      myChart.setOption(option);

  },

},
};
</script>


<style scoped>

.chart-container {
  width: 100%;
  height: 100%;
}
</style>
