from sre_constants import SUCCESS
from playwright.sync_api import Playwright, sync_playwright, expect
import itertools

# TIME_QUESTION_TITLES = [
#     "您的意向时间段 - 早上",
#     "您的意向时间段 - 下午",
#     "您的意向时间段 - 晚上",
# ]
TIME_QUESTION_TITLES = [
    "早上",
    "下午",
    "晚上",
]

def get_time_period(time: str) -> str:
    hour = int(time.split(":")[0])
    if hour <= 12:
        return "早上"
    elif hour <= 16:
        return "下午"
    else:
        return "晚上"

def reserve(name: str, phone_number: str, times: list, max: int, barber: str, mode: str) -> None:
    is_success = False
    time_ret = "00:00"

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        # Open new page
        page = context.new_page()
        # Go to https://www.lediaocha.com/r/g7qmz

        # 开启 https://www.lediaocha.com/r/g7qmz 同时监听带有页面数据的请求，将请求结果保存到 response_info
        with page.expect_response("https://www.lediaocha.com/*/init") as response_info:
            page.goto("https://www.lediaocha.com/r/g7qmz")
            while not page.locator("text=你的姓名").is_visible():
                if page.locator("text=问卷已关闭如有疑问，请联系问卷发布者").is_visible():
                    print("问卷已关闭，尝试刷新页面")
                    page.reload()

        
        # 获取到页面数据中选择预约时间的节点
        time_nodes = [node for node in response_info.value.json()["data"]["nodes"]
                      if node["title"] in TIME_QUESTION_TITLES]

        # 获取到页面数据中预约时间的选项
        time_options = itertools.chain(*[node["options"] for node in time_nodes])

        # 获取到每个时间节点id对应的人数
        num_of_people_in_timeid = {}
        for time_node in time_nodes:
            for id, num in time_node["responseData"].items():
                num_of_people_in_timeid[id] = num

        # 获取到每个时间节点对应的人数
        num_of_people_in_time = {options["title"].replace("：", ":").replace(" ", "").replace("&nbsp;", ""):
                                 num_of_people_in_timeid[str(options["id"])] for options in time_options}

        # Fill input[id="430956"] with name
        # page.locator(".node:has-text('您的姓名')").locator("input").fill(name)
        page.locator(".node:has-text('你的姓名')").locator("input").fill(name)

        # Fill input[id="430957"] with phone
        # page.locator(".node:has-text('您的手机号')").locator("input").fill(phone_number)
        page.locator(".node:has-text('你的手机号')").locator("input").fill(phone_number)

        # click input[value="4355474"]
        # page.locator(
        #     ".node:has-text('请选择发型师')").locator("label:has-text('{}')".format(barber)).click()
        page.locator(".node:has-text('理发师')").locator("label:has-text('{}')".format(barber)).click()

        # Click input[value="4355478"]
        # page.locator(
        #     ".node:has-text('预约项目')").locator("label:has-text('{}')".format(mode)).click()
        page.locator(".node:has-text('选项')").locator("label:has-text('{}')".format(mode)).click()

        # 按照优先级时间表依次查询
        # 若符合最大容忍人数要求，则直接选择
        for time in times:
            if num_of_people_in_time[time] <= max:
                # 设置返回的时间
                time_ret = time

                # 获取对应时间段
                time_period = get_time_period(time)

                # 点击对应的时间段按钮
                # page.locator(".node:has-text('您的意向时间')").locator(
                # "label:has-text('{}')".format(time_period)).click()
                page.locator(".node:has-text('时间')").locator(
                "label:has-text('{}')".format(time_period)).click()
                
                # 获取时间中的时和分
                hour = int(time.split(":")[0])
                minute = int(time.split(":")[1])

                # 点击对应的时间按钮
                # time_period_question = page.locator(
                # ".node:has-text('您的意向时间段 - {}')".format(time_period))
                time_period_question = page.locator(
                ".node:has-text('{}')".format(time_period))

                time_period_question.locator(
                "label:has-text('{}')".format(hour)).locator("text={}".format(minute)).click()
                break

        page.locator("button:has-text(\"提交\")").click()

        # Click text=提交成功，感谢您的参与
        # page.locator("text=预约成功").click()
        page.locator("text=提交成功，感谢您的参与").click()
        is_success = True
        # ---------------------
        context.close()
        browser.close()
    return is_success, time_ret 
