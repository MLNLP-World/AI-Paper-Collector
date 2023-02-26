<!--
 * @Author: 0x3E5
 * @Date: 2023-02-13 13:47:11
 * @LastEditTime: 2023-02-26 13:20:28
 * @LastEditors: 0x3E5
 * @Description: 
 * @FilePath: \web\src\components\SearchResultList.vue
-->
<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import FILE from '@/utils/file'

const emits = defineEmits<{
  (e: 'searchAuthor', val: string): void
}>()

let resultList: any = reactive({
  val: []
})

let sortMethod = ref('Hot')

const exportFile = (method: string): void => {
  if (method === 'csv') {
    FILE.exportCSV(resultList.val, 'result.csv')
  } else if (method === 'txt') {
    FILE.exportTxt(resultList.val, 'result.txt')
  }
}

const deleteResult = (index: number): void => {
  resultList.val.splice(index, 1)
}

const jumpUrl = (url: string) => {
  url && window.open(url)
}

const searchAuthor = (author: string): void => {
  emits('searchAuthor', author)
}

const filterResult: (target: any, option: any) => void = (target, option) => {
  resultList.val = []
  const { level, key, parent } = option
  if (Number(level) === 1) {
    getAllResult(target)
  } else if (Number(level) === 2) {
    for (let k in target[key]) {
      resultList.val = resultList.val.concat(target[key][k])
      changeSortMethod(sortMethod.value)
    }
  } else if (Number(level === 3)) {
    resultList.val = resultList.val.concat(target[parent][key])
    changeSortMethod(sortMethod.value)
  }
}

const getAllResult = (target: any): void => {
  if (Array.isArray(target)) {
    resultList.val = resultList.val.concat(target as never)
    changeSortMethod(sortMethod.value)
  } else {
    for (let k in target) {
      getAllResult(target[k])
    }
  }
}

const changeSortMethod = (method: any): void => {
  if (method === 'Hot') {
    resultList.val = resultList.val.sort(
      (a: any, b: any) => b.citation - a.citation
    )
  } else if (method === 'Year') {
    resultList.val = resultList.val.sort(
      (a: any, b: any) => Number(b.year) - Number(a.year)
    )
  } else if (method === 'Conf') {
    console.log(11)
    resultList.val = resultList.val.sort((a: any, b: any) => {
      let a1 = a.conf.toUpperCase()
      let b1 = b.conf.toUpperCase()
      if (a1 < b1) {
        return -1
      }
      if (a1 > b1) {
        return 1
      }
      return 0
    })
  }
}

// Handler pagination
type PAGE = {
  current: number
  size: number
}
const page: PAGE = reactive({
  current: 1,
  size: 200
})

const pageCurrentChange = (v: number): void => {
  page.current = v
}

const pageSizeChange = (v: number): void => {
  page.current = 1
  page.size = v
}

const virtualList = computed(() => {
  return resultList.val.slice(
    (page.current - 1) * page.size,
    page.current * page.size
  )
})

defineExpose({
  filterResult
})
</script>

<template>
  <el-card class="search-result-card mb-15" shadow="never">
    <el-row v-show="resultList.val.length > 0">
      <el-col class="align-right" :span="24">
        <el-space wrap>
          <el-link @click="exportFile('txt')">
            <el-icon class="el-icon--left"><Document /></el-icon>Export txt
          </el-link>
          <el-link @click="exportFile('csv')">
            <el-icon class="el-icon--left"><Collection /></el-icon>Export csv
          </el-link>
        </el-space>
      </el-col>
    </el-row>
    <el-divider v-show="resultList.val.length > 0" />
    <el-row
      class="mb-10 flex flex-align-center"
      v-show="resultList.val.length > 0"
    >
      <span style="padding-right: 10px">Sort By:</span>
      <el-radio-group v-model="sortMethod" @change="changeSortMethod">
        <el-radio label="Hot" />
        <el-radio label="Year" />
        <el-radio label="Conf" />
      </el-radio-group>
    </el-row>
    <el-space class="w-100" wrap fill direction="vertical">
      <el-card
        shadow="never"
        v-for="(itm, index) in virtualList"
        :key="index"
        class="paper-itm pos-relative"
      >
        <!-- Delete button -->
        <el-icon
          class="pos-absoulte delete pointer no-select"
          @click="deleteResult(index)"
          ><CloseBold
        /></el-icon>
        <el-row class="mb-5">
          <el-col :span="24">
            <!-- Title -->
            <el-link
              class="title"
              :href="itm.url"
              :underline="false"
              target="_blank"
              >{{ itm.title }}</el-link
            >
          </el-col>
        </el-row>
        <el-row class="mb-30">
          <el-col :span="24">
            <!-- Author -->
            <span
              v-for="(author, authorIndex) in itm.authors"
              :key="authorIndex"
              @click="searchAuthor(author)"
              class="mr-10"
            >
              <el-link class="author">{{ author }}</el-link>
            </span>
          </el-col>
        </el-row>
        <el-row class="mb-5">
          <el-col :span="24">
            <el-space wrap>
              <!-- Abstract -->
              <el-popover placement="top-start" :width="400" trigger="click">
                <template #reference>
                  <el-tag
                    class="pointer no-select"
                    v-show="itm.abstract"
                    type="success"
                  >
                    Abstract
                  </el-tag>
                </template>
                <div>
                  <h3 class="mb-10">{{ itm.title }}</h3>
                  <p>{{ itm.abstract }}</p>
                </div>
              </el-popover>
              <!-- Conf -->
              <el-tag type="warning">{{ itm.conf }}</el-tag>
              <!-- Year -->
              <el-tag type="danger">{{ itm.year }}</el-tag>
              <!-- Code -->
              <el-tag
                class="pointer no-select"
                v-if="itm.code !== '#'"
                @click="jumpUrl(itm.code)"
              >
                CODE
              </el-tag>
            </el-space>
          </el-col>
        </el-row>
      </el-card>
    </el-space>
    <el-empty
      v-show="resultList.val.length <= 0"
      description="No Search Result"
    ></el-empty>
    <div class="mt-15" v-show="resultList.val.length > 0">
      <el-pagination
        class="align-right"
        v-model:current-page="page.current"
        v-model:page-size="page.size"
        :page-sizes="[10, 20, 30, 50, 100, 150, 200, 300]"
        layout="sizes, prev, pager, next"
        :total="resultList.val.length"
        @size-change="pageSizeChange"
        @current-change="pageCurrentChange"
      />
    </div>
  </el-card>
</template>

<style scoped>
.search-result-card {
}
.title {
  font-size: 18px;
}
.author {
  color: #999;
  font-size: 16px;
}
.delete {
  top: 10px;
  right: 10px;
  color: #999;
}
</style>
