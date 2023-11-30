Popup.vue
<template>
    <div class="popup">
      <input v-model="inputValue" placeholder="输入内容" />
      <button @click="onButtonClick">确定</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        inputValue: ''
      };
    },
    methods: {
      onButtonClick() {
        // 在这里处理按钮点击事件，可以通过 this.inputValue 获取输入框的值
        // 例如，可以将输入的值提交给父组件或执行其他逻辑
        this.$emit('confirm', this.inputValue);
      }
    }
  };
  </script>
  
  <style scoped>
  /* 可以在这里添加样式，使弹出窗口看起来更好看 */
  .popup {
    padding: 20px;
    border: 1px solid #ccc;
    background-color: #fff;
  }
  </style>
  