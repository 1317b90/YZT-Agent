<template>
    <a-form :model="data" name="basic" :label-col="{ span: 6 }" @finish="onFinish">
        <a-form-item label="用户ID" name="userid" :rules="[{ required: true, message: '请输入对应用户ID' }]">
            <a-input v-model:value="data.userid" />
        </a-form-item>

        <a-form-item label="公司名称" name="company_name" :rules="[{ required: true, message: '请输入对应公司名称' }]">
            <a-input v-model:value="data.company_name" />
        </a-form-item>

        <a-form-item label="群聊名称" name="group_name">
            <a-input v-model:value="data.group_name" />
        </a-form-item>

        <a-form-item label="是否管理员" name="is_admin">
            <a-switch v-model:checked="data.is_admin" />
        </a-form-item>

        <a-form-item label="社会信用代码" name="uscid" :rules="[{ required: true, message: '请输入对应社会信用代码' }]">
            <a-input v-model:value="data.uscid" />
        </a-form-item>

        <a-form-item label="电税局账号" name="dsj_username" :rules="[{ required: true, message: '请输入对应电税局账号' }]">
            <a-input v-model:value="data.dsj_username" />
        </a-form-item>

        <a-form-item label="电税局密码" name="dsj_password" :rules="[{ required: true, message: '请输入对应电税局密码' }]">
            <a-input v-model:value="data.dsj_password" />
        </a-form-item>

        <a-form-item label="开户银行" name="bank_name" :rules="[{ required: true, message: '请输入对应开户银行' }]">
            <a-input v-model:value="data.bank_name" />
        </a-form-item>

        <a-form-item label="银行账号" name="bank_id" :rules="[{ required: true, message: '请输入对应银行账号' }]">
            <a-input v-model:value="data.bank_id" />
        </a-form-item>

        <a-form-item label="开票习惯" name="invoice_habit">
            <a-input v-model:value="data.invoice_habit" />
        </a-form-item>

        <a-form-item label="是否零申报" name="is_zero">
            <a-switch v-model:checked="data.is_zero" />
        </a-form-item>

        <a-form-item label="是否开票" name="is_bill">
            <a-switch v-model:checked="data.is_bill" />
        </a-form-item>

        <a-form-item label="傀儡ID" name="puppet_id">
            <a-input v-model:value="data.puppet_id" />
        </a-form-item>

        <a-form-item label="是否启用" name="enable">
            <a-switch v-model:checked="data.enable" />
        </a-form-item>

        <a-form-item style="text-align: right;">
            <a-button type="primary" html-type="submit">提交</a-button>
        </a-form-item>
    </a-form>
</template>
<script lang="ts" setup>
import { createUser, setUser } from "@/request/api"
import { message } from 'ant-design-vue';

const prop = defineProps(['data', 'getData'])
const submitFunc = prop.data.userid ? setUser : createUser;
const onFinish = (values: any) => {
    submitFunc(values).then(() => {
        prop.getData()
        message.success('提交成功！');
    }).catch(err => {
        message.error(err)
    })
};
</script>
