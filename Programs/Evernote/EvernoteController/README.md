#EvernoteController 160114
    Aimed at:
        Simplify Evernote API as mush as possible
        The following contents can be added:
            Oauth.py: get oauth automatically (added when DEV_TOKEN isn't set)
            Storage.py: local storage to accelerate searching (added when LOCAL_STORAGE is True)
    Environment:
        Windows 8.1 - 64
        Python 2.7.10
    Attention:
        Please fill in the evernote key and secret in Oauth.py before runing this
        Evernote provided sandbox, where normal account can't be used
        Expunge functions can only be used when using DeveloperToken
        For sake of safety, evernote key and secret is not provided. I'm available if you need help.

    目标：
        将Evernote API的调用尽可能的简化
        以下内容可以选择添加：
            Oauth.py: 自动完成开放授权（DEV_TOKEN未被设置时自动添加）
            Storage.py: 增加本地存储功能，加速浏览（LOCAL_STORAGE为真时添加）
    环境：
        Windows 8.1 - 64
        Python 2.7.10
    注意事项：
        在使用之前请填写Oauth.py中的evernote key和secret
        印象笔记提供了沙盒环境，沙盒环境中是无法使用普通账号的
        彻底删除笔记与笔记本仅在使用 针对单个笔记的DeveloperToken 时才能使用
        出于安全考虑，没有提供key与secret，需要帮助可以联系我
