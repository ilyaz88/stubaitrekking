from makeindex import MakeIndex
from search4tag import search4tag
from serv import *
from DiaryMark import DiaryMark
from PhotoPageGenrate import PhotoPageGenerate

copyright = '&copy; гр. А. Медведева, Нижегородский горный клуб, 2017 г., mail to <a href = "mailto:stubaitrekking@yandex.ru">stubaitrekking@yandex.ru</a>';
        
def TmpSave(text, fname = None):
    if fname is None:
        fname = 'tmp';
    fid = open(fname, 'w', encoding = 'utf-8');
    fid.write(text);
    fid.close();

intro_text, diary_index_prototype_name, chapters_texts, chapters_file_names = DiaryMark();

galery_list = [['07',''],
    ['09',''],
    ['12',''],
    ['14',''],
    ['20',''],
    ['22',''],
    ['24',''],
    ['25',''],
    ['26',''],
    ['32',''],
    ['33',''],
    ['40',''],
    ['44',''],
    ['47',''],
    ['48',''],
    ['49',''],
    ['51',''],
    ['54',''],
    ['57',''],
    ['63',''],    
    ['66',''],
    ['67',''],
    ['67a',''],
    ['68',''],
    ['69',''],
    ['80',''],    
    ['88','']];
    
galery_main, galery_pages, galery_fname_list = PhotoPageGenerate(galery_list, 'image/galery/preview/', 'image/galery/').Do();
TmpSave(galery_pages[0], SourseNameGenerator(galery_main));
menu = [[diary_index_prototype_name], ['stubai'], ['verona'], ['route', 'path_classification', 'signalgipfel', 'gamsspitzl',  'seescharte', 'beiljoch', 'grosser'], ['tirol_transport', 'transport', 'passage'], ['proviant', 'proviant_info', 'daily_menue', 'recipe'], ['equipment', 'gas'], ['money'], ['groupe'], [galery_main], ['links']];
menu_items = [];

TmpSave(intro_text, SourseNameGenerator(diary_index_prototype_name));

def DrawMenuItem(menu_index):
    return '<div class = \'menu_item\'><a class = "item" href = \'%s\'>%s</a></div>\n'%(WebpageNameGenerator(menu[menu_index][0]), menu_items[menu_index][0]);
    
def DrawSubmenuItem(menu_index, submenu_index):
    return '<div class = \'submenu_item\'><a class = "item" href = \'%s\'>%s</a></div>\n'%(WebpageNameGenerator(menu[menu_index][submenu_index]), menu_items[menu_index][submenu_index]);
    
def DrawActiveSubmenuItem(menu_index, submenu_index):
    return '<div class = \'selected_submenu_item\'>%s</div>\n'%(menu_items[menu_index][submenu_index]);

def DrawActiveMenuItem(menu_index):
    return '<div class = \'selected_menu_item\'>%s</div>\n'%(menu_items[menu_index][0]);

def PrintWersionLinkGenerator(print_version_name):
    return '[<a href = "%s">Версия для печати</a>]'%(print_version_name)

for menu_index in range(0, len(menu)):
    menu_items.append([]);
    for sub_menu_index in range(0, len(menu[menu_index])):
        sourse_name = SourseNameGenerator(menu[menu_index][sub_menu_index]);
        status, menu_name = ExtractMenuItem(sourse_name);
        if status < 0:
            print('i can\'t find menu item name in %s'%sourse_name)
        menu_items[menu_index].append(menu_name);

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

exception = {9};
    
for menu_index in range(1, len(menu)):
    if menu_index in exception:
        continue;
    for sub_menu_index in range(0, len(menu[menu_index])):
        name = menu[menu_index][sub_menu_index];
        print('%s processing...'%name)
        PageProcess('pattern.browser.html', SourseNameGenerator(name), WebpageNameGenerator(name), PrintNameGenerator(name), [menu_index, sub_menu_index]);
        PageProcess('pattern.printer.html', SourseNameGenerator(name), PrintNameGenerator(name), '', [menu_index, sub_menu_index]);
        print('%s processed'%name)
  

PageProcess('pattern.index.html', 'protoindex.html', 'index.html');

PageProcess('pattern.diary.html', SourseNameGenerator(diary_index_prototype_name), WebpageNameGenerator(diary_index_prototype_name), PrintNameGenerator(diary_index_prototype_name), [0, 0]);
PageProcess('pattern.printer.html', SourseNameGenerator('diary'), PrintNameGenerator(diary_index_prototype_name), '', [0, 0]);

for diary_chapter_index in range(len(chapters_file_names)):
    TmpSave(chapters_texts[diary_chapter_index]);
    PageProcess('pattern.diary.html', 'tmp', chapters_file_names[diary_chapter_index], PrintNameGenerator(diary_index_prototype_name), [0, 0]);
    
for i in range(1, 27):
    TmpSave(galery_pages[i]);
    PageProcess('pattern_galery.html', 'tmp', galery_fname_list[i], '', [9, 0]);

PageProcess('pattern_galery.html', SourseNameGenerator(galery_main), galery_fname_list[0], '', [9, 0]);
    