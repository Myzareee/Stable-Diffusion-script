import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import shutil

directory_output = r"S:\SD\stable-diffusion-portable-main\output" # Папка Output в SD
directory_test_result = r"C:\Users\user\Desktop\Test result" # Папка, в которую складывать папки с результатами
directory_with_txt = r"C:\Users\user\Desktop\91" # Папка с текстовыми файлами
batch_number = 2

count = 0  
file_count = len(os.listdir(directory_with_txt))
driver = webdriver.Chrome() 
driver.get("http://127.0.0.1:7860/?__theme=dark") 
time.sleep(15)  

for i in range(file_count):
    batch = 0
    count += 1
    file_number = str(count) + '.txt'
    txtfile = os.path.join(directory_with_txt, file_number)
    with open (txtfile, 'r') as txtprompt:
        file_content = txtprompt.read()
        time.sleep(2)

    clear = driver.find_element(By.XPATH, "//*[@id='txt2img_prompt']/label/textarea") 
    clear.clear() # Очистить тесттовое поле от старого prompt
    time.sleep(1)

    send_prompt = driver.find_element(By.XPATH, "//*[@id='txt2img_prompt']/label/textarea")  
    send_prompt.send_keys(file_content) 
    time.sleep(1)

    while batch <= batch_number:
        batch += 1
        
        Generate = driver.find_element(By.ID, "txt2img_generate")
        Generate.click() # Нажать кнопку для генерации   
        time.sleep(30)  

        new_name = str(count) + '_' + str(batch) + '.png' # Переименовать последний файл в нужном формате
        sort = os.scandir(directory_output)
        sorted_files = sorted(sort, key=lambda f: os.stat(f).st_ctime) 
        time.sleep(1)
        last_file = os.path.join(directory_output, sorted_files[-1])
        time.sleep(1)
        os.rename(last_file, os.path.join(directory_output, new_name))
        time.sleep(2)

        file_renamed = os.path.join(directory_output, new_name) # Копировать этот файл в папку, общую для этой модели
        new_dir_name = str(count)
        new_dir_path = os.path.join(directory_test_result, new_dir_name)
        if not os.path.exists(new_dir_path):
            os.mkdir(new_dir_path)
            time.sleep(1) 
        shutil.copy2(file_renamed, os.path.join(new_dir_path, new_name)) 
        time.sleep(2)  
else: 
    driver.close()          