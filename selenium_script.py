from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
import time
import uuid

# Twitter credentials
username = ''
password = ''

# ProxyMesh configuration
proxy_host = ""
proxy_port = ""
proxy_user = ""
proxy_pass = ""

def get_trending_topics():
    # Configure proxy
    options = webdriver.ChromeOptions()
    options.add_argument(f"--proxy-server=http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}")

    # Set up Chrome driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    # Log in to Twitter
    driver.get("https://twitter.com/login")
    time.sleep(2)
    
    username_field = driver.find_element(By.NAME, "session[username_or_email]")
    password_field = driver.find_element(By.NAME, "session[password]")
    
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    
    time.sleep(5)  # Wait for the login process to complete

    # Fetch trending topics
    driver.get("https://twitter.com/explore/tabs/trending")
    time.sleep(5)
    
    trends = driver.find_elements(By.XPATH, "//section//span[contains(text(), 'Trending')]")
    
    trending_topics = []
    for trend in trends[:5]:
        trending_topics.append(trend.text)
    
    driver.quit()
    
    return trending_topics, proxy_host

def store_to_mongodb(trending_topics, ip_address):
    client = MongoClient("mongodb+srv://shivamgujaria4:HARn0gQmjrjWffuA@cluster0.napnr69.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client['twitter_trends']
    collection = db['trending_topics']
    
    record = {
        "_id": str(uuid.uuid4()),
        "trend1": trending_topics[0],
        "trend2": trending_topics[1],
        "trend3": trending_topics[2],
        "trend4": trending_topics[3],
        "trend5": trending_topics[4],
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ip_address": ip_address
    }
    
    collection.insert_one(record)
    return record

if __name__ == "__main__":
    topics, ip = get_trending_topics()
    record = store_to_mongodb(topics, ip)
    print("Stored record:", record)
