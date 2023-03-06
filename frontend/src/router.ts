import Vue from 'vue';
import Router from 'vue-router';

import RouterComponent from './components/RouterComponent.vue';

Vue.use(Router);

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            component: () => import(/* webpackChunkName: "start" */ './views/main/Start.vue'),
            children: [
                {
                    path: 'auth',
                    component: () => import(/* webpackChunkName: "login" */ './views/auth/AuthPortal.vue'),
                    redirect: '/auth/login',
                    children: [
                        {
                            path: 'login',
                            component: () => import(/* webpackChunkName: "login" */ './views/auth/Login.vue'),
                        },
                        {
                            path: 'signup',
                            component: () => import(/* webpackChunkName: "login" */ './views/auth/Signup.vue'),
                        },
                    ]
                },
                {
                    path: 'recover-password',
                    component: () => import(/* webpackChunkName: "recover-password" */ './views/auth/PasswordRecovery.vue'),
                },
                {
                    path: 'reset-password',
                    component: () => import(/* webpackChunkName: "reset-password" */ './views/auth/ResetPassword.vue'),
                },
                {
                    path: 'main',
                    component: () => import(/* webpackChunkName: "main" */ './views/main/Main.vue'),
                    redirect: '/main/dashboard',
                    children: [
                        {
                            path: 'dashboard',
                            component: () => import(/* webpackChunkName: "main-dashboard" */ './views/main/Dashboard.vue'),
                        },
                        {
                            path: 'projects',
                            name: 'projects-home',
                            component: () => import(/* webpackChunkName: "main-dashboard" */ './views/main/project/ProjectsHome.vue'),
                        },
                        {
                            path: 'projects/:id',
                            component: () => import('./views/main/project/Project.vue'),
                            props: (route) => {
                                return {id: Number(route.params.id)}
                            },
                            children: [
                                {
                                    path: 'overview',
                                    name: 'project-overview',
                                    component: () => import('./views/main/project/ProjectOverview.vue'),
                                    props: (route) => {
                                        return {projectId: Number(route.params.id)}
                                    }
                                },
                                {
                                    path: 'datasets',
                                    name: 'project-datasets',
                                    component: () => import('./views/main/project/Datasets.vue'),
                                    props: (route) => {
                                        return {projectId: Number(route.params.id)}
                                    }
                                },
                                {
                                    path: 'models',
                                    name: 'project-models',
                                    component: () => import('./views/main/project/Models.vue'),
                                    props: (route) => {
                                        return {projectId: Number(route.params.id)}
                                    }
                                },
                                {
                                    path: 'inspection/:inspectionId',
                                    name: 'project-inspector',
                                    component: () => import('./views/main/project/InspectorWrapper.vue'),
                                    props: route => ({
                                        inspectionId: Number(route.params.inspectionId),
                                        projectId: Number(route.params.id)
                                    })
                                },
                                {
                                    path: 'feedbacks',
                                    name: 'project-feedbacks',
                                    component: () => import('./views/main/project/FeedbackList.vue'),
                                    props: (route) => {
                                        return {projectId: Number(route.params.id)}
                                    },
                                    children: [
                                        {
                                            path: ':feedbackId',
                                            name: 'feedback-detail',
                                            component: () => import('./views/main/project/FeedbackDetail.vue'),
                                            props: (route) => {
                                                return {id: Number(route.params.feedbackId)}
                                            },
                                            meta: {openFeedbackDetail: true}
                                        }
                                    ]
                                },
                                {
                                    path: 'project-tests-catalog',
                                    name: 'project-tests-catalog',
                                    component: () => import('./views/main/project/TestsCatalog.vue'),
                                    props: (route) => {
                                        return {projectId: Number(route.params.id)}
                                    },
                                },
                                {
                                    path: 'test-suites',
                                    name: 'project-test-suites',
                                    component: () => import('./views/main/project/TestSuites.vue'),
                                    props: (route) => {
                                        return {projectId: Number(route.params.id)}
                                    },
                                    children: []
                                }, {
                                    path: 'test-suite/:suiteId',
                                    name: 'test-suite',
                                    component: () => import('./views/main/project/TestSuite.vue'),
                                    props: (route) => {
                                        return {
                                            projectId: Number(route.params.id),
                                            suiteId: Number(route.params.suiteId),
                                        }
                                    },
                                    children: [
                                        {
                                            path: 'inputs',
                                            name: 'test-suite-inputs',
                                            component: () => import('./views/main/project/TestSuiteInputs.vue'),
                                            props: (route) => {
                                                return {
                                                    projectId: Number(route.params.id),
                                                    suiteId: Number(route.params.suiteId),
                                                }
                                            }
                                        },
                                        {
                                            path: 'test',
                                            name: 'test-suite-tests',
                                            component: () => import('./views/main/project/TestSuiteTests.vue'),
                                            props: (route) => {
                                                return {
                                                    projectId: Number(route.params.id),
                                                    suiteId: Number(route.params.suiteId),
                                                }
                                            }
                                        },
                                        {
                                            path: 'configuration',
                                            name: 'test-suite-configuration',
                                            component: () => import('./views/main/project/TestSuiteConfiguration.vue'),
                                            props: (route) => {
                                                return {
                                                    projectId: Number(route.params.id),
                                                    suiteId: Number(route.params.suiteId),
                                                }
                                            }
                                        },
                                        {
                                            path: 'execution/compare',
                                            name: 'test-suite-compare-executions',
                                            component: () => import('./views/main/project/TestSuiteCompareExecutions.vue'),
                                            props: (route) => {
                                                return {
                                                    suiteId: Number(route.params.suiteId),
                                                    projectId: Number(route.params.id)
                                                }
                                            }
                                        },
                                        {
                                            path: 'test/:testId/compare',
                                            name: 'test-suite-compare-test',
                                            component: () => import('./views/main/project/TestSuiteCompareTest.vue'),
                                            props: (route) => {
                                                return {
                                                    suiteId: Number(route.params.suiteId),
                                                    projectId: Number(route.params.id),
                                                    testId: Number(route.params.id)
                                                }
                                            }
                                        },
                                        {
                                            path: 'execution',
                                            name: 'test-suite-executions',
                                            component: () => import('./views/main/project/TestSuiteExecutions.vue'),
                                            props: (route) => {
                                                return {
                                                    suiteId: Number(route.params.suiteId),
                                                    projectId: Number(route.params.id),
                                                }
                                            },
                                            children: [
                                                {
                                                    path: ':executionId',
                                                    name: 'test-suite-execution',
                                                    component: () => import('./views/main/project/TestSuiteExecution.vue'),
                                                    props: (route) => {
                                                        return {
                                                            suiteId: Number(route.params.suiteId),
                                                            projectId: Number(route.params.id),
                                                            executionId: Number(route.params.executionId)
                                                        }
                                                    }
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            path: 'profile',
                            component: RouterComponent,
                            redirect: 'profile/view',
                            children: [
                                {
                                    path: 'view',
                                    component: () => import(
                                        /* webpackChunkName: "main-profile" */ './views/main/profile/UserProfile.vue'),
                                },
                                {
                                    path: 'password',
                                    component: () => import(
                                        /* webpackChunkName: "main-profile-password" */ './views/main/profile/UserProfileEditPassword.vue'),
                                },
                            ],
                        },
                        {
                            path: 'admin',
                            component: () => import(/* webpackChunkName: "main-admin" */ './views/main/admin/Admin.vue'),
                            redirect: 'admin/general',
                            children: [
                                {
                                    path: 'general',
                                    component: () => import(
                                        /* webpackChunkName: "main-admin" */ './views/main/admin/settings/SettingsGeneral.vue'),
                                },
                                {
                                    path: 'users',
                                    redirect: 'users/all',
                                },
                                {
                                    path: 'users/all',
                                    component: () => import(
                                        /* webpackChunkName: "main-admin-users" */ './views/main/admin/AdminUsers.vue'),
                                },
                                {
                                    path: 'users/invite',
                                    component: () => import(
                                        /* webpackChunkName: "main-admin-users" */ './views/main/admin/InviteUsers.vue'),
                                },
                                {
                                    path: 'users/edit/:id',
                                    name: 'main-admin-users-edit',
                                    component: () => import(
                                        /* webpackChunkName: "main-admin-users-edit" */ './views/main/admin/EditUser.vue'),
                                },
                                {
                                    path: 'users/create',
                                    name: 'main-admin-users-create',
                                    component: () => import(
                                        /* webpackChunkName: "main-admin-users-create" */ './views/main/admin/CreateUser.vue'),
                                },
                            ],
                        },
                    ],
                },
            ],
        },
        {
            path: '/*', redirect: '/',
        },
    ],
});
