from selenium.webdriver.common.keys import Keys
import autoit
import seltools
import os, time

PASS = 'myPass01!' # The internal password used for encrypting metamask. Can be almost anything

def mm_signin(driver):
    if 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/' not in str(driver.current_url): return
    if 'unlock' not in str(driver.current_url): return
    if len(driver.find_elements_by_xpath('//*[@id="password"]')) > 0:
        driver.find_element_by_xpath('//*[@id="password"]').send_keys(PASS)
        driver.find_element_by_xpath('//button').click()

def mm_bypass_seed(driver):
    if 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#initialize/seed-phrase' not in driver.current_url: return
    # sometimes metamask will show the congrats page here. This is annoying.
    if len(driver.find_elements_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/button')) > 0:
        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/button').click()
    if len(driver.find_elements_by_xpath('//*[@id="password"]')) > 0:
        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/div[2]/div[2]/button[1]').click()

def mm_solve_seed(driver, seed_phrase):
    driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#initialize/seed-phrase')
    seltools.wait_for_element(driver, '//*[@id="app-content"]/div/div[3]/div/div/div[2]/div[1]/div[1]/div[4]/div[2]').click()
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/div[2]/div[2]/button[2]').click()
    for word in seed_phrase.split(' '):
        for unselected_elem in driver.find_elements_by_xpath('//div[@class="btn-secondary notranslate confirm-seed-phrase__seed-word confirm-seed-phrase__seed-word--sorted"]'):
            if unselected_elem.text.lower().strip() == word.lower().strip():
                unselected_elem.click()

def mm_accept_all_popups(driver):
    driver.switch_to.window(driver.window_handles[-1])
    if 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/' not in str(driver.current_url): return
    driver.implicitly_wait(0.2)
    for xpath in ('//button[contains(@class,"button btn-primary")]','//button[contains(@class,"button btn-secondary")]','//button'):
        try:
            while len(driver.find_elements_by_xpath(xpath)) > 0:
                driver.find_element_by_xpath(xpath).click()
                time.sleep(0.2)
        except: continue

# metamask CONSTANTLY switches up what it displays when and where.
def mm_bullshit_bypass(driver): # attempt to get past all popup windows
    time.sleep(0.5)
    mm_signin(driver)
    mm_bypass_seed(driver)

def goto_tab(driver, tab:int=0, wait:float=3.0):
    while len(driver.window_handles) < tab+1: time.sleep(0.1)
    time.sleep(wait) # metamask sometimes flashes a window
    driver.switch_to.window(driver.window_handles[tab])
    seltools.wait_for_page_load(driver)
    time.sleep(0.1)

def single_tab(driver):
    while len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
    driver.switch_to.window(driver.window_handles[0])

def setup_metamask_with_opensea(driver, seed_phrase):
    # Create metamask account with seed phrase
    driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
    seltools.wait_for_element(driver, '//button').click()

    seltools.wait_for_element(driver, '//*[@id="app-content"]/div/div[3]/div/div/div[2]/div/div[2]/div[1]/button').click()

    seltools.wait_for_element(driver, '//*[@id="app-content"]/div/div[3]/div/div/div/div[5]/div[1]/footer/button[1]').click()

    seltools.wait_for_element(driver, '//*[@id="app-content"]/div/div[3]/div/div/form/div[4]/div[1]/div/input').send_keys(str(seed_phrase).upper())
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(PASS)
    driver.find_element_by_xpath('//*[@id="confirm-password"]').send_keys(PASS)
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/form/div[7]/div').click()
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/form/button').click()

    seltools.wait_for_page_load(driver)

    # manually trigger the annoying 'secret backup phrase'
    driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#initialize/seed-phrase')
    seltools.wait_for_page_load(driver)

    mm_bypass_seed(driver)

    # now attempt to trigger and solve the 'secret backup phrase'
    #mm_solve_seed(driver) # metamask is actual bs sometimes: it will ask us for the seed even when already solved!!!
    # okay. This will not bother us. (it totally will though)
    # Skip signing in here. I could, but it does not help.

    # Sign in to opensea
    driver.get('https://opensea.io/wallet/locked?referrer=%2Fcollections')
    seltools.wait_for_element(driver, '//div[contains(@class, "wallet--wrapper")]//div[contains(@class,"ActionButton") and contains(@data-testid,"Button")]').click()

    # Connect in metamask
    goto_tab(driver, tab=1)
    seltools.wait_for_page_load(driver)
    mm_bullshit_bypass(driver)
    mm_accept_all_popups(driver)
    single_tab(driver)

    # sometimes we need to try again. I love metamask
    time.sleep(1.0)
    try:
        if len(driver.find_elements_by_xpath('//div[contains(@class, "wallet--wrapper")]//div[contains(@class,"ActionButton") and contains(@data-testid,"Button")]')) > 0:
            time.sleep(1.5)
            driver.find_element_by_xpath('//div[contains(@class, "wallet--wrapper")]//div[contains(@class,"ActionButton") and contains(@data-testid,"Button")]').click()
            time.sleep(1.0)
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[1])
                seltools.wait_for_page_load(driver)
                mm_bullshit_bypass(driver)
                mm_accept_all_popups(driver)
                single_tab(driver)
    except:
        pass

    seltools.wait_for_page_load(driver)

