<!--
 * @Author: 0x3E5
 * @Date: 2023-02-11 19:27:09
 * @LastEditTime: 2023-02-21 15:44:38
 * @LastEditors: 0x3E5
 * @Description: 
 * @FilePath: \ai-paper-search-web\src\components\AdvancedSettingDlg.vue
-->
<script lang="ts" setup>
import { ref, watch, reactive } from 'vue'

const props = defineProps(['data'])
const emits = defineEmits<{
  (e: 'update:data', value: object): void
}>()

type FORMDATA = {
  query: string
  searchtype: string
  year: string
  sp_year: string
  sp_author: string
  confs: string[]
}

const isVisible = ref(false)
const CURRENT_YEAR = new Date().getFullYear()
const SPECIFIC_YEAR_LIST = [
  { label: `Since ${CURRENT_YEAR}`, value: `${String(CURRENT_YEAR)}` },
  { label: `Since ${CURRENT_YEAR - 3}`, value: `${String(CURRENT_YEAR - 3)}` },
  { label: `Since ${CURRENT_YEAR - 5}`, value: `${String(CURRENT_YEAR - 5)}` },
  { label: 'All', value: '' }
]
const CONFS_LIST = [
  'AAAI',
  'ACL',
  'AISTATS',
  'BMVC',
  'CIKM',
  'COLING',
  'COLT',
  'CVPR',
  'ECCV',
  'ECIR',
  'EMNLP',
  'ICASSP',
  'ICCV',
  'ICDM',
  'ICLR',
  'ICME',
  'ICML',
  'IJCAI',
  'IJCV',
  'INTERSPEECH',
  'ISWC',
  'JMLR',
  'KDD',
  'MICCAI',
  'MLSYS',
  'MM',
  'NAACL',
  'NIPS',
  'RECSYS',
  'SIGIR',
  'TASLP',
  'TIP',
  'TKDE',
  'TNNLS',
  'TOIS',
  'TPAMI',
  'VLDB',
  'WACV',
  'WSDM',
  'WWW'
]
let formData: FORMDATA = reactive({
  query: '',
  searchtype: '',
  year: '',
  sp_year: '',
  sp_author: '',
  confs: []
})

watch(
  () => props.data,
  v => {
    formData = v
  },
  {
    deep: true,
    immediate: true
  }
)

const checkMethod: (method: string) => void = method => {
  if (method === 'all') {
    formData.confs = CONFS_LIST
  } else if (method === 'invert') {
    const SELECTED = new Set(formData.confs)
    formData.confs = CONFS_LIST.filter(v => !SELECTED.has(v))
  }
}

const resetForm = (): void => {
  formData.year = ''
  formData.sp_year = ''
  formData.sp_author = ''
  formData.confs = CONFS_LIST
}

const confirmForm = (): void => {
  emits('update:data', formData)
  isVisible.value = false
}

defineExpose({
  isVisible
})
</script>
<template>
  <el-dialog
    class="dialog-advancedSetting"
    v-model="isVisible"
    title="Advanced Setting"
  >
    <el-form :model="formData" label-width="120px">
      <el-form-item label="Years" prop="year">
        <el-select class="w-100" v-model="formData.year">
          <el-option
            v-for="(itm, index) in SPECIFIC_YEAR_LIST"
            :key="index"
            :label="itm.label"
            :value="itm.value"
          >
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="Specific Year" prop="sp_year">
        <el-input
          v-model="formData.sp_year"
          placeholder="Input a specific year"
          clearable
        />
      </el-form-item>
      <el-form-item label="Specific Author" prop="sp_author">
        <el-input
          v-model="formData.sp_author"
          placeholder="Input a specific author"
          clearable
        />
      </el-form-item>
      <el-form-item label="Confs" prop="confs">
        <el-row class="w-100" :gutter="20">
          <el-col :span="12" :offset="0">
            <el-link type="primary" @click="checkMethod('all')"
              >Check All</el-link
            >
          </el-col>
          <el-col :span="12" :offset="0">
            <el-link type="primary" @click="checkMethod('invert')"
              >Check Invert</el-link
            >
          </el-col>
        </el-row>

        <el-checkbox-group v-model="formData.confs">
          <el-row>
            <el-col
              :xs="12"
              :sm="12"
              :md="8"
              :lg="8"
              :xl="6"
              v-for="(itm, index) in CONFS_LIST"
              :key="index"
            >
              <el-checkbox :label="itm">
                {{ itm }}
              </el-checkbox>
            </el-col>
          </el-row>
        </el-checkbox-group>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="resetForm">Reset</el-button>
        <el-button type="primary" @click="confirmForm">Done</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<style>
@media (min-width: 1920px) {
  .dialog-advancedSetting {
    width: 30%;
  }
}
@media (max-width: 1920px) {
  .dialog-advancedSetting {
    width: 35%;
  }
}
@media (max-width: 1200px) {
  .dialog-advancedSetting {
    width: 50%;
  }
}
@media (max-width: 992px) {
  .dialog-advancedSetting {
    width: 55%;
  }
}
@media (max-width: 768px) {
  .dialog-advancedSetting {
    width: 90%;
  }
}
</style>
<style scioed>
.checkbox-advancedSetting {
  width: 50%;
  margin-right: 0%;
}
</style>
