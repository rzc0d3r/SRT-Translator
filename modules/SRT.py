from deep_translator import GoogleTranslator

class SRT_Block:
    def __init__(self, subtitle_index: int, subtitle_time: str, subtitle_text: str):
        self.subtitle_index = subtitle_index
        self.subtitle_time = subtitle_time
        self.subtitle_text = subtitle_text

    def __str__(self):
        return '\n'.join([str(self.subtitle_index), self.subtitle_time, self.subtitle_text])
    
class SRT_Data:
    def __init__(self):
        self.subtitle_data = []

    def add_block(self, srt_block: SRT_Block):
        self.subtitle_data.append(srt_block)
    
    def edit_block(self, srt_block_index: int, srt_block: SRT_Block):
        self.subtitle_data[srt_block_index-1] = srt_block
        
    def get_blocks(self, start, end, build_srt_data_object=False):
        data = self.subtitle_data[start:end]
        result = data
        if build_srt_data_object:
            result = SRT_Data()
            for srt_block in data:
                result.add_block(srt_block)
        return result
    
    def __len__(self):
        return len(self.subtitle_data)

    def __iter__(self):
        return SRT_Data_Iterator(self.subtitle_data)

class SRT_Data_Iterator:
    def __init__(self, srt_data):
        self.srt_data = srt_data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.srt_data):
            result = self.srt_data[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration

class SRT_Manager:
    def save_to_file(srt_data: SRT_Data, path_to_file: str):
        f = open(path_to_file, 'w', encoding='utf-8-sig')
        for srt_block in srt_data:
            if srt_block.subtitle_index == len(srt_data): # removes an unnecessary line break at the end of the file
                f.write(str(srt_block)+'\n')
            else:
                f.write(str(srt_block)+'\n\n')
        f.close()
    
    def read_from_file(path_to_file):
        srt_data = SRT_Data()
        temp = []
        f = open(path_to_file, 'r', encoding='utf-8-sig')
        for line in f.readlines():
            line = line.strip()
            if line == '':
                srt_data.add_block(SRT_Block(int(temp[0]), temp[1], ' '.join(temp[2:])))
                temp = []
            else:
                temp.append(line)
        if temp != []: # in case there is no line break at the end of the file
            srt_data.add_block(SRT_Block(int(temp[0]), temp[1], ' '.join(temp[2:])))
        return srt_data

class SRTTranslator(object):
    def __init__(self, srt_data: SRT_Data, source_lang: str, target_lang: str):
        self.srt_data = srt_data
        self.translated_srt_data = SRT_Data()
        self.source_lang = source_lang
        self.target_lang = target_lang
        # define BATCH SIZEs
        if len(self.srt_data) < 20:
            self.BATCH_SIZE = len(self.srt_data)
        else:
            self.BATCH_SIZE = 20
            self.RESIDUE_BATCH_SIZE = len(self.srt_data)-((len(self.srt_data)//self.BATCH_SIZE)*self.BATCH_SIZE)
        self.AVAILABLE_BATCHS = len(self.srt_data)//self.BATCH_SIZE
        self.AVAILABLE_RESIDUE_BATCHS = len(self.srt_data)-(self.AVAILABLE_BATCHS*self.BATCH_SIZE)
        # init translator object
        self.translator = GoogleTranslator(self.source_lang, self.target_lang)

    def _translate_srt_batch(self, srt_batch): # srt_batch: list[SRT_Block]
        text_batch = ''
        for srt_block in srt_batch:
            text_batch += srt_block.subtitle_text+'\n#\n'
        translated_text_batch = [line.strip() for line in self.translator.translate(text_batch.strip()).split('#') if line.strip() != '']
        return translated_text_batch

    def translate(self, progressbar=None):
        # bundling
        srt_batchs = []
        #print(self.srt_data.subtitle_data[-1].subtitle_text)
        for i in range(1, self.AVAILABLE_BATCHS+1): # for BATCHS
            srt_batchs.append(self.srt_data.get_blocks((i-1)*self.BATCH_SIZE, self.BATCH_SIZE*i))
        srt_batchs.append(self.srt_data.get_blocks(self.BATCH_SIZE*i, (self.BATCH_SIZE*i)+self.AVAILABLE_RESIDUE_BATCHS)) # for RESIDUE BATCHS
        # translate
        for srt_batch in srt_batchs:
            close_translate_batch = False
            while not close_translate_batch:
                translated_text_batch = self._translate_srt_batch(srt_batch)
                if len(translated_text_batch) == len(srt_batch):
                    for i in range(0, len(srt_batch)):
                        translated_srt_block = SRT_Block(srt_batch[i].subtitle_index, srt_batch[i].subtitle_time, translated_text_batch[i])
                        self.translated_srt_data.add_block(translated_srt_block)
                    if progressbar is not None:
                        progressbar.update(len(srt_batch))
                    close_translate_batch = True
        return self.translated_srt_data
