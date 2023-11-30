<template>
    <div>
      <el-table :data="tableData" v-loading="loading">
        <el-table-column prop="id" label="编号" width="180"> </el-table-column>
        <el-table-column prop="name" label="用户名" width="180">
        </el-table-column>
        <el-table-column prop="role" label="角色"> </el-table-column>
        <el-table-column prop="phone" label="手机号码"> </el-table-column>
        <el-table-column prop="email" label="邮箱"> </el-table-column>
        <el-table-column prop="role" label="操作">
          <template v-slot="scope">
            <el-button
              type="danger"
              size="mini"
              @click="deleteData(scope.$index.tableData)"
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
  <!-- <script>
  import { mapState } from "vuex";
  export default {
    name: "User",
   
    data() {
      return {
        loading: false,
      };
    },
    computed: {
      ...mapState(["tableData"]),
    },
    mounted() {
      this.loading = true;
     setTimeout(() => {
       this.loading = false;
        this.$axios.get("/users").then((res) => {
        const home = res.data;
        this.$store.commit("addrecord", home);
      });
     }, 500);
    },
   
    methods: {
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
  </script> -->