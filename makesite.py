from makeindex import MakeIndex
from search4tag import search4tag

def ExtractMenuItem(sourse_name):
    p = open(sourse_name, 'r', encoding = 'utf-8');
    text = p.read();
    (status, _, _, menu_name) = search4tag(text, '!menu_item', '!/menu_item').FindTagPair();    
    p.close();
    return status, menu_name
    
def ExtractPageInfo(sourse_name, top_link = False):
    p = open(sourse_name, 'r', encoding = 'utf-8');
    text = MakeIndex(p.read(), top_link);
    (_, _, _, title) = search4tag(text, 'title', '/title').FindTagPair();
    (_, _, _, body) = search4tag(text, 'body', '/body').FindTagPair();    
    p.close();
    return title, body
    
def TagSubstitute(text, tag, inserted_text):    
    tag_begin_position = text.find('<' + tag);
    if tag_begin_position < 0:
        return text + '';
    tag_end_position = text.find('>', tag_begin_position);
    if tag_end_position < 0:
        return text[:tag_begin_position] + inserted_text;
    return text[:tag_begin_position] + inserted_text + text[tag_end_position + 1:];

def WebpageNameGenerator(name):
    return name + '.browser.html';
    
def SourseNameGenerator(name):
    return name + '.html';
    
def PrintNameGenerator(name):
    return name + '.printer.html';

def DrawActiveMenuItem(menu_index):
    return '<div class = \'selected_menu_item\'>%s</div>\n'%(menu_items[menu_index][0]);

def DrawActiveSubmenuItem(menu_index, submenu_index):
    return '<div class = \'selected_submenu_item\'>%s</div>\n'%(menu_items[menu_index][submenu_index]);
    
def DrawMenuItem(menu_index):
    return '<div class = \'menu_item\'><a class = "item" href = \'%s\'>%s</a></div>\n'%(WebpageNameGenerator(menu[menu_index][0]), menu_items[menu_index][0]);
    
def DrawSubmenuItem(menu_index, submenu_index):
    return '<div class = \'submenu_item\'><a class = "item" href = \'%s\'>%s</a></div>\n'%(WebpageNameGenerator(menu[menu_index][submenu_index]), menu_items[menu_index][submenu_index]);

def PrintWersionLinkGenerator(print_version_name):
    return '[<a href = "%s">Версия для печати</a>]'%(print_version_name)

def GenerateMenu(active_menu_indexes):
    text = '';
    if active_menu_indexes[0] < 0:
        for menu_index in range(0, len(menu)):
            text = text + DrawMenuItem(menu_index);
        return text;
    if active_menu_indexes[1] == 0:
        active_menu_index = active_menu_indexes[0];
        for menu_index in range(0, active_menu_index):
            text = text + DrawMenuItem(menu_index);
        text = text + DrawActiveMenuItem(active_menu_index);
        for sub_menu_index in range(1, len(menu[active_menu_index])):
            text = text + DrawSubmenuItem(active_menu_index, sub_menu_index);
        for menu_index in range(active_menu_index+1, len(menu)):
            text = text + DrawMenuItem(menu_index);
        return text;
    active_menu_index = active_menu_indexes[0];
    active_sub_menu_index = active_menu_indexes[1];
    for menu_index in range(0, active_menu_index+1):
        text = text + DrawMenuItem(menu_index);
    for sub_menu_index in range(1, active_sub_menu_index):
        text = text + DrawSubmenuItem(active_menu_index, sub_menu_index);
    text = text + DrawActiveSubmenuItem(active_menu_index, active_sub_menu_index);
    for sub_menu_index in range(active_sub_menu_index + 1, len(menu[active_menu_index])):
        text = text + DrawSubmenuItem(active_menu_index, sub_menu_index);
    for menu_index in range(active_menu_index+1, len(menu)):
        text = text + DrawMenuItem(menu_index);
    return text;    

menu = [['stubai'], ['proviant', 'proviant_info', 'daily_menue', 'recipe'], ['equipment', 'gas'], ['tirol_transport', 'transport', 'passage'], ['route', 'path_classification', 'signalgipfel', 'grosser', 'gamsspitzl', 'beiljoch'], ['money'], ['verona'], ['groupe'], ['links']];
menu_items = [];

for menu_index in range(0, len(menu)):
    menu_items.append([]);
    for sub_menu_index in range(0, len(menu[menu_index])):
        sourse_name = SourseNameGenerator(menu[menu_index][sub_menu_index]);
        status, menu_name = ExtractMenuItem(sourse_name);
        if status < 0:
            print('i can\'t find menu item name in %s'%sourse_name)
        menu_items[menu_index].append(menu_name);

copyright = 'stubaitrekking.ru, 2017 г., mail to admin@stubaitrekking.ru ';

p = open('pattern.browser.html', 'r', encoding = 'utf-8');
pattern = p.read();
p.close();
        
def PageProcess(pattern_name, sourse_name, page_name, print_name = '', menu_indexes = [-1, -1]):
    p = open(pattern_name, 'r', encoding = 'utf-8');
    pattern = p.read();
    p.close();   
    title, text = ExtractPageInfo(sourse_name, top_link = True);
    p = open(page_name, 'w', encoding = 'utf-8');
    resulted_text = TagSubstitute(pattern, '!title', title);
    resulted_text = TagSubstitute(resulted_text, '!menu', GenerateMenu(menu_indexes));
    resulted_text = TagSubstitute(resulted_text, '!text', text);
    resulted_text = TagSubstitute(resulted_text, '!copyright', copyright);
    if (len(print_name) > 0):
        resulted_text = TagSubstitute(resulted_text, '!print_version_link', PrintWersionLinkGenerator(print_name));
    p.write(resulted_text)
    p.close();


for menu_index in range(0, len(menu)):    
    for sub_menu_index in range(0, len(menu[menu_index])):
        name = menu[menu_index][sub_menu_index];
        print('%s processing...'%name)
        PageProcess('pattern.browser.html', SourseNameGenerator(name), WebpageNameGenerator(name), PrintNameGenerator(name), [menu_index, sub_menu_index]);
        PageProcess('pattern.printer.html', SourseNameGenerator(name), PrintNameGenerator(name), '', [menu_index, sub_menu_index]);
        print('%s processed'%name)

PageProcess('pattern.index.html', 'protoindex.html', 'index.html');
