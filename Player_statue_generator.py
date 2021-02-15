from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from PIL import Image
import requests
import base64
import json
import time
import os

#definitions
#uploads the skin
def upload_skin(file):
    elm = browser.find_element_by_xpath("//input[@type='file']")
    elm.send_keys(file)
    buttons = browser.find_elements_by_tag_name("button")
    try:
        upload = buttons[4]
        upload.click()
    except:
        upload = buttons[2]
        upload.click()
    print('[*]uploaded a skin...')
#is used by generate_armorstand
def find_texture_info(properties):
    for prop in properties:
        return json.loads(base64.b64decode(prop['value'], validate=True).decode('utf-8'))

#is used by generate_armorstand
def get_skin_url(username):
    r=requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}')
    USER_UUID = r.json()['id']
    r=requests.get(f'https://sessionserver.mojang.com/session/minecraft/profile/{USER_UUID}')
    userinfo = r.json()
    texture_info = find_texture_info(userinfo['properties'])
    texture_url=texture_info['textures']
    texture_url=texture_url['SKIN']
    texture_url=texture_url['url']
    s='{"textures":{"SKIN":{"url":"'+ texture_url +'"}}}'
    value = base64.b64encode(s.encode('utf-8'))
    skull = 'tag: {display:{Name:"{\\"text\\":\\"\\"}"},SkullOwner:{Id:[I;1453969447,2116502106,-1773076886,1306133934],Properties:{textures:[{Value:"'+value.decode()+'"}]}}}'
    return skull
    
#generates a armor stand with custom head and position
def generate_armorstand(username,name):
    return '{Tags:["'+ name +'"],Invisible:1b,NoBasePlate:1b,NoGravity:1b,ShowArms:1b,ArmorItems:[{},{},{},{}],HandItems:[{id:"player_head",Count:1b,'+get_skin_url(username)+'},{}],Pose:{RightArm:[315f,315f,0f]}}'

#Get's the value of certain pixels and replace them with th corect face 
def get_pixels(x,y,face,pix):
    pixels = {}
    for x_pos in range(4):
        for y_pos in range(4):
            pixels[x_pos,y_pos]=pix[x_pos+x,y_pos+y]
    if face == 'f':
        start_x = 8
        start_y = 8
    if face == 'ba':
        start_x = 24
        start_y = 8
    if face == 't':
        start_x = 8
        start_y = 0
    if face == 'bo':
        start_x = 16
        start_y = 0
    if face == 'l':
        start_x = 0
        start_y = 8
    if face == 'r':
        start_x = 16
        start_y = 8
    pixel_vals = pixels
    for ele in pixel_vals:
        pix[start_x+(ele[0]*2),start_y+(ele[1]*2)]= pixel_vals[ele]
        pix[start_x+(ele[0]*2)+1,start_y+(ele[1]*2)] = pixel_vals[ele]
        pix[start_x+(ele[0]*2),start_y+(ele[1]*2)+1] = pixel_vals[ele]
        pix[start_x+(ele[0]*2)+1,start_y+(ele[1]*2)+1] = pixel_vals[ele]

#cleans the alpha layer
def clean(pix):
    start_x = 8
    start_y = 8
    for o_x in range(8):
        for o_y in range(8):
            pix[o_x+start_x+32,o_y+start_y]=(0,0,0,0)
    start_x = 24
    start_y = 8
    for o_x in range(8):
        for o_y in range(8):
            pix[o_x+start_x+32,o_y+start_y]=(0,0,0,0)
    start_x = 8
    start_y = 0
    for o_x in range(8):
        for o_y in range(8):
            pix[o_x+start_x+32,o_y+start_y]=(0,0,0,0)
    start_x = 16
    start_y = 0
    for o_x in range(8):
        for o_y in range(8):
            pix[o_x+start_x+32,o_y+start_y]=(0,0,0,0)
    start_x = 0
    start_y = 8
    for o_x in range(8):
        for o_y in range(8):
            pix[o_x+start_x+32,o_y+start_y]=(0,0,0,0)
    start_x = 16
    start_y = 8
    for o_x in range(8):
        for o_y in range(8):
            pix[o_x+start_x+32,o_y+start_y]=(0,0,0,0)
            
