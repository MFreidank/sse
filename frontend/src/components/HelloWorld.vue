<template>
  <div>
    <v-container class="mx-0">
      <v-layout row>
        <v-flex xs3>
          <v-treeview
            :items="dateFilter"
            open-all
            selectable
            item-key="name"
            v-model="selectedFilter"
          >
          </v-treeview>
          <v-btn class="error" @click="fetchData">DELETE_ME!</v-btn>
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
          <v-card v-if="filterArticles(query, article.id), filteredDate(selectedFilter, article.id), (article.show || article.filter)" class="my-2" v-for="article in dummyArticles" :key="article.id">
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
          </v-card>
          <!-- END OF RESULTS DISPLAY -->
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>

export default {
  name: 'HelloWorld',
  data () {
    return {
      isEditing: false,
      search: null,
      items: [],
      randomMedicalWords: [
        'aspirin', 'insulin', 'hemoglobin', 'chlorophyl', 'diabetes',
        'blood pressure', 'leukemia', 'multiple sclerosis', 'glucose', 'LSD',
        'chemistry', 'quantum', 'evolution', 'rat', 'yeast',
        'adenine', 'hair loss', 'protein', 'hydrolic pressure', 'antibodies'
      ],
      dummyArticles: [
        {id: 0, title: 'Title of example aspirin article', text: 'Lorem ipsum dolor sit amet, aspirin sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At glucose eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet...', date: '25 November 2018', show: false, filter: false},
        {id: 1, title: 'Title of another article', text: 'Lorem antibodies dolor sit amet, leukemia sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, glucose diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet...', date: '01 December 2011', show: false, filter: false},
        {id: 2, title: 'Title of awesome article about LSD', text: 'Lorem ipsum dolor sit amet, antibodies sadipscing elitr, sed diam hydrolic eirmod tempor LSD ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet...', date: '06 May 2015', show: false, filter: false},
        {id: 3, title: 'Title of dummy article', text: 'Lorem rat dolor sit amet, yeast sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet...', date: '12 March 1977', show: false, filter: false},
        {id: 4, title: 'Title of fake article', text: 'Lorem ipsum hydrolic pressure sit amet, consetetur sadipscing elitr, sed diam LSD eirmod tempor invidunt ut hair loss et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet...', date: '25 November 2018', show: false, filter: false},
        {id: 5, title: 'Title of medical article', text: 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet...', date: '22 March 2001', show: false, filter: false},
        {id: 6, title: 'Title of article about diabetes', text: 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed aspirin nonumy eirmod tempor invidunt ut labore et dolore magna yeast erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet...', date: '09 January 2017', show: false, filter: false},
        {id: 7, title: 'Title of last article', text: 'Lorem ipsum dolor sit amet, hair loss sadipscing leukemia, sed diam rat eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet...', date: '30 January 2017', show: false, filter: false}
      ],
      query: '',
      selectedFilter: [],
      realData: {}
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
    fetchData () {
      const baseURI = 'http://localhost:8000/api/autocompletion/'
      this.$http.post(baseURI,
        {'query': 'As'},
        {headers: {'Content-type': 'application/json'}
        })
        .then((result) => {
          this.realData = result.data
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
