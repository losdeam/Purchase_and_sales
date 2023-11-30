import Vue from "vue";
import VueRouter from "vue-router";
import Login from "../views/Login.vue";
import Page from "../views/Page.vue";
import Page2 from "../views/Page2.vue";
import User from "../views/User.vue";
import Commodity from "../views/Commodity.vue";
import Header from "../components/Header.vue";
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
        redirect: "/page/user",
      },
      {
        path: "/page/user",
        name: "User",
        component: User,
      },
      {
        path: "/page/commodity",
        name: "Commodity",
        component: Commodity,
      },
    ],
  },
  {
    path: "/page2",
    name: "Page2",
    components: {
      default: Page2,
      Header,
    },
    children: [
      {
        path: "/page2",
        redirect: "/page2/commodity",
      },
      {
        path: "/page2/commodity",
        name: "Commodity2",
        component: Commodity,
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