#the main function
def main(Username, name , skin):
    time1=1
    time2=2
    datapack = {}
    directory= os.getcwd()
    save = os.path.join(directory,'skin/')
    datapack_folder = os.path.join(directory,"Player Statues")
    username='wocas'
    
    username='wocas'
    r=requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}')
    USER_UUID = r.json()['id']
    r=requests.get(f'https://sessionserver.mojang.com/session/minecraft/profile/{USER_UUID}')
    userinfo = r.json()
    texture_info = find_texture_info(userinfo['properties'])
    texture_url=texture_info['textures']
    texture_url=texture_url['SKIN']
    texture_url=texture_url['url']
    test=requests.get(texture_url)
    with open((f"{username}.png"), 'wb') as Original_skin:
        Original_skin.write(test.content)


    try:
        os.mkdir(save)
    except:
        pass
    try:
        os.mkdir(datapack_folder)
    except:
        pass
    #head
    #front 1
    im = Image.open(skin)
    pix = im.load()
    clean(pix)
    get_pixels(8, 8, 'f', pix)
    get_pixels(8, 4, 't', pix)
    get_pixels(4, 8, 'l', pix)
    im.save(f'{save}head1.png')
    im.close()
    upload_skin(f'{save}head1.png')
    time.sleep(time1)
    datapack['head1'] = generate_armorstand(Username, name)
    time.sleep(time2)

    #front 2
    im = Image.open(skin)
    pix = im.load()
    clean(pix)
    get_pixels(12, 8, 'f', pix)
    get_pixels(12, 4, 't', pix)
    get_pixels(16, 8, 'r', pix)
    im.save(f'{save}head2.png')
    im.close()
    upload_skin(f'{save}head2.png')
    time.sleep(time1)
    datapack['head2'] = generate_armorstand(Username, name)
    time.sleep(time2)

    #front 3
    im = Image.open(skin)
    pix = im.load()
    clean(pix)
    get_pixels(12, 12, 'f', pix)
    get_pixels(20, 4, 'bo', pix)
    get_pixels(16, 12, 'r', pix)
    im.save(f'{save}head3.png')
    im.close()
    upload_skin(f'{save}head3.png')
    time.sleep(time1)
    datapack['head3'] = generate_armorstand(Username, name)
    time.sleep(time2)

    #front 4
    im = Image.open(skin)
    pix = im.load()
    clean(pix)
    get_pixels(8, 12, 'f', pix)
    get_pixels(16, 4, 'bo', pix)
    get_pixels(4, 12, 'l', pix)
    im.save(f'{save}head4.png')
    im.close()
    upload_skin(f'{save}head4.png')
    time.sleep(time1)
    datapack['head4'] = generate_armorstand(Username, name)
    time.sleep(time2)

    #back 1
    im = Image.open(skin)
    pix = im.load()
    clean(pix)
    get_pixels(24, 8, 'ba', pix)
    get_pixels(12, 0, 't', pix)
    get_pixels(20, 8, 'r', pix)
    im.save(f'{save}head5.png')
    im.close()
    upload_skin(f'{save}head5.png')
    time.sleep(time1)
    datapack['head5'] = generate_armorstand(Username, name)
    time.sleep(time2)

    #back 2
    im = Image.open(skin)
    pix = im.load()
    clean(pix)
    get_pixels(28, 8, 'ba', pix)
    get_pixels(8, 0, 't', pix)
    get_pixels(0, 8, 'l', pix)
    im.save(f'{save}head6.png')
    im.close()
    upload_skin(f'{save}head6.png')
    time.sleep(time1)
    datapack['head6'] = generate_armorstand(Username, name)
    time.sleep(time2)

    #back 3
    im = Image.open(skin)
    pix = im.load()
    clean(pix)
    get_pixels(28, 12, 'ba', pix)
    get_pixels(16, 0, 'bo', pix)
    get_pixels(0, 12, 'l', pix)
    im.save(f'{save}head7.png')
    im.close()
    upload_skin(f'{save}head7.png')
    time.sleep(time1)
    datapack['head7'] = generate_armorstand(Username, name)
    time.sleep(time2)

    #back 4
    im = Image.open(skin)
    pix = im.load()
    clean(pix)
    get_pixels(24, 12, 'ba', pix)
    get_pixels(20, 0, 'bo', pix)
    get_pixels(20, 12, 'r', pix)
    im.save(f'{save}head8.png')
    im.close()
    upload_skin(f'{save}head8.png')
    time.sleep(time1)
    datapack['head8'] = generate_armorstand(Username, name)
    time.sleep(time2)


    #right arm
    #right arm 1
    im = Image.open(skin)
    pix = im.load()
    clean(pix)
    get_pixels(4, 20, 'f', pix)
    get_pixels(12, 20, 'ba', pix)
    get_pixels(4, 16, 't', pix)
    get_pixels(0, 20, 'l', pix)
    get_pixels(8, 20, 'r', pix)
    im.save(f'{save}rarm1.png')
    im.close()
    upload_skin(f'{save}rarm1.png')
    time.sleep(time1)
    datapack['rarm1'] = generate_armorstand(Username, name)
    time.sleep(time2)

    #right arm 2
    im = Image.open(skin)
    pix = im.load()
    clean(pix)
    get_pixels(4, 24, 'f', pix)
    get_pixels(12, 24, 'ba', pix)
    get_pixels(0, 24, 'l', pix)
    get_pixels(8, 24, 'r', pix)
    im.save(f'{save}rarm2.png')
    im.close()
    upload_skin(f'{save}rarm2.png')
    time.sleep(time1)
    datapack['rarm2'] = generate_armorstand(Username, name)
    time.sleep(time2)

    #right arm 3
    im = Image.open(skin)
    pix = im.load()
    clean(pix)
    get_pixels(4, 28, 'f', pix)
    get_pixels(12, 28, 'ba', pix)
    get_pixels(8, 16, 'bo', pix)
    get_pixels(0, 28, 'l', pix)
    get_pixels(8, 28, 'r', pix)
    im.save(f'{save}rarm3.png')
    im.close()
    upload_skin(f'{save}rarm3.png')
    time.sleep(time1)
    datapack['rarm3'] = generate_armorstand(Username, name)
    time.sleep(time2)


    #left arm
    #left arm 1
    im = Image.open(skin)
    pix = im.load()
    clean(pix)
    get_pixels(44, 20, 'f', pix)
    get_pixels(52, 20, 'ba', pix)
    get_pixels(44, 16, 't', pix)
    get_pixels(40, 20, 'l', pix)
    get_pixels(48, 20, 'r', pix)
    im.save(f'{save}larm1.png')
    im.close()
    upload_skin(f'{save}larm1.png')
    time.sleep(time1)
    datapack['larm1'] = generate_armorstand(Username, name)
    time.sleep(time2)

    #left arm 2
    im = Image.open(skin)
    pix = im.load()
    clean(pix)
    get_pixels(44, 24, 'f', pix)
    get_pixels(52, 24, 'ba', pix)
    get_pixels(40, 24, 'l', pix)
    get_pixels(48, 24, 'r', pix)
    im.save(f'{save}larm2.png')
    im.close()
    upload_skin(f'{save}larm2.png')
    time.sleep(time1)
    datapack['larm2'] = generate_armorstand(Username, name)
    time.sleep(time2)

    #left arm 3
    im = Image.open(skin)
    pix = im.load()
    clean(pix)
    get_pixels(44, 28, 'f', pix)
    get_pixels(52, 28, 'ba', pix)
    get_pixels(48, 16, 'bo', pix)
    get_pixels(40, 28, 'l', pix)
    get_pixels(48, 28, 'r', pix)
    im.save(f'{save}larm3.png')
    im.close()
    upload_skin(f'{save}larm3.png')
    time.sleep(time1)
    datapack['larm3'] = generate_armorstand(Username, name)
    time.sleep(time2)


    #body
    #body 1
    im = Image.open(skin)
    pix = im.load()
    clean(pix)
    get_pixels(20, 20, 'f', pix)
    get_pixels(16, 20, 'l', pix)
    get_pixels(20, 16, 't', pix)
    get_pixels(36, 20, 'ba', pix)
    im.save(f'{save}body1.png')
    im.close()
    upload_skin(f'{save}body1.png')
    time.sleep(time1)
    datapack['body1'] = generate_armorstand(Username, name)
    time.sleep(time2)

    #body 2
    im = Image.open(skin)
    pix = im.load()
    clean(pix)
    get_pixels(24, 20, 'f', pix)
    get_pixels(28, 20, 'r', pix)
    get_pixels(24, 16, 't', pix)
    get_pixels(32, 20, 'ba', pix)
    im.save(f'{save}body2.png')
    im.close()
    upload_skin(f'{save}body2.png')
    time.sleep(time1)
    datapack['body2'] = generate_armorstand(Username, name)
    time.sleep(time2)

    #body 3
    im = Image.open(skin)
    pix = im.load()
    clean(pix)
    get_pixels(20, 24, 'f', pix)
    get_pixels(16, 24, 'l', pix)
    get_pixels(36, 24, 'ba', pix)
    im.save(f'{save}body3.png')
    im.close()
    upload_skin(f'{save}body3.png')
    time.sleep(time1)
    datapack['body3'] = generate_armorstand(Username, name)
    time.sleep(time2)

    #body 4
    im = Image.open(skin)
    pix = im.load()
    clean(pix)
    get_pixels(24, 24, 'f', pix)
    get_pixels(28, 24, 'r', pix)
    get_pixels(32, 24, 'ba', pix)
    im.save(f'{save}body4.png')
    im.close()
    upload_skin(f'{save}body4.png')
    time.sleep(time1)
    datapack['body4'] = generate_armorstand(Username, name)
    time.sleep(time2)

    #body 5
    im = Image.open(skin)
    pix = im.load()
    clean(pix)
    get_pixels(20, 28, 'f', pix)
    get_pixels(16, 28, 'l', pix)
    get_pixels(28, 16, 'bo', pix)
    get_pixels(36, 28, 'ba', pix)
    im.save(f'{save}body5.png')
    im.close()
    upload_skin(f'{save}body5.png')
    time.sleep(time1)
    datapack['body5'] = generate_armorstand(Username, name)
    time.sleep(time2)

    #body 6
    im = Image.open(skin)
    pix = im.load()
    clean(pix)
    get_pixels(24, 28, 'f', pix)
    get_pixels(28, 28, 'r', pix)
    get_pixels(32, 16, 'bo', pix)
    get_pixels(32, 28, 'ba', pix)
    im.save(f'{save}body6.png')
    im.close()
    upload_skin(f'{save}body6.png')
    time.sleep(time1)
    datapack['body6'] = generate_armorstand(Username, name)
    time.sleep(time2)


    #right leg
    #right leg 1
    im = Image.open(skin)
    pix = im.load()
    clean(pix)
    get_pixels(20, 52, 'f', pix)
    get_pixels(28, 52, 'ba', pix)
    get_pixels(20, 48, 't', pix)
    get_pixels(16, 52, 'l', pix)
    get_pixels(24, 52, 'r', pix)
    im.save(f'{save}rleg1.png')
    im.close()
    upload_skin(f'{save}rleg1.png')
    time.sleep(time1)
    datapack['rleg1'] = generate_armorstand(Username, name)
    time.sleep(time2)

    #right leg 2
    im = Image.open(skin)
    pix = im.load()
    clean(pix)
    get_pixels(20, 56, 'f', pix)
    get_pixels(28, 56, 'ba', pix)
    get_pixels(16, 56, 'l', pix)
    get_pixels(24, 56, 'r', pix)
    im.save(f'{save}rleg2.png')
    im.close()
    upload_skin(f'{save}rleg2.png')
    time.sleep(time1)
    datapack['rleg2'] = generate_armorstand(Username, name)
    time.sleep(time2)

    #right leg 3
    im = Image.open(skin)
    pix = im.load()
    clean(pix)
    get_pixels(20, 60, 'f', pix)
    get_pixels(28, 60, 'ba', pix)
    get_pixels(24, 48, 'bo', pix)
    get_pixels(16, 60, 'l', pix)
    get_pixels(24, 60, 'r', pix)
    im.save(f'{save}rleg3.png')
    im.close()
    upload_skin(f'{save}rleg3.png')
    time.sleep(time1)
    datapack['rleg3'] = generate_armorstand(Username, name)
    time.sleep(time2)


    #left leg
    #left leg 1
    im = Image.open(skin)
    pix = im.load()
    clean(pix)
    get_pixels(36, 52, 'f', pix)
    get_pixels(44, 52, 'ba', pix)
    get_pixels(36, 48, 't', pix)
    get_pixels(32, 52, 'l', pix)
    get_pixels(40, 52, 'r', pix)
    im.save(f'{save}lleg1.png')
    im.close()
    upload_skin(f'{save}lleg1.png')
    time.sleep(time1)
    datapack['lleg1'] = generate_armorstand(Username, name)
    time.sleep(time2)

    #left leg 2
    im = Image.open(skin)
    pix = im.load()
    clean(pix)
    get_pixels(36, 56, 'f', pix)
    get_pixels(44, 56, 'ba', pix)
    get_pixels(32, 56, 'l', pix)
    get_pixels(40, 56, 'r', pix)
    im.save(f'{save}lleg2.png')
    im.close()
    upload_skin(f'{save}lleg2.png')
    time.sleep(time1)
    datapack['lleg2'] = generate_armorstand(Username, name)
    time.sleep(time2)

    #left leg 3
    im = Image.open(skin)
    pix = im.load()
    clean(pix)
    get_pixels(36, 60, 'f', pix)
    get_pixels(44, 60, 'ba', pix)
    get_pixels(40, 48, 'bo', pix)
    get_pixels(32, 60, 'l', pix)
    get_pixels(40, 60, 'r', pix)
    im.save(f'{save}lleg3.png')
    im.close()
    upload_skin(f'{save}lleg3.png')
    time.sleep(time1)
    datapack['lleg3'] = generate_armorstand(Username, name)
    time.sleep(time2)
    #make the datapack
    print('[*]making the datapack...')
    PackMcmeta = open(f"{datapack_folder}/pack.mcmeta", 'w')
    PackMcmeta.write('{\n   "pack":{\n      "pack_format":6,\n      "description":"Player Satues"\n   }\n}')
    PackMcmeta.close()

    data_folder = os.path.join(datapack_folder, "data")
    try:
        os.mkdir(data_folder)
    except:
        pass

    name_folder = os.path.join(data_folder, name)
    try:
        os.mkdir(name_folder)
    except:
        pass

    functions_folder = os.path.join(name_folder, 'functions')
    try:
        os.mkdir(functions_folder)
    except:
        pass
    GenerateMcfunction = open(f'{functions_folder}/generate.mcfunction','w')
    GenerateMcfunction.write(f'summon armor_stand ~-0.1 ~-0.9 ~-0.6  {datapack["rarm3"]}\ntag @e[type=minecraft:armor_stand,limit=1,sort=nearest] add base_building\nexecute as @e[tag=base_building] at @s run function {name}:build')
    GenerateMcfunction.close()

    BuildMcfuntion = open(f'{functions_folder}/build.mcfunction', 'w')
    BuildMcfuntion.write(f'#lleg2:\nexecute at @s run summon armor_stand ~ ~0.25 ~ {datapack["rarm2"]}\n#lleg1:\nexecute at @s run summon armor_stand ~ ~0.50 ~ {datapack["rarm1"]}\n#rleg3:\nexecute at @s run summon armor_stand ~ ~ ~0.25 {datapack["rleg3"]}\n#rleg2:\nexecute at @s run summon armor_stand ~ ~0.25 ~0.25 {datapack["rleg2"]}\n#rleg1:\nexecute at @s run summon armor_stand ~ ~0.50 ~0.25 {datapack["rleg1"]}\n#body6:\nexecute at @s run summon armor_stand ~ ~0.75 ~0.25 {datapack["body6"]}\n#body5:\nexecute at @s run summon armor_stand ~ ~0.75 ~ {datapack["body5"]}\n#body3:\nexecute at @s run summon armor_stand ~ ~1 ~ {datapack["body3"]}\n#body4:\nexecute at @s run summon armor_stand ~ ~1 ~0.25 {datapack["body4"]}\n#body1:\nexecute at @s run summon armor_stand ~ ~1.25 ~ {datapack["body1"]}\n#body2:\nexecute at @s run summon armor_stand ~ ~1.25 ~0.25 {datapack["body2"]}\n#larm3:\nexecute at @s run summon armor_stand ~ ~0.75 ~-0.25 {datapack["larm3"]}\n#larm2:\nexecute at @s run summon armor_stand ~ ~1 ~-0.25 {datapack["larm2"]}\n#larm1:\nexecute at @s run summon armor_stand ~ ~1.25 ~-0.25 {datapack["larm1"]}\n#rarm3:\nexecute at @s run summon armor_stand ~ ~0.75 ~0.5 {datapack["lleg3"]}\n#rarm2:\nexecute at @s run summon armor_stand ~ ~1 ~0.5 {datapack["lleg2"]}\n#rarm1:\nexecute at @s run summon armor_stand ~ ~1.25 ~0.5 {datapack["lleg1"]}\n#head4:\nexecute at @s run summon armor_stand ~0.12 ~1.5 ~ {datapack["head7"]}\n#head3:\nexecute at @s run summon armor_stand ~-0.12 ~1.5 ~0.25 {datapack["head3"]}\n#head7:\nexecute at @s run summon armor_stand ~-0.12 ~1.5 ~ {datapack["head4"]}\n#head8\nexecute at @s run summon armor_stand ~0.12 ~1.5 ~0.25 {datapack["head8"]}\n#head1:\nexecute at @s run summon armor_stand ~0.12 ~1.75 ~ {datapack["head6"]}\n#head2:\nexecute at @s run summon armor_stand ~-0.12 ~1.75 ~0.25 {datapack["head2"]}\n#head6:\nexecute at @s run summon armor_stand ~-0.12 ~1.75 ~ {datapack["head1"]}\n#head5:\nexecute at @s run summon armor_stand ~0.12 ~1.75 ~0.25 {datapack["head5"]}\ntag @s remove base_building')
    BuildMcfuntion.close()

    RemoveMcfunction = open(f'{functions_folder}/remove.mcfunction','w')
    RemoveMcfunction.write(f'kill @e[tag={name}]') 
    RemoveMcfunction.close()
    upload_skin(f'{os.getcwd()+"/"+username}.png')
    print('[*]done')


#opens the web browser
print("Hay, Welcome To the player statue generator i created.\nHere is how it works:\1st)Locate the skin you want as a statue and copy it's adress(e.g. C:/.../skin.png) !make sure you use / and not \\!\n2de You need to log in in the google tab that just opend and verfy that your a human.\n3th Hit enter after you've logged in.\n4th type 'main('Username', 'Name', 'Skin')' where:\n   Username=The name of your minecraft account that you used to login.\n   Name=The name that you want to give your statue(!important to take a different name each time!).\n   Skin=The adress of the skin.\n\nYou can do this as many times as you want just repeat step 1 and 4(as long as you don't close the browser or script)") 
browser = webdriver.Chrome()
web = browser.get('https://www.minecraft.net/nl-nl/profile/skin')
input('Enter when ready:')
