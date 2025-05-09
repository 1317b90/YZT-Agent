<template>
  <a-spin :spinning="isLoading">
    <div class="message-container">
      <a-form :model="queryForm" layout="inline" class="query-form">
        <a-form-item label="UserID">
          <a-input v-model:value="queryForm.userid" placeholder="请输入用户ID" allow-clear />
        </a-form-item>
        <a-form-item label="ServiceID">
          <a-input v-model:value="queryForm.serviceid" placeholder="请输入客服ID" allow-clear />
        </a-form-item>
        <a-form-item label="日期范围">
          <a-range-picker v-model:value="dateRange" format="YYYY-MM-DD" @change="onDateChange" />
        </a-form-item>
        <a-form-item>
          <a-button type="primary" @click="fetchMessages" class="query-button">
            <template #icon>
              <SearchOutlined />
            </template>
            查询
          </a-button>
        </a-form-item>
      </a-form>
      <a-divider />
      <div class="messages-table">
        <div class="messages-div" v-for="msg in messages" :key="msg.id">
          <a-card class="message-card">
            <!-- 元信息 -->
            <div class="message-meta">
              <a-tag color="blue">#{{ msg.id }}</a-tag>
              <a-tag color="cyan">用户: {{ msg.userid }}</a-tag>
              <a-tag color="purple">客服: {{ msg.serviceid }}</a-tag>
              <span class="create-time">{{ msg.created_at }}</span>
            </div>

            <!-- 对话内容 -->
            <div class="dialog-content">
              <div v-for="m in msg.messages" :key="m.key" class="message-item">
                <div :class="['message-bubble', m.role]">
                  <span class="role-tag">{{ m.role === 'user' ? '用户' : '客服' }}</span>
                  {{ m.content }}
                </div>
              </div>
            </div>

            <!-- 回答 -->
            <a-alert v-if="msg.answer" class="answer-section" type="info" :message="msg.answer" />
          </a-card>
        </div>

        <!-- 分页 -->
        <div class="pagination-container">
          <a-pagination v-model:current="pagination.current" v-model:pageSize="pagination.pageSize"
            :total="pagination.total" show-size-changer :pageSizeOptions="['10', '20', '50']" @change="handlePageChange"
            show-total :showQuickJumper="true" />
        </div>
      </div>
    </div>
  </a-spin>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted } from 'vue';
import { getMessages } from '@/request/api';
import { message } from 'ant-design-vue';

const isLoading = ref(false)

interface Message {
  id: number;
  created_at: string;
  userid: string;
  serviceid: string;
  messages: Array<{ role: string; content: string; key: number }>;
  answer: string;
}

const queryForm = reactive({
  userid: '',
  serviceid: '',
  page: 1,
  pageSize: 5,
  startDate: '',
  endDate: '',
});

const dateRange = ref();

const messages = ref<Message[]>([]);
const pagination = reactive({
  current: 1,
  pageSize: 5,
  total: 0,
});

const onDateChange = (dates: any) => {
  if (dates) {
    queryForm.startDate = dates[0].format('YYYY-MM-DD HH:mm:ss');
    queryForm.endDate = dates[1].format('YYYY-MM-DD HH:mm:ss');
  } else {
    queryForm.startDate = '';
    queryForm.endDate = '';
  }
};

const fetchMessages = async () => {
  isLoading.value = true
  try {
    const response = await getMessages({
      page: queryForm.page,
      pageSize: queryForm.pageSize,
      serviceid: queryForm.serviceid,
      userid: queryForm.userid,
      startDate: queryForm.startDate,
      endDate: queryForm.endDate,
    });
    messages.value = response.data.data.map((msg: Message) => ({
      ...msg,
      messages: msg.messages.map((m, index) => ({ ...m, key: index })),
    }));
    pagination.total = response.data.total;
  } catch (error) {
    message.error('查询消息失败：' + error);
  } finally {
    isLoading.value = false
  }
};

const handlePageChange = (page: number, pageSize: number) => {
  pagination.current = page;
  pagination.pageSize = pageSize;
  queryForm.page = page;
  queryForm.pageSize = pageSize;
  fetchMessages();
};

onMounted(() => {
  fetchMessages();
});
</script>

<style scoped lang="less">
.query-card {
  margin-bottom: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);

  .query-form {
    :deep(.ant-form-item) {
      margin-bottom: 16px;
    }

    .query-button {
      border-radius: 4px;
    }
  }
}

.message-card {
  margin-bottom: 16px;
  border-radius: 6px;
  transition: box-shadow 0.3s;

  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  .message-meta {
    margin-bottom: 16px;

    .ant-tag {
      border-radius: 4px;
      font-size: 12px;
    }

    .create-time {
      color: #999;
      font-size: 12px;
      margin-left: 8px;
    }
  }

  .dialog-content {
    margin: 12px 0;

    .message-item {
      margin: 8px 0;

      .message-bubble {
        padding: 10px 16px;
        border-radius: 18px;
        max-width: 80%;
        position: relative;

        &.user {
          background: #e6f4ff;
          margin-left: auto;

          .role-tag {
            color: #1890ff;
          }
        }

        &.assistant {
          background: #f6f6f6;

          .role-tag {
            color: #666;
          }
        }

        .role-tag {
          font-size: 12px;
          margin-right: 8px;
          font-weight: bold;
        }
      }
    }
  }

  .answer-section {
    margin-top: 16px;
    border-radius: 4px;
    background: #fafafa;
  }
}

.pagination-container {
  margin-top: 24px;
  display: flex;
  justify-content: center;
}
</style>