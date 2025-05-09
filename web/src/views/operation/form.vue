<template>
    <a-form :model="formData" :label-col="{ span: 5}"  @finish="onFinish"   >
        <a-form-item 
            v-for="item in selectedInput" 
            :key="item.var" 
            :name="item.var" 
            :label="`${item.name}`"
            :rules="[{ required: item.required, message: '不能为空!' }]"
            >
            <a-input v-model:value="formData[item.var]" />

        </a-form-item>

        <a-form-item style="text-align: right;">
            <a-button type="primary" html-type="submit">提交</a-button>
        </a-form-item>
    </a-form>

 

</template>
<script lang="ts" setup>

const prop = defineProps(['selectedInput','formData','onSave'])


const onFinish = (values: any) => {

    prop.onSave(values)
};

</script>
