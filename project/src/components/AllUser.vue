<template>
<div>
  <nav class="navbar">
    <div class="navbar-logo">
    </div>
    <ul class="navbar-menu">
      <li v-on:click="feed">Feed</li>
      <li v-on:click="profile">Profile</li>
      <li><router-link to="Login">Logout</router-link></li>
    </ul>
  </nav>
    <div class="container">
<div class="row bootstrap snippets bootdey">
    <div class="col-md-8 col-xs-12">
      <div class="panel" id="followers">
        <div class="panel-body">
          <ul class="list-group list-group-dividered list-group-full">
            <li class="list-group-item">
              <div class="media">
                <div class="media-left">
                <div v-for="item in items" :key="item.id">
                  <a class="avatar avatar-online" href="javascript:void(0)">
                    <img :src="item.user_dp" alt=""><span>{{ item.user_name }}</span>
                    <i></i>
                  </a>
                  <div>
                  <div class="pull-right">
                    <button type="button"  class="as" style="margin-right: 2%;" @click="click(item.user_id)">{{ buttonText(item.user_id) }}</button>
                    <div v-if="buttonText(item.user_id)=='Following'">
                    <button type="button"  @click="unfollow(item.user_id)">UnFollow</button>
                    </div>
                  </div>
                </div>
                </div>
              </div>
              </div>
             
            </li>
        </ul>
           
    </div>
</div>
</div>
</div>
    </div>
</div>
</template>

<script>
export default{
    name:"AllUser",
    data(){
        return{
            items:[],
            is_following:false,
            table:[]
        }
    },
    computed: {
    buttonText() {
      return (userId) => {
        const followStatus = this.table.find((r) => r.user_id=== userId);
        return followStatus ? "Following" : "Follow";
      };
  }
},
    mounted(){
            const user_id = this.$route.query.user_id
            fetch(`http://127.0.0.1:5000/api/alluser/${user_id}`, {
                method : 'GET',
                headers: { "Token": localStorage.getItem("token") },
            }).then((response)=>response.json())
                .then((data)=>{
                console.log(data)
                this.items = data})
                .catch(error => {
        console.log(error)
      })
            fetch(`http://127.0.0.1:5000/api/following/${user_id}`, {
                method: 'GET',
                headers: { "Token": localStorage.getItem("token") },
              }).then(response => response.json())
                .then((data)=>{
                console.log(data)
                this.table = data})
        
      .catch(error => {
        console.log(error)
      })
  },
    methods:{
      click(i){
        const user_id = this.$route.query.user_id
        fetch(`http://127.0.0.1:5000/api/Addfollower/${user_id}/${i}`, {
                  method: "GET",
                  headers: { "Token": localStorage.getItem("token") },
                  
                }).then((response)=> {if (!response.ok) {
                        throw new Error('HTTP error, status code ' + response.status);
                      }
                      return response.json();})
                .then((data)=>{
                  console.log(data);
                  this.$router.push( {name: 'Profile' ,query: {user_id : user_id }})

                }) .catch((error)=> this.$router.push( {name: 'newuser' ,query: {user_id : user_id }}))
    },
    unfollow(i){
      const user_id = this.$route.query.user_id
        fetch(`http://127.0.0.1:5000/api/unfollow/${user_id}/${i}`, {
                  method: "GET",
                  headers: { "Token": localStorage.getItem("token") },
                  
                }).then((response)=> {if (!response.ok) {
                        throw new Error('HTTP error, status code ' + response.status);
                      }
                      return response.json();})
                .then((data)=>{
                  console.log(data);
                  this.$router.push( {name: 'Profile' ,query: {user_id : user_id }})

                }) .catch((error)=> alert(error))
    },
    feed(){
          const user_id = this.$route.query.user_id
          console.log(user_id)
          this.$router.push( {name: 'feed' ,query: {user_id : user_id }})
        },
        profile(){
          const user_id = this.$route.query.user_id
          console.log(user_id)
          this.$router.push( {name: 'Profile' ,query: {user_id : user_id }})
        }
    
      }
}


</script>

<style>
    body{
    margin-top:20px;
    background:#eee;
}

.avatar {
    position: relative;
    display: inline-block;
    width: 40px;
    white-space: nowrap;
    border-radius: 1000px;
    vertical-align: bottom
}

.avatar i {
    position: absolute;
    right: 0;
    bottom: 0;
    width: 10px;
    height: 10px;
    border: 2px solid #fff;
    border-radius: 100%
}

.avatar img {
    width: 100%;
    max-width: 100%;
    height: auto;
    border: 0 none;
    border-radius: 1000px
}

.avatar-online i {
    background-color: #4caf50
}

.avatar-off i {
    background-color: #616161
}

.avatar-busy i {
    background-color: #ff9800
}

.avatar-away i {
    background-color: #f44336
}

.avatar-100 {
    width: 100px
}

.avatar-100 i {
    height: 20px;
    width: 20px
}

.avatar-lg {
    width: 50px
}

.avatar-lg i {
    height: 12px;
    width: 12px
}

.avatar-sm {
    width: 30px
}

.avatar-sm i {
    height: 8px;
    width: 8px
}

.avatar-xs {
    width: 20px
}

.avatar-xs i {
    height: 7px;
    width: 7px
}
.media{
  margin-bottom: 10%;
}
.media-left{
  margin-bottom: 10%;
}
.alluser-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  margin-right: 2rem;
}
.pull-right{
  display: flex;}

.list-group-item {
    position: relative;
    display: block;
    padding: 10px 15px;
    margin-bottom: -1px;
    background-color: #fff;
    border: 1px solid transparent;
    object-fit: cover;
    margin-left: 20%;
    margin-right: 20%;
    height: 150%;
}
.as{
  background-color: black;
  color: azure;
  margin-right: 5%
}
</style>