from search4tag import search4tag

class ReferenceSabstitution:
    def __init__(self, text):
        self.text = text;
        self.ref_classes = {};
        self.processed_text = '';
        self.label_tag = '!label';
        self.label_close_tag = '!/label';
        self.ref_tag = '!ref';
        self.ref_close_tag = '!/ref';
        self.href_tag = '!link';
        self.href_close_tag = '!/link';
        self.local_label_format = '<a name = \'{label:s}{number:d}\'></a>';
        self.local_href_format = '<a href = \'#{label:s}{number:d}\'>{number:d}</a>';
        self.local_ref_format = '{number:d}';
        
    def Do(self):
        print('searching for labels')
        self.SelectLabels();
        self.text = self.processed_text;
        self.processed_text = '';
        print(self.ref_classes);
        print(len(self.text))
        print('searching for refs')
        self.ReplaceRefTags(self.ref_tag, self.ref_close_tag, self.local_ref_format);
        self.text = self.processed_text;
        print(len(self.text))
        self.processed_text = '';
        print('searching for links')
        self.ReplaceRefTags(self.href_tag, self.href_close_tag, self.local_href_format);
        print(len(self.text))
        return self.processed_text;
        
    def SelectLabels(self):        
        seacher = search4tag(self.text, self.label_tag, self.label_close_tag);
        next_label_indexes = {};
        while True:
            search_stats, tag_content, text_chank = seacher.FindTagOrPair(2);
            print(tag_content)
            if search_stats < 0:
                self.processed_text = self.processed_text + text_chank;
                break
            if not(tag_content[0] in self.ref_classes):
                self.ref_classes[tag_content[0]] = {tag_content[1]: 1};
                next_label_indexes[tag_content[0]] = 1;
            self.ref_classes[tag_content[0]][tag_content[1]] = next_label_indexes[tag_content[0]];
            next_label_indexes[tag_content[0]] = next_label_indexes[tag_content[0]] + 1;
            self.processed_text = self.processed_text + text_chank + self.local_label_format.format(label = tag_content[0], number = self.ref_classes[tag_content[0]][tag_content[1]]);
        
        
    def ReplaceRefTags(self, ref_tag, close_tag, sabsitution_format):
        seacher = search4tag(self.text, ref_tag, close_tag);
        while True:
            search_stats, tag_content, text_chank = seacher.FindTagOrPair(2);
            print(tag_content)            
            if (search_stats < 0) or (len(tag_content) < 2):
                self.processed_text = self.processed_text + text_chank;
                break                
            if tag_content[0] in self.ref_classes:
                if tag_content[1] in self.ref_classes[tag_content[0]]:
                    self.processed_text = self.processed_text + text_chank + sabsitution_format.format(label = tag_content[0], number = self.ref_classes[tag_content[0]][tag_content[1]]);
                else:
                    self.processed_text = self.processed_text + text_chank;
            else:
                self.processed_text = self.processed_text + text_chank;
