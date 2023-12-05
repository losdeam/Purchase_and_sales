<template>
  <div class="header">
    <div class="header-left">
      <div class="left">进销货管理系统</div>
    </div>
    <div class="header-right">
      <div class="header-right__logout">
        <el-button type="danger" size="20" @click="logout">退出</el-button>
      </div>
      <div class="header-right__info">
        <div class="right">{{ name }}</div>
      </div>
    </div>
  </div>
</template>
 
<script>
import { mapState } from "vuex";
export default {
  name: "Header",
  data() {
    return {
      name: "",
    };
  },
  mounted() {
    this.name = window.sessionStorage.getItem("username");
  },
  methods: {
    logout_t(){
        // 使用后端提供的接口获取商品数据
        fetch("http://127.0.0.1:50000/api/auth/logout", {
                method: "post",
                headers: {
                  "Content-Type": "application/json",
                },
                credentials: "include", // 添加此行，确保携带 Cookie
              })
        .then((response) => response.json())
        .then((data) => {
        })

    },
    logout() {
      this.$confirm("您确定要退出吗, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.logout_t()
          this.$message({
            message: "你已经退出登陆！请重新登录账号",
            type: "warning",
          });
          this.$router.push({ path: "/" });
        })
        .catch((err) => err);
    },
    
  },
  computed: {
    ...mapState(["user"]),
  },
};
</script>
 
<style >
.header {
  height: 50px;
  line-height: 50px;
  background-color: rgb(73, 80, 96);
  padding: 0 50px;
  color: #fff;
}
.left {
  color: #fff;
  float: left;
}
.header-right__info {
  float: right;
  margin: 0 20px;
}
.header-right__logout {
  float: right;
}
</style>