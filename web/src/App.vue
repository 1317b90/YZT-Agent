<template>
  <a-layout style="height: 100vh">
    <!-- 左边导航栏 -->
    <a-layout-sider v-model:collapsed="collapsed" collapsible>
      <div class="logo">
        <img src="@/assets/logo_title.png" alt="" class="logo_img">
      </div>
      <!-- 菜单 -->

      <a-menu v-model:selectedKeys="selectedKeys" :open-keys="['/task', '/operation']" theme="dark" mode="inline"
        @select="selectMenu">

        <a-sub-menu key="/task">
          <template #title>
            <span>
              <FileDoneOutlined />
              <span>任务管理</span>
            </span>
          </template>
          <a-menu-item key="/">任务记录</a-menu-item>
          <a-menu-item key="/task/redis">Redis</a-menu-item>

        </a-sub-menu>

        <a-sub-menu key="/operation">
          <template #title>
            <span>
              <FileDoneOutlined />
              <span>脚本操作</span>
            </span>
          </template>
          <a-menu-item key="/operation/make_invoice">电税局开票</a-menu-item>

        </a-sub-menu>

        <a-menu-item key="/user">
          <FileTextOutlined />
          <span>用户管理</span>
        </a-menu-item>

        <a-menu-item key="/message">
          <CommentOutlined />
          <span>聊天记录</span>
        </a-menu-item>

        <a-menu-item key="/log">
          <FileTextOutlined />
          <span>日志管理</span>
        </a-menu-item>





      </a-menu>
    </a-layout-sider>

    <!-- 右边区域 -->
    <a-layout>
      <!-- 页头 -->
      <a-layout-header class="app-header">
        <h1>{{ $route.fullPath }}</h1>
      </a-layout-header>
      <!-- 页心 -->
      <a-layout-content class="app-content">

        <div class="app-content-div">
          <RouterView />
        </div>
      </a-layout-content>
      <!-- 页脚 -->
      <!-- <a-layout-footer class="app-footer" style="">
        RPA manage ©2024 Created by Olive
      </a-layout-footer> -->
    </a-layout>
  </a-layout>
</template>
<script lang="ts" setup>
import {
  FileDoneOutlined,
  FileTextOutlined,
  FolderOpenOutlined,
  CommentOutlined,
} from '@ant-design/icons-vue';

import { RouterView } from 'vue-router'
import { useRouter } from 'vue-router';
const router = useRouter();

import { ref } from 'vue';
const collapsed = ref<boolean>(false);
const selectedKeys = ref<string[]>(['/']);

selectedKeys.value[0] = sessionStorage.getItem('router') || '/';

// 选择菜单时
function selectMenu(item: any) {
  // 存储到本地，避免刷新丢失
  sessionStorage.setItem('router', item.key);
  router.push(item.key)
}
</script>
<style scoped>
.logo {
  padding: 15px;
}

.logo_img {
  width: 100%;
}

.site-layout .site-layout-background {
  background: #fff;
}

[data-theme='dark'] .site-layout .site-layout-background {
  background: #141414;
}

.app-header {
  background-color: #fff;
  box-shadow: rgba(0, 0, 0, 0.1) 0px 2px 12px 0px;
  padding: 0px 30px 0px 30px;
}

.app-content {

  margin: 15px;
}

.app-content-div {
  background-color: #fff;
  height: calc(100vh - 30px - 64px);
  padding: 15px;
  overflow: auto;
}

.app-footer {
  text-align: center;
  padding: 0px;
  height: 20px;
  width: 100%;
}
</style>
