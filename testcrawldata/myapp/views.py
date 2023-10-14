# async def index(request):
#     async with async_playwright() as playwright:
#         browser = await playwright.chromium.launch()
#         context = await browser.new_context()
#         page = await context.new_page()

#         await page.goto("https://dev-academy.megalithinc.com/")
#         content = await page.content()

#         await page.close()
#         await context.close()
#         await browser.close()

#     return HttpResponse(content)
from django.http import HttpResponse
from django.conf import settings
from google.cloud import storage
import io
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
import csv
from datetime import datetime
async def testCrawlCsv(request):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://ocpaweb.ocpafl.org/parcelsearch")
        await page.get_by_placeholder("Enter Property Address").click()
        await page.get_by_placeholder("Enter Property Address").fill("orange")
        await page.get_by_placeholder("Enter Property Address").press("Enter")
        await page.get_by_role("cell", name="HARRIS CHARLIE JR LIFE ESTATE REM: YOLANDA P HARRIS 1/5 INT REM: SHERI S HARRIS 1/5 INT REM: TERI L HARRIS 1/5 INT REM: HOLLY C HARRIS 1/5 INT REM: NOELLE C HARRIS 1/5 INT").click()
        await page.get_by_role("tab", name=" Sales").click()

        await page.wait_for_selector('td[data-title="Property Address"]')

        property_addresses = await page.query_selector_all('td[data-title="Property Address"]')
        sale_dates = await page.query_selector_all('td[data-title="Sale Date"]')
        sale_amounts = await page.query_selector_all('td[data-title="Sale Amt"]')
        deed_codes = await page.query_selector_all('td[data-title="Deed Code"]')
        beds_baths = await page.query_selector_all('td[data-title="Beds/Baths"]')
        inst_nums = await page.query_selector_all('td[data-title="Inst Num"]')

        stream = io.StringIO()
        writer = csv.writer(stream)
        writer.writerow(["Property Address", "Sale Date", "Sale Amount", "Deed Code", "Beds/Baths", "Inst Num"])
            
        for i in range(len(property_addresses)):
            address = await property_addresses[i].inner_text()
            print(property_addresses[i])
            sale_date = await sale_dates[i].inner_text()
            sale_amount = await sale_amounts[i].inner_text()
            deed_code = await deed_codes[i].inner_text()
            beds_baths_data = await beds_baths[i].inner_text()
            inst_num = await inst_nums[i].inner_text()

            writer.writerow([address, sale_date, sale_amount, deed_code, beds_baths_data, inst_num])
    
        await context.close()
        await browser.close()

        # Save the CSV file to Google Cloud Storage
        client = storage.Client()
        bucket = client.bucket('django-storage1')  #  GCS bucket name
        current_time = datetime.now().strftime("%Y%m%d-%H%M%S")  # Get the current timestamp
        blob = bucket.blob(f'csv/data_{current_time}.csv')  #  the filename and path in the bucket

        blob.upload_from_string(stream.getvalue(), content_type='text/csv')

    return HttpResponse("Data successfully scraped and saved to data.csv")



async def timtruyen(request):
    tentruyen_html = ''
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        page2 = await context.new_page()
        for i in range(1, 5):
            tentruyen = []
            await page.goto(f'https://www.nettruyenus.com/tim-truyen-nang-cao?genres=1,53&notgenres=&gender=-1&status=-1&minchapter=1&sort=0&page={i}')
            jtip_links = await page.query_selector_all('a.jtip')
            for link in jtip_links:
                href_value = await link.get_attribute('href')
                await page2.goto(href_value)
                await page2.wait_for_load_state('networkidle')
                rating_element = await page2.query_selector_all('span[itemprop="ratingValue"]')
                rating_text = ''
                for element in rating_element:
                    rating_text = await element.inner_text()
                    try:
                        rating_value = float(rating_text)
                    except ValueError:
                        rating_value = 0.0
                    if rating_value >= 3.7:
                        title_element = await page2.query_selector('h1.title-detail')
                        title_text = await title_element.inner_text()
                        a=title_text+f'<a href="{href_value}">    link</a>'+f'{rating_text}'
                        tentruyen.append(a)
            for truyen in tentruyen:
                tentruyen_html += truyen + '<br>'
        await browser.close()
    
   
    

    return HttpResponse(tentruyen_html)
# async def timtruyen(request):
#     tentruyen =[]
#     async with async_playwright() as playwright:
#         browser = await playwright.chromium.launch(headless=False)
#         context = await browser.new_context()
#         page = await context.new_page()


#         # Điều hướng đến URL
#         await page.goto('https://www.nettruyenmax.com/tim-truyen-nang-cao?genres=&notgenres=12%2C32%2C50&gender=-1&status=-1&minchapter=1&sort=0')

#         # Chụp màn hình và lưu lại ảnh
#         content =await page.content()
#         jtip_links = await page.query_selector_all('a[class="jtip"]')

#         # Chạy vòng lặp và click vào từng phần tử
#         for link in jtip_links:
#             href_value = await link.get_attribute('href')

#             await page.goto(href_value)
            
#             # Chờ cho dữ liệu được tải
#             page.wait_for_load_state("networkidle")

#             # Tìm thẻ <span> có itemprop="ratingValue"
#             rating_element = await page.query_selector_all('span[itemprop="ratingValue"]')
#             rating_element1 = await page.query_selector_all('span[itemprop="aggregateRating"]')
#             rating_text=''
#             for i in range(len(rating_element)):
#                 rating_text = await rating_element[i].inner_text()
#             # a=len(rating_element)
#             # rating_text = rating_element[0].inner_text()

#             try:
#                 rating_value = float(rating_text)
#             except ValueError:
#                 rating_value = 0.0

#             if rating_value > 4.0:
#                 title_element = await page.query_selector('h1[class="title-detail"]')
#                 tentruyen.append(title_element.inner_text())

#                     # Lưu nội dung của thẻ <h1 class="title-detail">
#                     # Có thể thực hiện các xử lý khác với title_text
#         # Sử dụng biến 'content' cho các xử lý tiếp theo

#         # Đóng trình duyệt
#         browser.close()

#     return HttpResponse(tentruyen)