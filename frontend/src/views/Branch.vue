<template>
	<v-sheet elevation="4">
		<v-container v-if="!loading && branch">
			<v-row justify="start">
				<v-col cols="auto">
					<v-btn icon @click="back">
						<v-icon>mdi-arrow-left</v-icon>
					</v-btn>
				</v-col>
				<v-col>
					<h2>Selected branch: {{ branch.branch }}</h2>
				</v-col>
			</v-row>
			<v-row>
				<v-col>
					<v-list>
						<v-list-item v-for="(commit, index) in branch.commits" :key="index" @click="commitDetail(commit.hexsha)">
							<v-list-item-content>
								<v-list-item-title>
									<strong>{{ commit.author }}</strong>
									<span class="text--disabled font-italic px-2">({{ commit.date }})</span>
								</v-list-item-title>
								{{ commit.message }}
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
	name: 'Branch',

	props: ['name'],

	data() {
		return {
			branch: null,
			loading: false
		}
	},

	methods: {
		back() {
			this.$router.push('/')
		},
		async getBranchDetail() {
			try {
				const response = await axios.get('/branches/' + this.name + '/commits/')
				if (response.status === 200) {
					this.branch = response.data.data
				}
			} catch (err) {
				console.log(err)
			}
		},
		commitDetail(hexsha) {
			this.$router.push('/commits/' + hexsha)
		}
	},

	async mounted() {
		this.loading = true
		await this.getBranchDetail()
		this.loading = false
	}
}
</script>