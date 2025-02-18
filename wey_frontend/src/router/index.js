import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import FeedView from '../views/FeedView.vue'
import SignupView from '../views/SignupView.vue'
import LoginView from '../views/LoginView.vue'
import SearchView from '../views/SearchView.vue'
import ProfileView from '../views/ProfileView.vue'
import FriendsView from '../views/FriendsView.vue'
import PostView from '../views/PostView.vue'
import ChatView from '../views/ChatView.vue'
import TrendView from '../views/TrendView.vue'
import EditProfileView from '../views/EditProfileView.vue'
import EditPasswordView from '../views/EditPasswordView.vue'
import NotificationsView from '../views/NotificationsView.vue'
import Overview from '../views/Overview.vue'
import SurveyView from '../views/SurveyView.vue'
import TrialOfConvertingFigma from '../views/Trial of converting figma.vue'
import Dashboard from '../views/Dashboard.vue'
import Company_Page from '../views/Company_Page.vue'
import CompanyDetails from '@/views/CompanyDetails.vue';
import FakeLogin from '../views/FakeLogin.vue'
import FakeSignup from '../views/FakeSignup.vue'
import Rating from '../components/ui/Rating.vue'
import OuterContainer from '../views/OuterContainer.vue'
import CompanyDashboard from '../views/CompanyDashboard.vue'
import UserNoCompany from '../views/UserNoCompany.vue'
import CompanyRegister from '../views/CompanyRegister.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/feed',
      name: 'feed',
      component: FeedView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView
    },
    {
      path: '/chat',
      name: 'chat',
      component: ChatView
    },
    {
      path: '/rating',
      name: 'rating',
      component: Rating
    },
    // {
    //   path: '/Dashboard',

    //   component: Dashboard,
    //   children: [
    //     {
    //       path: '',
    //       name: 'ov',
    //       component: Overview
    //     },
    //     {
    //       path: '/Company',
    //       name: 'company',
    //       component: Company_Page
    //     },

    //   ]
    // },
    {
      path: '/notifications',
      name: 'notifications',
      component: NotificationsView
    },
    {
      path: '/fakeSignup',
      name: 'fakeSignup',
      component: FakeSignup
    },
    {
      path: '/fakeLogin',
      name: 'fakeLogin',
      component: FakeLogin
    },
    {
      path: '/profile/edit',
      name: 'editprofile',
      component: EditProfileView
    },


    {
      path: '/profile/edit/password',
      name: 'editpassword',
      component: EditPasswordView
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/profile/:id/friends',
      name: 'friends',
      component: FriendsView
    },
    {
      path: '/:id',
      name: 'postview',
      component: PostView
    },
    {
      path: '/trends/:id',
      name: 'trendview',
      component: TrendView
    },
    {
      path: '/survey/:id',
      name: 'SurveyDetail',
      component: SurveyView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/figma',
      name: 'figma',
      component: TrialOfConvertingFigma
    },
    {
      path: "/users/no-company/",
      name: "user-no-company",
      component: UserNoCompany,
      props: true,
    },
    {
      path: '/OuterContainer',
      
      component: OuterContainer,
      children: [
        {
          path: '/',
          name: 'home',
          component: HomeView
        },
        {
          path: '/companies',
          name: 'companies',
          component: Company_Page
        },
        { path: '/companies/:id', 
          name: 'company-details', 
          component: CompanyDetails, 
          props: true 
        },
        {
          path: "/dashboard/:id",
          name: "company-dashboard",
          component: CompanyDashboard,
          props: true,
        },
        {
          path: "/users/no-company/",
          name: "user-no-company",
          component: UserNoCompany,
          props: true,
        },
        {
          path: "/profile-view/:id",
          name: "ProfileView",
          component: ProfileView,
          props: true,
        },
        {
          path: "/register",
          name: "register",
          component: CompanyRegister,
         
        },
        


      ]
    },
    // Company Pages
    // { path: '/', name: 'home', component: HomeView },
    // { path: '/companies', name: 'companies', component: Company_Page },
    // { path: '/companies/:id', name: 'company-details', component: CompanyDetails, props: true }, 
    
    
  ]

})

export default router
