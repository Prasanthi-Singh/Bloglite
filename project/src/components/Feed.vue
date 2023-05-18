<template>
  <div>
      <nav class="navbar">
        <div class="navbar-logo">
          <div style="display:flex">
          <li class="cc"><input type="text" placeholder="Search.." v-model="u_name"></li>
          <li><button type="submit" style="margin-top: 10px;" v-on:click="sear"><i class="fa fa-search"></i></button></li>
        </div>
        </div>
        <ul class="navbar-menu">
          <li v-on:click="profile">Profile</li>
          <li v-on:click='f'>Add Friend</li>
          <li><router-link to="Login">Logout</router-link></li>
        </ul>
      </nav>
      <div class="feed-container">
    <div class="feed-header">
    </div>
    <div class="feed-posts">
      <div class="feed-post" v-for="item in items" :key="id">
        <div class="feed-post-header">
          <!-- <img class="feed-post-profile-image" :src="item.user_dp" alt="Profile Image"> -->
          <div class="feed-post-profile-info">
            <h2 v-on:click="rend(item.user_id)">{{ item.user_name }}</h2>
            <!-- <p>{{ post.timestamp | formatDate }}</p> -->
          </div>
        </div>
        <img class="feed-post-image" :src="item.post_image" alt="Post Image">

        <div class="feed-post-footer">
          <!-- <button class="feed-post-like-button" :class="{ active: post.liked }" @click="toggleLike(post)">Like</button> -->
          <p>{{ item.post_descr }} </p>
        </div>
      </div>
    </div>
  </div>
</div>
</template>
  
<script>

export default {
  name: "Profile",
  data() {
    return {
      // user_name:"",
      // imageurl:"",
      // bio:"",
      // following_count:"",
      // follower_count:"",
      items: [],
      u_name:""

    }
  },
  mounted() {
    const user_id = this.$route.query.user_id
    fetch(`http://127.0.0.1:5000/api/feed/${user_id}`, {
      method: 'GET',
      headers: { "Token": localStorage.getItem("token") },
    }).then((response) => response.json())
      .then((data) => {
        console.log(data)
        this.items = data
        // this.user_name = this.items[0].user_name
        // this.imageurl = this.items[0].user_dp
        // this.bio = this.items[0].user_bio
        // this.following_count = this.items[0].following_count
        // this.follower_count = this.items[0].follower_count
      }).catch((err) => {
        console.log('yes')
        const user_id = this.$route.query.user_id
        console.log(user_id)
        this.$router.push({ name: 'newuser', query: { user_id: user_id } })
      }
      )
  },
  methods: {
    rend(user_id){
      const main_id = this.$route.query.user_id
      console.log(user_id)
      console.log(main_id)
      this.$router.push({name:'OtherProfile',query:{user_id :user_id , main_id:main_id}})
    },
    sear(){
      console.log('yes')
      console.log(this.u_name)
      const main_id = this.$route.query.user_id
      this.$router.push({name:'Search',query:{u_name:this.u_name , main_id:main_id}})

    },
    f() {
      const user_id = this.$route.query.user_id
      console.log(user_id)
      this.$router.push({ name: 'AllUser', query: { user_id: user_id } })
    },
    profile() {
      const user_id = this.$route.query.user_id
      console.log(user_id)
      this.$router.push({ name: 'Profile', query: { user_id: user_id } })
    }
  }
}
</script>

<style>
.feed-container {
  max-width: 700px;
  margin: 0 auto;
  padding: 1rem;
}

.feed-header {
  display: flex;
  align-items: center;
  padding-left: 20%;
}

.feed-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  margin-right: 2rem;
}


.feed-info {
  display: flex;
  flex-direction: column;
}

.feed-stats {
  display: flex;
  margin: 1rem 0;
}

.feed-stat {
  margin-right: 2rem;
}

.feed-stat-count {
  font-weight: bold;
}


.feed-box {
  max-width: 400px;
  min-width: 200px;
  object-fit: contain;
  margin: 0 auto;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  margin-right: 20%;
  margin-bottom: 10%;
  margin-left: 30%;
  padding: 3%;
  min-height: 250px;
}



.feed-post-image {
  width: 100%;
  height: 100%;
  margin-top: 5%;
}


.feed-posts {
  justify-content: center;
  align-items: center;
  margin-left: 20%;
}

.feed-post {
  max-width: 400px;
  margin: 20px;
  padding: 10px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  border-radius: 5px;
  text-align: center;
}
</style>