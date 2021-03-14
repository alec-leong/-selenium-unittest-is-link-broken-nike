import unittest
import urllib3
import json
from path import chromedriver_rel_path
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome(chromedriver_rel_path)


class NikeTest(unittest.TestCase):
    def test_is_link_broken(self):
        global driver

        driver.implicitly_wait(2)
        driver.get('https://www.nike.com/')

        # HTTP request
        http = urllib3.PoolManager()

        # Hover new releases anchor element
        xpath = '//a[text()="New Releases"]'
        anchor = driver.find_element_by_xpath(xpath)
        ActionChains(driver).move_to_element(anchor).perform()

        # Get links
        anchors = driver.find_elements_by_xpath(xpath + '/following-sibling::div //a')

        for a in anchors:
            url = a.get_attribute('href')
            response = http.request('GET', url)
            status_code = response.status

            # Print response
            print(json.dumps({
                'url': url,
                'status_code': status_code,
                'text': a.text
            }, sort_keys=True, indent=2))

            # Unit test
            self.assertTrue(status_code < 400)

        http.clear()


if __name__ == '__main__':
    unittest.main()
