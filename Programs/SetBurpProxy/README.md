#SetBurpProxy 160106
    Aimed at:
        Change windows environment value to let web goes to Burp ports
            if environment value not set properly this will get it done
            after everything is done runing this again will get values cleared
        Close shadowsocks to avoid unnecessary disturb
            after everything is done runing this again will start shadowsocks
        Save some time:)
    Environment:
        Windows 8.1 - 64
        Python 2.7.10 (with psutil installed)
    Setting:
        Burp ports (default:127.0.0.1:8080)
        Path of Shadowsocks (default:./Shadowsocks.lnk)

    目标：
        完成流量流向Burp所需要的系统设置
            如果系统设置没有完成时调用，将会完成相关设置
            在使用完成后，重新调用本程序将清理环境设置
        关闭Shadowsocks以减小影响
            在使用完成后，重新调用本程序将启动Shadowsocks
        我才不想每次抓包都点开那么多设置呢:)
    环境：
        Windows 8.1 - 64
        Python 2.7.10 (安装 psutil)
    设置：
        Burp端口设置（默认：127.0.0.1:8080）
        Shadowsocks文件位置（默认：./Shadowsocks.lnk）
