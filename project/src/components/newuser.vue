<script>
export default{
    name:"newuser",
    data (){
        return{
            user_name:"",
            imageurl:"",
            bio:"",
            user_id:""

        }
    },
    methods:{
    addnew(){
        this.$router.push( {name: 'post' ,query: {user_id : this.user_id  }})
        },
        adduser(){
        this.$router.push( {name: 'AllUser',query: {user_id : this.user_id  }})
        }
    },
    mounted(){
            const user_id = this.$route.query.user_id
            fetch(`http://127.0.0.1:5000/api/newuser/${user_id}` , {
                method : 'GET',
                headers: { "Token": localStorage.getItem("token") },
            }).then((response)=>response.json())
                .then((data)=>{
                console.log(data)
                this.imageurl=data.image
                this.user_name=data.user_name
                this.bio=data.bio
                // this.user_name = data.user_name
                // this.imageurl = data.image
                this.user_id = data.user_id
                // console.log(data.user_id)
            })
        }
}
</script>
<template>
    <div>
      <h2 style="text-align:center">New User Profile</h2>

<div class="card image-box">
    <img :src="imageurl" v-if="imageurl"> 
  <h1>{{ user_name }}</h1>
  <p class="title">{{ bio }}</p>
  <p><button class="aaa" v-on:click="adduser">Add Friend</button></p>
  <p><button class="aaa" v-on:click="addnew">Add Post</button></p>
</div>

    </div>
</template>
<style>
.image-box img {
  max-width: 300px; /* set the maximum width of the image to the width of its container */
  max-height: 80px; /* set the maximum height of the image to the height of its container */
  object-fit: contain; /* set how the image should fit within the container */
  border-radius: 50%;
  margin-left:5%;
margin-top:5%}
.card {
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  max-width: 300px;
  margin: auto;
  text-align: center;
  font-family: arial;
}

.title {
  color: grey;
  font-size: 18px;
}

.aaa {
  border: none;
  outline: 0;
  display: inline-block;
  padding: 8px;
  color: white;
  background-color: #020202;
  text-align: center;
  cursor: pointer;
  width: 100%;
  font-size: 18px;
}

a {
  text-decoration: none;
  font-size: 22px;
  color: black;
}

button:hover, a:hover {
  opacity: 0.7;
}
</style>