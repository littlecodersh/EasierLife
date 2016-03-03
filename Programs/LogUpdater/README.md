#LogUpdater 160215
    Aimed at:
        Read in xml record get from OutlookAttachView and automatically produce work log and update
    Environment:
        OutlookAttachView v2.8.7
        Windows 8.1 - 64
        Python 2.7.10
    Attention:
        Use `python run.py` to run this program
        Put the xml format attachment list in root path as atta.xml
        Fill in sheets in infolist path
        Use producexml.py, makeuploadfile.py, uploadlog.py in this order
        Follow the instruction to modify input and output files

    目标：
        通过读取OutlookAttachView导出Outlook邮件的xml记录，自动生成工作日志并上传
    环境：
        OutlookAttachView v2.8.7
        Windows 8.1 - 64
        Python 2.7.10
    注意事项：
        使用`python run.py`来开始程序
        将OutlookAttachView导出的xml形式附件列表改为atta.xml放入目录
        填写完成infolist文件夹中的各项数据
        依次使用producexml.py, makeuploadfile.py, uploadlog.py
        按照说明修改输入输出文件
