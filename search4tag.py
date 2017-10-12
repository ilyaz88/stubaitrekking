def TakeAwayEmptyStrings(string_list):
    returned_list = [];
    for str in string_list:
        if len(str) > 0:
            returned_list.append(str); 
    return returned_list;

class search4tag:
    def __init__(self, text = '', tag = '', close_tag = ''):
        self.tag = '<'+tag;
        self.text = text;
        self.close_tag = '<'+close_tag;
        self.text_position = 0;
    
    # status, tag_content, between_tag_text = FindNextTag()
    # status == 0 is 'ok'
    # status == -1 is 'there is no new tag'
    # status == -2 is 'tag is not closed'
    def FindTag(self, tag):  
        next_tag_begin = self.text.find(tag, self.text_position);        
        if -1 == next_tag_begin:
            between_tag_text = self.text[self.text_position:];
            self.text_position = len(self.text);            
            return -1, [], between_tag_text;
        next_tag_end = self.text.find('>', next_tag_begin);        
        if -1 == next_tag_end:
            between_tag_text = self.text[self.text_position:];
            self.text_position = len(self.text);
            return -2, [], between_tag_text;
        between_tag_text = self.text[self.text_position: next_tag_begin];
        tag_content = self.text[(next_tag_begin+1):next_tag_end].split()[1:];
        self.text_position = next_tag_end+1;
        return 0, TakeAwayEmptyStrings(tag_content), between_tag_text;
        
    def FindNextTag(self):
        return self.FindTag(self.tag)
        
    def FindCloseTag(self):
        return self.FindTag(self.close_tag)
        
    def FindTagPair(self):
        status, tag_content, between_tag_text = self.FindNextTag();
        if status < 0:
            return status, tag_content, between_tag_text, '';
        status_1, close_tag_contetnt, tag_text = self.FindCloseTag();
        return status_1, tag_content, between_tag_text, tag_text;
        
    def FindTagOrPair(self, target_tag_content_length):
        status, tag_content, between_tag_text = self.FindNextTag();        
        if (status < 0) or (len(tag_content) >= target_tag_content_length):
            return status, tag_content, between_tag_text;
        status, close_tag_content, tag_text = self.FindCloseTag();        
        tag_content.extend(tag_text.split())
        return status, TakeAwayEmptyStrings(tag_content), between_tag_text;
