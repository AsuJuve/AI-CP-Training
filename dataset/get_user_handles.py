from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()  
user_handles = []

for page in range(0,11):
    # Go to pages: 1, 72, 145, ... 711
    page = (page * 71) + 1
    driver.get(f"https://codeforces.com/ratings/page/{page}")

    datatable_div = driver.find_element(By.CSS_SELECTOR, "div.datatable.ratingsDatatable")
    div_with_table = datatable_div.find_element(By.CSS_SELECTOR, "div[style*='background-color: white;']")
    table = div_with_table.find_element(By.TAG_NAME, "table")
    tbody = table.find_element(By.TAG_NAME, "tbody")
    rows = tbody.find_elements(By.TAG_NAME, "tr")

    for row in rows[1:]:  # Start on second row to avoid header
        user_link = row.find_element(By.CSS_SELECTOR, "td:nth-child(2) a")
        user_handle = user_link.get_attribute("href").split("/")[-1]  # Get last string slice (user handle)
        user_handles.append(user_handle)

driver.quit()

with open("users.txt", "w") as file:
    for user in user_handles:
        file.write(user + "\n")

print(f"{len(user_handles)} users have been saved in users.txt.")