def create_nft(driver, info, sale_info={}):
    if 'image' not in info: return
    if 'name' not in info: return

    # Explicitly navigate to collections
    driver.get('https://opensea.io/collections')

    # Select the first collection (one must be pre-made)
    seltools.wait_for_element(driver, '//div[contains(@class,"ImageCardreact")]').click()
    seltools.wait_for_element(driver, '//a//div[contains(@class,"ActionButtonreact")]').click()

    # Sign with wallet
    goto_tab(driver, tab=1)
    seltools.wait_for_page_load(driver)
    mm_bullshit_bypass(driver)
    mm_accept_all_popups(driver)
    single_tab(driver)

    # Now we are on the create page. Good. We upload our file and hit go
    
    # Upload an image
    # Yes, this is ugly. Yes, this isn't ideal, 
    # but I couldn't get send_keys or setting the value with js to work
    seltools.wait_for_element(driver, '//div[contains(@class,"MediaInput") and contains(@class,"wrapper")]').click()
    time.sleep(2.0)
    autoit.win_active('Open')
    autoit.control_set_text('Open','Edit1',info['image'])
    autoit.control_send('Open','Edit1','{ENTER}')

    # Fill in all other fields
    driver.find_element_by_xpath(
        '//label[@for="name"]/..//input'
    ).send_keys(info['name'])

    if 'link' in info and len(info['link']) > 0:
        driver.find_element_by_xpath(
            '//label[@for="external_link"]/..//input'
        ).send_keys(info['link'])

    if 'description' in info and len(info['description']) > 0:
        driver.find_element_by_xpath(
            '//label[@for="description"]/..//input'
        ).send_keys(info['description'])

    def property_fillin(driver, infoname:str, start_xpath:str, row_input_box_xpaths:tuple or list):
        if 'opensea.io/collection' not in driver.current_url: return
        if 'assets/create' not in driver.current_url: return
        if infoname not in info or len(info[infoname]) == 0: return
        
        # I don't know why, but action chains are the only way I could do this without crashing.
        btn = driver.find_element_by_xpath(start_xpath)
        webdriver.common.action_chains.ActionChains(driver).move_to_element_with_offset(btn, 5, 5).click().perform()

        popup = seltools.wait_for_element(driver, '//div[contains(@class,"ModalV2react")]')
        
        # hit add more
        addmore = popup.find_elements_by_xpath('.//div[contains(@class,"ActionButtonreact")]')[0]
        for i in range(0,len(info[infoname])-1):
            addmore.click()
            driver.implicitly_wait(0.1)

        # loop over all table rows to fill in info
        i = 0
        for row in popup.find_elements_by_xpath('.//table//tr[contains(@class,"TrContainer")]'):
            for j in range(0, len(row_input_box_xpaths)):
                if j == 0:
                    val = list(info[infoname].items())[i][0]
                    input_box = row.find_element_by_xpath(row_input_box_xpaths[0])
                else:
                    if isinstance( list(info[infoname].items())[i][1], tuple) or isinstance( list(info[infoname].items())[i][1], list):
                        val = list(info[infoname].items())[i][1][j-1]
                    else:
                        val = list(info[infoname].items())[i][1]
                    input_box = row.find_element_by_xpath(row_input_box_xpaths[j])
                driver.execute_script('arguments[0].value="arguments[1]"', input_box, str(val).replace('"','')) 
                input_box.click()
                input_box.send_keys(Keys.CONTROL, 'a')
                input_box.send_keys(val)
            i += 1
        
        # hit save
        popup.find_elements_by_xpath('.//div[contains(@class,"ActionButtonreact")]')[1].click()

    # Fill in properties
    property_fillin(
        driver,
        'properties',
        '//form/div[5]/div/div[2]/div/div',
        ('.//input[contains(@placeholder,"Character")]', 
        './/input[contains(@placeholder,"Male")]')
    )

    # Fill in levels
    property_fillin(
        driver,
        'levels',
        '//form/div[6]/div/div[2]/div/div',
        ('.//input[contains(@placeholder,"Speed")]', 
        './/table/tbody/tr/td[2]/div/div/input',
        './/table/tbody/tr/td[3]/div/div/input')
    )

    # Fill in stats
    property_fillin(
        driver,
        'stats',
        '//form/div[7]/div/div[2]/div/div',
        ('.//input[contains(@placeholder,"Speed")]', 
        './/table/tbody/tr/td[2]/div/div/input',
        './/table/tbody/tr/td[3]/div/div/input')
    )

    # Fill in unlockable content
    if 'unlocked' in info:
        driver.find_element_by_xpath('//div[@class="switch"]').click()
        txtbox = seltools.wait_for_element(driver, '//div[contains(@class, "unlockable-content")]//textarea')
        txtbox.click()
        txtbox.send_keys(info['unlocked'])

    # Create NFT!!!
    driver.find_element_by_xpath('//div[contains(@class, "action")]//div[contains(@class, "DivButton")]').click()

    goto_tab(driver, tab=1)
    seltools.wait_for_page_load(driver)
    mm_bullshit_bypass(driver)
    mm_accept_all_popups(driver)
    single_tab(driver)

    # Wait for completion
    seltools.wait_for_element(driver, '//div//div[contains(@class,"collectionManagerAssetCreate")]/../header')


