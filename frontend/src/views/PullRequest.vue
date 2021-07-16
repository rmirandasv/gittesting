<template>
	<v-card elevation="4">
		<v-toolbar flat>
			<v-btn icon  @click="$router.push('/pullrequest')">
				<v-icon>mdi-arrow-left</v-icon>
			</v-btn>
			<v-toolbar-title>New Pull Request</v-toolbar-title>
		</v-toolbar>
		<v-container v-if="!loading">
			<v-row>
				<v-col>
					<h4>Select branches to compare</h4>
				</v-col>
			</v-row>
			<v-row>
				<v-col>
					<v-select :items="branches" label="Base" v-model="base"></v-select>
				</v-col>
				<v-col>
					<v-select :items="branches" label="Compare" v-model="compare"></v-select>
				</v-col>
			</v-row>
			<v-row justify="center" v-if="message">
				<v-col cols="auto">
					<h4 class="text--secondary">{{ message }}</h4>
				</v-col>
			</v-row>
			<v-row v-show="diffs.length > 0" class="grey lighten-5">
				<v-col cols="12">
					<h3 class="pb-4">Create New Pull Request: <span class="text--disabled">{{ base }}</span> &lt; <span class="text--disabled">{{ compare }}</span></h3>
					<v-text-field 
						class="pt-4"
						ref="title" 
						v-model="title" 
						label="Title" 
						outlined
						required
						:autofocus="true"
						hint="Add pull request title"></v-text-field>
				</v-col>
				<v-col cols="12">
					<v-textarea 
						outlined
						required
						ref="description" 
						v-model="description" 
						hint="Add comments to pull request" 
						label="Description"></v-textarea>
				</v-col>
				<v-col cols="12">
					<v-btn color="indigo" block :disabled="disabled" @click="save">
						Save
					</v-btn>
				</v-col>
				<v-col cols="12">
					<v-checkbox label="I hava already check differences." v-model="diffChecked"></v-checkbox>
				</v-col>
				<v-col cols="12">
					<v-checkbox label="Merge now" v-model="merge"></v-checkbox>
				</v-col>
				<v-col v-if="diffs.length > 0" cols="12" class="pt-0">
					<h2 class="pb-4">Check differences</h2>
					<pre>
						<samp>{{ diffs }}</samp>
					</pre>
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
	</v-card>
</template>

<script>

import axios from 'axios'

export default {
	name: 'PullRequest',

	data() {
		return {
			branches: [],
			loading: false,
			base: '',
			compare: '',
			message: 'Select branches to compare',
			diffs: '',
			title: '',
			description: '',
			diffChecked: false,
			merge: false,
			error: ''
		}
	},

	watch: {
		base: function(n, o) {
			if (n === o) {
				return
			}
			this.validate()
		},
		compare: function(n, o) {
			if (n === o) {
				return
			}
			this.validate()
		}
	},

	computed: {
		disabled: function() {
			let disabled = true
			if (this.base.length > 0 
					&& this.compare.length > 0 
					&& this.title.length > 0 
					&& this.description.length > 0 
					&& this.diffChecked) {
				disabled = false
			}
			return disabled
		}
	},

	methods: {
		validate() {
			this.message = ''
			if (this.base === '' || this.compare === '') {
				this.diffs = ''
				return
			}
			if (this.base === this.compare) {
				this.message = 'You must select two different branches.'
				this.diffs = ''
				return
			}
			this.getDiffs()
		},
		async getDiffs() {
			try {
				const response = await axios.get('/diff/' + this.base + '/' + this.compare + '/')
				if (response.status === 200) {
					this.diffs = response.data.diffs
					if (this.diffs.length === 0) {
						this.message = 'There is no difference between the brnaches'
					}
				}
			} catch (err) {
				console.log(err)
			}
		},
		async getBranches() {
			try {
				const response = await axios.get('/branches')
				if (response.status === 200) {
					const branches = response.data.data
					branches.map(b => {
						this.branches.push(b.name)
					})
				}
			} catch (err) {
				console.log(err)
			}
		},

		async save() {
			const data = new FormData()
			data.append('title', this.title)
			data.append('description', this.description)
			data.append('base', this.base)
			data.append('compare', this.compare)
			if (this.merge) {
				data.append('status', 3)
			} else {
				data.append('status', 1)
			}

			try {
				const response = await axios.post('/merge/', data)
				if (response.status === 200 || response.status === 201) {
					this.$router.push('/pullrequest')
				} else {
					this.error = response.data.message
				}
			} catch (err) {
				console.log(err)
			}
		}

	},

	async mounted() {
		this.loading = true
		await this.getBranches()
		this.loading = false
	}

}
</script>

<style scoped>
pre {
	background: rgb(35, 35, 35);
	color: white;
	width: 100%;
	overflow-x: auto;
	counter-reset: line;
	padding-left: 12px;
	padding-right: 12px;
}
</style>
