# coding: utf8
import Search4tag
class PhotoPageGenerate:
    def __init__(self, list_fname, proto_page, pict_dir, photo_dir, pages_dir = '', preview_postfix = '', page_prefix = 'galery'):
        self.div_pattern = """
<div style = "heigh: 654px;">
<a href = "%s"><img src = "%s" width = 872px></a>
</div>
%s
"""
        self.tray_pattern = """
<div style = "height: 66px; margin-top:10px;">
%s
</div>
"""
        self.tray_elemnt_pattern = """
<div style = "margin-left:%s;">
<a href = "%s">
<img src = "%s" width = 88px height = 66px>
</a>
</div>
"""
        self.active_tray_element_pattern = """
<div style = "margin-left:%s;">
<img src = "%s" width = 88px height = 66px>
</div>
"""
        self.pict_list = self.GetPictList(list_fname);
        self.proto_page = proto_page;
        self.preview_magrin_left = ['0px', '10px', '10px', '10px', '10px', '10px', '10px', '10px', '10px'];
        self.pict_dir = pict_dir;
        self.photo_dir = photo_dir;
        self.preview_postfix = preview_postfix;
        self.pages_dir = pages_dir;
        self.page_prefix = page_prefix;
        self.pasre_tag = '!paste_image_here';
        
    def PrewiewNameGen(self, preview_number):
        return self.pict_dir + self.pict_list[preview_number][0] + self.preview_postfix + '.jpg';
    
    def PageNameGen(self, image_number):
        return self.pages_dir + self.page_prefix + pict_list[preview_number][0] + '.html';
        
    def ImageNameGen(self, image_number):
        return self.photo_dir + self.page_prefix + pict_list[preview_number][0] + '.html';
    
    def GeneratePreviewBar(self, preview_number):
        item_row = preview_number//3;
        item_column = preview_number%3;
        bar_description_text = '';
        for row = range(3):
            line_descrition_text = '';
            for column = range(9):                
                if (item_row == row)&&(item_column == column):
                    line_descrition_text = line_descrition_text + self.active_tray_element_pattern%((self.preview_magrin_left[column]), PrewiewNameGen(preview_number));
                else:
                    line_descrition_text = line_descrition_text + self.tray_element_pattern%((self.preview_magrin_left[column]), PrewiewNameGen(preview_number));
            bar_description_text = bar_description_text + self.tray_pattern%(line_descrition_text);
        return bar_description_text
            
    def GenerateImageDiv(self, image_number):
        return self.div_pattern%(PageNameGen((image_number + 1)%27), ImageNameGen(image_number));
        
    def GeneratePage(self, image_number):
        page_text =  
        
def GeneratePage(dname, index):
    