def file_to_nft_info(path_to_file:str, overrides:dict={}, date_format:str='%B %d, %Y', add_placeholders:dict={}, defaults:dict={'name':'%n','properties':{'Created On': '%c','File Size': '%z'}}):
    # extract the file's name and type
    file_name = path_to_file[path_to_file.rfind(os.path.sep)+len(os.path.sep):path_to_file.find('.')].title()
    file_type = path_to_file[path_to_file.find('.')+1:].title()
    
    # get and format the file's info
    file_info = os.stat(path_to_file)
    
    file_created = datetime.fromtimestamp(file_info.st_ctime).strftime(str(date_format))
    file_lastmod = datetime.fromtimestamp(file_info.st_ctime).strftime(str(date_format))

    file_size = file_info.st_size
    step_names = ['b','Kb','Mb','Gb','Tb']
    while len(step_names) > 1 and file_size > 1024:
        file_size /= 1024; step_names.pop(0)
    file_size = f'{int(file_size+0.99)} {step_names[0]}'

    # Generate the dict
    nft_meta = ast.literal_eval(
        repr(defaults).replace(
            '%n', re.sub('\\|"|\'', '', file_name.replace('_',' '))
        ).replace(
            '%t', re.sub('\\|"|\'', '', file_type)
        ).replace(
            '%z', file_size
        ).replace(
            '%d', file_lastmod
        ).replace(
            '%c', file_created
        )
    )

    for p, v in add_placeholders.items():
        nft_meta = ast.literal_eval(
            repr(nft_meta).replace(
                f'%{p}', re.sub('\\|"|\'', '', v)
            )
        )
    
    nft_meta['image'] = os.path.abspath(file.path)
    return {**nft_meta, **overrides}

if __name__ == '__main__':
    from selenium import webdriver
    from datetime import datetime
    import ast, os, re

    # Ask for seed phrase
    seed = input('Please insert your seed phrase: ')

    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications" : 2})
    options.add_argument(f'load-extension={os.path.abspath(os.getcwd())}/extensions/metamask/')

    with webdriver.Chrome(options=options) as driver:
        # Immediately close the new tab metamask creates
        while len(driver.window_handles) < 2: time.sleep(0.1)
        single_tab(driver)

        # Setup
        setup_metamask_with_opensea(driver, seed)

        # Loop over all files
        i = 1; allfiles = list(os.scandir('./images'))
        for file in os.scandir('./images'):
            if file.is_dir(): continue
            
            # Generate the NFT's metadata
            nft_meta = file_to_nft_info(
                os.path.abspath(file.path),
                add_placeholders={
                    'i': str(i),
                    'o': str(len(allfiles))
                }
            )

            # Create the NFT!
            print(f'Creating NFT #{i} with metadata ', nft_meta)
            create_nft(driver, nft_meta)

            i += 1
        print('All NFTs created successfully')
        