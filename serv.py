# coding: utf-8
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

   
