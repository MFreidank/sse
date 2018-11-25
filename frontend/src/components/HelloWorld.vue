<template>
  <div>
    <v-container class="mx-0">
      <v-layout row>
        <v-flex xs3>
          <h3>Filters</h3>
          <v-treeview
            :items="dateFilter"
            open-all
            selectable
            item-key="name"
            v-model="selectedFilter"
          >
          </v-treeview>
        </v-flex>
        <v-flex xs9>
          <v-autocomplete
            v-model="query"
            :items="randomMedicalWords"
            :readonly="!isEditing"
            @click="toggleEdit()"
            :search-input.sync="search"
            append-icon="mdi-magnify"
            chips
            multiple
          >
          {{charactersTyped}}
            <template
              slot="selection"
              slot-scope="data"
            >
              <v-chip
                :selected="data.selected"
                close
                class="chip--select-multi"
                @input="remove(data.item)"
              >
                {{ data.item }}
              </v-chip>
            </template>
          </v-autocomplete>

          <!-- RESULTS DISPLAY -->
          {{articlesFound}}
          <!-- <v-card v-if="filterArticles(query, article.id), filteredDate(selectedFilter, article.id), (article.show || article.filter)" class="my-2" v-for="article in dummyArticles" :key="article.id">
            <v-card-title primary-title>
              <div>
                <div class="headline secondary--text" v-html="$options.filters.highlight(article.title, query)">{{article.title | highlight(query)}}</div>
                <span v-html="$options.filters.highlight($options.filters.truncateAbstract(article.text), query)">{{article.text | truncateAbstract | highlight(query)}}</span>
              </div>
              <v-spacer></v-spacer>
              <div class="grey--text text-xs-right">
                {{article.date}}
              </div>
            </v-card-title>
          </v-card> -->
          <v-card class="my-2" v-for="article in dummyArticles" :key="article">
            <v-card-title primary-title>
              <div>
                <div class="headline secondary--text" v-html="$options.filters.highlight(article.title, query)">{{article.title | highlight(query)}}</div>
              </div>
            </v-card-title>
          </v-card>
          <!-- END OF RESULTS DISPLAY -->
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
const BASE_URI = 'http://localhost:8000/api/'

export default {
  name: 'HelloWorld',
  data () {
    return {
      isEditing: false,
      search: null,
      items: [],
      randomMedicalWords: [],
      dummyArticles: [],
      query: '',
      selectedFilter: [],
      realData: {},
      realArticles: {}
    }
  },
  watch: {
    search (val) {
      val && this.querySelections(val)
    }
  },
  computed: {
    dateFilter () {
      return [
        {
          id: 1,
          name: 'Date',
          children: [
            { id: 2, name: 'Today' },
            { id: 3, name: 'January 2018' },
            { id: 4, name: 'January 2017' },
            { id: 5, name: 'May' }
          ]
        },
        {
          id: 6,
          name: 'Journal',
          children: [
            { id: 7, name: 'Science' },
            { id: 8, name: 'Nature' },
            { id: 9, name: 'Physics today' }
          ]
        }
      ]
    },
    charactersTyped () {
      if (this.search !== null && this.search.length > 1) {
        return this.fetchData(this.search)
      }
    },
    articlesFound () {
      if (this.query !== undefined && this.query.length > 0) {
        return this.fetchArticles(this.query)
      }
    }
  },
  methods: {
    toggleEdit () {
      this.isEditing = !this.isEditing
    },
    querySelections (v) {
      this.items = this.randomMedicalWords.filter(e => {
        return (e || '').toLowerCase().indexOf((v || '').toLowerCase()) > -1
      })
    },
    remove (item) {
      const index = this.randomMedicalWords.indexOf(item)
      if (index >= 0) this.randomMedicalWords.splice(index, 1)
    },
    filteredDate (selectedFilter, id) {
      if ((selectedFilter.includes('Today') && this.dummyArticles[id].date.includes('25 November 2018')) ||
      (selectedFilter.includes('January 2018') && this.dummyArticles[id].date.includes('January 2018')) ||
      (selectedFilter.includes('January 2017') && this.dummyArticles[id].date.includes('January 2017')) ||
      (selectedFilter.includes('May') && this.dummyArticles[id].date.includes('May'))) {
        this.dummyArticles[id].filter = true
      } else {
        this.dummyArticles[id].filter = false
      }
      return true
    },
    filterArticles (query, id) {
      for (let i = 0; i < query.length; i++) {
        if (this.dummyArticles[id].text.includes(query[i])) {
          this.dummyArticles[id].show = true
          break
        } else {
          this.dummyArticles[id].show = false
        }
      }
      return true
    },
    fetchData (query) {
      this.$http.post(BASE_URI + 'autocompletion/',
        {'query': query},
        {headers: {'Content-type': 'application/json'}
        })
        .then((result) => {
          this.realData = result.data
          this.realData.forEach(element => {
            this.randomMedicalWords.push(element.name)
          })
        })
    },
    fetchArticles (query) {
      this.$http.post(BASE_URI + 'search/',
        {'query': query},
        {headers: {'Content-type': 'application/json'}
        })
        .then((result) => {
          this.realArticles = result.data
          this.realArticles.forEach(element => {
            this.dummyArticles.push(element)
          })
        })
    }
  },
  filters: {
    highlight (text, searchTerm) {
      if (searchTerm[0] === undefined) {
        return text
      } else {
        searchTerm.forEach(element => {
          text = text.replace(element, '<span class=\'highlighting\'>' + element + '</span>')
        })
        searchTerm.forEach(element => {
          text = text.replace(element.toLowerCase(), '<span class=\'highlighting\'>' + element.toLowerCase() + '</span>')
        })
        return text
      }
    },
    truncateAbstract (value) {
      if (value.length > 350) {
        value = value.substring(0, 349) + '...'
        return value
      }
    }
  }
}
</script>

<style>
.highlighting {
  background-color: #FFAB91;
}
</style>
