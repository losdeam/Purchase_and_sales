import Vue from "vue";
import VueRouter from "vue-router";
import Page from "../views/Page.vue";
import Commodity from "../views/Commodity.vue";
import sales_record  from "../views/sales_record.vue";
import stock_goods from "../views/stock_goods.vue";
import Header from "../components/Header.vue";
import Login from "../views/Login.vue";
import User from "../views/User.vue";
import recognition from "../views/recognition.vue";
import model_operation from "../views/model_operation.vue";
import config from "../views/config.vue";
import analysis from "../views/data_analysis.vue";
Vue.use(VueRouter);
 
const routes = [
  {
    path: "/",
    redirect: "/Login",
  },
  {
    path: "/Login",
    name: "Login",
    component: Login,
  },
  {
    path: "/page",
    name: "Page",
    components: {
      default: Page,
      Header,
    },
    children: [
      {
        path: "/page",
        redirect: "/page/commodity",
      },
      {
        path: "/page/commodity",
        name: "Commodity",
        component: Commodity,
      },
      {
        path: "/page/analysis",
        name: "analysis",
        component: analysis,
      },
      {
        path: "/page/stock",
        name: "stock_goods",
        component: stock_goods,
      },
      {
        path: "/page/sales_record",
        name: "sales_record",
        component: sales_record,
      },
      {
        path: "/page/recognition",
        name: "recognition",
        component: recognition,
      },
      {
        path: "/page/user",
        name: "User",
        component: User,
      },
      {
        path: "/page/model_operation",
        name: "model_operation",
        component: model_operation,
      },
      {
        path: "/page/config",
        name: "config",
        component: config,
      },
    ],
  },
 
];
 
const router = new VueRouter({
  routes,
  mode: "history",
});
router.beforeEach((to, from, next) => {
  next();
  // if (to.path == "/login") {
  //   next();
  // } else {
  //   let token = window.sessionStorage.getItem("username");
  //   console.log(token);
  //   if (!token) {
  //     next("/login");
  //   } else {
  //     next();
  //   }
  // }
});
const originalPush = VueRouter.prototype.push;
// 重写了原型上的push方法，统一的处理了错误信息
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch((err) => err);
};
export default router;