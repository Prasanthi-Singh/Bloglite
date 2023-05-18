import SignUp from './components/SignUp.vue';
import EditProfile from './components/editprofile.vue'
import Login from './components/Login.vue';
import Profile from './components/Profile.vue';
import feed from './components/Feed.vue';
import post from './components/postadd.vue';
import newuser from './components/newuser.vue';
import AllUser from './components/AllUser.vue';
import EditPost from './components/EditPost.vue';
import otherprofile from './components/otherprofile.vue'
import search from './components/search.vue'


import{createRouter,createWebHistory} from 'vue-router'

const routes = [
    {name:'Search',
    component:search,
    path:'/search'},
    {
        name:'SignUp',
        component:SignUp,
        path:'/'
    },
    {
        name:'Login',
        component:Login,
        path:'/login'
    },
    {
        name:'Profile',
        component:Profile,
        path:'/profile'
    },
    {
        name:'feed',
        component:feed,
        path:'/feed'
    },
    {
        name:'post',
        component:post,
        path:'/post'
    },
    {
        name:'newuser',
        component:newuser,
        path:'/newuser'
    },
    {
        name:'AllUser',
        component:AllUser,
        path:'/alluser'
    },
    {
        name:'EditProfile',
        component:EditProfile,
        path:'/editprofile'
    },
    {
        name:'EditPost',
        component:EditPost,
        path:'/editpost'
    },
    {
        name:'OtherProfile',
        component:otherprofile,
        path:'/other'
    }


]

const router = createRouter({
    history:createWebHistory(),
    routes,
})

export default router;

