<template>
	<v-sheet elevation="4">
		<v-container v-if="!loading && commit">
			<v-row v-if="commit" justify="start">
				<v-col cols="auto">
					<v-btn icon @click="$router.go(-1)">
						<v-icon>mdi-arrow-left</v-icon>
					</v-btn>
				</v-col>
				<v-col>
					<h3 class="font-italic">Commit {{ commit.hexsha.substr(0, 8) }}</h3>
				</v-col>
			</v-row>
			<v-row>
				<v-col>
					<strong>Author </strong> {{ commit.author }} ({{ commit.author_email }})
				</v-col>
			</v-row>
			<v-row>
				<v-col>
					<strong>Commited at </strong> {{ commit.commited_date }}
				</v-col>
			</v-row>
			<v-row>
				<v-col>
					<v-textarea outlined label="Message" :value="commit.message" :disabled="true"></v-textarea>
				</v-col>
			</v-row>
			<v-row>
				<v-col>
					<h3>Files ({{ commit.file_list.length }})</h3>
					<v-list>
						<v-list-item v-for="(file, index) in commit.file_list" :key="index">
							<v-list-item-content>
								<v-list-item-title>{{ file }}</v-list-item-title>
							</v-list-item-content>
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
	name: 'Commit',

	props: ['commitid'],

	data() {
		return {
			commit: null,
			loading: false
		}
	},

	methods: {
		async getCommitDetail() {
			try {
				const response = await axios.get('/commits/' + this.commitid)
				if (response.status === 200) {
					this.commit = response.data.data
				}
			} catch (err) {
				console.log(err)
			} 
		}
	},

	async created() {
		this.loading = true
		await this.getCommitDetail()
		this.loading = false
	}

}
</script>