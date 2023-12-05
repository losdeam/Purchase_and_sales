<template>
    <div>
      <el-button type="primary" @click="self_add_auth">添加新用户</el-button>
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
              @click="deleteData(scope.row)"
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
      <el-dialog title="新用户添加"
      :visible.sync="add_new_auth"
      width="30%"
    >
      <!-- 弹窗内容 -->
      <div>
        <!-- 在这里放置弹窗中的内容，可以是表单、按钮等 -->
        <el-input v-model="new_user_data.user_name" placeholder="输入内容">
        <template slot="prepend">用户名：</template></el-input>
        <el-input v-model="new_user_data.password" placeholder="输入内容">
        <template slot="prepend">密码：</template></el-input>
        <div class="checkbox-group">
          <h3 class="group-title">权限设置</h3>
          <el-checkbox v-model="watch_good" label="Option 1">查看商品信息</el-checkbox>
          <el-checkbox v-model="change_good" label="Option 2">修改商品信息</el-checkbox>
          <el-checkbox v-model="add_new_good" label="Option 3">添加全新商品</el-checkbox>
          <el-checkbox v-model="add_new_user" label="Option 4">添加全新用户</el-checkbox>
        </div>
          <el-button @click="add_new_user_confirm">确定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="操作成功"
      :visible.sync="operation_success"
      width="30%"
    >
      <!-- 弹窗内容 -->
      <div>
        <!-- 在这里放置弹窗中的内容，可以是表单、按钮等 -->
        <p>{{ dynamicText }}</p>
      </div>
    </el-dialog>
    <el-dialog title="操作失败"
      
      :visible.sync="operation_fail"
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

  import { mapState } from "vuex";
  export default {

    name: "User",
    
    data() {
      return {
        formattedData :[],
        operation_success : false,
        operation_fail : false,
        add_new_auth : false ,
        watch_good : false,
        change_good : false,
        add_new_good : false,
        add_new_user : false,
        dynamicText : "",
        new_user_data:{
          user_name:""   ,
          password:"",
          rank:1,
          power:0,
        },
        user_data : {
          user_id :0 ,
        } ,
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
            user_id: item.user_id,
            user_name: item.user_name,
            user_password: item.user_password,
            user_rank: item.user_rank,
            user_power: item.user_power,
          };

        });
        })

    },
    self_add_auth(){
      this.add_new_auth = true 
    },
    add_new_user_confirm(){
      this.new_user_data.power = 0 
      if (this.watch_good) this.new_user_data.power = this.new_user_data.power + 1
      if (this.change_good) this.new_user_data.power = this.new_user_data.power + 2
      if (this.add_new_good) this.new_user_data.power = this.new_user_data.power + 4
      if (this.add_new_user) this.new_user_data.power = this.new_user_data.power + 8
        // 使用后端提供的接口获取商品数据
        console.log(this.new_user_data)
        fetch("http://127.0.0.1:50000/api/auth/register", {
                        method: "POST",
                        headers: {
                          "Content-Type": "application/json",
                        },
                        credentials: "include", // 添加此行，确保携带 Cookie
                        body: JSON.stringify(this.new_user_data),
                      })
                .then((response) =>{
                // 检查响应状态码
                if (!response.ok) {
                  this.operation_fail = true;
                }
                else{
                  this.operation_success = true;
                }
                return response.json();
              })
              .then((data) => {
                this.dynamicText = data;
                
              })
      },
    delete(){
      fetch("http://127.0.0.1:50000/api/auth/delete", {
                        method: "POST",
                        headers: {
                          "Content-Type": "application/json",
                        },
                        credentials: "include", // 添加此行，确保携带 Cookie
                        body: JSON.stringify(this.user_data),
                      })
                .then((response) =>{
                // 检查响应状态码
                if (!response.ok) {
                  this.add_new_auth = false
                  this.operation_fail = true;
                  
                }
                else{
                  this.add_new_auth = false
                  this.operation_success = true;
                  
                }
                return response.json();
              })
              .then((data) => {
                this.dynamicText = data;
                this.getdata()
              })
    },
      deleteData(row){
                this.$confirm('此操作将永久删除该文件, 是否继续?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning' 
          }).then(() => {
            this.user_data.user_id = row.user_id
            this.delete()
            this.$message({
              type: 'success',
              message: '删除成功!'
            })

          })
      },
      handleClick(tab, event) {
        console.log(tab, event);
      },
      handleCheckboxChange(checkedItems) {
      console.log('Checked items changed:', checkedItems);
    },
    },
  };
  </script>

<style scoped>
.checkbox-group {
  padding: 10px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  margin: 10px;
}

.group-title {
  margin-bottom: 0px;
  font-size: 16px;
  color: #333;
}
</style>