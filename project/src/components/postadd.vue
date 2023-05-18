<template>
  <div>
    <nav class="navbar">
        <div class="navbar-logo">
        </div>
        <ul class="navbar-menu">
          <li v-on:click="profile">Profile</li>
          <li v-on:click='f'>Feed</li>
          <li><a href="#">Logout</a></li>
        </ul>
      </nav>
    <div class="bloglite-post">
      <div class="post-header">
        <!-- <img :src=imageurl alt="Profile Image"> -->
        <h3>Prasanthi</h3>
      </div>
      <div class="post-image">
        <img :src="imageurl" v-if="imageurl">
        <input type="file" class ="a" placeholder="Add Image!" @change="handleUpload">
      </div>
      <div class="post-caption">
        <input type="text" placeholder="caption" v-model="post_descr" >
      </div>
      <div>
        <button class="a" v-on:click="addPost">Post</button>
     </div> 
    </div>
    </div>
  </template>
  
<script>
  export default{
    name:"post",
    data(){
        return {
            imageurl:"",
            post_name:"",
            post_descr:""
        }
    },
    methods:{
        handleUpload(event) {
            const file = event.target.files[0]
            const reader = new FileReader()
            reader.onload = (event) => {
                this.imageurl = event.target.result
                console.log(this.imageurl);
            }
            reader.readAsDataURL(file)
        },
    
    addPost(){
        const user_id = this.$route.query.user_id
        fetch(`http://127.0.0.1:5000/api/post/${user_id}` , {
            method : "POST",
            headers : {
                "Content-Type" : "application/json",
                "Token": localStorage.getItem("token"),
            },
            body:JSON.stringify({
                post_descr : this.post_descr,
                post_name : this.post_name,
                image : this.imageurl
            }),
        }).then((response)=>response.json())
                .then((data)=>{
                  console.log(data);
                  this.$router.push( {name: 'Profile' ,query: {user_id : data.user_id }})


                })
    },profile() {
      const user_id = this.$route.query.user_id
      console.log(user_id)
      this.$router.push({ name: 'Profile', query: { user_id: user_id } })
    },
    f() {
      const user_id = this.$route.query.user_id
      console.log(user_id)
      this.$router.push({ name: 'feed', query: { user_id: user_id } })
    }
}
}
</script>
  <style>
  .bloglite-post {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
  margin: 20px 0;
  padding: 20px;
  width:300px;
  margin-left: 35%;
}

.post-header {
  align-items: center;
  display: flex;
}

.post-header img {
  border-radius: 50%;
  margin-right: 10px;
  width: 30px;
  height: 30px;
  object-fit: contain;
}
.post-header h3 {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
}

.post-image {
  margin: 20px 0;
}

.post-image img {
  border-radius: 10px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
  max-width: 100%;
}

.post-caption {
  font-size: 10px;
  margin: 8px 0;
  width:90%
}


</style>





