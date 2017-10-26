# coding: utf8

from ReferenceSabstitution import ReferenceSabstitution

class LocalIndex:
    
    def GoToNextFilePosition(self, next_position):
        self.output_file = self.output_file + self.origin_file[self.origin_file_position:next_position];
        ##print(self.origin_file[self.origin_file_position:next_position]);
        self.origin_file_position = next_position;
        
    def AddLocalRef(self, header):
        self.index = self.index + '<li class = "local_index"><a href = \'#index%05d\'>%s</a></li>\n'%(self.next_index_nomber, header);
        self.next_index_nomber = self.next_index_nomber + 1;
        
    def SelectHeader(self, looked_header_level):
        looked_for_tag = self.headerses_close_tag[looked_header_level][0];
        closing_tag_position = self.origin_file.find(looked_for_tag, self.origin_file_position);
        if -1 == closing_tag_position:
            looked_for_tag = self.headerses_close_tag[looked_header_level][1];
            closing_tag_position = self.origin_file.find(looked_for_tag, self.origin_file_position);
            if -1 == closing_tag_position:
                return (-1, '');
        header = self.origin_file[self.origin_file_position:closing_tag_position];
        self.output_file = self.output_file + '<a name = \'index%05d\'></a>'%(self.next_index_nomber);
        if self.top_link:
            self.GoToNextFilePosition(closing_tag_position);
            self.output_file = self.output_file + '<div style = "float: right; font-size: small">[<a href = "#">к оглавлению</a>]</div>';
            self.GoToNextFilePosition(closing_tag_position + len(looked_for_tag));
        else:
            self.GoToNextFilePosition(closing_tag_position + len(looked_for_tag));
        return (0, header)
        
    def LookForHeader(self):
        while True:
            next_tag_begin = self.origin_file.find('<', self.origin_file_position);
            if -1 == next_tag_begin:
                return 0;
            self.GoToNextFilePosition(next_tag_begin);
            next_tag_end = self.origin_file.find('>', next_tag_begin)+1;
            if -1 == next_tag_end:
                return -1;
            self.GoToNextFilePosition(next_tag_end);
            tag = self.origin_file[next_tag_begin:next_tag_end];
            if tag in self.headerses_garde:
                return self.headerses_garde[tag];
                
    def IncreaseHeaderLevel(self, target_header_level):
        while self.header_level < target_header_level:
                self.index = self.index + '<ul>\n';
                self.header_level = self.header_level + 1;
    
    def DecreaseHeaderLevel(self, target_header_level):
        while self.header_level > target_header_level:
                self.index = self.index + '</ul>\n';
                self.header_level = self.header_level - 1;
    
    def ConstructIndex(self):
        while True:
            next_header_grade = self.LookForHeader();
            if 0 == next_header_grade:
                self.DecreaseHeaderLevel(0)
                return 0;
            if -1 == next_header_grade:
                return -1;
            status, header = self.SelectHeader(next_header_grade);
            if -1 == status:
                return -1;
            self.IncreaseHeaderLevel(next_header_grade);
            self.DecreaseHeaderLevel(next_header_grade);
            self.AddLocalRef(header);

    def __init__(self, origin_file = '', top_link = False):
        self.error_status = 0;
        self.index_tag = '<!paste_index_here>';
        self.headerses_garde = {
            '<h2>': 1,
            '<H2>': 1,
            '<h3>': 2,
            '<H3>': 2,
            '<h4>': 3,
            '<H4>': 3
        };
        self.headerses_close_tag = {
            1: ['</h2>', '</H2>'],
            2: ['</h3>', '</H3>'],
            3: ['</h4>', '</H4>']
        };
        self.origin_file = origin_file;
        self.origin_file_position = 0;
        self.header_level = 0;
        self.next_index_nomber = 0;
        self.index = '';
        self.output_file = '';
        self.top_link = top_link;
        
    def Do(self):
        index_paste_position = self.origin_file.find(self.index_tag);
        if -1 == index_paste_position:  
            text = self.origin_file;
            return 0, text, '';        
        status = self.ConstructIndex();
        output_file = self.output_file[:index_paste_position];
        output_file = output_file + '\n' + self.index;
        output_file = output_file + self.output_file[index_paste_position + len(self.index_tag):];
        return status, output_file, self.index;
        
def MakeIndex(file, top_link = False):
    output_file = WriteLabels(file);    
    status, output_file, index = LocalIndex(output_file, top_link).Do();
    if status < 0:
        print('an error occured during index construction');
    return output_file

def WriteLabels(file):
    return ReferenceSabstitution(file).Do();

#open('Beiljoch.indexed.html', 'w', encoding='utf8').write(MakeIndex(open('Beiljoch.html','r',encoding='utf8').read()));
#open('gamsspitzl.indexed.html', 'w').write(MakeIndex(open('gamsspitzl.html','r').read()));
#open('grosser.indexed.html', 'w').write(MakeIndex(open('grosser.html','r').read()));

