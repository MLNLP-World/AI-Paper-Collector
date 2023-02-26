<!--
 * @Author: 0x3E5
 * @Date: 2023-02-11 13:48:18
 * @LastEditTime: 2023-02-24 17:38:08
 * @LastEditors: 0x3E5
 * @Description: 
 * @FilePath: \ai-paper-search-web\src\views\HomeView.vue
-->
<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useDark, useToggle } from '@vueuse/core'
import { ElMessage, ElLoading } from 'element-plus'
import AdvancedSettingDlg from '@/components/AdvancedSettingDlg.vue'
import ConfsTree from '@/components/ConfsTree.vue'
import SearchResultList from '@/components/SearchResultList.vue'
import GuessYourLike from '@/components/GuessYourLike.vue'
import { paperSearch, guessYourLike } from '@/api/paper.js'
// First entry
let firstEntry = ref(true)
// Query content
let searchContent = reactive({
  query: '',
  searchtype: 'title',
  year: '',
  sp_year: '',
  sp_author: '',
  confs: [
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
})
// Search type list
const SEARCH_TYPE_LIST = [
  { label: 'Title', value: 'title' },
  { label: 'Author', value: 'author' }
]
// Query result
let queryResult = reactive({
  val: {}
})
// Advanced setting dialog
const settingDlg = ref(null)
// Search result component
const searchResult = ref(null)

// Handle Search
let guessLoading = ref(false)
let guessList = reactive({
  val: []
})
const search = (): void => {
  if (searchContent.query === '' && searchContent.sp_author === '') {
    ElMessage.warning('Please input your keywords for search.')
    return
  }
  const loading = ElLoading.service({
    lock: true,
    text: 'Searching...'
    // background: 'rgba(0, 0, 0, 0.7)',
  })
  queryResult.val = {}
  guessList.val = []
  paperSearch({
    ...searchContent,
    confs: searchContent.confs.join(',')
  })
    .then((res: any) => {
      const { data, msg } = res
      if (msg === 'success') {
        queryResult.val = data
        handleTreeClick({ level: 1 })
      }
    })
    .catch(err => {
      console.log(err)
    })
    .finally(() => {
      firstEntry.value = false
      loading && loading.close()
    })
  guessLoading.value = true
  guessYourLike({ query: searchContent.query })
    .then((res: any) => {
      const { data, msg } = res
      if (msg === 'success' && data.keywords) {
        guessList.val = data.keywords
      }
    })
    .catch(err => {
      console.log(err)
    })
    .finally(() => {
      guessLoading.value = false
    })
}

// Handle search author
const handleSearchAuthor = (data: string): void => {
  searchContent.query = ''
  // searchContent.searchtype = 'author'
  searchContent.sp_author = data
  search()
}

// Handle search guess
const handleSearchGuess = (data: string): void => {
  searchContent.query = data
  search()
}

// Handle tree click
const handleTreeClick = (data: Object): void => {
  if (searchResult.value) {
    ;(searchResult.value as any).filterResult(queryResult.val, data)
  }
}

// Show advanced setting dialog
const showSetting = (): void => {
  if (settingDlg.value) {
    ;(settingDlg.value as any).isVisible = true
  }
}

// Change dark mode
const isDark = useDark()
const toggleDark = useToggle(isDark)
</script>

<template>
  <main class="full pos-relative">
    <el-row justify="center" :class="['mb-15 pos-absolute', firstEntry ? 'first-entry' : 'normal']">
      <el-col class="gutter-20" :xs="24" :sm="16" :md="14" :lg="10" :xl="8">
        <h1 class="title mb-15"><a href="/">AI-Paper-Search</a></h1>
        <!-- Search Bar -->
        <el-input
          v-model="searchContent.query"
          placeholder="Input your keywords"
          clearable
          @keyup.enter="search"
          size="large"
          class="mb-10"
        >
          <template #prepend>
            <el-select
              v-model="searchContent.searchtype"
              placeholder="Select"
              style="width: 100px"
              size="large"
            >
              <el-option
                v-for="(itm, index) in SEARCH_TYPE_LIST"
                :key="index"
                :label="itm.label"
                :value="itm.value"
              />
            </el-select>
          </template>
          <template #append>
            <el-button icon="Search" @click="search" />
          </template>
        </el-input>
        <!-- Toolbar -->
        <div class="toolbar mb-15">
          <el-link type="primary" icon="Setting" @click="showSetting">
            &nbsp;Advanced setting
          </el-link>
          <el-link
            type="primary"
            :icon="isDark ? 'Sunny' : 'Moon'"
            @click="toggleDark()"
          >
            &nbsp;{{ `${isDark ? 'Light' : 'Dark'}Mode` }}
          </el-link>
          <el-link
            type="primary"
            icon="Link"
            href="https://github.com/MLNLP-World/AI-Paper-Collector"
            target="_blank"
          >
            &nbsp;GitHub
          </el-link>
        </div>
        <!-- Tips -->
        <el-alert
          title="Tips!"
          type="info"
          :center="true"
          description="You can get more precise results by using advanced setting. If this project is helpful to you, please give us a ⭐star!"
        />
      </el-col>
    </el-row>
    <el-row justify="center" v-show="!firstEntry">
      <el-col class="gutter-20" :xs="24" :sm="16" :md="5" :lg="4" :xl="3">
        <!-- Select tree -->
        <ConfsTree :data="queryResult.val" @click="handleTreeClick" />
      </el-col>
      <el-col class="gutter-20" :xs="24" :sm="16" :md="14" :lg="10" :xl="8">
        <!-- Search result list -->
        <SearchResultList
          ref="searchResult"
          @search-author="handleSearchAuthor"
        />
      </el-col>
      <el-col class="gutter-20" :xs="24" :sm="16" :md="5" :lg="4" :xl="3">
        <GuessYourLike
          :loading="guessLoading"
          :result="guessList.val"
          @search-guess="handleSearchGuess"
        />
      </el-col>
    </el-row>

    <!-- Advanced setting dialog -->
    <AdvancedSettingDlg ref="settingDlg" v-model:data="searchContent" />
    <!-- Back to top -->
    <el-backtop :right="50" :bottom="50" />
    <!-- Copy right -->
    <div :class="['copy-right mb-15', firstEntry ? 'copy-first-entry' : '']">
      <a href="https://beian.miit.gov.cn/" target="_blank">
        <img src="@/assets/beian.png" />浙ICP备2023002681号-1
      </a>
    </div>
  </main>
</template>

<style scoped>
.title {
  font-size: 60px;
  text-align: center;
  user-select: none;
}

.title a {
  text-decoration: none;
  color: #333;
}

.title a:hover {
  text-decoration: underline;
}
.toolbar {
  text-align: center;
  user-select: none;
}
.toolbar a + a {
  margin-left: 20px;
}
.gutter-20 {
  padding: 0 20px;
}
.copy-right {
  text-align: center;
  font-size: 14px;
  font-weight: 500;
  line-height: 16px;
}
.copy-right a {
  text-decoration: none;
  color: #999;
}
.copy-right a > * {
  vertical-align: middle;
}
.copy-right a img {
  width: 14px;
  margin-right: 5px;
}
.first-entry {
  top: calc(50% - 80px);
  transform: translateY(-50%);
}
.normal {
  top: 0;
  transform: translateY(0);
}
.copy-first-entry {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
}
</style>
