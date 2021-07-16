<template>
  <v-sheet elevation="4">
    <v-container v-if="!loading">
      <v-row justify="center">
        <v-col cols="auto">
          <h2>Branches</h2>
        </v-col>
        <v-col cols="auto">
          <v-btn plain @click="$router.push('/pullrequest')">
            Pull Requests
          </v-btn>
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-col cols="auto">
          <v-list>
            <v-list-item v-for="(branch, index) in branches" :key="index" @click="detail(branch.name)">
              <v-list-item-content>
                <v-list-item-title>{{ branch.name }}</v-list-item-title>
              </v-list-item-content>
              <v-list-item-icon>
                <v-icon>mdi-github</v-icon>
              </v-list-item-icon>
            </v-list-item>
          </v-list>
        </v-col>
      </v-row>
    </v-container>
    <v-container v-else>
      <v-row justify="center">
        <v-col cols="auto">
          <v-progress-circular :indeterminate="true"></v-progress-circular>
        </v-col>
      </v-row>
    </v-container>
  </v-sheet>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Home',

  data() {
    return {
      branches: [],
      loading: false
    }
  },

  methods: {
    detail(branch) {
      console.log(branch)
      this.$router.push('/branch/' + branch)
    }
  },

  async mounted() {
    this.loading = true
    try {
      const response = await axios.get('/branches/')
      this.branches = response.data.data
    } catch (err) {
      console.log('ERR', err)
    } finally {
      this.loading = false
    }
  }
}
</script>
