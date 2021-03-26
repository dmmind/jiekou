import os
import unittest
import time
import HTMLTestRunner
import smtplib
from email.mime.text import MIMEText


# 当前脚本所在文件的真实路径
cur_path = os.path.dirname(os.path.realpath(__file__))


# 1、构造测试集，用 discover 方法加载所有的测试用例
def add_case(caseName="case", rule="test*.py"):
    # 用例文件夹路径，os.path.join把目录和文件名合成一个路径
    case_path = os.path.join(cur_path, caseName)

    # 如果不存在这个case文件夹，就自动创建一个
    if not os.path.exists(case_path):
        os.mkdir(case_path)
    print("test case path:%s" %case_path)

    # 构造测试集,discover可自动根据测试目录case_path匹配查找测试用例文件test*.py，
    # 并将查找到的测试用例组装到测试套件，因此可以直接通过run()方法执行discover
    discover = unittest.defaultTestLoader.discover(case_path,
                                                   pattern=rule,
                                                   top_level_dir=None)
    print(discover)
    return discover


# 2、执行所有的用例，并把结果写入HTML测试报告
def run_case(all_case, reportName="report"):
    now = time.strftime("%Y_%m_%d, %H:%M:%S")
    # 报告文件夹
    report_path = os.path.join(cur_path, reportName)
    if not os.path.exists(reportName):
        os.mkdir(reportName)
    report_abspath = os.path.join(report_path, now+"result.html")
    print("report path:%s" %report_abspath)

    fp = open(report_abspath, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                           title=u'自动化测试报告，测试结果如下：',
                                           description=u'用例执行情况：')
    # 调用add_case函数返回值
    runner.run(all_case)
    fp.close()


# 3、获取最新的测试报告
def get_report_file(report_path):
    # os.listdir()返回指定的文件夹包含的文件或文件夹的名字的列表
    lists = os.listdir(report_path)
    lists.sort(key=lambda fn: os.path.getmtime(os.path.join(report_path, fn)))
    print(u'最新测试生成的报告：'+lists[-1])
    # 找到最新生成的报告文件
    report_file = os.path.join(report_path, lists[-1])
    return


# 4、发送最新的测试报告内容
def send_mail(sender, psw, receiver, smtpserver, report_file, port):
    with open(report_file, "rb") as f:
        mail_body = f.read()
    # 定义邮件内容
    body = "<p>这个是qq发送的qq邮件</p>"
    msg = MIMEText(mail_body, _subtype='html', _charset='utf-8')
    msg['Subject'] = u"自动化测试报告"
    msg['from'] = sender
    msg['to'] = psw
    msg.attach(body)
    # 添加附件
    att = MIMEText(open(report_file, 'rb').read(), "base64", "utf-8")
    att['Content-Type'] = 'application/octet-stream'
    att['Content-Disposition'] = 'attachment; file="report.html'
    msg.attach(att)
    # 发送邮件
    try:
        smtp = smtplib.SMTP_SSL(smtpserver, port)  # 连接服务器
    except:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver, port)
    # 用户名密码
    smtp.login(sender, psw)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    print('test report email has send out!')


if __name__ == "__main__":
    # 1、加载用例
    all_case = add_case()

    # 2、执行用例
    run_case(all_case)

    # 3、获取最新的测试报告
    report_path = os.path.join(cur_path, "report")
    report_file = get_report_file(report_path)

    # 4、邮箱配置，发送报告
    from config import readConfig
    sender = readConfig.sender
    psw = readConfig.psw
    smtp_server = readConfig.smtp_server
    port = readConfig.port
    receiver = readConfig.receiver
    send_mail(sender, psw, receiver, smtp_server, report_file, port)

