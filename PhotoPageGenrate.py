# coding: utf8

from serv import *

class PhotoPageGenerate:
    def __init__(self, pict_list, pict_dir, photo_dir, pages_dir = '', preview_postfix = '', page_prefix = 'galery'):
        self.div_pattern = """
<div style = "height: 588px; border-bottom-width: 3px; border-color: #20b2aa; border-bottom-style: solid; margin-right: 12px;">
<a href = "%s"><img src = "%s" width = 872px></a>
</div>
"""
        self.tray_pattern = """
<div style = "height: 58px; margin-top:10px;">
%s
</div>
"""
        self.tray_elemnt_pattern = """
<div style = "margin-left:%s; float: left;">
<a href = "%s">
<img src = "%s" width = 88px height = 58px>
</a>
</div>
"""
        self.active_tray_element_pattern = """
<div style = "margin-left: %s; float: left;">
<img src = "%s" width = 88px height = 58px>
</div>
"""
        self.pict_list = pict_list;
        self.preview_magrin_left = ['0px', '10px', '10px', '10px', '10px', '10px', '10px', '10px', '10px'];
        self.pict_dir = pict_dir;
        self.photo_dir = photo_dir;
        self.preview_postfix = preview_postfix;
        self.pages_dir = pages_dir;
        self.page_prefix = page_prefix;
        self.page_pattern = """
<html>
    <head>
        <meta charset="utf-8">        
        <title>Галерея</title>
        <!menu_item>Галерея<!/menu_item>
    </head>
    <body>
        %s
        %s
    </body>
</html>
"""
        
    def PrewiewNameGen(self, preview_number):
        return self.pict_dir + self.pict_list[preview_number][0] + self.preview_postfix + '.jpg';
    
    def PageNameGen(self, image_number):
        if image_number > 0:
            return self.pages_dir + self.page_prefix + self.pict_list[image_number][0] + '.html';
        else:
            return self.pages_dir + WebpageNameGenerator(self.page_prefix);
        
    def ImageNameGen(self, image_number):
        return self.photo_dir + self.pict_list[image_number][0] + '.jpg';
    
    def GeneratePreviewBar(self, preview_number):
        item_row = preview_number//9;
        item_column = preview_number%9;
        bar_description_text = '';
        for row in range(3):
            line_descrition_text = '';
            for column in range(9):                
                if (item_row == row) and (item_column == column):
                    line_descrition_text = line_descrition_text + self.active_tray_element_pattern%((self.preview_magrin_left[column]), self.PrewiewNameGen(preview_number));
                else:
                    line_descrition_text = line_descrition_text + self.tray_elemnt_pattern%(self.preview_magrin_left[column], (self.PageNameGen(column+9*row)), self.PrewiewNameGen(column+9*row));
            bar_description_text = bar_description_text + self.tray_pattern%(line_descrition_text);
        return bar_description_text
            
    def GenerateImageDiv(self, image_number):
        return self.div_pattern%(self.PageNameGen((image_number + 1)%27), self.ImageNameGen(image_number));
        
    def GeneratePage(self, image_number):
        page_text = self.page_pattern%(self.GenerateImageDiv(image_number), self.GeneratePreviewBar(image_number));
        return page_text;
        
    def Do(self):
        pages = [];
        fname_list = [];
        for i in range(27):
            pages.append(self.GeneratePage(i));
            fname_list.append(self.PageNameGen(i));
        return self.page_prefix, pages, fname_list;
            
