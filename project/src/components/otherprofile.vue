<script>

export default {
  name: "OtherProfile",
  data() {
    return {
      user_name: "",
      imageurl: "",
      bio: "",
      following_count: "",
      follower_count: "",
      items: [],

    }
  },
  methods: {
    
    feed() {
      const user_id = this.$route.query.main_id
      console.log(user_id)
      this.$router.push({ name: 'feed', query: { user_id: user_id } })
    },
    unfollow(){
      console.log("yes")
      const main_id = this.$route.query.main_id
      console.log(main_id)
      const user_id = this.$route.query.user_id
        fetch(`http://127.0.0.1:5000/api/unfollow/${main_id}/${user_id}`, {
                  method: "GET",
                  headers: { "Token": localStorage.getItem("token") },
                  
                }).then((response)=> {if (!response.ok) {
                        throw new Error('HTTP error, status code ' + response.status);
                      }
                      return response.json();})
                .then((data)=>{
                  console.log(data);
                  this.$router.push( {name: 'Profile' ,query: {user_id : main_id }})

                }) .catch((error)=> alert(error))
    
  }
},
  mounted() {
    const user_id = this.$route.query.user_id
    fetch(`http://127.0.0.1:5000/api/post/${user_id}`, {
      method: 'GET',
      headers: { "Token": localStorage.getItem("token") },
    }).then((response) => response.json())
      .then((data) => {
        console.log(data)
        // this.user_name = data.user_name
        // this.imageurl = data.image
        // this.user_id = data.user_id
        // console.log(data.user_id)
        this.items = data
        this.user_name = this.items[0].user_name
        this.imageurl = this.items[0].user_dp
        this.bio = this.items[0].user_bio
        this.following_count = this.items[0].following_count
        this.follower_count = this.items[0].follower_count
      }).catch((err) => {
        console.log('yes')
        const user_id = this.$route.query.user_id
        console.log(user_id)
        this.$router.push({ name: 'newuser', query: { user_id: user_id } })
      }
      )
  }
}

</script>


<template>
  <div>
    <nav class="navbar">
      <!-- <ul class="navbar-logo">
        <div style="display:flex">
        <li class="cc"><input type="text" placeholder="Search.."></li>
        <li><button type="submit" style="margin-top: 10px;"><i class="fa fa-search"></i></button></li>
        </div>
      </ul> -->
      <ul class="navbar-menu">
        <li v-on:click="feed">Feed</li>
        <li><router-link to="Login">Logout</router-link></li>
      </ul>
    </nav>
    <div class="profile-container">
      <div class="profile-header">
        <img class="profile-image" :src="imageurl" v-if="imageurl" alt="Profile Image">
        <div class="profile-info">
          <h1>{{ user_name }}</h1>
          <div class="profile-stats">
            <div class="profile-stat">
              <span class="profile-stat-count">{{ items.length }}</span> posts
            </div>
            <div class="profile-stat">
              <span class="profile-stat-count">{{ follower_count }}</span> followers
            </div>
            <div class="profile-stat">
              <span class="profile-stat-count">{{ following_count }}</span> following
            </div>
          </div>
          <span>{{ bio }}</span>
          <div>
            <button class="profile-edit-button" style="background-color: black; color: aliceblue;margin-right: 5%;">following</button>
            <button class="profile-edit-button"  v-on:click="unfollow">Unfollow</button>
          </div>
        </div>
      </div>
      <div class="profile-posts">
        <div class="profile-post" v-for="item in items" :key="item.id">
          <div class="profile-box">
              <!-- <div>{{ item.post_time }}</div> -->
              <img class="profile-post-image" :src="item.post_image" alt="Post Image">
              <div style="margin-top: 2%;bottom: 5%; text-align: center;">
                {{ item.post_descr }}
              </div>
              <!-- <button class="za"  v-on:click="editpost(item.post_id)">Edit Post</button>
              <button class="za"  v-on:click="delete1(item.post_id)">Delete Post</button> -->
            </div>
          </div>
        </div>
      </div>
    </div>
  
</template>
  
  
  
<style>
/* .cc{
  float: right;
  padding:3px;
  border: 1px black;
  margin-top: 5px;
  margin-right: 100px;
  font-size: 17px;
} */
.za{
  margin-right: 10px;
  margin-left: 15px;
  margin-top:50%;
  font-size:10px
}

.profile-container {
  max-width: 700px;
  margin: 0 auto;
  padding: 1rem;
}

.profile-header {
  display: flex;
  align-items: center;
  padding-left: 20%;
}

.profile-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  margin-right: 2rem;
}


.profile-info {
  display: flex;
  flex-direction: column;
}

.profile-stats {
  display: flex;
  margin: 1rem 0;
}

.profile-stat {
  margin-right: 2rem;
}

.profile-stat-count {
  font-weight: bold;
}

.profile-edit-button {
  padding: 0.5rem 2rem;
  margin-top: 1rem;
  background-color: #fff;
  color: #000;
  border: 1px solid #000;
  border-radius: 0.5rem;
  cursor: pointer;
}

.profile-box {
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
  padding: 3%;
  min-height: 250px;
}

.profile-posts {
  display: flex;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-top: 2rem;
  overflow-x: scroll;
  max-height: 500px;
}

.profile-post {
  position: relative;
  object-fit: contain;
  max-height: 200px;
}

.profile-post-image {
  width: 100%;
  height: 100%;
  margin-top: 5%;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff;

  /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); */
}
.navbar-logo li {
  list-style: none;
  float: right;
  padding:3px;
  margin-top: 5px;
  margin-right: 30px;
  font-size: 17px;
}

.navbar-logo img {
  height: 40px;
}

.navbar-menu {
  display: flex;
  justify-content: center;
  align-items: center;
}

.navbar-menu li {
  margin: 0 10px;
  list-style: none;
}

.navbar-menu a {
  color: #000;
  text-decoration: none;
  font-size: 18px;
}

.navbar-menu a:hover {
  text-decoration: underline;
}

.dropdown {
  position: relative;
  display: inline-block;
}

.dropbtn {
  background-color: transparent;
  border: none;
  color: #666;
  cursor: pointer;
  font-size: 18px;
  margin-right: 10px;
  outline: none;
}
::-webkit-scrollbar {
  display: none;
}
</style>