
<template>
      <div>
      
      <div id = "main" style="width:1200px;height:600px;"></div>
      <div id="cate" style="width:1200px;height:600px;"></div>

      <div>
        最常同时出现的销售组合
        {{ recommend }}
      </div>
    </div>
</template>

<script>

export default {
  
  data() {
    return {
      recommend :"",
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
  // 在组件加载时获取商品数据
  this.$nextTick(() => {
      this.fetchProducts();
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
        for (let key in this.dict_data.percateData) {
          this.list_data.percatelist.push({name: key, value: this.dict_data.percateData[key]})
        }
        this.draw("各类商品的最高销量","cate",this.list_data.percatelist,this.dict_data.percateData)


        const recommend_ = JSON.stringify( data["best_percate"]);
        const recommend_1 = JSON.parse(rawData_);
        for (let key in this.dict_data.percateData) {
          this.list_data.percatelist.push({name: key, value: this.dict_data.percateData[key]})
        }


        this.recommend = data["recommend"]
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
