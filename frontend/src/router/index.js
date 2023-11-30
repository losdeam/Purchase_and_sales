import Vue from "vue";
import VueRouter from "vue-router";
import Page from "../views/Page.vue";
import Commodity from "../views/Commodity.vue";
import stock_goods from "../views/stock_goods.vue";
import Header from "../components/Header.vue";
Vue.use(VueRouter);
 
const routes = [
  {
    path: "/",
    redirect: "/Page",
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
        path: "/page/stock",
        name: "stock_goods",
        component: stock_goods,
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