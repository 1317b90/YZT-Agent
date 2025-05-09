<template>
  <a-table class="varTable" :columns="columns" :rowKey="(record: userI) => record.userid" :data-source="data"
    :pagination="{ current: page, pageSize: pageSize, total: total, showSizeChanger: true, showTotal: (total: number) => `共 ${total} 条记录`, onChange: handleTableChange }">
    <template #headerCell="{ column }">
      <template v-if="column.dataIndex === 'operation'">
        <a-button class="editable-add-btn" @click="onAddVar" type="primary" :icon="h(PlusOutlined)">添加用户</a-button>
      </template>
    </template>
    <template #bodyCell="{ column, record }">
      <template v-if="column.dataIndex === 'enable'">
        <a-switch v-model:checked="record.enable" size="small" disabled />
      </template>
      <template v-if="column.dataIndex === 'is_admin'">
        <a-switch v-model:checked="record.is_admin" size="small" disabled />
      </template>
      <template v-if="column.dataIndex === 'is_zero'">
        <a-switch v-model:checked="record.is_zero" size="small" disabled />
      </template>
      <template v-if="column.dataIndex === 'is_bill'">
        <a-switch v-model:checked="record.is_bill" size="small" disabled />
      </template>
      <template v-if="column.dataIndex === 'operation'">
        <a-space>
          <a-button type="primary" size="small" :icon="h(FormOutlined)" @click="onEdit(record)">编辑</a-button>
          <a-popconfirm title="确定删除此用户?" placement="leftTop" ok-text="确定" cancel-text="取消" @confirm="onDel(record)">
            <a-button type="primary" danger size="small" :icon="h(DeleteOutlined)">删除</a-button>
          </a-popconfirm>
        </a-space>
      </template>
    </template>
  </a-table>
  <a-modal v-if="isModal" v-model:open="isModal" :title="modalData?.userid ? '编辑用户' : '添加用户'" :width="600">
    <VarForm :data="modalData" :getData="getData" />
    <template #footer></template>
  </a-modal>
</template>

<script lang="ts" setup>
import { message, type TableColumnType } from 'ant-design-vue';
import { onMounted, ref, type Ref } from 'vue';
import { h } from 'vue';
import { DeleteOutlined, FormOutlined, PlusOutlined } from '@ant-design/icons-vue';
import { getUser, delUser } from "@/request/api";
import VarForm from './form.vue';
import type { userI } from '@/interface';

// 状态和引用
const data: Ref<userI[]> = ref([]);
const isModal = ref(false);
const modalData = ref<userI>();
const page = ref(1);
const pageSize = ref(10);
const total = ref(0);

// 表格列定义
const columns: TableColumnType<userI>[] = [
  { title: '用户ID', dataIndex: 'userid', width: 100, align: "center" },
  { title: '公司名称', dataIndex: 'company_name', align: "center" },
  { title: '群聊名称', dataIndex: 'group_name', align: "center" },

  { title: '社会信用代码', dataIndex: 'uscid', align: "center" },
  { title: '电税局账号', dataIndex: 'dsj_username', align: "center" },
  { title: '电税局密码', dataIndex: 'dsj_password', align: "center" },
  { title: '开户银行', dataIndex: 'bank_name', align: "center" },
  { title: '银行卡号', dataIndex: 'bank_id', align: "center" },
  // { title: '是否管理员', dataIndex: 'is_admin', width: 100, align: "center" },
  // { title: '是否零申报', dataIndex: 'is_zero', width: 100, align: "center" },
  // { title: '是否上传对账单', dataIndex: 'is_bill', width: 100, align: "center" },
  { title: '是否启用', dataIndex: 'enable', width: 100, align: "center" },
  { title: '操作', dataIndex: 'operation', fixed: 'right', width: 180, align: "center" },
];

// 处理表格分页变化
const handleTableChange = (newPage: number, newPageSize: number) => {
  page.value = newPage;
  pageSize.value = newPageSize;
  getData();
};

// 获取用户数据
const getData = () => {
  getUser({
    page: page.value,
    page_size: pageSize.value
  }).then(res => {
    data.value = res.data.data;
    total.value = res.data.total;
    isModal.value = false;
  }).catch(err => {
    message.error(err);
  });
};

// 点击添加用户
const onAddVar = () => {
  isModal.value = true;
  modalData.value = {
    userid: "",
    company_name: "",
    group_name: "",
    is_admin: false,
    uscid: "",
    dsj_username: "",
    dsj_password: "",
    bank_name: "",
    bank_id: "",
    invoice_habit: "",
    is_zero: false,
    is_bill: false,
    puppet_id: "",
    enable: true
  }
};

// 点击编辑用户
const onEdit = (rowData: userI) => {
  modalData.value = { ...rowData };
  isModal.value = true;
};

// 点击删除用户
const onDel = (rowData: userI) => {
  delUser(rowData.userid || "").then(() => {
    getData();
    message.success("删除成功！");
  }).catch(err => {
    message.error(err);
  });
};

// 初始化
onMounted(() => {
  getData()
})
</script>

<style scoped>
.varTable {
  background: #fff;
  padding: 16px;
  border-radius: 8px;
}

.editable-add-btn {
  margin-bottom: 8px;
}
</style>