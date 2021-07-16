<template>
  <v-app>
    <v-app-bar app dense>
      <v-toolbar-title>GitWrapper</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn outlined href="https://github.com/rmirandasv/fullstack-interview-test/tree/develop" target="_blank">
        <span>View on github</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>
    <v-main>
      <v-container>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>