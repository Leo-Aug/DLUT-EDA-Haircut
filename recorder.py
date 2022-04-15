from playwright.sync_api import Playwright, sync_playwright, expect

NAME = "刘洋"
PHONE_NUMBER = "18234317031"

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    # Open new page
    page = context.new_page()
    # Go to https://www.lediaocha.com/r/g7qmz
    page.goto("https://www.lediaocha.com/r/mpgp5")

    while page.is_visible("text=问卷已关闭"):
        print("问卷已关闭，尝试刷新页面")
        page.reload()
    

    # Fill input[id="430956"] with name
    page.locator(".node:has-text('您的姓名')").locator("input").fill(NAME)
    # page.locator(".node:has-text('你的姓名')").locator("input").fill(NAME)

    # Fill input[id="430957"] with phone
    page.locator(".node:has-text('您的手机号')").locator("input").fill(PHONE_NUMBER)
    # page.locator(".node:has-text('你的手机号')").locator("input").fill(PHONE_NUMBER)

    # click input[value="4355474"]
    page.locator(".node:has-text('请选择发型师')").locator("label:has-text('都可以')").click()
    # page.locator(".node:has-text('理发师')").locator("label:has-text('都行')").click()
    # Click input[value="4355478"]
    page.locator(".node:has-text('预约项目')").locator("label:has-text('理发')").click()
    # page.locator(".node:has-text('选项')").locator("label:has-text('理发')").click()


    time_periods = ["早上", "下午", "晚上"]

    for time_period in time_periods[::-1]:
        # Click input[value="4360655"]
        page.locator(".node:has-text('您的意向时间')").locator("label:has-text('{}')".format(time_period)).click()
        # page.locator(".node:has-text('时间')").locator("label:has-text('{}')".format(time_period)).click()

        # Click input[value="4360681"]
        time_period_question = page.locator(".node:has-text('您的意向时间段 - {}')".format(time_period))
        # time_period_question = page.locator(".node:has-text('{}')".format(time_period))
        
        time_period_question.locator("label:has-text('19')").locator("text=30").click()
        break

    page.locator("button:has-text(\"提交\")").click()
    # Click text=提交成功，感谢您的参与
    page.locator("text=预约成功").click()
    print("预约成功")
    # ---------------------
    context.close()
    browser.close()
with sync_playwright() as playwright:
    run(playwright)