// import Vue from 'vue'
// import Vuex from 'vuex'
 
// Vue.use(Vuex)
 
// export default new Vuex.Store({
//   state: {
//     tableData:[],
//     table:[],
//     user:JSON.parse(window.sessionStorage.getItem('user') || '[]'),
//   },
//   // 存储用户管理页面数据
//   mutations: {
//     addrecord(state,preload){
//       state.tableData = preload
//       window.sessionStorage.setItem('rightsList',JSON.stringify(preload))
//     },
//     // 存储商品管理数据
//     record(state,preload){
//       state.table = preload
//       console.log(JSON.stringify(preload));  
// 			window.sessionStorage.setItem('user',JSON.stringify(state.user));
// 		},
//   },
//   actions: {
//   },
//   modules: {
//   }
// })