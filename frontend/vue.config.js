const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})
module.exports = {
	//关闭每次保存代码都进行eslint检验
   lintOnSave: false,
};