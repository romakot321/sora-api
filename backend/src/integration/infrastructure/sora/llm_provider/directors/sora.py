import time
from typing import Dict, Any, Literal
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from src.integration.infrastructure.sora.llm_provider.browsers.base import BaseBrowser
from src.integration.infrastructure.sora.llm_provider.directors.base import BaseDirectorProvider
from src.integration.infrastructure.sora.llm_provider.utils.preprocessing import preprocess_prompt


class SoraDirector(BaseDirectorProvider):
    def __init__(self, browser: BaseBrowser, config: Dict[str, Any]):
        super().__init__(browser, config)
        self.browser.driver.get(self.config["url"])
        self.browser.random_time_delay(15, 30)
        if "Verify you are human by completing the action below." in self.browser.driver.find_element(By.CSS_SELECTOR,
                                                                                                      "html").text:
            print("CAPTCHA required")

    def upload_file(self, filepath: str):
        self.browser.click_element(self.config["attach_media_button_xpath"])
        self.browser.driver.execute_script('''document.querySelector("input[type='file']").style.display="block"''')
        # self.browser.click_element(self.config["upload_from_device_button_xpath"])

        self.browser.send_keys(self.config["file_input_xpath"], filepath, clear_first=True)

    def create_video(self, message: str) -> bool:
        try:
            # Send the prompt message to the input field
            send_status = self.browser.send_keys(
                self.config["input_xpath"], message, clear_first=True
            )
            if not send_status:
                print("Failed to send message to input field")
                return False

            # Click the general button
            click_status = self.browser.click_element(
                self.config["create_button_xpath"]
            )
            if not click_status:
                print("Failed to click general button")
                return False

            for request in self.browser.driver.requests:
                if request.response:
                    print(
                        request.url,
                        request.response.status_code,
                        request.response.headers['Content-Type']
                    )

            return True

        except Exception as e:
            print(f"Error creating video: {e}")
            return False

    def create_image(self, message: str, delay: int = 10, interval: int = 5) -> bool:
        _ = self.browser.send_keys(self.config["input_image_xpath"], "", clear_first=True)

        messages = preprocess_prompt(message)
        for message in messages:
            send_status = self.browser.send_keys(
                self.config["input_image_xpath"], message, clear_first=False
            )
            self.browser.random_delay(interval, interval)
            newline_status = self.browser.send_keys(
                self.config["input_image_xpath"], (Keys.SHIFT + Keys.ENTER), clear_first=False
            )
            self.browser.random_delay(interval, interval)

            if not (send_status and newline_status):
                print("Failed to send message to input field")
                return False

        self.browser.random_delay(delay, delay)
        # Click the general button
        click_status = self.browser.click_element(self.config["remix_button_xpath"])
        if not click_status:
            click_status = self.browser.click_element(self.config["create_image_button_xpath"])
            if not click_status:
                print("Failed to click general button")
                return False

        return True

    def create_video_safely(
            self, message: str, delay: int = 10, interval: int = 5
    ) -> bool:
        # Send the prompt message to the input field
        _ = self.browser.send_keys(self.config["input_xpath"], "", clear_first=True)

        messages = preprocess_prompt(message)
        for message in messages:
            send_status = self.browser.send_keys(
                self.config["input_xpath"], message, clear_first=False
            )
            self.browser.random_delay(interval, interval)
            newline_status = self.browser.send_keys(
                self.config["input_xpath"], (Keys.SHIFT + Keys.ENTER), clear_first=False
            )
            self.browser.random_delay(interval, interval)

            if not (send_status and newline_status):
                print("Failed to send message to input field")
                return False

        self.browser.random_delay(delay, delay)
        # Click the general button
        click_status = self.browser.click_element(self.config["create_button_xpath"])
        if not click_status:
            print("Failed to click general button")
            return False

        return True

    def _click_general_button_by_text(self, possible_texts: list) -> bool:
        """Helper method to click general button using list of possible text values"""
        try:
            # Generate xpath with OR conditions for all possible text values
            text_conditions = " or ".join(
                [f'contains(., "{text}")' for text in possible_texts]
            )
            # Combine with general button xpath
            base_xpath = self.config["general_button_xpath"]
            full_xpath = f"{base_xpath}[.//span[{text_conditions}]]"

            # Click the button
            click_status = self.browser.click_element(full_xpath)
            self.browser.random_delay(3, 7)

            if not click_status:
                print(f"No button found matching any of texts: {possible_texts}")
                return False

            return True

        except Exception as e:
            print(f"Error clicking general button: {e}")
            return False

    def _select_option_from_popup(self, option_text: str) -> bool:
        """Helper method to select option from popup menu"""
        try:
            # Wait for popup menu
            popup = self.browser.find_element(
                './/div[contains(@style, "position: fixed;") and @dir="ltr"]'
            )
            if not popup:
                print("Popup menu not found")
                return False

            # Find and click the option with matching text
            options = popup.find_elements(By.XPATH, './/div[@role="option"]')
            sorted_options = sorted(
                options, key=lambda x: len(x.get_attribute("innerText"))
            )
            for option in sorted_options:
                if option_text in option.get_attribute("innerText"):
                    option.click()
                    self.browser.random_delay(3, 7)
                    return True

            print(f"Option not found: {option_text}")
            return False

        except Exception as e:
            print(f"Error selecting option: {e}")
            return False

    def update_type(self, type: Literal["Image", "Video"]) -> bool:
        if not self._click_general_button_by_text(["Image", "Video"]):
            return False

        # Select the desired option
        return self._select_option_from_popup(type)

    def update_aspect_ratio(self, aspect_ratio: str) -> bool:
        """Update aspect ratio setting"""
        if aspect_ratio not in self.config["aspect_ratios"]:
            print(f"Invalid aspect ratio: {aspect_ratio}")
            return False

        # Click the aspect ratio button using all possible values
        if not self._click_general_button_by_text(self.config["aspect_ratios"]):
            return False

        # Select the desired option
        return self._select_option_from_popup(aspect_ratio)

    def update_resolution(self, resolution: str) -> bool:
        """Update resolution setting"""
        if resolution not in self.config["resolutions"]:
            print(f"Invalid resolution: {resolution}")
            return False

        # Click the resolution button using all possible values
        if not self._click_general_button_by_text(self.config["resolutions"]):
            return False

        # Select the desired option
        return self._select_option_from_popup(resolution)

    def update_duration(self, duration: int) -> bool:
        """Update duration setting"""
        duration_str = f"{duration}s"
        if duration_str not in self.config["durations"]:
            print(f"Invalid duration: {duration_str}")
            return False

        # Click the duration button using all possible values
        if not self._click_general_button_by_text(self.config["durations"]):
            return False

        # Select the desired option
        return self._select_option_from_popup(duration_str.replace("s", " seconds"))

    def update_variation(self, variation: int) -> bool:
        """Update variation setting"""
        variation_str = f"{variation}v"
        if variation_str not in self.config["variations"]:
            print(f"Invalid variation: {variation_str}")
            return False

        # Click the variation button using all possible values
        if not self._click_general_button_by_text(self.config["variations"]):
            return False

        # Select the desired option
        if variation_str == "1v":
            variation_str = "1 video"
        else:
            variation_str = variation_str.replace("v", " videos")

        return self._select_option_from_popup(variation_str)

    def check_improvement(self) -> bool:
        check_xpath = f"{self.config['latest_video_container_xpath']}//{self.config['improve_div_xpath'].lstrip('./')}"
        check_element = self.browser.find_element(check_xpath)
        if check_element:
            task_xpath = f"{self.config['latest_video_container_xpath']}//{self.config['task_href_xpath'].lstrip('./')}"
            task_links = self.browser.find_elements(task_xpath, timeout=30)

            # Extract unique video IDs
            task_urls = set()
            for link in task_links:
                href = link.get_attribute("href")
                full_url = urljoin(self.config["prefix"], href)
                if href:
                    task_urls.add(full_url)

            for url in task_urls:
                self.browser.driver.get(url)
                self.browser.random_delay(30, 15)
                self.browser.click_element(self.config["improve_confirm_xpath"])
                self.browser.random_delay(5, 5)
                self.browser.click_element(self.config["keep_none_button_xpath"])
                self.browser.random_delay(5, 5)
                self.browser.click_element(self.config["final_none_button_xpath"])
                self.browser.random_delay(15, 20)
            return True
        else:
            return False

    def download_videos(self, max_wait_time: int = 600) -> bool:
        """Download all generated videos"""
        original_url = self.browser.driver.current_url

        # Find the video container div
        video_container = self.browser.find_element(
            self.config["latest_video_container_xpath"]
        )
        if not video_container:
            print("Video container not found")
            return False

        start_time = time.time()
        combined_xpath = f"{self.config['latest_video_container_xpath']}//{self.config['video_href_xpath'].lstrip('./')}"
        while time.time() - start_time < max_wait_time:
            # Get all video hrefs
            video_links = self.browser.find_elements(combined_xpath, timeout=30)
            if not video_links:
                print("No video links found")

            # Extract unique video IDs
            video_urls = set()
            for link in video_links:
                href = link.get_attribute("href")
                full_url = urljoin(self.config["prefix"], href)
                if href and "/g/" in href:
                    video_urls.add(full_url)

            if not video_urls:
                # Check if we're still within wait time
                if time.time() - start_time >= max_wait_time:
                    print("Timeout waiting for videos to generate")
                    return False

                print("No videos ready yet, waiting 30 seconds...")
                self.browser.random_time_delay(30, 30)

                if self.check_improvement():
                    return False

                continue
            else:
                # print(f'Found {len(video_urls)} unique videos to download')
                break

        # Process each video URL
        for url in video_urls:
            # Navigate to video page
            self.browser.driver.get(url)
            self.browser.random_delay(3, 7)

            # Click download button
            download_button = self.browser.find_element(
                self.config["first_download_xpath"], 10, wait_type="clickable"
            )
            download_button.click()
            self.browser.random_delay(3, 7)

            # Find and click Video option in dropdown
            video_option = self.browser.find_element(
                self.config["download_option_xpath"], 10, wait_type="clickable"
            )
            video_option.click()
            self.browser.random_delay(3, 7)

            # Click final download button
            final_download = self.browser.find_element(
                self.config["second_download_xpath"], 10, wait_type="clickable"
            )
            final_download.click()
            self.browser.random_delay(3, 7)

        self.browser.driver.get(original_url)
        self.browser.random_delay(3, 8)

        return True

    def download_last_video(self, max_wait_time: int = 600) -> bool:
        """Download all generated videos"""
        original_url = self.browser.driver.current_url

        # Find the video container div
        video_container = self.browser.find_element(
            self.config["latest_video_container_xpath"]
        )
        if not video_container:
            print("Video container not found")
            return False

        start_time = time.time()
        combined_xpath = f"{self.config['latest_video_container_xpath']}//{self.config['video_href_xpath'].lstrip('./')}"
        while time.time() - start_time < max_wait_time:
            # Get all video hrefs
            video_links = self.browser.find_elements(combined_xpath, timeout=30)
            if not video_links:
                print("No video links found")

            # Extract unique video IDs
            video_urls = set()
            for link in video_links:
                href = link.get_attribute("href")
                full_url = urljoin(self.config["prefix"], href)
                if href and "/g/" in href:
                    video_urls.add(full_url)

            if not video_urls:
                # Check if we're still within wait time
                if time.time() - start_time >= max_wait_time:
                    print("Timeout waiting for videos to generate")
                    return False

                print("No videos ready yet, waiting 30 seconds...")
                self.browser.random_time_delay(30, 30)

                if self.check_improvement():
                    return False

                continue
            else:
                # print(f'Found {len(video_urls)} unique videos to download')
                break

        # Process each video URL
        url = list(video_urls)[-1]
        print("Downloading", url)
        # Navigate to video page
        self.browser.driver.get(url)
        self.browser.random_delay(30, 15)

        # Click download button
        download_button = self.browser.find_element(
            self.config["first_download_xpath"], 10, wait_type="clickable"
        )
        download_button.click()
        self.browser.random_delay(10, 15)

        # Find and click Video option in dropdown
        video_option = self.browser.find_element(
            self.config["download_option_xpath"], 10, wait_type="clickable"
        )
        video_option.click()
        self.browser.random_delay(15, 15)

        # Click final download button
        final_download = self.browser.find_element(
            self.config["second_download_xpath"], 10, wait_type="clickable"
        )
        final_download.click()
        self.browser.random_delay(15, 15)

        self.browser.driver.get(original_url)
        self.browser.random_delay(15, 30)

        return True
