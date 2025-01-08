from django.shortcuts import render
import os
import heapq
import pickle
from collections import defaultdict #for dict
from django.shortcuts import render #for displaying html files
from django.http import HttpResponse,FileResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError

# Create your views here.

class HuffmanCoding:
    def __init__(self,path):
        self.path=path
        self.heap=[]
        self.codes={}
        self.reverse_mapping={}
    def make_freq_dict(self,text):
        freq=defaultdict(int)
        for ch in text:
            freq[ch]+=1
        return freq
    def build_heap(self, freq):
        for key in freq:
            # if not isinstance(freq[key], int):
            #     raise ValueError(f"Invalid frequency value for '{key}': {freq[key]}")
            node = [freq[key], key,0]  # Frequency and character as a list
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            print("Heap after building:", self.heap)

            # Validate node structure
            merged = [node1[0] + node2[0], node1[1], node2[1]]
            print("Heap after building:", self.heap)
            heapq.heappush(self.heap, merged)

    def make_codes_helper(self,root,curr_code):
        if root[1] is not None:  # Leaf node has a character in the second element
            ch = root[1]
            self.codes[ch] = curr_code
            self.reverse_mapping[curr_code] = ch
            return

    # Internal node: recursively process left and right children
        self.make_codes_helper(root[2][0], curr_code + "0")  # Left child
        self.make_codes_helper(root[2][1], curr_code + "1")  # Right child
    def make_codes(self):
        root=heapq.heappop(self.heap)
        curr_code=""
        self.make_codes_helper(root,curr_code)
    def get_encoded_text(self,text):
        if self.codes:
            return ''.join(self.codes.values() )
        return
    def pad_encoded_text(self,encoded_text):
        extra_pad=8-len(encoded_text)%8
        encoded_text+="0"*extra_pad
        padded_info=f"{extra_pad:08b}"
        return padded_info+encoded_text
    
    def get_byte_arr(self,padded_enc_text):
        return bytearray(int(padded_enc_text[i:i+8],2) for i in range(0,len(padded_enc_text),8))
    
    def compress(self):
        with open(self.path,'rb') as file:
            text=file.read()
        freq=self.make_freq_dict(text)
        self.build_heap(freq)
        self.merge_nodes()
        self.make_codes()
        encoded_text=self.get_encoded_text(text)
        padded_enc_text=self.pad_encoded_text(encoded_text)
        output_path=os.path.join(settings.MEDIA_ROOT,'compressed',os.path.basename(self.path)+'.bin')
        os.makedirs(os.path.dirname(output_path),exist_ok=True)
        with open(output_path,'wb') as output:
            byte_arr=self.get_byte_arr(padded_enc_text)
            output.write(bytes(byte_arr))
        with open(output_path+'mapping','wb') as mapping_file:
            pickle.dump(self.reverse_mapping,mapping_file)
        return output_path
def upload_file(request):
    if request.method == 'POST':
        # Debugging: print request.FILES to check if the file is received
        print("Uploaded files:", request.FILES)

        # Check if the file is part of the request
        if 'file' not in request.FILES:
            return HttpResponse("No file selected. Please choose a file to upload.", status=400)

        # Get the uploaded file
        uploaded_file = request.FILES['file']

        # Optionally, print the name of the uploaded file to confirm it
        print("Uploaded file:", uploaded_file.name)

        # Save the uploaded file to MEDIA_ROOT
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploads'))
        file_path = fs.save(uploaded_file.name, uploaded_file)
        full_path = fs.path(file_path)

        # Perform compression
        huffman = HuffmanCoding(full_path)
        compressed_path = huffman.compress()

        # Get file sizes
        original_size = uploaded_file.size  # Original size in bytes
        compressed_size = os.path.getsize(compressed_path)  # Compressed size in bytes

        # Return size information and compression details
        return HttpResponse(
            f"Uploaded file: {uploaded_file.name}<br>"
            f"Original size: {original_size} bytes<br>"
            f"Compressed file saved at: {compressed_path}<br>"
            f"Compressed size: {compressed_size} bytes"
        )
    
    return render(request, 'index.html')
