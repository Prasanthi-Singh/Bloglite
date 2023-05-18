<template>
    <div class="editprofile-container">
  <div>
    <div class="image-container form-group" style="width:500px">
    <img :src="imageurl" v-if="imageurl"> 
    <input type="file" id="upload-file" name="upload-file" @change="onFileChange">
    </div> 
    <div class="form-group">
      <input type="text" id="name" name="name" placeholder="Enter your new user_name" v-model="user_name">
    </div>
    <div class="form-group">
      <input type="email" id="email" name="email" placeholder="Enter your new email" v-model="email">
    </div>
    <div class="form-group">
      <input type="text" id="name"  placeholder="Enter your new Bio" v-model="bio">
    </div>
    <div style="display:flex ; margin-left: 30%;">
    <button class="editprofile-btn" v-on:click="cancel">Cancel</button>
    <button type="submit" class="editprofile-btn" v-on:click="EditProfile" >Edit </button>
  </div>
  </div>
</div>

</template>
<script >
export default {
  name: "editProfile",
  data() {
    return {
      user_name: "",
      imageurl: "",
      bio: "",
      email:"",
      user_id:""

    }
  },
 mounted() {
    const user_id = this.$route.query.user_id
    fetch(`http://127.0.0.1:5000/api/editprofile/${user_id}`, {
      method: 'GET',
      headers: { "Token": localStorage.getItem("token") },
    }).then((response) => response.json())
      .then((data) => {
        console.log(data)
        this.user_name = data.user_name
        this.imageurl = data.image
        this.bio = data.bio
        this.email = data.email
        this.user_id = data.user_id
      }).catch((err) => {
        console.log('yes')
        const user_id = this.$route.query.user_id
        console.log(user_id)
        this.$router.push({ name: 'newuser', query: { user_id: user_id } })
      }
      )
  },
  methods:{
    EditProfile(){
        fetch(`http://127.0.0.1:5000/api/editprofile/${this.user_id}`, {
                  method: "PUT",
                  headers: { "Content-Type": "application/json" , 
                  "Token": localStorage.getItem("token") },
                  body: JSON.stringify({
                    user_name: this.user_name,
                    email: this.email,
                    bio:this.bio,
                    image:this.imageurl,
                  }),
                }).then((response)=>{
                      if (!response.ok) {
                        throw new Error('HTTP error, status code ' + response.status);
                      }
                      return response.json();
                })
                .then((data)=>{
                  console.log('yes');
                  if (data) {
                        // User registered successfully
                        this.$router.push( {name: 'Profile' ,query: {user_id : this.user_id }})
                      } else {
                        // Error occurred
                        throw new Error(data.description);
                      }

                }).catch((error)=>{
                  console.log("User already exist");
                  alert("User already exist")})
    }
  ,
  onFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.fileName = file.name;
            const reader = new FileReader()
            reader.onload = (event) => {
                this.imageurl = event.target.result
                console.log(this.imageurl);
            }
            reader.readAsDataURL(file)
      } else {
        this.fileName = 'Select Profile Photo';
      }
    },
    cancel(){
        this.$router.push( {name: 'Profile' ,query: {user_id : this.user_id }})
    }
}
}
</script>
<style scoped>
/* .image-container {
  width: 300px; /* set the width of the container */
  /* height: 200px; /* set the height of the container */
/* }  */

.image-container img {
  max-width: 150px; /* set the maximum width of the image to the width of its container */
 
  max-height: 100px; /* set the maximum height of the image to the height of its container */
  object-fit: contain; /* set how the image should fit within the container */
  border-radius: 50%;
  margin-left:40%}
.editprofile-container {
  max-width: 350px;
  margin: 0 auto;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 10px;
  max-width: 70%;
  margin-left: 10%;
}


input {
  font-size: 10px;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.editprofile-btn {
  background-color: #0c0e0d;
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 5px 10px;
  font-size: 15px;
  cursor: pointer;
  margin-top: 10px;
  margin-left: 5%;
                        
}
.editprofile-btn:hover {
  background-color: #f2f7f2;
  color: #0c0e0d;
}
</style>