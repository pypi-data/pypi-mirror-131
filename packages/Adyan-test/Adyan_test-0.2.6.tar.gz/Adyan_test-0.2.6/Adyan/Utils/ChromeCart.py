#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/17 15:15
# @Author  : Adyan
# @File    : ChromeCart.py
import random
import time

import asyncio
from Adyan.config_mongo import settings
from .proxy import ProxyGetter

from pyppeteer import launch
from retrying import retry

set = settings.Settings


async def chrome_page(url, browser=None, proxy=None):
    if browser is None:
        args = ['--no-sandbox']
        if proxy:
            print(proxy)
            args = ['--no-sandbox', f'--proxy-server={proxy}']
        browser = await launch(options={
            'handleSIGINT': False,
            'handleSIGTERM': False,
            'handleSIGHUP': False,
            'headless': False,
            'args': args
        })
    page = await browser.newPage()
    tasks = [
        asyncio.ensure_future(
            page.setUserAgent(
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
            )
        ),
        asyncio.ensure_future(page.setJavaScriptEnabled(True)),
        asyncio.ensure_future(page.setCacheEnabled(False)),
    ]
    await asyncio.wait(tasks)
    await page.goto(url)
    return page, browser


def _pages(browser, url):
    for _page in browser:
        if url in _page.url:
            return _page


class Chrome:

    async def cart(self, url, proxy=None):
        page, browser = await chrome_page(url, proxy)
        await Login().login(page)
        await asyncio.sleep(2)
        slider_again = await page.Jeval(
            'div.order-button-children-list > div:nth-child(2) > div',
            'node => node.textContent'
        )
        print(slider_again)
        await asyncio.sleep(2)
        await page.click(
            "#sku-count-widget-wrapper > div:nth-child(1) > div:nth-child(2) > span > span > span.next-input-group-addon.next-after > button")
        await asyncio.sleep(2)
        await page.click('div.order-button-children-list > div:nth-child(2) > div')
        await asyncio.sleep(3)
        cg = await page.Jeval('div.order-cart-logo > h4 > em', 'node => node.textContent')
        print(cg)
        await browser.close()

    def start(self, url, proxy=None):
        loop1 = asyncio.new_event_loop()
        asyncio.set_event_loop(loop1)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.cart(url, proxy))


class Login:
    def __init__(self):
        user = set(host='47.107.86.234').config.get("MY_USER")
        print(user)
        self.usr = user.get('name')
        self.pwd = user.get('pwd')

    def retry_if_result_none(result):
        return result is None

    @retry(retry_on_result=retry_if_result_none, )
    async def mouse_slide(self, page=None):
        await asyncio.sleep(2)
        try:
            await page.hover('#nc_1_n1z')
            await page.mouse.down()
            await page.mouse.move(2000, 0, {'delay': random.randint(1000, 2000)})
            await page.mouse.up()
        except Exception as e:
            print(e, ':验证失败')
            return None, page
        else:
            await asyncio.sleep(2)
            slider_again = await page.Jeval('.nc-lang-cnt', 'node => node.textContent')
            if slider_again != '验证通过':
                return None, page
            else:
                print('验证通过')
                return 1, page

    async def slide(self, page):
        slider = await page.Jeval('#nc_1_n1z', 'node => node.style')
        if slider:
            print('当前页面出现滑块')
            flag, page = await self.mouse_slide(page=page)
            if flag:
                await page.keyboard.press('Enter')
                print("print enter", flag)
        else:
            print("正常进入")
            await page.keyboard.press('Enter')
            await asyncio.sleep(2)

            try:
                global error
                print("error_1:", error)
                error = await page.Jeval('.error', 'node => node.textContent')
                print("error_2:", error)
            except Exception as e:
                error = None
            finally:
                if error:
                    print('确保账户安全重新入输入')
                else:
                    print(page.url)
                    await asyncio.sleep(5)
                    return 'cg'

    async def login(self, page, browser=None):
        await page.evaluate(
            '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
        await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
        await page.evaluate(
            '''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
        await page.evaluate(
            '''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')

        if 'login' in page.url:
            print(self.usr)
            await page.type("#fm-login-id", self.usr, {'delay': self.input_time_random() - 50})
            await page.type("#fm-login-password", self.pwd, {'delay': self.input_time_random()})
            await self.slide(page)
        # page = _pages(await browser.pages(), 'advance')
        return page

    def input_time_random(self):
        return random.randint(100, 151)


if __name__ == '__main__':
    url = "https://detail.1688.com/offer/614252293961.html?spm=a260k.dacugeneral.home2019rec.15.6633436cLdqrVw&scm=1007.21237.114566.0&pvid=f473cbd1-fe33-4107-8601-739784cc1b83&object_id=614252293961&udsPoolId=2274586&resourceId=1797996&resultType=normal"
    Chrome().start(f'https://login.taobao.com/?redirect_url={url}')
    # 'https://detail.1688.com/offer/650271479831.html?spm=a260k.dacugeneral.pc_index_cht.6.6633436cLdqrVw&&object_id=650271479831&udsPoolId=2607161')
