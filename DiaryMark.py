# coding: utf8
from search4tag import search4tag
from serv import * 

diary_index_prototype_name = 'diary_index';

def SelectBody(fname):
    fid = open(fname, 'r', encoding = 'utf-8');
    text = fid.read();
    fid.close();
    return (search4tag(text, 'body', '/body').FindTagPair())[3];

def SelectChapters(text):
    searh = search4tag(text, 'h2', '/h2');
    headers = list();
    content = list();
    while True:
        status, _, before_tag_text, between_tag_text = searh.FindTagPair();
        content.append(before_tag_text);
        if status < 0:
            break;
        headers.append(between_tag_text);
    print(type(content[0]), len(content))
    print(type(headers[0]), len(headers))
    return content[0], headers, content[1:];
    
def ChapterNameAndLinkGenerator(chapter_number):
    if chapter_number >= 0:
        file_name = 'diary.day%02d.html'%(chapter_number);
        name = 'Глава %d'%(chapter_number + 1);
    else:
        file_name = WebpageNameGenerator(diary_index_prototype_name);
        name = 'Зачин'
    return file_name, name;

bar_link_item_pattern = """
        <td class = 'diary_bar'>
            <a class = 'item' href = '%s'>
                %s
            </a>
        </td>
"""
bar_selected_item_pattern = """
        <td class = 'selected'>
            %s            
        </td>
"""

class TableItemsCounter:
    def __init__(self, column_count = 4):
        self.column_count = column_count;
        self.column_index = 0;
    def step(self):
        self.column_index = self.column_index + 1;
        if self.column_index == self.column_count:
            self.column_index = 0;
            return '</tr><tr>'
        else:
            return '';

def GenerateLinkBar(chapters_count, chapter_number):
    column_counter = TableItemsCounter(10);
    bar_text = """
<table class = 'diary_bar'>
    <tr>
"""
    for chapter_index in range(-1, chapter_number):
        file_name, name = ChapterNameAndLinkGenerator(chapter_index);
        bar_text = bar_text + bar_link_item_pattern%(file_name, name);
        bar_text = bar_text + column_counter.step();
    bar_text = bar_text + bar_selected_item_pattern%(ChapterNameAndLinkGenerator(chapter_number)[1]);
    bar_text = bar_text + column_counter.step();
    for chapter_index in range(chapter_number + 1, chapters_count):
        file_name, name = ChapterNameAndLinkGenerator(chapter_index);
        bar_text = bar_text + bar_link_item_pattern%(file_name, name);
        bar_text = bar_text + column_counter.step();
    bar_text = bar_text + """
    </tr>
</table>
"""
    return bar_text;

intro_text_pattern = """"
<html>
    <head>
        <meta charset="utf-8">
        <link rel="stylesheet" href="text.css">
        <title>%s</title>
        <!menu_item>Дневник<!/menu_item>
    </head>
    <body>
        %s
        %s
        <p>
            <i>Читать далее:</i> <a href = 'diary.day00.html'>Глава 1</a>
        </p>
        %s
    </body>
</html>
"""

def GenerateIntroText(chapters_count, intro_text):
    link_bar = GenerateLinkBar(chapters_count, -1);
    _, name = ChapterNameAndLinkGenerator(-1);
    return intro_text_pattern%(name, link_bar, intro_text, link_bar);

chapter_text_pattern = """"
<html>
    <head>
        <meta charset="utf-8">        
        <title>%s</title>
    </head>
    <body>
        %s
        <h2>%s</h2>
        %s
        %s
    </body>
</html>
"""

def GenerateChapterText(chapter_headers, chapter_content, chapter_index):
    chapters_count = len(chapter_headers);
    link_bar = GenerateLinkBar(chapters_count, chapter_index);
    chapter_text = chapter_content[chapter_index];
    print(type(chapter_text))
    _, name = ChapterNameAndLinkGenerator(chapter_index);
    if chapter_index < (chapters_count - 1):
        next_file_name, next_name = ChapterNameAndLinkGenerator(chapter_index+1);
        chapter_text = chapter_text + "<p><i>Читать далее:</i> <a href = '%s'>%s</a></p>"%(next_file_name, next_name);
    chapter_text = chapter_text_pattern%(name, link_bar, chapter_headers[chapter_index], chapter_text, link_bar)
    return chapter_text;

def DiaryMark():
    diary_content = SelectBody('diary.html');
    diary_content = TagSubstitute(diary_content, '!paste_index_here', '')    
    intro_content, chapters_headers, chapters_content = SelectChapters(diary_content);
    chapters_count = len(chapters_headers);
    intro_text = GenerateIntroText(chapters_count, intro_content);
    chapters_texts = [GenerateChapterText(chapters_headers, chapters_content, i) for i in range(chapters_count)]
    chapters_file_names = [ChapterNameAndLinkGenerator(i)[0] for i in range(chapters_count)]
    return intro_text, diary_index_prototype_name, chapters_texts, chapters_file_names;
  
