<template>
<div class="af">
  </div>
  <div class="loader">
    <div class="song">
      <div v-for="item in items" :key="id">
      <p class="name" v-on:click="rende(item.user_id)">{{ item.user_name }}</p>
      <p class="artist">{{ item.bio }}</p>
    </div>
    </div>
    <div class="albumcover"></div>
    <div class="play"></div>
    </div>
</template>
<script>
export default{
  name:'search',
  data(){
    return{
      user_name:"",
      items:[]
    }
  },
  mounted(){
    const user_name = this.$route.query.u_name
      fetch("http://127.0.0.1:5000/api/search/" + user_name, {
        method: "GET",
        headers: { "Token": localStorage.getItem("token") },
    }).then((response) => response.json())
      .then((data) => {
        console.log(data)
        // this.$router.push({ name: 'Profile' , query: {user_id : data.user_id}})
        this.items = data
        
        
      }).catch((err) => {
        console.log(err)
      }
      )
  },
  methods:{
    rende(user_id){
      const main_id = this.$route.query.main_id
      console.log(user_id)
      console.log(main_id)
      this.$router.push({name:'OtherProfile',query:{user_id :user_id ,main_id:main_id}})
    }
  }
}
</script>
<style>
.af {
  background-color: white;
  padding: 1em;
  padding-bottom: 1.1em;
  border-radius: 15px;
  margin: 1em;
}

.loader {
  display: flex;
  flex-direction: row;
  height: 4em;
  padding-left: 1em;
  padding-right: 1em;
  transform: rotate(180deg);
  justify-content: right;
  border-radius: 10px;
  transition: .4s ease-in-out;
}

.loader:hover {
  cursor: pointer;
  background-color: lightgray;
}

.currentplaying {
  display: flex;
  margin: 1em;
}


.load {
  width: 2px;
  height: 33px;
  background-color: limegreen;
  animation: 1s move6 infinite;
  border-radius: 5px;
  margin: 0.1em;
}

.load:nth-child(1) {
  animation-delay: 0.2s;
}

.load:nth-child(2) {
  animation-delay: 0.4s;
}

.load:nth-child(3) {
  animation-delay: 0.6s;
}

.play {
  position: relative;
  left: 0.35em;
  height: 1.6em;
  width: 1.6em;
  clip-path: polygon(50% 50%, 100% 50%, 75% 6.6%);
  background-color: black;
  transform: rotate(-90deg);
  align-self: center;
  margin-top: 0.7em;
  justify-self: center;
}

.albumcover {
  position: relative;
  margin-right: 1em;
  height: 40px;
  width: 40px;
  background-color: rgb(233, 232, 232);
  align-self: center;
  border-radius: 5px;
}

.song {
  position: relative;
  transform: rotate(180deg);
  margin-right: 1em;
  color: black;
  align-self: center;
}

.artist {
  font-size: 0.6em;
}

@keyframes move6 {
  0% {
    height: 0.2em;
  }

  25% {
    height: 0.7em;
  }

  50% {
    height: 1.5em;
  }

  100% {
    height: 0.2em;
  }
}
</style>