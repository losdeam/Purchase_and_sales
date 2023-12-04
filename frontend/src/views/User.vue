<template>
    <div>
      <el-table :data="formattedData">
        <el-table-column prop="user_id" label="编号" width="180"> </el-table-column>
        <el-table-column prop="user_name" label="用户名" width="180">
        </el-table-column>
        <el-table-column prop="user_rank" label="角色"> </el-table-column>
        <el-table-column prop="user_power" label="权限"> </el-table-column>
        <el-table-column prop="role" label="操作">
          <template v-slot="scope">
            <el-button
              type="danger"
              size="mini"
              @click="deleteData"
              >删除</el-button
            >
            <!--  @click="deleteData(scope.row.name)" -->
            <el-dialog title="提示" width="30%">
              <span class="warcont"
                ><i class="el-icon-warning"></i>是否确定要删除该用户</span
              >
              <span slot="footer" class="dialog-footer">
                <el-button>取 消</el-button>
                <el-button type="primary">确 定</el-button>
              </span>
            </el-dialog>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </template>
  <script>
  import { mapState } from "vuex";
  export default {
    name: "User",
   
    data() {
      return {
        formattedData :[],

      };
    },
    computed: {
      ...mapState(["tableData"]),
    },
    mounted() {

      this.getdata()
    //  setTimeout(() => {
    //    this.loading = false;
    //     this.$axios.get("/users").then((res) => {
    //     const home = res.data;
    //     this.$store.commit("addrecord", home);
    //   });
    //  }, 500);
    },
   
    methods: {
      getdata(){
        // 使用后端提供的接口获取商品数据
        fetch("http://127.0.0.1:50000/api/auth/show", {
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
            user_id: item.user_id,
            user_name: item.user_name,
            user_password: item.user_password,
            user_rank: item.user_rank,
            user_power: item.user_power,
          };

        });
        })

    },
      //  deleteData(name)
      deleteData(index,row){
                this.$confirm('此操作将永久删除该文件, 是否继续?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            this.$message({
              type: 'success',
              message: '删除成功!'
            });
          /*    var index = this.tableData.findIndex(item => {
                          return item.name === name;
                      });
            this.tableData.splice(index,1) */
            this.tableData.splice(index,1)
          }).catch(() => {
            this.$message({
              type: 'info',
              message: '已取消删除'
            });          
          });
      },
      handleClick(tab, event) {
        console.log(tab, event);
      },
    },
  };
  </script>