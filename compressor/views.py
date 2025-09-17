import zstandard as zstd
import os
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def compress_file_zstd(input_path):
    # Create a Zstandard compressor object
    compressor = zstd.ZstdCompressor(level=3)
    output_path = os.path.join(settings.MEDIA_ROOT, 'compressed', os.path.basename(input_path) + '.zst')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
        # Compress and write to file
        compressed_data = compressor.compress(f_in.read())
        f_out.write(compressed_data)

    return output_path

def upload_file(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return HttpResponse("No file selected. Please choose a file to upload.", status=400)

        # Save the uploaded file
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploads'))
        file_path = fs.save(uploaded_file.name, uploaded_file)
        full_path = fs.path(file_path)

        # Perform Zstandard compression
        compressed_path = compress_file_zstd(full_path)

        # Get file sizes
        original_size = uploaded_file.size
        compressed_size = os.path.getsize(compressed_path)

        return HttpResponse(
            f"Uploaded file: {uploaded_file.name}<br>"
            f"Original size: {original_size} bytes<br>"
            f"Compressed file saved at: {compressed_path}<br>"
            f"Compressed size: {compressed_size} bytes"
        )

    return render(request, 'index.html')

