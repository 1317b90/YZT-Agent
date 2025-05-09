<template>
  <div class="content">
    <!-- 上传数据 -->
    <!-- <div class="file-upload">
      <a-button :icon="h(PlusOutlined)" class="addButton" type="primary" @click="onAdd"/>
      <a-upload
      accept=".xlsx"
      :beforeUpload="handleBeforeUpload"
      :showUploadList="false"
      >

      <a-button class="action-button">
        从本地上传文件
      </a-button>
    </a-upload>

  </div> -->
    <a-button :icon="h(PlusOutlined)" class="addButton" type="primary" @click="onAdd" />
    <!-- 数据表格 -->
    <a-table :row-selection="{ onChange: onSelectChange, selectedRowKeys: selectedRow }"
      :row-key="(record: DataType, index: number) => index" :columns="columns" :data-source="tableData"
      :expandedRowKeys="errorIndex" :pagination="{ pageSize: 9 }" :scroll="{ x: 850 }">
      <template #expandedRowRender="{ index }">
        <p v-for="errorMsg in errorList[index]">
          <a-tag :bordered="false" color="processing">{{ errorMsg.name }}</a-tag>
          <a-tag :bordered="false" color="error">{{ errorMsg.msg }}</a-tag>
        </p>
      </template>
      <template #bodyCell="{ column, text }">
        <template v-if="column.dataIndex === 'name'">
          <a>{{ text }}</a>
        </template>
      </template>
    </a-table>

    <!-- 操作按钮 -->
    <div class="doButtonDiv">
      <a-button type="primary" :icon="h(CaretRightOutlined)" @click="onExec" :loading="isLoading">执行</a-button>
      <a-button :icon="h(EditOutlined)" @click="onEdit" />
      <a-button :icon="h(DeleteOutlined)" @click="onDel" />
      <a-button :icon="h(ClearOutlined)" @click="onClear" />
    </div>

  </div>

  <a-modal v-if="isFrom" v-model:open="isFrom" title="Title" style="width: 650px;">
    <VarForm :selectedInput="selectedMenu.input" :formData="formData" :onSave="onSave" />

    <!-- 去除默认的底部按钮 -->
    <template #footer>
    </template>
  </a-modal>


</template>

<script lang="ts" setup>
import { onMounted, ref, type Ref } from 'vue';
import { h } from 'vue';
import { message } from 'ant-design-vue';
import { DeleteOutlined, EditOutlined, PlusOutlined, ClearOutlined, CaretRightOutlined } from '@ant-design/icons-vue';
import { createTask } from '@/request/api'
import VarForm from './form.vue'
import { menuDict } from '@/data/menu';

import { useRoute } from 'vue-router';

const route = useRoute();
const operationType = route.params.operationType;


// 接口定义
interface DataType {
  [key: string]: string;
}

// ref 变量
const file = ref<File | null>(null);
const isLoading = ref(false);
const columns = ref<{ title: string; dataIndex: string }[]>([]);
const tableData = ref<DataType[]>([]);
const selectedRow = ref<number[]>([]);
const formData = ref();
const isFrom = ref(false);
const fromType = ref("set");

const errorIndex = ref<number[]>([]);
const errorList = ref<Record<number, { name: string; msg: string }[]>>({});


const selectedMenu = ref<MenuItem>({
  type: '',
  name: '',
  input: []
});


onMounted(() => {
  const menu = menuDict.find(item => item.type === operationType);
  if (menu) {
    selectedMenu.value = menu;
    selectedMenu.value.input.forEach(input => {
      if (input.required) {
        columns.value.push({
          title: `${input.name} ${input.var}`,
          dataIndex: input.var,
        });
      }
    });
  }
});

interface MenuInput {
  var: string;
  name: string;
  required: boolean;
  default: string;
}
interface MenuItem {
  type: string;
  name: string;
  input: MenuInput[];
}



// 点击手动添加数据
const onAdd = () => {
  if (!selectedMenu.value) {
    message.error('请先选择功能');
    return;
  }
  formData.value = selectedMenu.value.input.reduce((obj: any, column: MenuInput) => {
    obj[column.var] = column.default;
    return obj;
  }, {});
  isFrom.value = true;
  fromType.value = "new";
};


// 上传文件之前
// const handleBeforeUpload = (fileObj: File) => {
//   file.value = fileObj;
//   uploadFile();
//   return false;
// };

