SIMPLEUI_CONFIG = {
    "system_keep": False,
    "menu_display": [
        "用户管理",
        "校园管理",
        "标签管理",
        "动物管理",
        "领养管理",
        "志愿者与社区",
        "捐赠管理",
        "活动管理",
        "海报管理",
        "问题管理",
        "通知管理",
    ],
    "dynamic": False,
    "menus": [
        {
            "app": "accounts",
            "name": "用户管理",
            "icon": "fas fa-users-cog",
            "models": [
                {
                    "name": "用户列表",
                    "icon": "fas fa-user-friends",
                    "url": "accounts/user/",
                },
                {
                    "name": "新增用户",
                    "icon": "fas fa-user-plus",
                    "url": "accounts/user/add/",
                },
                {
                    "name": "批量新增",
                    "icon": "fas fa-file-import",
                    "url": "accounts/user/bulk-add/",
                },
            ],
        },
        {
            "app": "campuses",
            "name": "校园管理",
            "icon": "fas fa-school",
            "models": [
                {
                    "name": "学校管理",
                    "icon": "fas fa-university",
                    "url": "campuses/school/",
                },
                {
                    "name": "校区管理",
                    "icon": "fas fa-map-marker-alt",
                    "url": "campuses/campus/",
                },
            ],
        },
        {
            "app": "tags",
            "name": "标签管理",
            "icon": "fas fa-tags",
            "models": [
                {
                    "name": "标签分类",
                    "icon": "fas fa-folder-open",
                    "url": "tags/tagcategory/",
                },
                {
                    "name": "标签内容",
                    "icon": "fas fa-tag",
                    "url": "tags/tag/",
                },
            ],
        },
        {
            "app": "animals",
            "name": "动物管理",
            "icon": "fas fa-paw",
            "models": [
                {
                    "name": "动物分类",
                    "icon": "fas fa-list",
                    "url": "animals/animalcategory/",
                },
                {
                    "name": "动物信息",
                    "icon": "fas fa-paw",
                    "url": "animals/animal/",
                },
                {
                    "name": "救助申请审核",
                    "icon": "fas fa-clipboard-check",
                    "url": "animals/rescuerequest/",
                },
            ],
        },
        {
            "app": "adoptions",
            "name": "领养管理",
            "icon": "fas fa-home",
            "models": [
                {
                    "name": "领养申请审核",
                    "icon": "fas fa-clipboard-check",
                    "url": "adoptions/adoptionapplication/",
                },
                {
                    "name": "领养关系",
                    "icon": "fas fa-hand-holding-heart",
                    "url": "adoptions/adoptionrelationship/",
                },
            ],
        },
        {
            "app": "volunteers",
            "name": "志愿者与社区",
            "icon": "fas fa-users",
            "models": [
                {
                    "name": "志愿者申请",
                    "icon": "fas fa-user-check",
                    "url": "volunteers/volunteerapplication/",
                },
                {
                    "name": "志愿者档案",
                    "icon": "fas fa-id-card",
                    "url": "volunteers/volunteerprofile/",
                },
                {
                    "name": "社区文章",
                    "icon": "fas fa-newspaper",
                    "url": "volunteers/communityarticle/",
                },
                {
                    "name": "用户帖子",
                    "icon": "fas fa-comments",
                    "url": "volunteers/communitypost/",
                },
                {
                    "name": "举报管理",
                    "icon": "fas fa-flag",
                    "url": "volunteers/communityreport/",
                },
            ],
        },
        {
            "app": "donations",
            "name": "捐赠管理",
            "icon": "fas fa-hand-holding-heart",
            "models": [
                {
                    "name": "捐赠项目",
                    "icon": "fas fa-box-open",
                    "url": "donations/donationproject/",
                },
                {"name": "物资认捐", "icon": "fas fa-gift", "url": "donations/pledge/"},
            ],
        },
        {
            "app": "activities",
            "name": "活动管理",
            "icon": "fas fa-calendar-alt",
            "models": [
                {
                    "name": "校园活动",
                    "icon": "fas fa-calendar",
                    "url": "activities/activity/",
                },
                {
                    "name": "活动报名",
                    "icon": "fas fa-user-check",
                    "url": "activities/participation/",
                },
            ],
        },
        {
            "app": "posters",
            "name": "海报管理",
            "icon": "fas fa-images",
            "models": [
                {"name": "海报列表", "icon": "fas fa-image", "url": "posters/poster/"}
            ],
        },
        {
            "app": "faqs",
            "name": "问题管理",
            "icon": "fas fa-question-circle",
            "models": [
                {
                    "name": "FAQ 分类",
                    "icon": "fas fa-folder",
                    "url": "faqs/faqcategory/",
                },
                {"name": "FAQ 内容", "icon": "fas fa-question", "url": "faqs/faq/"},
            ],
        },
        {
            "app": "notifications",
            "name": "通知管理",
            "icon": "fas fa-bell",
            "models": [
                {
                    "name": "站内通知",
                    "icon": "fas fa-envelope",
                    "url": "notifications/notification/",
                }
            ],
        },
    ],
}

SIMPLEUI_LOGIN_PARTICLES = False


# 首页标题
SIMPLEUI_HOME_TITLE = "首页"

SIMPLEUI_HOME_INFO = False

# 首页快捷入口由数据看板替代
SIMPLEUI_HOME_QUICK = False

# 最近动作
SIMPLEUI_HOME_ACTION = False

# 分析
SIMPLEUI_ANALYSIS = False

# 遮罩层
SIMPLEUI_LOADING = True

# 后台品牌信息
SIMPLEUI_LOGO = "/static/accounts/brand/logo.png"
SIMPLEUI_LOGIN_LOGO = SIMPLEUI_LOGO
SIMPLEUI_INDEX = "/"