// 上传文件函数
// const uploadFile = async () => {
//   if (!file.value) {
//     message.error('请选择文件');
//     return;
//   }
//   const formData = new FormData();
//   formData.append('file', file.value);
//   try {
//     const res = await upFileBatch(formData);
//     message.success('上传成功');
//     tableData.value.push(...res.data.data);
//   } catch (err) {
//     message.error(`上传失败: ${err}`);
//     console.error('上传失败', err);
//   }
// };

// 选中表格数据时
const onSelectChange = (selectedRowKeys: number[]) => {
  selectedRow.value = selectedRowKeys;
};

// 表格数据新增或修改时
const onSave = (newData: DataType) => {
  if (fromType.value == "set") {
    tableData.value[selectedRow.value[0]] = newData;
    message.success('保存成功！');
  } else {
    tableData.value.push(newData);
    message.success('新增成功！');
  }

  isFrom.value = false;
};


// 点击提交任务
const onExec = async () => {
  if (selectedRow.value.length === 0 && columns.value.length !== 0) {
    message.warning('请选择要执行的数据');
  } else if (tableData.value.length === 0 && columns.value.length !== 0) {
    message.error('表格数据为空，请先上传数据');
  } else {
    isLoading.value = true;
    errorIndex.value = [];
    errorList.value = {};

    // 如果列头为空，则说明不需要输入，可直接执行
    if (columns.value.length === 0) {
      selectedRow.value = [0];
      tableData.value = [{}];
    }

    const delIndex = new Set<number>();

    for (const i of selectedRow.value) {
      const rowData = tableData.value[i];
      const rowErrorMsg: { name: string; msg: string }[] = [];

      try {
        await createTask(selectedMenu.value?.type || '', rowData);
        delIndex.add(i);
      } catch (err: any) {
        errorIndex.value.push(i);
        rowErrorMsg.push({ name: selectedMenu.value?.type || '', msg: err.toString() });
        errorList.value[i] = rowErrorMsg;
      }
    }

    tableData.value = tableData.value.filter((_, index) => !delIndex.has(index));
    selectedRow.value = [];

    if (errorIndex.value.length > 0) {
      message.warning('部分任务添加失败，请检查错误信息！');
    } else {
      message.success('任务添加完毕！');
    }
    isLoading.value = false;
  }
};

// 编辑表格数据
const onEdit = () => {
  if (selectedRow.value.length === 0) {
    message.warning('请选择要编辑的数据');
  } else if (selectedRow.value.length > 1) {
    message.warning('只能选择一条数据进行编辑');
  } else {
    const index = selectedRow.value[0];
    const rowData = tableData.value[index];
    formData.value = rowData;
    isFrom.value = true;
    fromType.value = "set";
  }
};

// 删除表格数据
const onDel = () => {
  if (selectedRow.value.length === 0) {
    message.warning('请选择要删除的数据');
    return;
  }
  const indexesToDelete = new Set(selectedRow.value.sort((a, b) => b - a));
  tableData.value = tableData.value.filter((_, index) => !indexesToDelete.has(index));
  selectedRow.value = [];
  message.success(`成功删除 ${indexesToDelete.size} 条数据`);
};

// 清空表格数据
const onClear = () => {
  tableData.value = [];
  selectedRow.value = [];
  message.success('清空成功！');
};



</script>

<style scoped>
#selectFuncDiv {
  background-color: #f7f7f7;
  padding: 10px 10px 10px 30px;
  border-radius: 4px;

}

#selectFuncDiv h3 {
  color: #1890ff;
  font-weight: bold;
  margin-bottom: 10px;
}

#selectButtonDiv {
  margin-top: 10px;
  display: flex;
  justify-content: flex-end;
  gap: 15px;
}

.addButton {
  margin-right: 20px;
}

.file-upload {
  margin-top: 10px;
  margin-bottom: 10px;
  padding-bottom: 20px;
  padding-left: 20px;
  display: flex;
  align-items: center;
  /* background-color: #f5f5f5; */
}

.file-label {
  display: inline-block;
  padding: 4px 15px;
  background-color: #1890ff;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.file-label:hover {
  background-color: #40a9ff;
}

.file-input {
  display: none;
}

.file-name {
  margin-left: 10px;
  font-size: 14px;
}

.doButtonDiv {
  margin-left: 20px;
  margin-top: 20px;
}

.doButtonDiv>* {
  margin-right: 10px;
}
</style>